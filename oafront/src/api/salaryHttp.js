import http from './http.js'

export default {
  list: (params) => {
    return http.get('/salary/records', params)
  },
  detail: (id) => {
    return http.get(`/salary/records/${id}`)
  },
  create: (data) => {
    return http.post('/salary/records', data)
  },
  update: (id, data) => {
    return http.put(`/salary/records/${id}`, data)
  }
}