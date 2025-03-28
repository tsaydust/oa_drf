<script setup name="staffadd">
import { ref, reactive, onMounted } from 'vue'
import staffHttp from '@/api/staffHttp'
import { useRouter, useRoute } from 'vue-router'
import OAMain from '@/components/OAMain.vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

let departments = ref([])
let staffForm = reactive({
  email: '',
  password: '',
  realname: '',
  department_id: authStore.user.department?.id || null, // 设置默认部门ID
  role: 'staff', // 默认为员工角色
})
const formRef = ref()
let isRoleLocked = ref(false) // 添加角色锁定状态
let rules = reactive({
  email: [{ required: true, message: '请输入邮箱！', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码！', trigger: 'blur' }],
  realname: [{ required: true, message: '请输入真实姓名！', trigger: 'blur' }],
  department_id: [
    { required: true, message: '请选择部门！', trigger: 'change' },
  ],
  role: [{ required: true, message: '请选择角色！', trigger: 'change' }],
})

// 获取所有部门
const fetchDepartments = async () => {
  try {
    const data = await staffHttp.getAllDepartment()
    departments.value = data.results
  } catch (detail) {
    ElMessage.error(detail)
  }
}

// 监听部门变化，如果是董事会则自动设置为领导角色并锁定
const handleDepartmentChange = (departmentId) => {
  const department = departments.value.find((d) => d.id === departmentId)
  if (department && department.name === '董事会') {
    staffForm.role = 'leader'
    isRoleLocked.value = true
  } else {
    isRoleLocked.value = false
  }
}

const onSubmit = () => {
  formRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        await staffHttp.addStaff(
          staffForm.realname,
          staffForm.email,
          staffForm.password,
          staffForm.department_id,
          staffForm.role
        )
        ElMessage.success('员工添加成功！')
        router.push({ name: 'staff_list' })
      } catch (detail) {
        ElMessage.error(detail)
      }
    }
  })
}

onMounted(async () => {
  await fetchDepartments()
  // 如果路由中有部门ID，则使用路由中的部门ID，否则使用auth store中的部门ID
  // 如果有部门ID，则触发部门变化处理
  if (staffForm.department_id) {
    handleDepartmentChange(staffForm.department_id)
  }
})
</script>

<template>
  <OAMain title="新增员工">
    <el-card shadow="always">
      <el-form
        :rules="rules"
        :model="staffForm"
        ref="formRef"
        label-width="80px"
      >
        <el-form-item label="姓名" prop="realname">
          <el-input v-model="staffForm.realname" placeholder="请输入姓名">
          </el-input>
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="staffForm.email"
            placeholder="请输入邮箱"
          ></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="staffForm.password"
            placeholder="请输入密码"
            type="password"
          >
          </el-input>
        </el-form-item>

        <el-form-item label="部门" prop="department_id">
          <el-select
            v-model="staffForm.department_id"
            placeholder="请选择部门"
            @change="handleDepartmentChange"
          >
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-radio-group v-model="staffForm.role" :disabled="isRoleLocked">
            <el-radio label="staff">员工</el-radio>
            <el-radio label="leader">领导</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSubmit">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </OAMain>
</template>

<style scoped></style>
