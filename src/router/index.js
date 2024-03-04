import { createRouter, createWebHashHistory } from 'vue-router'
import MyHome from '@/components/Home.vue'
import MyLeaderboard from '@/components/Leaderboard.vue'

const routes = [
  {
    path: '/',
    component: MyHome
  },
  {
    path: '/leaderboard',
    component: MyLeaderboard
  }
];

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})
export default router

