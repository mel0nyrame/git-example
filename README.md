# Git 练习仓库

用于学习 Git 的仓库。你通过 Pull Request 把自己的文件加入仓库。

个人文件的放置规则见 [members/README.md](members/README.md)。

## 贡献者

[![贡献者头像](https://contrib.rocks/image?repo=mel0nyrame/git-example&max=1000)](https://github.com/mel0nyrame/git-example/graphs/contributors)

## 分支

- 基于 `main` 创建，命名 `add-你的用户名`，例如 `add-octocat`。
- 一个分支只提交一个 PR。

## Commit

格式：`<类型>: <简短说明>`

| 类型 | 用途 |
| --- | --- |
| `feat` | 新增文件或内容 |
| `fix` | 修复错误内容 |
| `docs` | 修改说明文档 |
| `chore` | 其他改动 |

- 说明不超过 50 字符，一个 commit 只做一件事。
- 禁止 `update`、`111`、`test` 这类无意义说明。

示例：`feat: 添加 members/octocat/octocat.md`

## PR

- 只包含自己的文件，标题格式与 commit 一致。
- 创建 PR 时按自动带出的模板填写「做了什么」「改了哪些文件」；用命令行创建时请手动按模板填写。
- 不要暴露真实姓名：标题、描述、文件内容和 commit 的作者名/邮箱都不要写；提交前用 `git config user.name` 和 `git config user.email` 检查。
- 目标分支必须是原仓库的 `main`，不是你 Fork 仓库的 `main`。
- 有冲突时在本地解决后重新提交，不要关闭重开。

## 提交前检查

- [ ] 文件位置和命名符合 [members/README.md](members/README.md)。
- [ ] 没有改动他人的文件，也没有提交 `.DS_Store` 等杂项。
- [ ] 分支名、commit message、PR 标题都符合本规范。
- [ ] PR 描述按模板填写，写清了做了什么、改了哪些文件。
- [ ] 没有暴露真实姓名。
- [ ] PR 目标分支是原仓库的 `main`。
