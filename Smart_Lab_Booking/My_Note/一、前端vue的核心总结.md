

## 1. 掌握 Vue3 单文件组件的标准写法，理解结构、逻辑、样式分离与 scoped 样式隔离

```vue
<template>
  <!-- 模板：写HTML结构，页面长什么样子 -->
</template>

<script setup>
  <!-- 脚本：写JS逻辑，处理数据、事件、导入组件、路由 -->
</script>

<style scoped>
  <!-- 样式：写CSS，控制页面长什么外观 -->
</style>
```

1. **单文件组件(SFC)**：一个 `.vue` 文件，把「页面结构、业务逻辑、CSS样式」全部放在同一个文件里，这就是Vue标准写法。
2. **结构、逻辑、样式分离**
    - `<template>`：只管页面长啥样（标签、按钮、输入框）
    - `<script setup>`：只管业务逻辑（变量、登录函数、导入路由）
    - `<style>`：只管外观（颜色、宽高、居中、阴影）
        
        > 各司其职，不要把js写在template，不要把css写在script。
        
3. **`scoped` 样式隔离（重点）**
    - 加了 `scoped`：**这个css只对当前这个vue文件生效，不会污染别的页面组件**。
    - 去掉 `scoped`：样式变成全局，写的css会影响项目里所有页面，容易出现样式冲突。

> 例子：`Login.vue` 写的 `.login-box` 样式，加了scoped，就不会跑到 Register.vue 里生效。

---

## 2. 能使用 Element Plus 表单组件快速搭建登录、注册类页面，熟练使用 v‑model 双向绑定

### Element Plus表单组件
**(详细零散的知识点在  03. 开发前端登录页面)**
`el-form`、`el-form-item`、`el-input`、`el-button` 这些不是原生html标签，是UI库封装好的组件。 不用自己写input的css，直接拿过来拼一拼，快速做出登录注册页面。

### v‑model 双向绑定（核心）

```vue
<el-input v-model="form.username" placeholder="请输入账号"/>
```

```javascript
const form = reactive({
  username: ''
})
```

**双向 = 两个方向同步：**

1. ✍️ 用户在输入框打字 → 自动更新 `form.username` 变量（视图 → 数据）
2. 🧑‍💻 代码修改 `form.username = 'admin'` → 输入框内容自动跟着改变（数据 → 视图）

> 对比原生html：原生需要手动获取dom、拿value赋值，很麻烦；`v‑model` Vue帮你封装好了。 在登录页面，点击登录的时候，直接拿 `form.username`、`form.password` 就拿到用户输入，不需要去读DOM。

简单记忆：**v-model 就是输入框和JS变量之间的自动桥梁**。

---

## 3. 理解 vue‑router 的配置逻辑，掌握重定向、懒加载、嵌套路由三种核心用法

> vue‑router 作用：管理浏览器地址栏 URL 和页面组件的对应关系。访问 `/login` 就展示 Login.vue。

### ① 重定向 redirect

```javascript
{ path: '/', redirect: '/manager/home' }
```

含义：当访问根地址 `/` 的时候，**自动跳转到 `/manager/home`**。 解决问题：打开首页 `/` 什么页面都不渲染，出现空白页。

### ② 路由懒加载 `() => import('xxx.vue')`

```javascript
component: () => import('@/views/Login.vue')
```

- 不懒加载：程序启动就一次性把所有页面全部加载。
- 懒加载：**只有用户真正访问这个路由地址的时候，才去加载这个页面的代码**。 
>好处：项目初始打开速度更快，后台页面很多的时候效果明显。Vue项目标准写法。

### ③ 嵌套路由 children（本项目最关键）

```javascript
{
  path: '/manager',
  component: () => import('@/layouts/Layout.vue'), //父布局壳
  children: [
    { path: 'home', component: () => import('@/views/Home.vue') }
  ]
}
```

- `Layout.vue`：公共父布局，包含顶部头像栏、侧边菜单栏，页面固定不变。内部必须写 `<router-view />` 占位标签。
- `children` 里面是子页面：Home、Lab。子页面内容会渲染到父组件的 `<router-view/>` 的位置。
- 子路由path**不要写斜杠**，自动拼接父路径：`/manager` + `home` → 最终地址 `/manager/home`

业务场景：管理后台系统。头部侧边栏保持不动，中间区域切换不同业务页面，就是嵌套路由。

> 流程：访问 `/manager/home` → 先加载Layout外壳，再把Home页面塞进Layout的router-view位置显示。

---

## 4. 建立「布局壳 + 子页面」的嵌套路由思维，实现公共部分复用，减少重复代码

> 属于工程思想，基于嵌套路由语法。
> **就是 `Layout.vue` + `children` + `<router-view />`**

- 不变的内容（顶部导航、侧边栏）统一放到布局壳 `Layout.vue`；
- 每个页面独有的业务内容，写成子页面，配置在 `children` 下；
- 切换页面时只更新中间业务区域，布局壳保持不变。

一句话总结：**不变的放 Layout 壳，变化的放子页面**

## 5. 掌握前端基础交互能力

**按钮点击、路由跳转、消息提示、加载状态控制 全部是页面可见的用户交互：**
1. `@click` 按钮点击：点登录按钮执行登录函数
2. `router.push()` 路由跳转：登录成功跳到首页，退出登录跳回登录页
3. `ElMessage.success()` 消息提示：弹出 “登录成功” 小提示框
4. `:loading` 加载状态控制：点击登录，按钮变成转圈，防止用户重复多点

> 实操感受：运行项目，在页面上点击操作，就可以直观看到这几个交互的效果