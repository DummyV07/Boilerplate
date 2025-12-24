import request from '@/utils/request'

export interface LoginForm {
  username: string
  password: string
}

export interface RegisterForm {
  username: string
  email: string
  password: string
}

export interface UserInfo {
  id: number
  username: string
  email: string
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  // 登录
  login(form: LoginForm) {
    const formData = new FormData()
    formData.append('username', form.username)
    formData.append('password', form.password)
    
    return request.post<TokenResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },

  // 注册
  register(form: RegisterForm) {
    return request.post<UserInfo>('/auth/register', form)
  },

  // 获取当前用户信息
  getCurrentUser() {
    return request.get<UserInfo>('/auth/me')
  }
}

