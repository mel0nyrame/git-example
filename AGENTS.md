# AGENTS.md

## 开工前

- 对照记忆索引。中文输出、隐私判断、仓库流程三类任务，先 read 对应条目。
- 中文输出前读《中文写作必须遵循 ASD-STE100 改编规则》。

## 按任务导航

- 修改成员文件或审查学生 PR 时，读 [members/README.md](members/README.md)。
- 准备分支或 commit 时，读 README 的[分支](README.md#分支)和 [Commit](README.md#commit) 规范。
- 审查或创建 PR 时，读 README 的 [PR 规范](README.md#pr)；创建时按 [PR 模板](.github/pull_request_template.md)填写。
- 调查或修改 PR 检查时，读[工作流](.github/workflows/pr-check.yml)、[检查脚本](.github/scripts/check_pr.py)和[测试](.github/scripts/test_check_pr.py)。
- 维护贡献者头像、名单或 README 头像区域时，先读[头像维护说明](docs/contributors.md)。
- 查询权限或头像方案的理由时，读 [docs/adr/](docs/adr/)。当前操作规则见对应 README、维护说明和配置。

## 验证入口

- 修改检查脚本、头像生成脚本或相关工作流时，运行回归测试：
  `python3 -m unittest discover -s .github/scripts -p 'test_*.py'`。
- 修改贡献者名单、生成脚本或 README 头像区域时，离线检查生成物：
  `python3 .github/scripts/update_contributors.py --check`。
