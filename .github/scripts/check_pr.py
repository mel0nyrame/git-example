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

login = os.environ["LOGIN"]
branch = os.environ["BRANCH"]
title = os.environ.get("PR_TITLE", "")
body = os.environ.get("PR_BODY", "")
head_ref = os.environ.get("HEAD_REF", "HEAD")

errors = []
warnings = []


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout


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


if not git("rev-parse", "--verify", "origin/main"):
    errors.append("找不到 origin/main，检查无法运行，workflow 需要 fetch-depth: 0")

if branch.lower() != "add-" + login.lower():
    errors.append("分支名应为 add-" + login + "，现在是 " + branch)

problem = check_subject(title)
if problem:
    errors.append("PR 标题" + problem + "，现在是 " + title)

if not body.strip():
    errors.append("PR 描述为空，请写明做了什么、改了哪些文件")

for subject in git("log", "origin/main.." + head_ref, "--no-merges", "--format=%s").splitlines():
    problem = check_subject(subject)
    if problem:
        errors.append("commit 信息" + problem + "，现在是 " + subject)

own_file = re.compile("^members/" + re.escape(login) + "/" + re.escape(login) + r"\.(md|txt)$", re.I)
other_member = re.compile(r"^members/([^/]+)/", re.I)
own_folder_prefix = "members/" + login.lower() + "/"

canonical_seen = False
for line in git("-c", "core.quotepath=false", "diff", "--raw", "--no-renames",
                "origin/main..." + head_ref).splitlines():
    if not line:
        continue
    fields, path = line[1:].split("\t", 1)
    parts = fields.split()
    dst_mode, status = parts[1], parts[4]

    folder = other_member.match(path)
    if folder and folder.group(1).lower() != login.lower():
        errors.append("不能改动别人的成员文件夹，请撤回对 " + path + " 的改动")
        continue

    if status.startswith("D"):
        continue

    if dst_mode not in ("100644", "100755"):
        errors.append("子模块和符号链接不能提交，请删除 " + path)
    elif own_file.match(path):
        canonical_seen = True
    elif path.lower().startswith(own_folder_prefix):
        warnings.append("自己文件夹里的附加文件，仅作提示，路径 " + path)
    else:
        errors.append("文件位置不对，应为 members/" + login + "/" + login + ".md 或 .txt，现在是 " + path)

if not canonical_seen:
    errors.append("缺少成员文件 members/" + login + "/" + login + ".md 或 .txt")

for w in warnings:
    print("提示 " + w)

if errors:
    print("检查未通过")
    for e in errors:
        print("  - " + e)
    raise SystemExit(1)

print("检查通过")
