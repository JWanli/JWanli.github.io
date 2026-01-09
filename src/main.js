import { createApp } from 'vue'
import App from './App.vue'

// 1. 引入 Element Plus 和 样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 2. 引入 路由
import router from './router'

import 'element-plus/theme-chalk/dark/css-vars.css'

const app = createApp(App)

app.use(ElementPlus) // 安装 UI 库
app.use(router)      // 安装 路由
app.mount('#app')