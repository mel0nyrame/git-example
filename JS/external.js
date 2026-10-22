// ② 外部脚本：由 <script src="JS/external.js"></script> 引入
// 外部脚本和 HTML 里的内联脚本共用同一个全局作用域

print('外部', '我是 JS/external.js 里的代码，被 src 引入后执行。');

// 挂到 window 上，别的脚本（包括模块脚本）也能读到
window.externalMessage = '我是外部脚本创建的变量';
