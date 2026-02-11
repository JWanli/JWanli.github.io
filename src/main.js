import { createApp } from 'vue'
import App from './App.vue'

// 2. 引入 路由
import router from './router'

import 'element-plus/theme-chalk/dark/css-vars.css'

const app = createApp(App)

app.use(router)      // 安装 路由
app.mount('#app')