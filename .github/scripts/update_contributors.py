#!/usr/bin/env python3
"""合并贡献者和课程成员，保留已收录账号，并生成 README 头像。"""
import argparse
import json
from pathlib import Path
import re
import subprocess


REPOSITORY = "mel0nyrame/git-example"
ROOT = Path(__file__).resolve().parents[2]
START = "<!-- contributors:start -->"
END = "<!-- contributors:end -->"
LOGIN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\[bot\])?")


def api(endpoint, paginate=False):
    command = ["gh", "api", "--hostname", "github.com", endpoint]
    if paginate:
        command += ["--paginate", "--slurp"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def account(value):
    """仅保存公开账号 ID 和用户名，不保存姓名或邮箱。"""
    if (not isinstance(value, dict)
            or type(value.get("id")) is not int or value["id"] <= 0
            or not isinstance(value.get("login"), str)
            or not LOGIN.fullmatch(value["login"])):
        raise ValueError("账号必须包含有效的 GitHub ID 和用户名")
    return {"id": value["id"], "login": value["login"]}


def load_roster(root):
    values = json.loads((root / ".github/contributors.json").read_text(encoding="utf-8"))
    if not isinstance(values, list):
        raise ValueError("贡献者名单必须是数组")
    roster = {}
    for value in values:
        user = account(value)
        if user["id"] in roster:
            raise ValueError("贡献者名单包含重复 ID")
        roster[user["id"]] = user
    return roster


def collect(root, roster):
    # API 可能返回缓存或不完整的历史统计，因此只补充，不用它删除账号。
    roster = dict(roster)
    pages = api(f"repos/{REPOSITORY}/contributors?per_page=100", paginate=True)
    if not isinstance(pages, list) or not pages or any(not isinstance(p, list) for p in pages):
        raise ValueError("贡献者 API 未返回完整的分页数组")
    for page in pages:
        for value in page:
            user = account(value)
            roster[user["id"]] = user

    known = {user["login"].lower() for user in roster.values()}
    for member in sorted((root / "members").iterdir()):
        if member.is_symlink():
            raise ValueError("成员目录不能是符号链接")
        if not member.is_dir():
            continue
        if not LOGIN.fullmatch(member.name):
            raise ValueError(f"成员目录不是有效用户名: {member.name!r}")
        if member.name.lower() in known:
            continue
        user = account(api(f"users/{member.name}"))
        roster[user["id"]] = user
        known.add(user["login"].lower())
    return roster


def contribution_times():
    """返回每个账号在默认分支上最早一次提交的 UTC 时间，用于按贡献时间排列。"""
    pages = api(f"repos/{REPOSITORY}/commits?per_page=100", paginate=True)
    if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
        raise ValueError("提交 API 未返回完整的分页数组")
    times = {}
    for page in pages:
        for node in page:
            if not isinstance(node, dict):
                raise ValueError("提交数据格式错误")
            author = node.get("author")
            login = author.get("login") if isinstance(author, dict) else None
            if not isinstance(login, str) or not LOGIN.fullmatch(login):
                continue
            commit = node.get("commit")
            date = None
            for part in ("author", "committer"):
                value = commit.get(part) if isinstance(commit, dict) else None
                if isinstance(value, dict) and isinstance(value.get("date"), str):
                    date = value["date"]
                    break
            if date is None:
                continue
            key = login.lower()
            if key not in times or date < times[key]:
                times[key] = date
    return times


def sorted_users(roster, times=None):
    users = list(roster.values())
    if not users:
        raise ValueError("贡献者名单不能为空")
    if len({user["login"].lower() for user in users}) != len(users):
        raise ValueError("多个账号 ID 使用同一用户名，请检查账号更名")
    if times is None:
        # 名单中的顺序就是展示顺序；离线检查不查询提交时间。
        return users
    return sorted(
        users,
        key=lambda user: (
            times.get(user["login"].lower(), "") == "",
            times.get(user["login"].lower(), ""),
            user["login"].lower(),
        ),
    )


def render(readme, users):
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README 必须包含唯一的贡献者起止标记")
    before, rest = readme.split(START)
    if END not in rest:
        raise ValueError("README 贡献者标记顺序错误")
    _, after = rest.split(END)
    lines = [START, "", "<p>"]
    for user in users:
        login, user_id = user["login"], user["id"]
        lines.append(
            f'  <a href="https://github.com/{login}">'
            f'<img src="https://avatars.githubusercontent.com/u/{user_id}?s=96&amp;v=4" '
            f'width="48" height="48" alt="@{login}" title="@{login}" /></a>'
        )
    lines += ["</p>", "", END]
    return before + "\n".join(lines) + after


def update(root=ROOT, check=False):
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    roster = load_roster(root)
    if check:
        users = sorted_users(roster)
    else:
        roster = collect(root, roster)
        users = sorted_users(roster, contribution_times())
    generated = render(readme, users)
    if check:
        if generated != readme:
            raise ValueError("README 头像与贡献者名单不一致，请重新生成")
    else:
        # 所有网络请求和校验成功后才写文件；失败的工作流不能提交半份结果。
        data = json.dumps(users, ensure_ascii=False, indent=2) + "\n"
        roster_path = root / ".github/contributors.json"
        if roster_path.read_text(encoding="utf-8") != data:
            roster_path.write_text(data, encoding="utf-8")
        if generated != readme:
            readme_path.write_text(generated, encoding="utf-8")
    return len(users)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="离线检查 README 与名单是否一致")
    args = parser.parse_args()
    try:
        print(f"贡献者名单共 {update(check=args.check)} 个账号")
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"贡献者更新失败: {error}\n")
