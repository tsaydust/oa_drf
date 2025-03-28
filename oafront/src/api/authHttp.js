import http from '@/api/http.js'

const login = (email, password) => {
  const path = 'oaauth/login'
  return http.post(path, { email, password })
}

const resetPwd = (oldpwd, pwd1, pwd2) => {
  const path = 'oaauth/resetpwd'
  return http.post(path, { oldpwd, pwd1, pwd2 })
}

const getProfile = () => {
  const path = 'oaauth/profile'
  return http.get(path)
}

const updateProfile = (data) => {
  const path = 'oaauth/profile'
  return http.put(path, data)
}

export default {
  login,
  resetPwd,
  getProfile,
  updateProfile,
}
