"""头像名单与生成物回归测试，不访问网络。"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import update_contributors as updater


class ContributorsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="contributors-", dir=os.environ.get("TMPDIR"))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".github").mkdir()
        (self.root / "members").mkdir()
        self.roster = self.root / ".github/contributors.json"
        self.readme = self.root / "README.md"
        self.roster.write_text("[]\n", encoding="utf-8")
        self.original = f"# 仓库\n\n## 贡献者\n{updater.START}\n{updater.END}\n\n## 分支\n原文保留\n"
        self.readme.write_text(self.original, encoding="utf-8")

    def seed(self, *users):
        self.roster.write_text(json.dumps(users), encoding="utf-8")

    def users(self):
        return json.loads(self.roster.read_text(encoding="utf-8"))

    def test_union_keeps_contributor_without_member_directory(self):
        (self.root / "members/student").mkdir()
        (self.root / "members/README.md").write_text("规则", encoding="utf-8")
        with patch.object(updater, "api", side_effect=[
            [[{"id": 1, "login": "maintainer"}]], {"id": 2, "login": "student"}, [[]],
        ]):
            self.assertEqual(updater.update(self.root), 2)
        self.assertEqual(self.users(), [
            {"id": 1, "login": "maintainer"}, {"id": 2, "login": "student"},
        ])
        readme = self.readme.read_text(encoding="utf-8")
        self.assertEqual(readme.count("<img "), 2)
        self.assertIn('alt="@maintainer"', readme)
        self.assertTrue(readme.startswith("# 仓库\n\n## 贡献者\n"))
        self.assertTrue(readme.endswith("\n\n## 分支\n原文保留\n"))

    def test_cached_statistics_and_removed_directory_do_not_remove_users(self):
        self.seed({"id": 1, "login": "previous"})
        with patch.object(updater, "api", return_value=[[]]):
            self.assertEqual(updater.update(self.root), 1)
        self.assertEqual(self.users(), [{"id": 1, "login": "previous"}])

    def test_all_pages_are_merged_and_not_limited_to_100(self):
        users = [{"id": i, "login": f"user-{i}"} for i in range(1, 106)]
        with patch.object(updater, "api", return_value=[users[:100], users[100:]]) as api:
            self.assertEqual(updater.update(self.root), 105)
        api.assert_any_call(
            f"repos/{updater.REPOSITORY}/contributors?per_page=100", paginate=True,
        )
        api.assert_any_call(f"repos/{updater.REPOSITORY}/commits?per_page=100", paginate=True)
        self.assertEqual(api.call_count, 2)
        self.assertEqual(self.readme.read_text().count("<img "), 105)

    def test_api_requests_follow_pagination(self):
        with patch.object(updater.subprocess, "run") as run:
            run.return_value.stdout = '[[{"id": 1, "login": "user"}], []]'
            self.assertEqual(len(updater.api("repos/owner/repo/contributors", paginate=True)), 2)
        self.assertEqual(run.call_args.args[0], [
            "gh", "api", "--hostname", "github.com", "repos/owner/repo/contributors",
            "--paginate", "--slurp",
        ])

    def test_case_insensitive_member_lookup(self):
        (self.root / "members/USER").mkdir()
        with patch.object(updater, "api", return_value=[[{"id": 1, "login": "user"}]]) as api:
            updater.update(self.root)
        self.assertEqual(api.call_count, 2)

    def test_users_are_ordered_by_first_contribution_time(self):
        with patch.object(updater, "api", side_effect=[
            [[{"id": 1, "login": "later"}, {"id": 2, "login": "earlier"}]],
            [[
                {"author": {"login": "later"}, "commit": {"author": {"date": "2026-03-02T00:00:00Z"}}},
                {"author": {"login": "earlier"}, "commit": {"author": {"date": "2026-03-01T00:00:00Z"}}},
                {"author": {"login": "earlier"}, "commit": {"committer": {"date": "2026-02-01T00:00:00Z"}}},
                {"author": None, "commit": {"author": {"date": "2026-01-01T00:00:00Z"}}},
            ]],
        ]):
            self.assertEqual(updater.update(self.root), 2)
        self.assertEqual([user["login"] for user in self.users()], ["earlier", "later"])
        readme = self.readme.read_text(encoding="utf-8")
        self.assertLess(readme.index('alt="@earlier"'), readme.index('alt="@later"'))

    def test_missing_time_sorts_last_and_ties_use_login(self):
        users = [{"id": 1, "login": "zzz"}, {"id": 2, "login": "aaa"}, {"id": 3, "login": "mmm"}]
        with patch.object(updater, "api", side_effect=[
            [users],
            [[{"author": {"login": "zzz"}, "commit": {"author": {"date": "2026-01-01T00:00:00Z"}}}]],
        ]):
            updater.update(self.root)
        self.assertEqual([user["login"] for user in self.users()], ["zzz", "aaa", "mmm"])

    def test_rename_uses_id_and_bot_is_not_silently_filtered(self):
        self.seed({"id": 1, "login": "old-login"})
        with patch.object(updater, "api", return_value=[[
            {"id": 1, "login": "new-login"}, {"id": 2, "login": "github-actions[bot]"},
        ]]):
            self.assertEqual(updater.update(self.root), 2)
        self.assertNotIn("old-login", self.readme.read_text())
        self.assertIn("/u/1?s=96", self.readme.read_text())
        self.assertIn('alt="@github-actions[bot]"', self.readme.read_text())

    def test_network_failure_preserves_both_files(self):
        self.seed({"id": 1, "login": "previous"})
        (self.root / "members/new-student").mkdir()
        before = (self.roster.read_bytes(), self.readme.read_bytes())
        with patch.object(updater, "api", side_effect=[
            [[{"id": 2, "login": "new-contributor"}]],
            subprocess.CalledProcessError(1, ["gh", "api"]),
        ]):
            with self.assertRaises(subprocess.CalledProcessError):
                updater.update(self.root)
        self.assertEqual(before, (self.roster.read_bytes(), self.readme.read_bytes()))

    def test_invalid_api_response_preserves_both_files(self):
        self.seed({"id": 1, "login": "previous"})
        for response in ([], {}, [[] , {}], [[{"id": 2}]], [[{"id": 2, "login": '<img src="x">'}]]):
            with self.subTest(response=response):
                before = (self.roster.read_bytes(), self.readme.read_bytes())
                with patch.object(updater, "api", return_value=response):
                    with self.assertRaises(ValueError):
                        updater.update(self.root)
                self.assertEqual(before, (self.roster.read_bytes(), self.readme.read_bytes()))

    def test_markers_missing_duplicated_or_reversed_preserve_files(self):
        self.seed({"id": 1, "login": "user"})
        for readme in ("no markers", updater.START * 2 + updater.END, updater.END + updater.START):
            with self.subTest(readme=readme):
                self.readme.write_text(readme)
                before = (self.roster.read_bytes(), self.readme.read_bytes())
                with patch.object(updater, "api", return_value=[[]]):
                    with self.assertRaises(ValueError):
                        updater.update(self.root)
                self.assertEqual(before, (self.roster.read_bytes(), self.readme.read_bytes()))

    def test_idempotent_and_offline_check_does_not_call_api_or_write(self):
        with patch.object(updater, "api", return_value=[[{"id": 1, "login": "user"}]]):
            updater.update(self.root)
            times = (self.roster.stat().st_mtime_ns, self.readme.stat().st_mtime_ns)
            updater.update(self.root)
        self.assertEqual(times, (self.roster.stat().st_mtime_ns, self.readme.stat().st_mtime_ns))
        with patch.object(updater, "api") as api:
            self.assertEqual(updater.update(self.root, check=True), 1)
        api.assert_not_called()
        self.assertEqual(times, (self.roster.stat().st_mtime_ns, self.readme.stat().st_mtime_ns))

    def test_offline_check_detects_stale_readme(self):
        self.seed({"id": 1, "login": "user"})
        with self.assertRaisesRegex(ValueError, "不一致"):
            updater.update(self.root, check=True)
        self.assertEqual(self.readme.read_text(), self.original)

    def test_empty_roster_is_not_written(self):
        with patch.object(updater, "api", return_value=[[]]):
            with self.assertRaisesRegex(ValueError, "不能为空"):
                updater.update(self.root)
        self.assertEqual(self.roster.read_text(), "[]\n")

    def test_invalid_accounts_are_rejected(self):
        for user in ({"id": True, "login": "user"}, {"id": -1, "login": "user"},
                     {"id": 1, "login": "../user"}, {"id": 1, "login": "user\n"}):
            with self.subTest(user=user):
                with self.assertRaises(ValueError):
                    updater.account(user)

    def test_duplicate_ids_or_logins_are_rejected(self):
        self.seed({"id": 1, "login": "user"}, {"id": 1, "login": "user"})
        with self.assertRaisesRegex(ValueError, "重复 ID"):
            updater.load_roster(self.root)
        with self.assertRaisesRegex(ValueError, "同一用户名"):
            updater.sorted_users({1: {"id": 1, "login": "user"}, 2: {"id": 2, "login": "USER"}})

    def test_invalid_or_symlink_member_directory_is_rejected(self):
        invalid = self.root / "members/not a login"
        invalid.mkdir()
        with patch.object(updater, "api", return_value=[[{"id": 1, "login": "user"}]]):
            with self.assertRaisesRegex(ValueError, "不是有效用户名"):
                updater.update(self.root)
        invalid.rmdir()
        (self.root / "members/link").symlink_to(self.root, target_is_directory=True)
        with patch.object(updater, "api", return_value=[[{"id": 1, "login": "user"}]]):
            with self.assertRaisesRegex(ValueError, "不能是符号链接"):
                updater.update(self.root)


if __name__ == "__main__":
    unittest.main()
