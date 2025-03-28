import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

const USER_KEY = 'OA_USER_KEY'
const TOKEN_KEY = 'OA_TOKEN_KEY'
const REFRESH_KEY = 'OA_REFRESH_KEY'

export const useAuthStore = defineStore('auth', () => {
  let _user = ref({})
  let _token = ref('')
  let _refresh = ref('')

  function setUserToken(user, token, refresh) {
    // 保存到对象上（内存中）
    _user.value = user
    _token.value = token
    _refresh.value = refresh

    // 存储到浏览器的localStorge中（硬盘上）
    localStorage.setItem(USER_KEY, JSON.stringify(user))
    localStorage.setItem(TOKEN_KEY, token)
    localStorage.setItem(REFRESH_KEY, refresh)
  }

  function clearUserToken() {
    _user.value = {}
    _token.value = ''
    _refresh.value = ''
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
  }

  // 计算属性
  let user = computed(() => {
    if (Object.keys(_user.value).length === 0) {
      let user_str = localStorage.getItem(USER_KEY)
      if (user_str) {
        _user.value = JSON.parse(user_str)
      }
    }
    return _user.value
  })

  let token = computed(() => {
    if (!_token.value) {
      let token_str = localStorage.getItem(TOKEN_KEY)
      if (token_str) {
        _token.value = token_str
      }
    }
    return _token.value
  })

  let refresh = computed(() => {
    if (!_refresh.value) {
      let refresh_str = localStorage.getItem(REFRESH_KEY)
      if (refresh_str) {
        _refresh.value = refresh_str
      }
    }
    return _refresh.value
  })

  let is_logined = computed(() => {
    if (Object.keys(user.value).length > 0 && token.value) {
      return true
    }
    return false
  })

  // 角色相关的计算属性
  let roles = computed(() => {
    return _user.value.roles || []
  })

  let permissions = computed(() => {
    return _user.value.permissions || []
  })

  // 角色检查
  let hasRole = computed(() => (role) => {
    return roles.value.includes(role)
  })

  // 权限检查
  let hasPermission = computed(() => (permission) => {
    return permissions.value.includes(permission)
  })

  // 角色层级检查
  let isAdmin = computed(() => {
    return roles.value.includes('admin')
  })

  let isManager = computed(() => {
    return roles.value.includes('manager')
  })

  let isEmployee = computed(() => {
    return roles.value.includes('employee')
  })

  // 功能访问控制
  let canAccess = computed(() => (feature) => {
    // 管理员拥有所有权限
    if (isAdmin.value) {
      return true
    }

    // 经理拥有除管理员外的所有权限
    if (isManager.value) {
      return true
    }

    // 普通员工权限限制
    if (isEmployee.value) {
      switch (feature) {
        case 'add_user': // 新增员工
        case 'publish_inform': // 发布通知
          return false
        default:
          return true
      }
    }

    return false
  })

  // 按钮级别权限控制
  let canOperate = computed(() => (operation) => {
    // 管理员拥有所有操作权限
    if (isAdmin.value) {
      return true
    }

    // 经理的操作权限
    if (isManager.value) {
      switch (operation) {
        case 'manage_department': // 部门管理
        case 'manage_employee': // 员工管理
        case 'manage_attendance': // 考勤管理
        case 'manage_salary': // 薪资管理
          return true
        default:
          return false
      }
    }

    // 普通员工只有基础操作权限
    if (isEmployee.value) {
      switch (operation) {
        case 'view_profile': // 查看个人信息
        case 'apply_leave': // 请假申请
        case 'view_attendance': // 查看考勤
        case 'view_salary': // 查看薪资
          return true
        default:
          return false
      }
    }

    return false
  })

  // 想要让外面访问到的，就必须要返回
  return {
    setUserToken,
    user,
    token,
    refresh,
    is_logined,
    clearUserToken,
    roles,
    permissions,
    hasRole,
    hasPermission,
    isAdmin,
    isManager,
    isEmployee,
    canAccess,
    canOperate,
  }
})
