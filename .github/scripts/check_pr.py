#!/usr/bin/env python3
"""PR 规范检查，只读。

规则来自仓库根目录的 README.md 和 members/README.md。
检查不过时打印原因，并以退出码 1 结束，让 CI 失败。
HEAD_REF 环境变量指定被检查的提交，默认为 HEAD。
不写任何东西，不发评论，不加标签。
"""
import os
import re
import subprocess

BLOCKLIST = {"update", "test", "111"}
MAINTAINER = "mel0nyrame"

login = os.environ["LOGIN"]
branch = os.environ["BRANCH"]
title = os.environ.get("PR_TITLE", "")
body = os.environ.get("PR_BODY", "")
head_ref = os.environ.get("HEAD_REF", "HEAD")

errors = []


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def check_subject(text):
    match = re.match(r"^(feat|fix|docs|chore): (\S.*)$", text)
    if not match:
        return "格式不对，应为《类型: 说明》，类型限 feat fix docs chore"
    desc = match.group(2)
    if len(desc) < 2 or desc.lower() in BLOCKLIST:
        return "说明太短或没有意义"
    if len(desc) > 50:
        return "说明超过 50 个字符"
    return None


def clean_text(text):
    """去掉模板注释和标题，留下作者写的正文。"""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def body_content(text):
    """去掉模板注释、标题和自查小节，判断描述里有没有实际内容。"""
    text = re.sub(r"(?ms)^##\s*提交前自查\s*$.*?(?=^##\s|\Z)", "", text)
    return clean_text(text)


def section_content(text, heading):
    """返回某个二级标题下的正文；标题不存在时返回 None。"""
    match = re.search(
        r"(?ms)^##\s*" + re.escape(heading) + r"\s*$(.*?)(?=^##\s|\Z)", text
    )
    if not match:
        return None
    return clean_text(match.group(1))


if not (re.fullmatch(r"(feat|fix|docs|chore)/[^\s/]+", branch)
        or branch.lower() == "add-" + login.lower()):
    errors.append("分支名应为《类型/内容》，类型限 feat fix docs chore；也兼容 add-" + login + "，现在是 " + branch)

problem = check_subject(title)
if problem:
    errors.append("PR 标题" + problem + "，现在是 " + title)

if not body_content(body):
    errors.append("PR 描述为空，请按 PR 模板写明做了什么、改了哪些文件")
else:
    for heading in ("做了什么", "改了哪些文件"):
        if not section_content(body, heading):
            errors.append("PR 描述的「" + heading + "」没有填写，请按 PR 模板补充")

for subject in git("log", "origin/main.." + head_ref, "--no-merges", "--format=%s").splitlines():
    problem = check_subject(subject)
    if problem:
        errors.append("commit 信息" + problem + "，现在是 " + subject)

if login.lower() != MAINTAINER:
    own_file = re.compile(
        "members/" + re.escape(login) + "/(?:" + re.escape(login) + r"\.(?:txt|md)|[^/]+\.html)",
        re.I,
    )
    # 禁用重命名检测，分别检查旧路径和新路径，避免借移动文件越权。
    # NUL 分隔保留文件名中的换行和制表符，不能按行解析 Git 路径。
    records = git("diff", "--raw", "-z", "--no-renames", "origin/main..." + head_ref).split("\0")
    for fields, path in zip(records[0::2], records[1::2]):
        parts = fields.split()
        dst_mode, status = parts[1], parts[4]
        if not own_file.fullmatch(path):
            errors.append("只能改动 members/" + login + "/ 下的 " + login + ".txt、" + login + ".md 和任意名称的 .html 文件，请撤回对 " + repr(path) + " 的改动")
        elif not status.startswith("D") and dst_mode not in ("100644", "100755"):
            errors.append("子模块和符号链接不能提交，请删除 " + repr(path))

if errors:
    print("检查未通过")
    for e in errors:
        print("  - " + e)
    raise SystemExit(1)

print("检查通过")
