import http from "./http"

const getDepartmentStaffCount = () => {
    const path = "/home/department/staff/count"
    return http.get(path)
}

const getLatestInforms = () => {
    const path = "/home/latest/inform"
    return http.get(path)
}

const getLatestAbsents = () => {
    const path = "/home/latest/absent"
    return http.get(path)
}

// 添加图片上传接口
const uploadImage = (formData) => {
    const path = "/image/upload"
    return http.post(path, formData)
}

export default {
    getDepartmentStaffCount,
    getLatestInforms,
    getLatestAbsents,
    uploadImage
}