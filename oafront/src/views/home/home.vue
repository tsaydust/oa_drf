<script setup name="home">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import timeFormatter from '@/utils/timeFormatter'
import OAMain from '@/components/OAMain.vue'
import homeHttp from '@/api/homeHttp'
import * as echarts from 'echarts'

let informs = ref([])
let absents = ref([])

onMounted(async () => {
  try {
    informs.value = await homeHttp.getLatestInforms()
    absents.value = await homeHttp.getLatestAbsents()

    let rows = await homeHttp.getDepartmentStaffCount()
    console.log(rows)
    let xdatas = []
    let ydatas = []
    for (let row of rows) {
      xdatas.push(row.name)
      ydatas.push(row.staff_count)
    }

    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(
      document.getElementById('department-staff-count')
    )
    // 绘制图表
    myChart.setOption({
      tooltip: {},
      xAxis: {
        data: xdatas,
      },
      yAxis: {},
      series: [
        {
          name: '员工数量',
          type: 'bar',
          data: ydatas,
        },
      ],
    })
  } catch (detail) {
    ElMessage.error(detail)
  }
})
</script>

<template>
  <OAMain title="首页">
    <el-card>
      <template #header>
        <h2>部门员工数量</h2>
      </template>
      <div id="department-staff-count" style="width: 100%; height: 300px"></div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <h2>部门最新通知</h2>
          </template>
          <el-table :data="informs" :row-style="{ height: '50px' }">
            <el-table-column label="标题" height="50" show-overflow-tooltip>
              <template #default="scope">
                <router-link
                  :to="{ name: 'inform_detail', params: { pk: scope.row.id } }"
                  class="title-link"
                  >{{ scope.row.title }}</router-link
                >
              </template>
            </el-table-column>
            <el-table-column
              label="发布者"
              prop="author.username"
              height="50"
              show-overflow-tooltip
            ></el-table-column>
            <el-table-column label="发布时间" height="50">
              <template #default="scope">
                <span class="time-text">{{
                  timeFormatter.stringFromDate(scope.row.create_time)
                }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <h2>最新请假</h2>
          </template>
          <el-table :data="absents" :row-style="{ height: '50px' }">
            <el-table-column
              label="部门"
              prop="requester.department.name"
              height="50"
              show-overflow-tooltip
            ></el-table-column>
            <el-table-column
              label="发起人"
              prop="requester.username"
              height="50"
              show-overflow-tooltip
            ></el-table-column>
            <el-table-column
              label="起始日期"
              prop="start_date"
              height="50"
              show-overflow-tooltip
            ></el-table-column>
            <el-table-column
              label="结束日期"
              prop="end_date"
              height="50"
              show-overflow-tooltip
            ></el-table-column>
            <el-table-column label="发起时间" height="50">
              <template #default="scope">
                <span class="time-text">{{
                  timeFormatter.stringFromDateTime(scope.row.create_time)
                }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </OAMain>
</template>

<style scoped>
.title-link {
  color: #409eff;
  text-decoration: none;
  transition: all 0.3s ease;
}

.title-link:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.time-text {
  font-family: monospace;
  letter-spacing: 0.5px;
}

:deep(.el-table__row) {
  transition: all 0.3s ease;
}

:deep(.el-table__row:hover) {
  background-color: #f5f7fa;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
}

:deep(.el-card__header h2) {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}
</style>
