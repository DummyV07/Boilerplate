import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type UserInfo } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<UserInfo | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  // 登录
  const login = async (username: string, password: string) => {
    try {
      const response = await authApi.login({ username, password })
      token.value = response.access_token
      localStorage.setItem('token', response.access_token)
      
      // 获取用户信息
      await fetchUserInfo()
      
      ElMessage.success('登录成功')
      return true
    } catch (error: any) {
      ElMessage.error(error.message || '登录失败')
      return false
    }
  }

  // 注册
  const register = async (username: string, email: string, password: string) => {
    try {
      await authApi.register({ username, email, password })
      ElMessage.success('注册成功，请登录')
      return true
    } catch (error: any) {
      ElMessage.error(error.message || '注册失败')
      return false
    }
  }

  // 获取用户信息
  const fetchUserInfo = async () => {
    try {
      const info = await authApi.getCurrentUser()
      userInfo.value = info
      localStorage.setItem('userInfo', JSON.stringify(info))
    } catch (error) {
      console.error('获取用户信息失败', error)
    }
  }

  // 登出
  const logout = () => {
    token.value = null
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    ElMessage.success('已退出登录')
  }

  // 初始化（从localStorage恢复）
  const init = () => {
    const savedToken = localStorage.getItem('token')
    const savedUserInfo = localStorage.getItem('userInfo')
    
    if (savedToken) {
      token.value = savedToken
    }
    
    if (savedUserInfo) {
      try {
        userInfo.value = JSON.parse(savedUserInfo)
      } catch (e) {
        console.error('解析用户信息失败', e)
      }
    }
  }

  return {
    token,
    userInfo,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUserInfo,
    init
  }
})

