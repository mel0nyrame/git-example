# OpenCode 中文介绍页

一个纯静态的单页站点：介绍开源 AI 编码代理 **OpenCode**（终端 TUI / 桌面端 / IDE / Web）。
无构建步骤、无外部依赖（不加载任何 CDN 字体或脚本），双击即可打开，也可以直接丢到任意静态托管上。

## 打开方式

直接双击 `index.html`，或在浏览器里打开它。若想用本地服务器：

```bash
python -m http.server 8000
# 然后访问 http://localhost:8000
```

## 文件结构

```
opencode-site/
├── index.html   # 页面结构与全部文案
├── styles.css   # 设计系统：颜色变量、布局、响应式、动效
└── script.js    # 主题切换、导航高亮、安装命令复制、入场动画、FAQ 折叠
```

## 想改点什么

| 需求 | 位置 |
| --- | --- |
| 改文案 | `index.html`，每个 `section` 开头都有注释标记（HERO / WHAT / FEATURES …） |
| 改配色 | `styles.css` 顶部 `:root` 与 `[data-theme="light"]` 中的变量 |
| 改数据条数字 | `index.html` 中 `.stats` 区块 |
| 改安装命令 | `index.html` 中 `.panes` 里的四个 `pre.pane` |
| 换字体 | `styles.css` 的 `--sans` / `--mono` 变量（默认使用系统字体，保证离线可用） |

页面默认深色主题，右上角按钮可切换浅色并记住偏好；如果系统偏好浅色，首次访问会自动用浅色。

## 内容说明

- 事实与数据核对于 **2026-10-23**，来源为 [opencode.ai](https://opencode.ai) 官网与官方文档（含 V2 文档、Server API）。
- 本页是第三方整理的中文介绍，非官方页面；命令与功能可能随版本变化。
- 终端窗口是界面示意，不是真实截图。
- 同目录外的 `../opencode-intro.md` 是这份内容的 Markdown 版本，方便复制到别处。
