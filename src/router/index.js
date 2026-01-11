import { createRouter, createWebHashHistory } from 'vue-router' // 或者 createWebHistory

// 引入组件
import Home from '../views/Home.vue'
import Leaderboard from '../views/Leaderboard.vue'
import Activity from '../views/Activity.vue'
import Profile from '../views/Profile.vue' // <--- 新增引入

const routes = [
  { path: '/', component: Home },
  { path: '/rank', component: Leaderboard },
  { path: '/activity', component: Activity },
  // 新增详情页路由，:id 是动态参数
  { path: '/profile/:id', component: Profile }, 
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router