<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-center align-items-center">
      <div class="spinner-border text-primary" role="status" v-if="loading">
        <span class="visually-hidden">Loading...</span>
      </div>
      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import authHttp from '@/api/authHttp'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const code = route.query.code
    if (!code) {
      throw new Error('未收到GitHub授权码')
    }

    const response = await authHttp.handleGithubCallback(code)
    // 验证并处理后端返回的认证信息
    if (!response || typeof response !== 'object') {
      throw new Error('登录失败：服务器返回数据格式错误')
    }

    const { user, access, refresh } = response
    if (!user || !access || !refresh) {
      throw new Error('登录失败：缺少必要的认证信息')
    }

    // 确保token格式正确
    if (typeof access !== 'string' || typeof refresh !== 'string') {
      throw new Error('登录失败：token格式错误')
    }

    authStore.setUserToken(user, access, refresh)
    router.push({ name: 'home' })
  } catch (err) {
    error.value = err.message || 'GitHub登录失败，请重试'
    setTimeout(() => {
      router.push({ name: 'login' })
    }, 3000)
  } finally {
    loading.value = false
  }
})
</script>
