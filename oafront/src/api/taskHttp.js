import http from './http'

const addTask = (title, content, assignee, department) => {
  const path = '/task/task'
  return http.post(path, { title, content, assignee, department })
}

const getTaskList = (page = 1, size = 10, params) => {
  const path = '/task/task'
  params = params ? params : {}
  params['page'] = page
  params['size'] = size
  return http.get(path, params)
}

const updateTask = (task_id, title, content, assignee, department) => {
  const path = '/task/task/' + task_id
  return http.put(path, { title, content, assignee, department })
}

const completeTask = (task_id) => {
  const path = '/task/task/' + task_id + '/complete'
  return http.post(path)
}

export default {
  addTask,
  getTaskList,
  updateTask,
  completeTask,
}