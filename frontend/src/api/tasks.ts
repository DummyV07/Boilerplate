import request from '@/utils/request'

export interface Task {
  id: number
  task_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  result: string | null
  error_message: string | null
  created_at: string
  updated_at: string
}

export const tasksApi = {
  // 获取任务状态
  getTaskStatus(taskId: string) {
    return request.get<Task>(`/tasks/${taskId}`)
  }
}

