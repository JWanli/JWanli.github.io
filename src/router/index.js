import { createRouter, createWebHashHistory } from 'vue-router' // 或者 createWebHistory

// 视图组件使用懒加载（路由级动态 import），减少首屏 JS 体积
const Home = () => import('../views/Home.vue')
const Leaderboard = () => import('../views/Leaderboard.vue')
const Info = () => import('../views/Info.vue')
const Profile = () => import('../views/Profile.vue')

const routes = [
  { path: '/', component: Home },
  { path: '/rank', component: Leaderboard },
  { path: '/info', component: Info },
  // 新增详情页路由，:id 是动态参数
  { path: '/profile/:id', component: Profile }, 
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router