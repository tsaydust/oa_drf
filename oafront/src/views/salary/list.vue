<template>
  <OAMain title="薪资列表">
    <el-card>
      <div class="filter-container">
        <el-form :inline="true" :model="queryParams" class="demo-form-inline">
          <el-form-item label="生效日期">
            <el-date-picker
              v-model="queryParams.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD"
              @change="handleFilter"
            />
          </el-form-item>
          <el-form-item label="薪资范围">
            <el-input-number
              v-model="queryParams.minAmount"
              :min="0"
              :precision="2"
              placeholder="最小金额"
              @change="handleFilter"
            />
            <span class="mx-2">-</span>
            <el-input-number
              v-model="queryParams.maxAmount"
              :min="0"
              :precision="2"
              placeholder="最大金额"
              @change="handleFilter"
            />
          </el-form-item>
          <el-form-item label="部门">
            <el-select
              v-model="queryParams.departmentId"
              placeholder="选择部门"
              clearable
              @change="handleFilter"
              style="width: 100px"
            >
              <el-option
                v-for="dept in departmentList"
                :key="dept.id"
                :label="dept.name"
                :value="dept.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              @click="handleCreate"
              v-permission="manager"
              >新增薪资记录</el-button
            >
            <el-button type="primary" @click="handleFilter">查询</el-button>
            <el-button @click="resetQuery">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-table
        :data="salaryList"
        style="width: 100%"
        :row-style="{ height: '60px' }"
        border
      >
        <el-table-column prop="employee_name" label="员工姓名" />
        <el-table-column prop="amount" label="薪资金额">
          <template #default="scope">
            {{ scope.row.amount }}
          </template>
        </el-table-column>
        <el-table-column prop="effective_date" label="生效日期" />
        <el-table-column prop="created_by_name" label="创建人" />
        <el-table-column
          v-permission="manager"
          label="操作"
          width="200"
          fixed="right"
          align="center"
        >
          <template #default="scope">
            <el-button
              type="primary"
              link
              :icon="Edit"
              @click="handleEdit(scope.row, 'salary')"
              >编辑薪资</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <OAPagination
        v-model:page="page"
        v-model:limit="limit"
        :total="total"
        @pagination="getSalaryList"
      />
    </el-card>

    <template #footer>
      <OAPagination
        v-model:page="page"
        v-model:limit="limit"
        :total="total"
        @pagination="getSalaryList"
      />
    </template>
  </OAMain>

  <OADialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="500"
    @cancel="resetForm"
    @submit="submitForm"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
      <el-form-item
        label="员工"
        prop="employee"
        v-if="dialogTitle === '新增薪资记录'"
      >
        <el-select v-model="form.employee" placeholder="请选择员工">
          <el-option
            v-for="staff in staffList"
            :key="staff.id"
            :label="staff.username"
            :value="staff.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item
        label="薪资金额"
        prop="amount"
        v-if="dialogTitle === '编辑薪资' || dialogTitle === '新增薪资记录'"
      >
        <el-input-number v-model="form.amount" :min="0" :precision="2" />
      </el-form-item>
      <el-form-item
        label="生效日期"
        prop="effective_date"
        v-if="
          dialogTitle === '编辑薪资' ||
          dialogTitle === '修改生效时间' ||
          dialogTitle === '新增薪资记录'
        "
      >
        <el-date-picker
          v-model="form.effective_date"
          type="date"
          placeholder="选择生效日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
    </el-form>
  </OADialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import OAMain from '@/components/OAMain.vue'
import OAPagination from '@/components/OAPagination.vue'
import OADialog from '@/components/OADialog.vue'
import salaryHttp from '@/api/salaryHttp'
import staffHttp from '@/api/staffHttp'
import { useAuthStore } from '@/stores/auth'
import { Edit, Timer } from '@element-plus/icons-vue'

const authStore = useAuthStore()
const salaryList = ref([])
const page = ref(1)
const limit = ref(10)
const total = ref(0)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const staffList = ref([])
const departmentList = ref([])
const formRef = ref(null)

const queryParams = ref({
  dateRange: [],
  minAmount: null,
  maxAmount: null,
  departmentId: null,
})

const form = ref({
  employee: '',
  amount: 0,
  effective_date: '',
})

const rules = {
  employee: [{ required: true, message: '请选择员工', trigger: 'change' }],
  amount: [{ required: true, message: '请输入薪资金额', trigger: 'blur' }],
  effective_date: [
    { required: true, message: '请选择生效日期', trigger: 'change' },
  ],
}

const getSalaryList = async () => {
  try {
    const params = {
      page: page.value,
      limit: limit.value,
    }

    if (
      queryParams.value.dateRange &&
      queryParams.value.dateRange.length === 2
    ) {
      params.start_date = queryParams.value.dateRange[0]
      params.end_date = queryParams.value.dateRange[1]
    }

    if (queryParams.value.minAmount !== null) {
      params.min_amount = queryParams.value.minAmount
    }

    if (queryParams.value.maxAmount !== null) {
      params.max_amount = queryParams.value.maxAmount
    }

    if (queryParams.value.departmentId) {
      params.department_id = queryParams.value.departmentId
    }

    const res = await salaryHttp.list(params)
    salaryList.value = res.results
    total.value = res.count
  } catch (error) {
    ElMessage.error('获取薪资列表失败')
  }
}

const getStaffList = async () => {
  try {
    const res = await staffHttp.getStaffList(1, 1000)
    staffList.value = res.results
  } catch (error) {
    ElMessage.error('获取员工列表失败')
  }
}

const getDepartmentList = async () => {
  try {
    const res = await staffHttp.getAllDepartment()
    departmentList.value = res.results
  } catch (error) {
    ElMessage.error('获取部门列表失败')
  }
}

const handleFilter = () => {
  page.value = 1
  getSalaryList()
}

const resetQuery = () => {
  queryParams.value = {
    dateRange: [],
    minAmount: null,
    maxAmount: null,
    departmentId: null,
  }
  handleFilter()
}

const handleCreate = () => {
  dialogTitle.value = '新增薪资记录'
  dialogVisible.value = true
  getStaffList()
}

const handleEdit = async (row, type = 'salary') => {
  dialogTitle.value = type === 'salary' ? '编辑薪资' : '修改生效时间'
  try {
    const res = await salaryHttp.detail(row.id)
    form.value = {
      id: res.id,
      employee: res.employee,
      amount: res.amount || 0,
      effective_date: res.effective_date || '',
    }
    // 根据编辑类型设置表单验证规则
    if (type === 'salary') {
      rules.amount = [
        { required: true, message: '请输入薪资金额', trigger: 'blur' },
      ]
      rules.effective_date = []
    } else {
      rules.amount = []
      rules.effective_date = [
        { required: true, message: '请选择生效日期', trigger: 'change' },
      ]
    }
    dialogVisible.value = true
    getStaffList()
  } catch (error) {
    ElMessage.error('获取薪资详情失败')
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  form.value = {
    employee: '',
    amount: 0,
    effective_date: '',
  }
}

const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (form.value.id) {
          await salaryHttp.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await salaryHttp.create(form.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        getSalaryList()
      } catch (error) {
        ElMessage.error(error.message || '操作失败')
      }
    }
  })
}

onMounted(() => {
  getDepartmentList()
  getSalaryList()
})
</script>

<style scoped>
.box-card {
  margin-top: 20px;
}
</style>
