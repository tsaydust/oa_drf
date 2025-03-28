<script setup name="login">
import login_img from '@/assets/images/bg.jpg'
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useRouter } from 'vue-router'
import authHttp from '@/api/authHttp.js'
import { ElMessage } from 'element-plus'

const router = useRouter()

const authStore = useAuthStore()

let form = reactive({
  email: '',
  password: '',
})
const isEmailInvalid = ref(false)
const isPasswordInvalid = ref(false)

const onSubmit = async () => {
  let pwdRgx = /^[0-9a-zA-Z_-]{6,20}/
  let emailRgx = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9])+/
  
  isEmailInvalid.value = !emailRgx.test(form.email)
  isPasswordInvalid.value = !pwdRgx.test(form.password)
  
  if (isEmailInvalid.value) {
    ElMessage.info('邮箱格式不满足！')
    return
  }
  if (isPasswordInvalid.value) {
    ElMessage.info('密码格式不满足！')
    return
  }
  
  try {
    let data = await authHttp.login(form.email, form.password)
    let token = data.access
    let refresh = data.refresh
    let user = data.user
    authStore.setUserToken(user, token, refresh)
    //   跳转到oa系统首页
    router.push('/')
  } catch (detail) {
    ElMessage.error(detail)
  }
}
const backgroundStyle = {
  backgroundImage: `url(${login_img})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
}
const loading = ref(false)
const showPassword = ref(false)

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const isEmailEmpty = ref(false)
const isPasswordEmpty = ref(false)

const handleFocus = (field) => {
  if (field === 'email') isEmailInvalid.value = false
  if (field === 'password') isPasswordInvalid.value = false
}

const handleLogin = async (e) => {
  if (!form.email.trim() || !form.password.trim()) {
    isEmailInvalid.value = !form.email.trim()
    isPasswordInvalid.value = !form.password.trim()
    return
  }
  loading.value = true
  try {
    await onSubmit()
  } finally {
    loading.value = false
  }
}

// 如果不需要社交登录功能，建议移除相关代码
const loginWithFacebook = () => {
  ElMessage.info('Facebook登录功能未实现')
}

const loginWithTwitter = () => {
  ElMessage.info('Twitter登录功能未实现')
}
</script>

<template>
  <div class="img js-fullheight" :style="backgroundStyle">
    <section class="ftco-section">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6 text-center mb-5">
            <h2 class="heading-section">员工登录</h2>
          </div>
        </div>
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-4">
            <div class="login-wrap p-0">
              <form class="signin-form" @submit.prevent="handleLogin">
                <div class="form-group">
                  <input
                    type="text"
                    class="form-control"
                    :class="{ 'is-invalid': isEmailInvalid }"
                    placeholder="Email"
                    v-model="form.email"
                    @focus="handleFocus('email')"
                  />
                </div>
                <div class="form-group">
                  <input
                    id="password-field"
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control"
                    :class="{ 'is-invalid': isPasswordInvalid }"
                    placeholder="Password"
                    v-model="form.password"
                    @focus="handleFocus('password')"
                  />
                  <span
                    @click="togglePasswordVisibility"
                    toggle="#password-field"
                    class="fa fa-fw fa-eye field-icon toggle-password"
                  ></span>
                </div>
                <div class="form-group">
                  <button
                    type="submit"
                    class="form-control btn btn-primary submit px-3"
                    :disabled="loading"
                  >
                    <span v-if="loading">登录中...</span>
                    <span v-else>登录</span>
                  </button>
                </div>
              </form>
              <!-- <p class="w-100 text-center">&mdash; Or Sign In With &mdash;</p> -->
              <!-- <div class="social d-flex text-center">
                <a
                  href="#"
                  class="px-2 py-2 mr-md-1 rounded"
                  @click.prevent="loginWithFacebook"
                >
                  <span class="ion-logo-facebook mr-2"></span> Facebook
                </a>
                <a
                  href="#"
                  class="px-2 py-2 ml-md-1 rounded"
                  @click.prevent="loginWithTwitter"
                >
                  <span class="ion-logo-twitter mr-2"></span> Twitter
                </a>
              </div> -->
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.img.js-fullheight {
  min-height: 100vh;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
}

.ftco-section {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.form-control.is-invalid {
  border-color: #ff4444;
  animation: shake 0.5s linear;
  box-shadow: 0 0 5px rgba(255, 68, 68, 0.5);
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.form-control {
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05) !important;
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.form-control:focus {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.05);
}

.form-control.is-invalid {
  background: rgba(255, 68, 68, 0.05) !important;
  border-color: rgba(255, 68, 68, 0.2) !important;
  box-shadow: 0 0 15px rgba(255, 68, 68, 0.1);
}

/* 优化按钮样式 */
.btn-primary {
  background: rgba(100, 181, 246, 0.2) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background: rgba(100, 181, 246, 0.3) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 0 20px rgba(100, 181, 246, 0.1);
  transform: translateY(-2px);
}

.btn-primary:disabled {
  background: rgba(100, 181, 246, 0.1) !important;
  opacity: 0.7;
}
</style>
<style scoped src="@/assets/css/style.css"></style>
