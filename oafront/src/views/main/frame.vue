<script setup name="frame">
import { ref, computed, reactive, onMounted } from 'vue'
import { Expand, Fold, Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import authHttp from '@/api/authHttp'
import { ElMessage } from 'element-plus'
import routes from '@/router/frame'

import homeHttp from '@/api/homeHttp'

const authStore = useAuthStore()
const router = useRouter()

let displayUser = reactive({
  department: {},
  realname: '',
})
let defaultActive = ref('home')
let isCollapse = ref(false)
let dialogVisible = ref(false)
let formLabelWidth = '100px'
let resetPwdForm = reactive({
  oldpwd: '',
  pwd1: '',
  pwd2: '',
})
let formTag = ref()
let rules = reactive({
  oldpwd: [
    { required: true, message: '请输入旧密码！', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度需在6~20之间！', trigger: 'blur' },
  ],
  pwd1: [
    { required: true, message: '请输入新密码！', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度需在6~20之间！', trigger: 'blur' },
  ],
  pwd2: [
    { required: true, message: '请输入确认密码！', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度需在6~20之间！', trigger: 'blur' },
  ],
})
let asideWidth = computed(() => {
  if (isCollapse.value) {
    return '64px'
  } else {
    return '250px'
  }
})

onMounted(() => {
  defaultActive.value = router.currentRoute.value.name
  displayUser.department = authStore.user.department
  displayUser.realname = authStore.user.username
//   console.log(authStore.user.avatar);
  
})

const onCollapseAside = () => {
  isCollapse.value = !isCollapse.value
}

const onExit = () => {
  authStore.clearUserToken()
  router.push({ name: 'login' })
}

const onControlResetPwdDialog = () => {
  resetPwdForm.oldpwd = ''
  resetPwdForm.pwd1 = ''
  resetPwdForm.pwd2 = ''
  dialogVisible.value = true
}

const onSubmit = () => {
  formTag.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        await authHttp.resetPwd(
          resetPwdForm.oldpwd,
          resetPwdForm.pwd1,
          resetPwdForm.pwd2
        )
        ElMessage.success('密码修改成功！')
        dialogVisible.value = false
      } catch (detail) {
        ElMessage.error(detail)
      }
    } else {
      ElMessage.info('请按要求填写字段！')
    }
  })
}

// 添加个人信息表单数据
let profileDialogVisible = ref(false)
let profileForm = reactive({
  username: '',
  phone: '',
  bio: '',
  birth_date: '',
  avatar: null,
  department: null,
})

// 获取个人信息
const getProfileData = async () => {
  try {
    const data = await authHttp.getProfile()
    Object.assign(profileForm, data)
  } catch (detail) {
    ElMessage.error(detail)
  }
}

// 打开个人信息对话框
const onControlProfileDialog = async () => {
  profileDialogVisible.value = true
  await getProfileData()
}

// 提交个人信息
const onSubmitProfile = async () => {
  try {
    await authHttp.updateProfile(profileForm)
    ElMessage.success('个人信息修改成功！')
    profileDialogVisible.value = false
    // 更新显示的用户信息
    displayUser.realname = profileForm.username
    authStore.user.avatar = profileForm.avatar  // 更新头像
  } catch (detail) {
    ElMessage.error(detail)
  }
}

// 添加头像处理方法
const handleAvatarChange = async (file) => {
  // 检查文件大小（限制为 2MB）
  if (file.raw.size / 1024 / 1024 > 2) {
    ElMessage.error('头像图片大小不能超过 2MB!')
    return
  }
  
  // 创建 FormData
  const formData = new FormData()
  formData.append('image', file.raw)
  
  try {
    const result = await homeHttp.uploadImage(formData)
    if (result.errno === 0) {
      // 设置头像URL
      profileForm.avatar = import.meta.env.VITE_BASE_URL + result.data.url
    } else {
      ElMessage.error(result.message || '上传失败')
    }
  } catch (error) {
    ElMessage.error('上传失败')
  }
}
</script>

