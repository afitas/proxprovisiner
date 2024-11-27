import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashboard.vue'
import InfraForm from '../components/InfraForm.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/create',
    name: 'CreateInfra',
    component: InfraForm,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const user = localStorage.getItem('user')
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!user) {
      next('/login')
    } else {
      next()
    }
  } else {
    if (user && to.path === '/login') {
      next('/dashboard')
    } else {
      next()
    }
  }
})

export default router
