import { createRouter, createWebHashHistory } from 'vue-router'
// 引入刚才创建的三个页面
import Home from '../views/Home.vue'
import Leaderboard from '../views/Leaderboard.vue'
import Activity from '../views/Activity.vue'

const routes = [
  { path: '/', component: Home },           // 根路径显示主页
  { path: '/rank', component: Leaderboard }, // /rank 显示排行榜
  { path: '/activity', component: Activity } // /activity 显示活动
]

const router = createRouter({
  // 使用 Hash 模式 (网址里带 # 号)，这种模式在 GitHub Pages 上最不容易出错
  history: createWebHashHistory(),
  routes
})

export default router