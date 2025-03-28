import { useAuthStore } from '@/stores/auth'

export default {
  mounted(el, binding) {
    const authStore = useAuthStore()
    const { value } = binding

    // 如果value是数组，检查是否有权限
    if (Array.isArray(value)) {
      const hasPermission = value.some((permission) =>
        authStore.hasPermission(permission)
      )
      if (!hasPermission) {
        el.parentNode?.removeChild(el)
      }
      return
    }

    // 如果value是字符串，检查身份
    switch (value) {
      case 'manager':
        if (!authStore.isManager) {
          el.parentNode?.removeChild(el)
        }
        break
      case 'admin':
        if (!authStore.isAdmin) {
          el.parentNode?.removeChild(el)
        }
        break
      case 'employee':
        if (!authStore.isEmployee) {
          el.parentNode?.removeChild(el)
        }
        break
    }
  },
}