<template>
  <el-container class="container">
    <el-aside class="aside" :width="asideWidth">
      <router-link to="/" class="brand"
        ><strong>WUMI</strong
        ><span v-show="!isCollapse">OA系统</span></router-link
      >
      <el-menu
        :router="true"
        active-text-color="#64b5f6"
        background-color="#f6f9fc"
        class="el-menu-vertical-demo"
        :default-active="defaultActive"
        text-color="#5d6d7e"
        :collapse="isCollapse"
        :collapse-transition="true"
      >
        <template v-for="route in routes[0].children">
          <el-menu-item
            v-if="!route.children"
            :index="route.name"
            :route="{ name: route.name }"
          >
            <el-icon>
              <component :is="route.meta.icon"></component>
            </el-icon>
            <span>{{ route.meta.text }}</span>
          </el-menu-item>

          <el-sub-menu v-else :index="route.name">
            <template #title>
              <el-icon>
                <component :is="route.meta.icon"></component>
              </el-icon>
              <span>{{ route.meta.text }}</span>
            </template>
            <template v-for="child in route.children">
              <el-menu-item
                v-if="!child.meta.hidden"
                :index="child.name"
                :route="{ name: child.name }"
              >
                <el-icon>
                  <component :is="child.meta.icon"></component>
                </el-icon>
                <span>{{ child.meta.text }}</span>
              </el-menu-item>
            </template>
          </el-sub-menu>
        </template>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="left-header">
          <el-button
            v-show="isCollapse"
            :icon="Expand"
            @click="onCollapseAside"
          />
          <el-button
            v-show="!isCollapse"
            :icon="Fold"
            @click="onCollapseAside"
          />
        </div>
        <el-dropdown>
          <span class="el-dropdown-link">
            <div class="user-info">
              <el-avatar 
                :size="30" 
                :src="authStore.user.avatar" 
                :icon="!authStore.user.avatar ? 'UserFilled' : ''"
              />
              <span class="user-name">[{{ displayUser.department.name }}]{{ displayUser.realname }}</span>
            </div>
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="onControlProfileDialog"
                >个人信息</el-dropdown-item
              >
              <el-dropdown-item divided @click="onControlResetPwdDialog"
                >修改密码</el-dropdown-item
              >
              <el-dropdown-item divided @click="onExit"
                >退出登录</el-dropdown-item
              >
            </el-dropdown-menu>
          </template>

          <!-- 将个人信息对话框移到这里 -->
        </el-dropdown>
      </el-header>
      <el-main class="main">
        <RouterView></RouterView>
      </el-main>
    </el-container>
  </el-container>
  <el-dialog v-model="dialogVisible" title="修改密码" width="500">
    <el-form :model="resetPwdForm" :rules="rules" ref="formTag">
      <el-form-item label="旧密码" :label-width="formLabelWidth" prop="oldpwd">
        <el-input
          v-model="resetPwdForm.oldpwd"
          autocomplete="off"
          type="password"
        />
      </el-form-item>

      <el-form-item label="新密码" :label-width="formLabelWidth" prop="pwd1">
        <el-input
          v-model="resetPwdForm.pwd1"
          autocomplete="off"
          type="password"
        />
      </el-form-item>

      <el-form-item label="确认密码" :label-width="formLabelWidth" prop="pwd2">
        <el-input
          v-model="resetPwdForm.pwd2"
          autocomplete="off"
          type="password"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmit"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="profileDialogVisible" title="个人信息" width="500">
    <el-form :model="profileForm" label-width="100px">
      <el-form-item label="头像" class="avatar-item">
        <el-upload
          class="avatar-uploader"
          action="#"
          :auto-upload="false"
          :show-file-list="false"
          accept="image/*"
          @change="handleAvatarChange"
        >
          <el-avatar
            v-if="profileForm.avatar"
            :size="100"
            :src="profileForm.avatar"
            class="avatar-preview"
          />
          <div v-else class="avatar-uploader-icon">
            <el-icon><Plus /></el-icon>
          </div>
        </el-upload>
      </el-form-item>
      <el-form-item label="用户名">
        <el-input v-model="profileForm.username" />
      </el-form-item>
      <el-form-item label="手机号">
        <el-input v-model="profileForm.phone" />
      </el-form-item>
      <el-form-item label="个人简介">
        <el-input
          v-model="profileForm.bio"
          type="textarea"
          :rows="3"
          placeholder="请输入个人简介"
        />
      </el-form-item>
      <el-form-item label="出生日期">
        <el-date-picker
          v-model="profileForm.birth_date"
          type="date"
          placeholder="选择日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="profileDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmitProfile">确认</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.container {
  height: 100vh;
  background-color: #f8fafc;
}

.aside {
  background-color: #f6f9fc;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: width 0.3s ease-in-out;
  overflow: hidden;
}

.aside .brand {
  color: #5d6d7e;
  text-decoration: none;
  border-bottom: 1px solid #edf2f7;
  background-color: #f8fafc;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  transition: all 0.3s ease-in-out;
  white-space: nowrap;
}

.header {
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #edf2f7;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-menu-item:hover),
:deep(.el-sub-menu__title:hover) {
  background-color: #edf2f7 !important;
  color: #64b5f6 !important;
}

:deep(.el-menu-item.is-active) {
  background-color: #edf2f7 !important;
  color: #64b5f6 !important;
}

.aside::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 1px;
  height: 100%;
  background: linear-gradient(to bottom, #64b5f6, #90caf9);
  opacity: 0.3;
}

.el-dropdown-menu__item:hover {
  background-color: #f8fafc;
  color: #64b5f6;
  transform: translateX(5px);
}

/* 添加一些样式优化 */
.el-form-item {
  margin-bottom: 20px;
}

.el-input {
  width: 100%;
}

.el-date-picker {
  width: 100%;
}

.avatar-item {
  text-align: center;
}

.avatar-uploader {
  text-align: center;
  cursor: pointer;
}

.avatar-uploader-icon {
  width: 100px;
  height: 100px;
  border: 1px dashed var(--el-border-color);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--el-text-color-secondary);
}

.avatar-preview {
  border: 1px solid var(--el-border-color-light);
  transition: all 0.3s;
}

.avatar-uploader:hover .avatar-uploader-icon,
.avatar-uploader:hover .avatar-preview {
  border-color: var(--el-color-primary);
  color: var(--el-color-primary);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-name {
  font-size: 14px;
  color: #5d6d7e;
}

.el-dropdown-link {
  display: flex;
  align-items: center;
  cursor: pointer;
}
</style>
