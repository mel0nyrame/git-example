// ③ ES 模块：写了 export，别的文件才能 import
// 注意：这个文件里可以写 import/export，但引入它的 <script> 必须带 type="module"

export function greet(who) {
    return '你好，' + who + '！我是从 JS/module.js 里 import 进来的。';
}

export const add = (a, b) => a + b;
