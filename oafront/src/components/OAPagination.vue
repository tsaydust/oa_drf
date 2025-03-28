<script setup name="OAPagination">
import {defineProps, defineModel} from "vue";

let props = defineProps({
  total: {
    type: Number,
    default: 0
  },
  pageSize:{
    type: Number,
    default:10
  }
})

let page = defineModel({required:true});
</script>

<template>
  <el-pagination background layout="prev, pager, next" :total="props.total"
                 v-model:current-page="page" :page-size="pageSize"/>
</template>

<style scoped>
.el-pagination {
  justify-content: center;
}
</style>