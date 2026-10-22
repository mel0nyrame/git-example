# Git 练习仓库

用于学习 Git 的仓库。你通过 Pull Request 把自己的文件加入仓库。

个人文件的放置规则见 [members/README.md](members/README.md)。

## 贡献者

[![贡献者头像](https://contrib.rocks/image?repo=mel0nyrame/git-example&max=1000)](https://github.com/mel0nyrame/git-example/graphs/contributors)

---

## 你怎么能直接 commit 到我的 main 分支啊？！GitHub 上不是这样！你应该先 fork 我的仓库，然后从 develop 分支 checkout 一个新的 feature 分支，比如叫 feature/confession。然后你把你的心意写成代码，并为它写好单元测试和集成测试，确保代码覆盖率达到95%以上。接着你要跑一下 Linter，通过所有的代码风格检查。然后你再 commit，commit message 要遵循 Conventional Commits 规范。之后你把这个分支 push 到你自己的远程仓库，然后给我提一个 Pull Request。在 PR 描述里，你要详细说明你的功能改动和实现思路，并且 @ 我和至少两个其他的评审。我们会 review 你的代码，可能会留下一些评论，你需要解决所有的 thread。等 CI/CD 流水线全部通过，并且拿到至少两个 LGTM 之后，我才会考虑把你的分支 squash and merge 到 develop 里，等待下一个版本发布。你怎么直接上来就想 force push 到 main？！GitHub 上根本不是这样！我拒绝合并！

## 分支

- 基于 `main` 创建，命名为 `<类型>/<内容>`，例如 `feat/add-profile`、`docs/update-readme`。
- 类型限 `feat`、`fix`、`docs`、`chore`，内容不能为空，不能包含空白或额外的 `/`。
- CI 同时兼容旧格式 `add-你的GitHub用户名`，例如 `add-octocat`；新建分支推荐使用 `<类型>/<内容>`。
- 一个分支只提交一个 PR。

## Commit

格式：`<类型>: <简短说明>`

| 类型 | 用途 |
| --- | --- |
| `feat` | 新增文件或内容 |
| `fix` | 修复错误内容 |
| `docs` | 修改说明文档 |
| `chore` | 其他改动 |

- 说明使用 2–50 个字符，一个 commit 只做一件事。
- 禁止 `update`、`111`、`test` 这类无意义说明。

示例：`feat: 添加 members/octocat/octocat.md`

## PR

- 标题格式与 commit 一致，使用 `<类型>: <简短说明>`。
- 除维护者 `mel0nyrame` 外，PR 作者只能改动 `members/自己的GitHub用户名/` 下的 `用户名.txt`、`用户名.md` 和任意名称的 `.html` 文件。可以只改其中一种文件。
- 新增、修改、删除和重命名都受此限制；不能改动其他目录，也不能提交图片、符号链接、子模块或其他附加文件。
- 维护者 `mel0nyrame` 不受文件范围限制，仍需遵守分支、commit、PR 标题和描述规范。
- 创建 PR 时按自动带出的模板填写「做了什么」「改了哪些文件」；用命令行创建时请手动按模板填写。
- 不要暴露真实姓名：标题、描述、文件内容和 commit 的作者名/邮箱都不要写；提交前用 `git config user.name` 和 `git config user.email` 检查。
- 目标分支必须是原仓库的 `main`，不是你 Fork 仓库的 `main`。
- 有冲突时在本地解决后重新提交，不要关闭重开。

## 自动检查

PR 会自动检查分支名、commit、标题、描述和文件范围。检查脚本为 [.github/scripts/check_pr.py](.github/scripts/check_pr.py)。权限依据 PR 作者的 GitHub 用户名判断，不依据触发检查的人或 commit 作者。

检查在默认分支上运行，只读取 PR 的 Git 数据，不执行 PR 中的代码。安全边界和维护者例外的理由见 [检查权限决策](docs/adr/0001--pr-file-permissions.md)。

维护检查脚本时，运行 `python3 -m unittest discover -s .github/scripts -p 'test_*.py'`。

## 提交前检查

- [ ] 文件位置和命名符合 [members/README.md](members/README.md)。
- [ ] 改动范围符合自己的权限，没有提交 `.DS_Store` 等杂项。
- [ ] 分支名、commit message、PR 标题都符合本规范。
- [ ] PR 描述按模板填写，写清了做了什么、改了哪些文件。
- [ ] 没有暴露真实姓名。
- [ ] PR 目标分支是原仓库的 `main`。
