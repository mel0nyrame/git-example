<!doctype html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OpenCode 中文介绍 · 为终端而生的开源 AI 编码代理</title>
<meta name="description" content="OpenCode 是一个 MIT 开源、厂商中立的 AI 编码代理，提供终端 TUI、桌面应用、IDE 扩展与 Web 界面。本文介绍它的定位、架构、核心能力与五分钟上手指南。">
<meta name="color-scheme" content="dark light">
<meta property="og:title" content="OpenCode 中文介绍 · 为终端而生的开源 AI 编码代理">
<meta property="og:description" content="开源、模型无关、终端优先。了解 OpenCode 的定位、架构、能力与上手方式。">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect width='24' height='24' rx='5' fill='%230d0d0f'/%3E%3Cpath d='M8 16V8h8' stroke='%23f0b45e' stroke-width='2.4' fill='none' stroke-linecap='square'/%3E%3C/svg%3E">
<script>
  /* 尽早应用主题，避免闪烁 */
  try {
    var savedTheme = localStorage.getItem('opencode-intro-theme');
    if (!savedTheme) {
      savedTheme = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    }
    document.documentElement.dataset.theme = savedTheme;
  } catch (e) {}
</script>
<style>
/* =========================================================
   OpenCode 中文介绍 · 样式表
   深色为默认主题，支持浅色切换
   ========================================================= */
