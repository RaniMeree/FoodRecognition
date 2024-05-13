import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import Signup from '../views/Register/Signup.vue'
import login from '../views/Register/Login.vue'
import Intake from '../views/IntakeTabel.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/intake',
      name: 'intake',
      component: Intake
    },

  ]
})

export default router
