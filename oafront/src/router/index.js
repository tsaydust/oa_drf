import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import frame_routes from '@/router/frame'
import login_routes from '@/router/login'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: frame_routes.concat(login_routes),
})

// 过滤路由函数
function filterRoutes(routes, authStore) {
  return routes.filter((route) => {
    // 1. 如果路由需要经理权限，检查是否是经理
    if (route.meta?.requiresManager && !authStore.isManager) {
      return false
    }

    // 2. 如果有子路由，递归过滤
    if (route.children) {
      route.children = filterRoutes(route.children, authStore)
      return route.children.length > 0
    }

    return true
  })
}

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 1. 检查登录状态
  if (!authStore.is_logined && to.name !== 'login') {
    return next({ name: 'login' })
  }

  // 2. 如果已登录且访问登录页，重定向到首页
  if (authStore.is_logined && to.name === 'login') {
    return next({ name: 'home' })
  }

  // 3. 过滤路由
  if (authStore.is_logined) {
    // 过滤主框架路由
    frame_routes.forEach((route) => {
      if (route.children) {
        route.children = filterRoutes(route.children, authStore)
      }
    })
  }

  next()
})

export default router
