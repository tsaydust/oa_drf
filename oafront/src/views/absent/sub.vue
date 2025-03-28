<script setup name="subabsent">
import OAPageHeader from '@/components/OAPageHeader.vue'
import { Plus } from '@element-plus/icons-vue'
import { onMounted, reactive, ref, watch } from 'vue'
import timeFormatter from '@/utils/timeFormatter.js'
import absentHttp from '@/api/absentHttp.js'
import OAMain from '@/components/OAMain.vue'
import OAPagination from '@/components/OAPagination.vue'
import { ElMessage } from 'element-plus'
import OADialog from '@/components/OADialog.vue'

let pagination = reactive({
  total: 0,
  page: 1,
})
let dialogVisible = ref(false)
let absents = ref([])
let absentFormRef = ref()
let absentForm = reactive({
  status: 2,
  response_content: '',
})
let handleIndex = null
let rules = reactive({
  status: [{ required: true, message: '请选择处理结果！', trigger: 'change' }],
  response_content: [
    { required: true, message: '请输入理由！', trigger: 'blur' },
  ],
})

watch(
  () => pagination.page,
  async (value) => {
    requestAbsents(value)
  }
)

const requestAbsents = async (page) => {
  try {
    let data = await absentHttp.getSubAbsents(page)
    pagination.total = data.count
    absents.value = data.results
  } catch (detail) {
    ElMessage.error(detail)
  }
}

onMounted(async () => {
  try {
    requestAbsents(1)
  } catch (detail) {
    ElMessage.error(detail)
  }
})

const onShowDialog = (index) => {
  absentForm.status = 2
  absentForm.response_content = ''
  dialogVisible.value = true
  handleIndex = index
}

const onSubmitAbsent = () => {
  absentFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        // 隐藏对话框
        dialogVisible.value = false
        const absent = absents.value[handleIndex]
        console.log(absent)
        const data = await absentHttp.handleSubAbsent(
          absent.id,
          absentForm.status,
          absentForm.response_content
        )
        absents.value.splice(handleIndex, 1, data)
        ElMessage.success('员工考勤处理成功！')
      } catch (detail) {
        ElMessage.error(detail)
      }
    }
  })
}
</script>

<template>
  <OADialog title="处理考勤" v-model="dialogVisible" @submit="onSubmitAbsent">
    <el-form
      :model="absentForm"
      :rules="rules"
      ref="absentFormRef"
      label-width="100px"
    >
      <el-form-item label="结果" prop="status">
        <el-radio-group v-model="absentForm.status" class="ml-4">
          <el-radio :value="2" size="large">通过</el-radio>
          <el-radio :value="3" size="large">拒绝</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="理由" prop="response_content">
        <el-input
          type="textarea"
          v-model="absentForm.response_content"
          autocomplete="off"
        />
      </el-form-item>
    </el-form>
  </OADialog>
  <OAMain title="部门考勤">
    <el-card>
      <el-table
        :data="absents"
        style="width: 100%"
        :row-style="{ height: '60px' }"
      >
        <el-table-column
          prop="title"
          label="标题"
          height="60"
          show-overflow-tooltip
        />
        <el-table-column
          label="发起者"
          min-width="100"
          height="60"
          show-overflow-tooltip
        >
          <template #default="scope">
            <span>
              {{
                '[' +
                scope.row.requester.department.name +
                ']' +
                scope.row.requester.username
              }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="absent_type.name"
          label="类型"
          height="60"
          show-overflow-tooltip
        />
        <el-table-column
          prop="request_content"
          label="原因"
          height="60"
          show-overflow-tooltip
        />
        <el-table-column prop="create_time" label="发起时间" height="60">
          <template #default="scope">
            {{ timeFormatter.stringFromDateTime(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column
          prop="start_date"
          label="开始日期"
          height="60"
          show-overflow-tooltip
        />
        <el-table-column
          prop="end_date"
          label="结束日期"
          height="60"
          show-overflow-tooltip
        />
        <el-table-column
          prop="department_manager.username"
          label="审核领导"
          height="60"
          show-overflow-tooltip
        />
        <el-table-column
          prop="response_content"
          label="反馈意见"
          height="60"
          show-overflow-tooltip
        />
        <el-table-column label="审核状态" height="60">
          <template #default="scope">
            <el-tag type="info" v-if="scope.row.status == 1">审核中</el-tag>
            <el-tag type="success" v-else-if="scope.row.status == 2"
              >已通过</el-tag
            >
            <el-tag type="danger" v-else>已拒绝</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="处理" height="60">
          <template #default="scope">
            <el-button
              @click="onShowDialog(scope.$index)"
              v-if="scope.row.status == 1"
              type="primary"
              icon="EditPen"
            />
            <el-button disabled v-else type="default">已处理</el-button>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <OAPagination
          v-model="pagination.page"
          :total="pagination.total"
          :page-size="10"
        ></OAPagination>
      </template>
    </el-card>
  </OAMain>
</template>

<style scoped></style>
