"""在临时 Git 仓库中验证 PR 检查，不访问网络。"""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("check_pr.py").resolve()
BODY = "## 做了什么\n更新个人页面。\n\n## 改了哪些文件\n更新个人文件。\n"


class CheckPRTests(unittest.TestCase):
    def setUp(self):
        # Git 可能在提交后仍在写入临时仓库，清理失败不应让测试报错。
        self.temp = tempfile.TemporaryDirectory(
            prefix="pr-check-", dir=os.environ.get("TMPDIR"), ignore_cleanup_errors=True,
        )
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "octocat")
        self.git("config", "user.email", "octocat@example.invalid")
        for path in (
            "README.md", ".github/workflows/check.yml",
            "members/octocat/octocat.md", "members/octocat/octocat.txt", "members/octocat/old.html",
            "members/octocat/legacy.txt", "members/other/other.md",
        ):
            self.write(path, "base\n")
        self.commit("docs: 初始化测试仓库")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("switch", "-c", "feat/add-profile")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.repo, check=True, capture_output=True, text=True,
        ).stdout

    def write(self, path, content="changed\n"):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def commit(self, subject="feat: 更新个人页面"):
        self.git("add", "--all")
        self.git("commit", "-m", subject)

    def check(self, passed=True, contains=None, **env):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)], cwd=self.repo, capture_output=True, text=True,
            env={**os.environ, "LOGIN": "octocat", "BRANCH": "feat/add-profile",
                 "BASE_REF": "main", "PR_TITLE": "feat: 更新个人页面",
                 "PR_BODY": BODY, "HEAD_REF": "HEAD", **env},
        )
        self.assertEqual(result.returncode, 0 if passed else 1, result.stdout + result.stderr)
        if contains:
            self.assertIn(contains, result.stdout)

    def test_own_markdown_and_arbitrary_html(self):
        self.write("members/octocat/octocat.md")
        self.write("members/octocat/我的主页.html")
        self.write("members/octocat/another.html")
        self.commit()
        self.check()

    def test_html_only(self):
        self.write("members/octocat/old.html")
        self.commit()
        self.check()

    def test_own_text_file(self):
        self.write("members/songyang-prog/songyang-prog.txt")
        self.commit()
        self.check(LOGIN="songyang-prog")

    def test_modify_own_text_file(self):
        self.write("members/octocat/octocat.txt")
        self.commit()
        self.check()

    def test_login_is_case_insensitive(self):
        self.write("members/octocat/octocat.md")
        self.write("members/octocat/octocat.txt")
        self.commit()
        self.check(LOGIN="OctoCat")

    def test_forbidden_paths(self):
        for path in (
            "README.md", ".github/workflows/check.yml", "members/other/other.md",
            "members/octocat/wrong.md", "members/octocat/legacy.txt", "members/other/other.txt",
            "members/octocat/photo.png", "members/octocat/.DS_Store",
            "members/octocat/sub/page.html", "members/octocat/sub/octocat.txt", "members/octocat-evil/page.html",
            "members/octocat/page.html\nREADME.md", "members/octocat/page.html\t.txt",
        ):
            with self.subTest(path=path):
                self.write(path)
                self.commit()
                self.check(False, "只能改动")
                # 推进比较基线，让下个子用例只检查自己的改动。
                self.git("update-ref", "refs/remotes/origin/main", "HEAD")

    def test_delete_own_allowed_files(self):
        (self.repo / "members/octocat/octocat.md").unlink()
        (self.repo / "members/octocat/octocat.txt").unlink()
        (self.repo / "members/octocat/old.html").unlink()
        self.commit()
        self.check()

    def test_forbidden_deletions(self):
        for path in ("README.md", "members/other/other.md", "members/octocat/legacy.txt"):
            with self.subTest(path=path):
                (self.repo / path).unlink()
                self.commit()
                self.check(False, "只能改动")
                self.git("update-ref", "refs/remotes/origin/main", "HEAD")

    def test_rename_own_html(self):
        self.git("mv", "members/octocat/old.html", "members/octocat/new.html")
        self.commit()
        self.check()

    def test_rename_own_text_to_markdown(self):
        self.write("members/octocat/octocat.txt")
        self.git("rm", "members/octocat/octocat.md")
        self.git("mv", "members/octocat/octocat.txt", "members/octocat/octocat.md")
        self.commit()
        self.check()

    def test_text_symlink(self):
        path = self.repo / "members/octocat/octocat.txt"
        path.unlink()
        path.symlink_to("../../README.md")
        self.commit()
        self.check(False, "符号链接")

    def test_move_other_member_file_into_own_folder(self):
        self.git("mv", "members/other/other.md", "members/octocat/new.html")
        self.commit()
        self.check(False, "members/other/other.md")

    def test_move_own_file_outside_folder(self):
        self.git("mv", "members/octocat/old.html", "outside.html")
        self.commit()
        self.check(False, "outside.html")

    def test_symlink(self):
        (self.repo / "members/octocat/link.html").symlink_to("../../README.md")
        self.commit()
        self.check(False, "符号链接")

    def test_gitlink(self):
        self.git("update-index", "--add", "--cacheinfo", "160000",
                 self.git("rev-parse", "HEAD").strip(), "members/octocat/repo.html")
        self.git("commit", "-m", "feat: 添加子模块")
        self.check(False, "子模块")

    def test_maintainer_can_change_any_path(self):
        self.write("README.md")
        self.write(".github/workflows/check.yml")
        self.write("members/other/other.md")
        (self.repo / "members/octocat/legacy.txt").unlink()
        self.commit()
        self.check(LOGIN="Mel0nyrame")

    def test_actor_and_commit_author_do_not_grant_permissions(self):
        self.git("config", "user.name", "mel0nyrame")
        self.write("README.md")
        self.commit()
        self.check(False, "只能改动", GITHUB_ACTOR="mel0nyrame")

    def test_branch_format(self):
        self.write("members/octocat/octocat.md")
        self.commit()
        for branch in ("feat/add-profile", "fix/fix-page", "docs/update-profile", "chore/cleanup",
                       "add-octocat", "add-OctoCat"):
            with self.subTest(branch=branch):
                self.check(BRANCH=branch)
        for branch in ("add-other", "add-", "feat/", "other/add-profile", "feat/a/b", "feat/has space"):
            with self.subTest(branch=branch):
                self.check(False, "分支名应为", BRANCH=branch)

    def test_invalid_title(self):
        self.write("members/octocat/octocat.md")
        self.commit()
        for title in ("update", "feat: test", "feat: " + "长" * 51):
            with self.subTest(title=title):
                self.check(False, "PR 标题", PR_TITLE=title)

    def test_invalid_commit(self):
        self.write("members/octocat/octocat.md")
        self.commit("update")
        self.check(False, "commit 信息")

    def test_title_separator_tolerance(self):
        self.write("members/octocat/octocat.md")
        self.commit()
        for title in ("docs:添加说明", "docs:  添加说明", "docs：添加说明", "docs:\t添加说明", "docs:\u3000添加说明"):
            with self.subTest(title=title):
                self.check(PR_TITLE=title)
        for title in ("docs :添加说明", "docs:", "docs:   ", "docs: 测"):
            with self.subTest(title=title):
                self.check(False, "PR 标题", PR_TITLE=title)

    def test_meaningless_chinese_description(self):
        self.write("members/octocat/octocat.md")
        self.commit()
        for title in ("docs: 测试", "docs: 更新", "docs: 修改", "docs: 提交", "docs: 添加", "docs: 修复", "docs: add", "docs: fix"):
            with self.subTest(title=title):
                self.check(False, "没有意义", PR_TITLE=title)
        self.check(PR_TITLE="docs: 更新个人说明")

    def test_body_missing_and_empty_sections(self):
        self.write("members/octocat/octocat.md")
        self.commit()
        self.check(False, "缺少「## 改了哪些文件」", PR_BODY="## 做了什么\n改了页面\n")
        self.check(False, "「## 做了什么」是空的", PR_BODY="## 做了什么\n<!-- 说明 -->\n## 改了哪些文件\n改了页面\n")

    def test_wrong_member_file_path_hint(self):
        self.write("members/octocat.md")
        self.commit()
        self.check(False, "正确路径是 members/octocat/octocat.md")

    def test_target_branch(self):
        self.write("members/octocat/octocat.md")
        self.commit()
        self.check(BASE_REF="main")
        self.check(False, "目标分支必须是 main", BASE_REF="dev")

    def test_commit_hint(self):
        self.write("members/octocat/octocat.md")
        self.commit("update")
        self.check(False, "git commit --amend")

    def test_body_sections(self):
        self.write("members/octocat/octocat.md")
        self.commit()
        for body in ("", "<!-- 说明 -->", "## 提交前自查\n- [x] 完成",
                     "只有一行描述", "## 做了什么\n改了页面\n## 改了哪些文件\n<!-- 待填 -->"):
            with self.subTest(body=body):
                self.check(False, "PR 描述", PR_BODY=body)

    def test_maintainer_still_needs_valid_metadata(self):
        self.write("README.md")
        self.commit("update")
        self.check(False, "commit 信息", LOGIN="mel0nyrame")
        self.check(False, "分支名应为", LOGIN="mel0nyrame", BRANCH="main")
        self.check(False, "PR 标题", LOGIN="mel0nyrame", PR_TITLE="update")
        self.check(False, "PR 描述", LOGIN="mel0nyrame", PR_BODY="")

    def test_explicit_head_ref(self):
        self.write("members/octocat/old.html")
        self.commit()
        self.git("update-ref", "refs/remotes/pr/head", "HEAD")
        self.git("switch", "main")
        self.write("README.md")
        self.commit()
        self.check(HEAD_REF="refs/remotes/pr/head")


if __name__ == "__main__":
    unittest.main()
