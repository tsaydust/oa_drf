<script setup>
import OAPageHeader from '@/components/OAPageHeader.vue'
import { defineProps } from 'vue'

let props = defineProps({
  title: '',
})
</script>

<template>
  <el-space
    direction="vertical"
    fill
    :size="20"
    style="width: 100%"
    class="main-container"
  >
    <OAPageHeader :content="props.title"></OAPageHeader>
    <slot> </slot>
  </el-space>
</template>

<style scoped>
.el-space :deep(.el-space__item) {
  width: 100%;
}

.main-container {
  transition: all 0.3s ease-in-out;
}

.main-container :deep(.el-card) {
  transition: all 0.3s ease-in-out;
}
</style>
