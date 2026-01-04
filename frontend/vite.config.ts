import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '')
  
  // 获取 API 基础 URL，如果没有设置则使用默认值
  const apiBaseURL = env.VITE_API_BASE_URL || 'http://localhost:8000'
  
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      port: 5173,
      proxy: {
        '/api': {
          target: apiBaseURL,
          changeOrigin: true
          // 不重写路径，保留 /api 前缀，因为后端路由就是 /api/auth/login
        }
      }
    }
  }
})

