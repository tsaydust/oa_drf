import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import frame_routes from '@/router/frame'
import login_routes from '@/router/login'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: frame_routes.concat(login_routes),
})

// 过滤路由函数
function filterRoutes(routes, authStore) {
  return routes.filter((route) => {
    // 1. 如果路由需要经理权限，检查是否是经理
    if (route.meta?.requiresManager && !authStore.isManager) {
      return false
    }
    if (route.meta?.requiresEmployee && !authStore.isEmployee) {
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

  // 1. 检查登录状态，排除GitHub OAuth回调路径
  if (!authStore.is_logined && to.name !== 'login' && !to.path.startsWith('/oaauth/github/callback')) {
    return next({ name: 'login' })
  }

  // 2. 如果已登录且访问登录页，重定向到首页
  if (authStore.is_logined && to.name === 'login') {
    return next({ name: 'home' })
  }

  // 3. 过滤路由
  if (authStore.is_logined) {
    // 重新创建路由器以应用新的过滤后的路由
    const filteredRoutes = frame_routes.map(route => {
      if (route.children) {
        return {
          ...route,
          children: filterRoutes(route.children, authStore)
        }
      }
      return route
    })

    // 更新路由配置
    router.options.routes = filteredRoutes.concat(login_routes)
    router.addRoute(...filteredRoutes)

    // 如果路由不存在于过滤后的路由中，重定向到首页
    if (to.matched.length === 0) {
      return next({ name: 'home' })
    }
  }

  next()
})

export default router
