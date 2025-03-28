<script setup>
let dialogVisible = defineModel({ required: true })
let props = defineProps({
  title: {
    type: String,
    default: '',
  },
  width: {
    type: String,
    default: '500',
  },
})

const onCancel = () => {
  dialogVisible.value = false
  emits('cancel')
}

const onSubmit = () => {
  emits('submit')
}

let emits = defineEmits(['cancel', 'submit'])
</script>

<template>
  <el-dialog v-model="dialogVisible" :title="props.title" :width="props.width">
    <slot></slot>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="onCancel">取消</el-button>
        <el-button type="primary" @click="onSubmit"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped></style>
