<template>
  <OAMain title="任务列表">
    <el-card>
      <div class="header-container">
        <div class="left">
          <el-button type="primary" @click="handleAdd" v-if="isManager">
            <el-icon>
              <Plus />
            </el-icon>
            发起任务
          </el-button>
        </div>
      </div>

      <el-table
        :data="tasks"
        style="width: 100%"
        :row-style="{ height: '60px' }"
        border
      >
        <el-table-column
          prop="title"
          label="任务标题"
          show-overflow-tooltip
          height="60"
        />
        <el-table-column
          prop="content"
          label="任务内容"
          show-overflow-tooltip
          height="60"
        />
        <el-table-column label="执行人" height="60" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.assignee_info?.username }}
          </template>
        </el-table-column>
        <el-table-column label="所属部门" height="60" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.assignee_info?.department?.name }}
          </template>
        </el-table-column>
        <el-table-column label="状态" height="60" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 'completed' ? 'success' : 'info'">
              {{ row.status === 'completed' ? '已完成' : '进行中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="150"
          fixed="right"
          align="center"
          height="60"
        >
          <template #default="{ row }">
            <el-button
              v-if="canEdit(row)"
              type="primary"
              link
              :icon="Edit"
              @click="handleEdit(row)"
              :disabled="row.status === 'completed'"
            >
              修改
            </el-button>
            <el-button
              type="success"
              link
              :icon="Check"
              @click="handleComplete(row)"
              :disabled="row.status === 'completed'"
            >
              完成
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <OAPagination
          v-model="page"
          :total="total"
          :page-size="size"
          @pagination="loadTasks"
        />
      </template>
    </el-card>
  </OAMain>

  <OADialog
    :title="dialogType === 'add' ? '发起任务' : '编辑任务'"
    v-model="dialogVisible"
    @submit="handleSubmit"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" placeholder="请输入任务标题" clearable />
      </el-form-item>
      <el-form-item label="内容" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="4"
          placeholder="请输入任务内容"
          resize="none"
        />
      </el-form-item>
      <el-form-item label="执行人" prop="assignee">
        <el-select
          v-model="form.assignee"
          placeholder="请选择执行人"
          style="width: 100%"
          clearable
          @change="handleAssigneeChange"
        >
          <el-option
            v-for="staff in staffList"
            :key="staff.id"
            :label="staff.username"
            :value="staff.id"
          />
        </el-select>
      </el-form-item>
    </el-form>
  </OADialog>
</template>

<script setup>
// 添加 OAMain 和 OADialog 组件的导入
import OAMain from '@/components/OAMain.vue'
import OADialog from '@/components/OADialog.vue'
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import taskHttp from '@/api/taskHttp'
import OAPageHeader from '@/components/OAPageHeader.vue'
import OAPagination from '@/components/OAPagination.vue'
import { Plus, Edit, Check } from '@element-plus/icons-vue'
import staffHttp from '@/api/staffHttp'

const authStore = useAuthStore()
const isManager = authStore.isManager
const isAdmin = authStore.isAdmin

const tasks = ref([])
const page = ref(1)
const size = ref(10)
const total = ref(0)

const dialogVisible = ref(false)
const dialogType = ref('add')
const staffList = ref([])
const form = ref({
  title: '',
  content: '',
  assignee: '',
  department: '',
})

const rules = {
  title: [{ required: true, message: '请输入任务标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入任务内容', trigger: 'blur' }],
  assignee: [{ required: true, message: '请选择执行人', trigger: 'change' }],
}

const loadTasks = async () => {
  try {
    const res = await taskHttp.getTaskList(page.value, size.value)
    tasks.value = res.results
    total.value = res.count
  } catch (error) {
    ElMessage.error('加载任务列表失败')
  }
}

const handleAdd = () => {
  dialogType.value = 'add'
  form.value = {
    title: '',
    content: '',
    assignee: '',
    department: '',
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogType.value = 'edit'
  form.value = {
    id: row.id,
    title: row.title,
    content: row.content,
    assignee: row.assignee,
    department: row.department.id,
  }
  dialogVisible.value = true
}

const handleManagerEdit = (row) => {
  dialogType.value = 'manager_edit'
  form.value = {
    id: row.id,
    title: row.title,
    content: row.content,
    assignee: row.assignee,
    department: row.department.id,
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  try {
    if (dialogType.value === 'add') {
      await taskHttp.addTask(
        form.value.title,
        form.value.content,
        form.value.assignee,
        form.value.department
      )
      ElMessage.success('发布任务成功')
    } else if (dialogType.value === 'manager_edit') {
      await taskHttp.updateTask(
        form.value.id,
        form.value.title,
        form.value.content,
        form.value.assignee
      )
      ElMessage.success('更新任务成功')
    } else {
      await taskHttp.updateTask(
        form.value.id,
        form.value.title,
        form.value.content,
        form.value.assignee
      )
      ElMessage.success('更新任务成功')
    }
    dialogVisible.value = false
    loadTasks()
  } catch (error) {
    ElMessage.error(
      dialogType.value === 'add' ? '发布任务失败' : '更新任务失败'
    )
  }
}

const handleComplete = async (row) => {
  try {
    await ElMessageBox.confirm('确认完成该任务？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await taskHttp.completeTask(row.id)
    ElMessage.success('完成任务成功')
    loadTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('只有任务执行者可以完成任务')
    }
  }
}

const canEdit = (row) => {
  return (isManager || isAdmin) && row.status !== 'completed'
}

const canComplete = (row) => {
  return row.status !== 'completed' && row.assignee === authStore.id
}

const loadStaffList = async () => {
  try {
    const res = await staffHttp.getStaffList(1, 1000)
    staffList.value = res.results
  } catch (error) {
    ElMessage.error('加载员工列表失败')
  }
}

const handleAssigneeChange = (staffId) => {
  const selectedStaff = staffList.value.find((staff) => staff.id === staffId)
  if (selectedStaff && selectedStaff.department) {
    form.value.department = selectedStaff.department.id
  }
}

onMounted(() => {
  loadTasks()
  loadStaffList()
})
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-container .left {
  display: flex;
  align-items: center;
  gap: 10px;
}

:deep(.el-table .success-row) {
  background-color: #f0f9eb;
}
</style>
