# 贡献者头像维护

## 名单和生成物

`.github/contributors.json` 保存已收录账号的 ID 和用户名。
生成脚本合并 GitHub 贡献者和 `members/` 下的成员账号。
脚本按账号 ID 去重，并保留名单中的历史账号。
名单包含没有成员目录的贡献者，也包含未被贡献统计识别的学员。
脚本只保存公开用户名和 ID，不保存姓名或邮箱。

README 的 `contributors:start` 与 `contributors:end` 之间是生成区域。
不要手工修改区域内的头像。
脚本按每个账号在 `main` 上最早一次提交的时间先后排列，为每个账号生成独立头像链接。
无法取得提交时间的账号排在最后，同一时间按用户名排列。

## 更新

运行 `python3 .github/scripts/update_contributors.py` 更新名单和头像。
本地需要已认证的 GitHub CLI，工作流使用 `GH_TOKEN`。
运行 `python3 .github/scripts/update_contributors.py --check` 可离线检查生成物。
测试命令为 `python3 -m unittest discover -s .github/scripts -p 'test_*.py'`。

“更新贡献者头像”工作流在 `main` 更新后运行。
它每天还会补查一次，并支持手动运行。
定时补查用于补充延迟出现的 GitHub 贡献者统计。
图片本身仍受 GitHub 头像缓存影响。

API 请求或数据校验失败时，脚本不会更新名单和 README。
账号改名或删除导致查询失败时，维护者需检查成员目录和名单。
脚本不会静默跳过查询失败的成员。

## 写入边界

写入任务只在原仓库的 `main` 上运行。
它不检出 PR 分支，不执行成员网页或脚本。
机器人只暂存 README 和贡献者名单。
现有 PR 检查及学生文件权限保持不变。

自动更新会增加一条机器人提交。
没有变化时，机器人不提交。
工作流串行执行，并检出最新 `main`。
如果其他提交抢先进入 `main`，推送会安全失败。
维护者可以重新运行任务；机器人不会强制推送。
分支保护必须允许这项自动写入，否则需要调整交付方式。

名单保留与权限选择的理由见[相关决策](adr/0002--contributor-avatars.md)。