:root {
  --bg: #0a0a0b;
  --bg-2: #0d0d0f;
  --panel: #121215;
  --panel-2: #17171b;
  --line: #26262c;
  --line-soft: #1c1c21;
  --text: #ecebe7;
  --text-2: #c6c3bc;
  --muted: #918d85;
  --accent: #f0b45e;
  --accent-2: #ffd79a;
  --accent-soft: rgba(240, 180, 94, 0.1);
  --accent-line: rgba(240, 180, 94, 0.28);
  --accent-ink: #1a1206;
  --green: #8fe0a8;
  --radius: 16px;
  --shadow: 0 24px 60px -32px rgba(0, 0, 0, 0.9);
  --mono: "JetBrains Mono", "Cascadia Code", "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  --sans: "Inter", "Segoe UI Variable Text", "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif;
  --maxw: 1160px;
}
[data-theme="light"] {
  --bg: #faf8f3;
  --bg-2: #f4f1ea;
  --panel: #ffffff;
  --panel-2: #f6f3ec;
  --line: #e3ddd1;
  --line-soft: #ebe5da;
  --text: #1a1916;
  --text-2: #43403a;
  --muted: #6f6a61;
  --accent: #a9660f;
  --accent-2: #8a5210;
  --accent-soft: rgba(169, 102, 15, 0.09);
  --accent-line: rgba(169, 102, 15, 0.3);
  --accent-ink: #fffaf2;
  --green: #2c7a4b;
  --shadow: 0 24px 50px -34px rgba(60, 45, 20, 0.45);
}
* { box-sizing: border-box; }
html {
  scroll-behavior: smooth;
  scroll-padding-top: 90px;
  -webkit-text-size-adjust: 100%;
}
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  overflow-x: hidden;
}
::selection { background: var(--accent); color: var(--accent-ink); }
img, svg { display: block; }
a { color: inherit; text-decoration: none; }
button { font: inherit; color: inherit; background: none; border: 0; cursor: pointer; }
h1, h2, h3, h4 { margin: 0; font-weight: 620; letter-spacing: -0.02em; line-height: 1.25; }
p { margin: 0; }
ul, ol, dl, dd { margin: 0; padding: 0; }
li { list-style: none; }
code, kbd, pre { font-family: var(--mono); }
.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
.skip-link {
  position: fixed; top: 10px; left: 10px; z-index: 200;
  padding: 10px 16px; border-radius: 8px;
  background: var(--accent); color: var(--accent-ink);
  font-size: 14px; transform: translateY(-160%);
  transition: transform 0.2s;
}
.skip-link:focus-visible { transform: none; }
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
  border-radius: 4px;
}
.wrap {
  width: min(var(--maxw), calc(100% - 48px));
  margin-inline: auto;
}
/* ---------------- 顶部导航 ---------------- */
.site-nav {
  position: fixed; inset: 0 0 auto 0; z-index: 100;
  border-bottom: 1px solid transparent;
  transition: background 0.25s, border-color 0.25s, backdrop-filter 0.25s;
}
.site-nav.is-scrolled {
  background: var(--bg);
  background: color-mix(in srgb, var(--bg) 82%, transparent);
  backdrop-filter: blur(14px) saturate(140%);
  -webkit-backdrop-filter: blur(14px) saturate(140%);
  border-bottom-color: var(--line-soft);
}
.nav-inner {
  display: flex; align-items: center; gap: 24px;
  height: 64px;
}
.brand {
  display: inline-flex; align-items: center; gap: 9px;
  color: var(--text); flex: none;
}
.brand-mark { width: 24px; height: 24px; color: var(--accent); }
.brand-name {
  font-size: 15.5px; font-weight: 640; letter-spacing: -0.01em;
}
.brand-tag {
  font-size: 11px; letter-spacing: 0.08em;
  color: var(--muted); border: 1px solid var(--line);
  padding: 2px 7px; border-radius: 999px;
}
.nav-links {
  display: flex; align-items: center; gap: 4px;
  margin-left: auto;
}
.nav-links a {
  position: relative;
  padding: 7px 12px; border-radius: 8px;
  font-size: 13.5px; color: var(--muted);
  transition: color 0.2s, background 0.2s;
}
.nav-links a:hover { color: var(--text); background: var(--panel); }
.nav-links a.is-active { color: var(--text); }
.nav-links a.is-active::after {
  content: ""; position: absolute; left: 12px; right: 12px; bottom: 2px;
  height: 1.5px; background: var(--accent); border-radius: 2px;
}
.nav-actions { display: flex; align-items: center; gap: 8px; flex: none; }
.icon-btn {
  display: grid; place-items: center;
  width: 36px; height: 36px; border-radius: 9px;
  border: 1px solid var(--line);
  color: var(--text-2);
  transition: color 0.2s, border-color 0.2s, background 0.2s;
}
.icon-btn:hover { color: var(--accent); border-color: var(--accent-line); background: var(--accent-soft); }
.icon-btn svg { width: 17px; height: 17px; fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round; }
[data-theme="dark"] .i-sun { display: none; }
[data-theme="light"] .i-moon { display: none; }
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 9px 14px; border-radius: 9px;
  font-size: 13.5px; font-weight: 520;
  border: 1px solid var(--line);
  transition: transform 0.18s, border-color 0.2s, background 0.2s, color 0.2s;
  white-space: nowrap;
}
.btn:hover { transform: translateY(-1px); }
.btn-ghost { color: var(--text-2); }
.btn-ghost:hover { color: var(--text); border-color: var(--accent-line); background: var(--accent-soft); }
.btn-ghost .gh { width: 15px; height: 15px; fill: currentColor; }
.btn-primary {
  background: var(--accent); color: var(--accent-ink);
  border-color: transparent; font-weight: 640;
}
.btn-primary:hover { background: var(--accent-2); }
.nav-burger { display: none; flex-direction: column; gap: 4px; }
.nav-burger span { display: block; width: 16px; height: 1.6px; background: currentColor; border-radius: 2px; transition: transform 0.2s, opacity 0.2s; }
.nav-burger[aria-expanded="true"] span:nth-child(1) { transform: translateY(5.6px) rotate(45deg); }
.nav-burger[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
.nav-burger[aria-expanded="true"] span:nth-child(3) { transform: translateY(-5.6px) rotate(-45deg); }
.nav-progress {
  height: 1px; width: 0%;
  background: linear-gradient(90deg, transparent, var(--accent));
  transition: width 0.1s linear;
}
/* ---------------- Hero ---------------- */
.hero {
  position: relative;
  padding: 140px 0 72px;
  overflow: hidden;
}
.hero-bg {
  position: absolute; inset: 0; pointer-events: none;
  background:
    radial-gradient(900px 420px at 78% -6%, var(--accent-soft), transparent 70%),
    radial-gradient(760px 380px at 4% 12%, rgba(143, 224, 168, 0.05), transparent 72%);
}
.hero-bg::after {
  content: ""; position: absolute; inset: 0;
  background-image:
    linear-gradient(to right, var(--line-soft) 1px, transparent 1px),
    linear-gradient(to bottom, var(--line-soft) 1px, transparent 1px);
  background-size: 64px 64px;
  opacity: 0.5;
  mask-image: radial-gradient(760px 460px at 62% 22%, #000 10%, transparent 78%);
  -webkit-mask-image: radial-gradient(760px 460px at 62% 22%, #000 10%, transparent 78%);
}
.hero-grid {
  position: relative;
  display: grid;
  grid-template-columns: 1.06fr 0.94fr;
  gap: 56px;
  align-items: center;
}
.eyebrow {
  display: inline-flex; align-items: center; gap: 9px;
  font-family: var(--mono); font-size: 11.5px;
  letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--muted);
  border: 1px solid var(--line);
  background: color-mix(in srgb, var(--panel) 70%, transparent);
  padding: 6px 12px; border-radius: 999px;
  margin-bottom: 24px;
}
.pulse {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 0 0 rgba(143, 224, 168, 0.5);
  animation: pulse 2.4s ease-out infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(143, 224, 168, 0.45); }
  70% { box-shadow: 0 0 0 8px rgba(143, 224, 168, 0); }
  100% { box-shadow: 0 0 0 0 rgba(143, 224, 168, 0); }
}
.hero h1 {
  font-size: clamp(2.3rem, 4.9vw, 3.75rem);
  line-height: 1.1;
  letter-spacing: -0.035em;
  font-weight: 660;
}
.hero h1 .mark {
  background: linear-gradient(100deg, var(--accent) 10%, var(--accent-2) 90%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.lede {
  margin-top: 22px;
  max-width: 34em;
  font-size: 16.5px;
  line-height: 1.78;
  color: var(--text-2);
}
.lede strong { color: var(--text); font-weight: 620; }
/* 安装框 */
.install {
  margin-top: 30px;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: var(--panel);
  overflow: hidden;
  box-shadow: var(--shadow);
}
.install-head {
  display: flex; align-items: center; gap: 10px;
  padding: 7px 8px 7px 10px;
  border-bottom: 1px solid var(--line-soft);
  background: var(--panel-2);
}
.tabs { display: flex; gap: 2px; overflow-x: auto; scrollbar-width: none; }
.tabs::-webkit-scrollbar { display: none; }
.tab {
  padding: 5px 10px; border-radius: 7px;
  font-size: 12.5px; color: var(--muted);
  white-space: nowrap;
  transition: color 0.18s, background 0.18s;
}
.tab:hover { color: var(--text); }
.tab.is-active { color: var(--accent); background: var(--accent-soft); }
.copy-btn {
  margin-left: auto; flex: none;
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 9px; border-radius: 7px;
  font-size: 12px; color: var(--muted);
  transition: color 0.2s, background 0.2s;
}
.copy-btn:hover { color: var(--text); background: var(--panel); }
.copy-btn svg { width: 13px; height: 13px; fill: none; stroke: currentColor; stroke-width: 1.7; stroke-linejoin: round; }
.copy-btn.is-done { color: var(--green); }
.panes { position: relative; }
.pane {
  display: none;
  margin: 0; padding: 16px 16px 17px;
  font-size: 13px; line-height: 1.95;
  color: var(--text-2);
  overflow-x: auto;
  tab-size: 2;
}
.pane.is-active { display: block; }
.c-dim { color: var(--muted); }
.c-p { color: var(--accent); margin-right: 4px; user-select: none; }
.hero-facts {
  display: flex; flex-wrap: wrap; gap: 8px 20px;
  margin-top: 22px;
  font-size: 12.8px; color: var(--muted);
}
.hero-facts li { display: inline-flex; align-items: center; gap: 7px; }
.hero-facts svg {
  width: 13px; height: 13px; flex: none;
  fill: none; stroke: var(--green); stroke-width: 2.2;
  stroke-linecap: round; stroke-linejoin: round;
}
/* 终端示意 */
.hero-art { position: relative; }
.hero-art::before {
  content: ""; position: absolute; inset: -18% -8% -12%;
  background: radial-gradient(closest-side, var(--accent-soft), transparent 75%);
  pointer-events: none;
}
.term {
  position: relative;
  border: 1px solid #2b2b31;
  border-radius: 14px;
  background: #0c0c0e;
  overflow: hidden;
  box-shadow: 0 30px 70px -30px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(255, 255, 255, 0.02) inset;
  font-family: var(--mono);
  font-size: 12.5px;
  line-height: 1.85;
  color: #d8d5ce;
  transform: perspective(1400px) rotateY(-3deg) rotateX(1deg);
  transition: transform 0.6s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.term:hover { transform: perspective(1400px) rotateY(0deg) rotateX(0deg); }
.term-bar {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 13px;
  border-bottom: 1px solid #202024;
  background: #111114;
}
.lights { display: flex; gap: 6px; }
.lights i { width: 9px; height: 9px; border-radius: 50%; background: #35353b; }
.lights i:nth-child(1) { background: #4a3f33; }
.lights i:nth-child(2) { background: #3f4438; }
.lights i:nth-child(3) { background: #3a3a41; }
.term-title { margin-inline: auto; font-size: 11.5px; color: #7e7a72; }
.term-ver {
  font-size: 10.5px; color: #c9a06a;
  border: 1px solid #3a3025; background: #1a1611;
  padding: 1px 6px; border-radius: 5px;
}
.term-body { padding: 16px 18px 18px; }
.term-body p { white-space: pre-wrap; word-break: break-word; }
.t-gap { height: 6px; }
.t-dim { color: #7b776f; }
.t-indent { padding-left: 16px; }
.t-body { color: #b9b5ad; }
.t-prompt { color: #f0b45e; margin-right: 6px; }
.t-branch { color: #8fa8c8; }
.t-key { color: #cfcac2; }
.t-mode { color: #0c0c0e; background: #f0b45e; padding: 0 6px; border-radius: 4px; font-size: 11px; }
.t-ref { color: #9ec6e8; text-decoration: underline; text-decoration-color: rgba(158, 198, 232, 0.35); text-underline-offset: 3px; }
.t-accent { color: #f0b45e; }
.t-foot {
  margin-top: 14px; padding-top: 12px;
  border-top: 1px solid #1e1e22;
  color: #6f6b64; font-size: 11px;
}
.t-foot .t-key { color: #a8a29a; border: 1px solid #2c2c32; border-radius: 4px; padding: 0 4px; }
.t-caret {
  display: inline-block; width: 6px; height: 13px;
  margin-left: 6px; vertical-align: -2px;
  background: #f0b45e;
  animation: blink 1.15s steps(2, start) infinite;
}
@keyframes blink { to { opacity: 0; } }
.art-note {
  margin-top: 12px; text-align: right;
  font-size: 11px; color: var(--muted); font-family: var(--mono);
}
/* 数据条 */
.stats {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-top: 64px;
  padding-top: 26px;
  border-top: 1px solid var(--line-soft);
}
.stat dt {
  font-family: var(--mono); font-size: 10.5px;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 6px;
}
.stat dd {
  font-size: clamp(1.4rem, 2.6vw, 1.9rem);
  font-weight: 600; letter-spacing: -0.03em;
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
}
.stat dd .plus { color: var(--accent); font-size: 0.75em; }
.stat-license dd { color: var(--green); }
.stats-note { margin-top: 16px; font-size: 11.5px; color: var(--muted); }
/* ---------------- 通用区块 ---------------- */
.section { padding: 100px 0; position: relative; }
.section-alt {
  background: linear-gradient(180deg, transparent, var(--bg-2) 18%, var(--bg-2) 82%, transparent);
  border-top: 1px solid var(--line-soft);
  border-bottom: 1px solid var(--line-soft);
}
.sec-head { max-width: 760px; margin-bottom: 52px; }
.sec-kicker {
  font-family: var(--mono); font-size: 11.5px;
  letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 16px;
  display: flex; align-items: center; gap: 10px;
}
.sec-kicker::after {
  content: ""; height: 1px; width: 44px;
  background: var(--accent-line);
}
.sec-head h2 {
  font-size: clamp(1.65rem, 3.3vw, 2.5rem);
  letter-spacing: -0.03em;
  line-height: 1.22;
}
.sec-sub {
  margin-top: 16px;
  font-size: 15.5px; line-height: 1.8;
  color: var(--muted);
  max-width: 40em;
}
.split {
  display: grid;
  grid-template-columns: 1.12fr 0.88fr;
  gap: 56px;
  align-items: start;
}
.split-wide { grid-template-columns: 1.02fr 0.98fr; gap: 48px; }
.prose p {
  color: var(--text-2);
  font-size: 15.3px;
  line-height: 1.85;
  margin-bottom: 18px;
}
.prose p:last-child { margin-bottom: 0; }
.prose strong { color: var(--text); font-weight: 620; }
.prose h3 { font-size: 17px; margin-bottom: 14px; }
.prose code,
.callout code,
.faq-list code {
  font-size: 0.86em;
  padding: 1.5px 6px;
  border-radius: 5px;
  color: var(--accent-2);
  background: var(--accent-soft);
  border: 1px solid var(--accent-line);
  white-space: nowrap;
}
.facts-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel);
  padding: 26px;
  box-shadow: var(--shadow);
}
.facts-card h3 {
  font-size: 12px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--muted);
  margin-bottom: 14px; font-family: var(--mono); font-weight: 500;
}
.facts-card dl > div {
  display: grid;
  grid-template-columns: 78px 1fr;
  gap: 12px;
  padding: 11px 0;
  border-top: 1px solid var(--line-soft);
  font-size: 13.3px;
  line-height: 1.6;
}
.facts-card dt { color: var(--muted); }
.facts-card dd { color: var(--text-2); }
.callout {
  display: flex; gap: 12px; align-items: flex-start;
  margin-top: 40px;
  padding: 16px 18px;
  border: 1px dashed var(--line);
  border-radius: 12px;
  background: var(--panel);
  color: var(--muted);
  font-size: 13.8px;
  line-height: 1.75;
}
.callout svg {
  width: 17px; height: 17px; flex: none; margin-top: 3px;
  fill: none; stroke: var(--accent); stroke-width: 1.7;
  stroke-linecap: round;
}
.callout strong { color: var(--text); }
/* ---------------- 卡片网格 ---------------- */
.grid { display: grid; gap: 16px; }
.grid-4 { grid-template-columns: repeat(4, 1fr); }
.grid-2 { grid-template-columns: repeat(2, 1fr); }
.card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel);
  padding: 22px;
  transition: transform 0.25s, border-color 0.25s, background 0.25s;
}
.card:hover {
  transform: translateY(-3px);
  border-color: var(--accent-line);
  background: var(--panel-2);
}
.card-icon {
  display: grid; place-items: center;
  width: 38px; height: 38px;
  border-radius: 10px;
  color: var(--accent);
  background: var(--accent-soft);
  border: 1px solid var(--accent-line);
}
.card-icon svg {
  width: 19px; height: 19px;
  fill: none; stroke: currentColor; stroke-width: 1.6;
  stroke-linecap: round; stroke-linejoin: round;
}
.card h3 { font-size: 15.5px; margin: 16px 0 8px; letter-spacing: -0.01em; }
.card p { font-size: 13.6px; line-height: 1.75; color: var(--muted); }
.card code {
  font-size: 0.9em; color: var(--accent-2);
}
/* ---------------- 架构图 ---------------- */
.arch {
  border: 1px solid var(--line);
  border-radius: 18px;
  background:
    radial-gradient(600px 300px at 50% 0%, var(--accent-soft), transparent 70%),
    var(--panel);
  padding: 30px 26px;
}
.arch-row {
  display: flex; flex-wrap: wrap; gap: 9px;
  justify-content: center;
}
.chip {
  border: 1px solid var(--line);
  background: var(--panel-2);
  border-radius: 10px;
  padding: 9px 15px;
  font-size: 13px;
  color: var(--text-2);
  white-space: nowrap;
}
.chip-sm { font-size: 11.8px; padding: 7px 11px; color: var(--muted); }
.arch-link {
  position: relative;
  display: grid; place-items: center;
  height: 58px;
}
.arch-link::before {
  content: "";
  position: absolute; left: 50%; top: 6px; bottom: 6px;
  width: 1px;
  background: linear-gradient(180deg, transparent, var(--accent-line) 30%, var(--accent-line) 70%, transparent);
}
.arch-link span {
  position: relative;
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.04em;
  color: var(--muted);
  background: var(--panel);
  padding: 3px 9px;
  border-radius: 999px;
  border: 1px solid var(--line-soft);
}
.node {
  text-align: center;
  border: 1px solid var(--accent-line);
  background: linear-gradient(180deg, var(--accent-soft), transparent);
  border-radius: 12px;
  padding: 14px 26px;
}
.node strong { display: block; font-size: 14.5px; letter-spacing: -0.01em; }
.node small { display: block; margin-top: 4px; font-size: 11.5px; color: var(--muted); }
.ticks { margin: 4px 0 20px; display: grid; gap: 9px; }
.ticks li {
  position: relative; padding-left: 22px;
  font-size: 14.2px; line-height: 1.7; color: var(--text-2);
}
.ticks li::before {
  content: ""; position: absolute; left: 4px; top: 0.62em;
  width: 7px; height: 7px; border-radius: 2px;
  background: var(--accent); opacity: 0.85;
}
.code-block {
  margin: 14px 0 0;
  padding: 15px 17px;
  border: 1px solid #2b2b31;
  border-radius: 11px;
  background: #0c0c0e;
  color: #d8d5ce;
  font-size: 12.6px;
  line-height: 1.9;
  overflow-x: auto;
  tab-size: 2;
}
.code-block .c-dim { color: #77736b; }
.code-block .c-p { color: #f0b45e; }
/* ---------------- 上手步骤 ---------------- */
.steps { display: grid; gap: 14px; counter-reset: step; }
.step {
  display: grid;
  grid-template-columns: 52px 1fr;
  gap: 20px;
  align-items: start;
  padding: 22px 24px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel);
  transition: border-color 0.25s, background 0.25s;
}
.step:hover { border-color: var(--accent-line); background: var(--panel-2); }
.step-no {
  display: grid; place-items: center;
  width: 34px; height: 34px;
  border-radius: 50%;
  border: 1px solid var(--accent-line);
  background: var(--accent-soft);
  color: var(--accent);
  font-family: var(--mono); font-size: 13px;
}
.step-body h3 { font-size: 16px; margin-bottom: 6px; }
.step-body > p { font-size: 14px; line-height: 1.75; color: var(--muted); }
.step .code-block { margin-top: 12px; }
/* ---------------- 速查表 ---------------- */
.table-wrap {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--panel);
}
.cheat { width: 100%; border-collapse: collapse; }
.cheat th {
  text-align: left;
  padding: 13px 20px;
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 500;
  background: var(--panel-2);
  border-bottom: 1px solid var(--line);
}
.cheat td {
  padding: 13px 20px;
  font-size: 14px;
  color: var(--text-2);
  border-top: 1px solid var(--line-soft);
  vertical-align: top;
}
.cheat tbody tr:first-child td { border-top: 0; }
.cheat tbody tr:hover td { background: var(--panel-2); }
.cheat td:first-child { white-space: nowrap; }
.cheat td code {
  font-size: 12.6px;
  color: var(--accent-2);
  background: var(--accent-soft);
  border: 1px solid var(--accent-line);
  border-radius: 5px;
  padding: 1.5px 7px;
}
.cheat td code + code { margin-left: 4px; }
.cheat td kbd {
  display: inline-block;
  font-size: 11.5px;
  padding: 2px 8px;
  border: 1px solid var(--line);
  border-bottom-width: 2px;
  border-radius: 6px;
  background: var(--panel-2);
  color: var(--text-2);
}
/* ---------------- 适合谁 ---------------- */
.who {
  border: 1px solid var(--line);
  border-top: 2px solid var(--accent-line);
  border-radius: 12px;
  background: var(--panel);
  padding: 22px;
  transition: border-color 0.25s, transform 0.25s;
}
.who:hover { transform: translateY(-2px); border-top-color: var(--accent); }
.who h3 { font-size: 15px; margin-bottom: 8px; }
.who p { font-size: 13.4px; line-height: 1.75; color: var(--muted); }
/* ---------------- 生态 ---------------- */
.eco {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel);
  padding: 24px;
  transition: border-color 0.25s, background 0.25s;
}
.eco:hover { border-color: var(--accent-line); background: var(--panel-2); }
.eco-top { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 10px; }
.eco h3 { font-size: 16.5px; }
.eco p { font-size: 13.8px; line-height: 1.75; color: var(--muted); }
.eco code { font-size: 0.9em; color: var(--accent-2); }
.tag {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
  border: 1px solid var(--accent-line);
  background: var(--accent-soft);
  padding: 3px 8px;
  border-radius: 999px;
}
/* ---------------- FAQ ---------------- */
.faq-list { border-top: 1px solid var(--line); }
.faq-list details {
  border-bottom: 1px solid var(--line);
  padding: 18px 2px;
}
.faq-list summary {
  display: flex; align-items: center; gap: 14px;
  font-size: 15.2px;
  font-weight: 520;
  color: var(--text);
  cursor: pointer;
  list-style: none;
  transition: color 0.2s;
}
.faq-list summary::-webkit-details-marker { display: none; }
.faq-list summary:hover { color: var(--accent); }
.faq-list summary::after {
  content: "+";
  margin-left: auto;
  font-family: var(--mono);
  font-size: 16px;
  color: var(--accent);
  line-height: 1;
  transition: transform 0.25s;
}
.faq-list details[open] summary::after { transform: rotate(45deg); }
.faq-list details p {
  margin-top: 12px;
  padding-left: 0;
  max-width: 62em;
  font-size: 14.2px;
  line-height: 1.82;
  color: var(--muted);
}
/* ---------------- CTA ---------------- */
.cta { padding: 100px 0; }
.cta-inner {
  text-align: center;
  border: 1px solid var(--line);
  border-radius: 24px;
  padding: 60px 32px;
  background:
    radial-gradient(560px 240px at 50% 0%, var(--accent-soft), transparent 70%),
    var(--panel);
}
.cta h2 { font-size: clamp(1.55rem, 3vw, 2.2rem); letter-spacing: -0.03em; }
.cta p { margin-top: 12px; color: var(--muted); font-size: 14.8px; }
.cta-actions {
  display: flex; flex-wrap: wrap; gap: 10px;
  justify-content: center;
  margin-top: 26px;
}
/* ---------------- 页脚 ---------------- */
.site-footer {
  border-top: 1px solid var(--line-soft);
  padding: 56px 0 28px;
  background: var(--bg-2);
}
.footer-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 48px;
}
.footer-about p {
  margin-top: 14px;
  max-width: 26em;
  font-size: 12.8px;
  line-height: 1.8;
  color: var(--muted);
}
.footer-links { display: flex; gap: 64px; justify-content: flex-end; }
.footer-links h4 {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 12px;
  font-weight: 500;
}
.footer-links a {
  display: block;
  font-size: 13.5px;
  color: var(--text-2);
  padding: 5px 0;
  transition: color 0.2s;
}
.footer-links a:hover { color: var(--accent); }
.footer-bottom {
  display: flex; flex-wrap: wrap; gap: 12px;
  justify-content: space-between;
  margin-top: 44px;
  padding-top: 20px;
  border-top: 1px solid var(--line-soft);
  font-size: 12px;
  color: var(--muted);
}
.footer-bottom a:hover { color: var(--accent); }
/* ---------------- 动效 ---------------- */
.reveal {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.7s cubic-bezier(0.2, 0.7, 0.2, 1), transform 0.7s cubic-bezier(0.2, 0.7, 0.2, 1);
  will-change: opacity, transform;
}
.reveal.is-in { opacity: 1; transform: none; }
/* ---------------- 响应式 ---------------- */
@media (max-width: 1080px) {
  .hero-grid { grid-template-columns: 1fr; gap: 44px; }
  .hero { padding-top: 124px; }
  .hero-art { max-width: 640px; }
  .term { transform: none; }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
  .split, .split-wide { grid-template-columns: 1fr; gap: 36px; }
  .stats { grid-template-columns: repeat(3, 1fr); gap: 24px; }
  .footer-grid { grid-template-columns: 1fr; gap: 32px; }
  .footer-links { justify-content: flex-start; gap: 56px; }
  .nav-links a { padding: 7px 9px; }
}
@media (max-width: 860px) {
  .nav-links {
    position: fixed;
    top: 64px; left: 0; right: 0;
    display: none;
    flex-direction: column;
    align-items: stretch;
    gap: 2px;
    padding: 12px 20px 20px;
    background: var(--bg);
    border-bottom: 1px solid var(--line);
    box-shadow: var(--shadow);
  }
  .nav-links.is-open { display: flex; }
  .nav-links a { padding: 11px 10px; font-size: 14.5px; }
  .nav-links a.is-active::after { display: none; }
  .nav-links a.is-active { color: var(--accent); }
  .nav-burger { display: flex; }
  .brand-tag { display: none; }
  .nav-actions .btn-ghost { padding: 8px 10px; }
}
@media (max-width: 640px) {
  .wrap { width: calc(100% - 36px); }
  .hero { padding: 112px 0 56px; }
  .hero h1 { font-size: clamp(2rem, 8.6vw, 2.6rem); }
  .lede { font-size: 15.5px; }
  .section { padding: 68px 0; }
  .sec-head { margin-bottom: 36px; }
  .grid-4, .grid-2 { grid-template-columns: 1fr; }
  .stats { grid-template-columns: repeat(2, 1fr); margin-top: 44px; }
  .stat-license { display: none; }
  .step { grid-template-columns: 1fr; gap: 14px; padding: 20px; }
  .step-no { width: 30px; height: 30px; font-size: 12px; }
  .cheat th, .cheat td { padding: 11px 14px; }
  .cheat td { font-size: 13px; }
  .arch { padding: 22px 16px; }
  .chip { padding: 8px 11px; font-size: 12px; }
  .cta-inner { padding: 40px 22px; }
  .term-body { padding: 14px 14px 16px; font-size: 11.8px; }
  .t-indent { padding-left: 12px; }
  .footer-links { gap: 40px; flex-wrap: wrap; }
  .facts-card { padding: 20px; }
  .facts-card dl > div { grid-template-columns: 72px 1fr; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
  }
  .reveal { opacity: 1; transform: none; }
  .term { transform: none; }
}
@media print {
  .site-nav, .hero-bg, .cta, .site-footer { display: none; }
  body { background: #fff; color: #000; }
  .reveal { opacity: 1; transform: none; }
}
</style>
</head>
<body>
<a class="skip-link" href="#main">跳到正文</a>
<header class="site-nav" id="siteNav">
  <div class="wrap nav-inner">
    <a class="brand" href="#top" aria-label="OpenCode 中文介绍 · 回到顶部">
      <svg class="brand-mark" viewBox="0 0 24 24" aria-hidden="true">
        <rect x="2.5" y="2.5" width="19" height="19" rx="4.5" fill="none" stroke="currentColor" stroke-width="1.6" />
        <path d="M8 16.5V8h8" fill="none" stroke="currentColor" stroke-width="2.2" />
      </svg>
      <span class="brand-name">OpenCode</span>
      <span class="brand-tag">中文介绍</span>
    </a>
    <nav class="nav-links" id="navLinks" aria-label="页面导航">
      <a href="#what">是什么</a>
      <a href="#features">能力</a>
      <a href="#arch">架构</a>
      <a href="#start">上手</a>
      <a href="#cheatsheet">速查</a>
      <a href="#faq">问答</a>
    </nav>
    <div class="nav-actions">
      <button class="icon-btn" id="themeToggle" type="button" aria-label="切换深色 / 浅色主题" title="切换主题">
        <svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.2" /><path d="M12 2.5v2.2M12 19.3v2.2M21.5 12h-2.2M4.7 12H2.5M18.7 5.3l-1.6 1.6M6.9 17.1l-1.6 1.6M18.7 18.7l-1.6-1.6M6.9 6.9L5.3 5.3" /></svg>
        <svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z" /></svg>
      </button>
      <a class="btn btn-ghost" href="https://github.com/anomalyco/opencode" target="_blank" rel="noopener noreferrer">
        <svg viewBox="0 0 16 16" aria-hidden="true" class="gh"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z" /></svg>
        GitHub
      </a>
      <button class="icon-btn nav-burger" id="navBurger" type="button" aria-label="展开导航" aria-expanded="false" aria-controls="navLinks">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
  <div class="nav-progress" id="navProgress"></div>
</header>
<main id="main">
  <!-- ============ HERO ============ -->
  <section class="hero" id="top">
    <div class="hero-bg" aria-hidden="true"></div>
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <p class="eyebrow"><span class="pulse"></span>开源 · MIT 许可 · 约 21.5 万 GitHub Stars</p>
        <h1>把 AI 放进终端，<br>让它和你<span class="mark">一起写代码</span></h1>
        <p class="lede">
          <strong>OpenCode</strong> 是一个开源、厂商中立的 AI 编码代理。它在终端、桌面应用、IDE 和浏览器里，
          用你指定的任意模型读仓库、改文件、跑命令、查文档——不把你绑在任何一家模型商身上。
        </p>
        <div class="install" id="install">
          <div class="install-head">
            <div class="tabs" role="tablist" aria-label="安装方式">
              <button class="tab is-active" role="tab" aria-selected="true" data-tab="unix" type="button">macOS / Linux</button>
              <button class="tab" role="tab" aria-selected="false" data-tab="npm" type="button">npm</button>
              <button class="tab" role="tab" aria-selected="false" data-tab="docker" type="button">Docker</button>
              <button class="tab" role="tab" aria-selected="false" data-tab="win" type="button">Windows</button>
            </div>
            <button class="copy-btn" id="copyInstall" type="button" aria-label="复制安装命令">
              <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2" /><path d="M6 15H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v1" /></svg>
              <span>复制</span>
            </button>
          </div>
          <div class="panes">
            <pre class="pane is-active" data-pane="unix"><code><span class="c-dim"># 安装 OpenCode 2</span>
<span class="c-p">$</span> curl -fsSL https://opencode.ai/v2/install | bash</code></pre>
            <pre class="pane" data-pane="npm"><code><span class="c-dim"># npm 包会按平台挑选原生二进制</span>
<span class="c-p">$</span> npm install -g opencode-ai
<span class="c-dim"># 也可以：brew install anomalyco/tap/opencode</span></code></pre>
            <pre class="pane" data-pane="docker"><code><span class="c-dim"># 镜像使用版本号标签</span>
<span class="c-p">$</span> docker run -it --rm ghcr.io/anomalyco/opencode:2.0.0</code></pre>
            <pre class="pane" data-pane="win"><code><span class="c-dim"># 推荐在 WSL 中使用，或下载独立二进制</span>
<span class="c-p">$</span> wsl --install
<span class="c-p">$</span> curl -fsSL https://opencode.ai/v2/install | bash</code></pre>
          </div>
        </div>
        <ul class="hero-facts">
          <li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5" /></svg>免费模型，无需注册即可起步</li>
          <li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5" /></svg>75+ 模型提供商，含本地模型</li>
          <li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5" /></svg>Windows / macOS / Linux</li>
        </ul>
      </div>
      <div class="hero-art">
        <div class="term" role="img" aria-label="OpenCode 终端界面示意：在 plan 模式下规划给 settings 路由添加鉴权">
          <div class="term-bar">
            <span class="lights" aria-hidden="true"><i></i><i></i><i></i></span>
            <span class="term-title">opencode — ~/code/notes</span>
            <span class="term-ver">v2</span>
          </div>
          <div class="term-body">
            <p class="t-dim">~/code/notes <span class="t-branch">git:(main)</span></p>
            <p><span class="t-prompt">❯</span> opencode</p>
            <p class="t-gap"></p>
            <p class="t-dim t-indent">opencode <span class="t-key">v2</span> &nbsp;·&nbsp; model <span class="t-key">claude-sonnet</span> &nbsp;·&nbsp; <span class="t-mode">plan</span></p>
            <p class="t-gap"></p>
            <p><span class="t-prompt">❯</span> 给 /settings 加上鉴权，参考 <span class="t-ref">@packages/functions/src/notes.ts</span></p>
            <p class="t-gap"></p>
            <p class="t-accent">● 计划</p>
            <p class="t-indent t-body">1. 复用 notes.ts 中的 requireUser() 中间件</p>
            <p class="t-indent t-body">2. 在 settings.ts 的 handler 前挂载</p>
            <p class="t-indent t-body">3. 补一条 401 的集成测试</p>
            <p class="t-gap"></p>
            <p class="t-dim t-indent">按 Tab 切到 build 模式开始实施…</p>
            <p class="t-foot">
              <span class="t-key">TAB</span> 模式 · <span class="t-key">/</span> 命令 · <span class="t-key">@</span> 文件<span class="t-caret" aria-hidden="true"></span>
            </p>
          </div>
        </div>
        <p class="art-note">界面示意，非真实截图</p>
      </div>
    </div>
    <div class="wrap">
      <dl class="stats">
        <div class="stat"><dt>GitHub Stars</dt><dd>215K<span class="plus">+</span></dd></div>
        <div class="stat"><dt>贡献者</dt><dd>950<span class="plus">+</span></dd></div>
        <div class="stat"><dt>提交</dt><dd>20K<span class="plus">+</span></dd></div>
        <div class="stat"><dt>每月使用开发者</dt><dd>16M</dd></div>
        <div class="stat stat-license"><dt>许可</dt><dd>MIT</dd></div>
      </dl>
      <p class="stats-note">数据来自 opencode.ai 官网，核对于 2026-10-23；数字会随项目增长而变化。</p>
    </div>
  </section>
  <!-- ============ WHAT ============ -->
  <section class="section" id="what">
    <div class="wrap">
      <header class="sec-head reveal">
        <p class="sec-kicker">01 / 定位</p>
        <h2>它不是一个补全插件，<br>而是一个能自己动手的代理</h2>
        <p class="sec-sub">
          补全工具预测你的下一行；代理则接受一个目标，自己决定读哪些文件、跑哪些命令、改哪几行，
          过程中把关键动作交给你确认。
        </p>
      </header>
      <div class="split">
        <div class="prose reveal">
          <p>
            你在项目目录里敲下 <code>opencode</code>，得到的是一个全屏终端界面：左边是对话，右边是文件与 diff，
            下方是输入框。它可以按 <code>@</code> 模糊搜索仓库里的文件、自动加载对应的语言服务器、
            在改动前先给出计划，在改动后展示逐文件的差异。
          </p>
          <p>
            更关键的是它的取舍——<strong>不绑定模型厂商</strong>。通过 Models.dev 接 75+ 提供商，
            也能复用你已有的 GitHub Copilot 或 ChatGPT Plus/Pro 订阅，甚至接本地 Ollama。
            如果懒得挑，官方还有经过实测筛选的 <strong>Zen</strong> 模型集与每月 10 美元的 <strong>Go</strong> 订阅。
          </p>
          <p>
            代码层面它完全开源（MIT），仓库公开、可审计、可 fork。官方声明不存储你的代码与上下文数据
            （使用官方免费模型时除外），因此也被用在隐私敏感的环境里。对合规有要求的团队，还有企业版。
          </p>
          <p>
            值得单独一提的是它的<strong>客户端 / 服务端架构</strong>：TUI 只是一个客户端，
            背后是一个本地 HTTP 服务，暴露 OpenAPI 3.1 与 SSE 事件流。这件事决定了后面所有的可扩展性。
          </p>
        </div>
        <aside class="facts-card reveal">
          <h3>速览</h3>
          <dl>
            <div><dt>项目</dt><dd>anomalyco/opencode（Anomaly 团队维护）</dd></div>
            <div><dt>许可</dt><dd>MIT，完全开源</dd></div>
            <div><dt>形态</dt><dd>终端 TUI · 桌面应用 · IDE 扩展 · Web</dd></div>
            <div><dt>技术栈</dt><dd>TypeScript / Bun 核心 + Go 编写的 TUI</dd></div>
            <div><dt>模型接入</dt><dd>Models.dev，75+ 提供商，支持本地模型</dd></div>
            <div><dt>当前版本</dt><dd>OpenCode 2（与 1 共用 <code>opencode</code> 命令）</dd></div>
            <div><dt>价格</dt><dd>软件免费；模型可用免费额度、自备 Key 或订阅</dd></div>
          </dl>
        </aside>
      </div>
      <p class="callout reveal">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M12 11v5.5M12 7.6v.2" /></svg>
        <span><strong>版本提醒：</strong>OpenCode 1 与 OpenCode 2 都使用 <code>opencode</code> 命令，默认情况下不能并存。
        本页以 <strong>v2</strong> 为主；从旧版本升级请先看官方迁移文档，安装脚本地址也不同（v2 是 <code>/v2/install</code>）。</span>
      </p>
    </div>
  </section>
  <!-- ============ FEATURES ============ -->
  <section class="section section-alt" id="features">
    <div class="wrap">
      <header class="sec-head reveal">
        <p class="sec-kicker">02 / 能力</p>
        <h2>八件它做得很到位的事</h2>
        <p class="sec-sub">从模型接入到会话回滚，这些设计共同指向同一个目标：让代理的行为可预期、可控制、可复现。</p>
      </header>
      <div class="grid grid-4">
        <article class="card reveal">
          <span class="card-icon"><svg viewBox="0 0 24 24"><rect x="2.5" y="4" width="19" height="14" rx="2.5" /><path d="M8 20.5h8M7.5 8.5l2.5 2.5-2.5 2.5M12.5 13.5h3.5" /></svg></span>
          <h3>终端优先，多端同源</h3>
          <p>核心体验是终端里的全屏 TUI，同时提供桌面应用、IDE 扩展和 Web 界面。它们连的是同一个本地服务，会话与配置共用。</p>
        </article>
        <article class="card reveal">
          <span class="card-icon"><svg viewBox="0 0 24 24"><path d="M3 7.5h18M3 12h18M3 16.5h12" /><circle cx="18" cy="16.5" r="3" /></svg></span>
          <h3>任意
