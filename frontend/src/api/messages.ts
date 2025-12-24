import request from '@/utils/request'

export interface MessageCreate {
  role: 'user' | 'assistant'
  content: string
}

export interface MessageResponse {
  task_id: string
  status: string
  message: string
}

export const messagesApi = {
  // 发送消息（返回202和task_id）
  sendMessage(conversationId: number, data: MessageCreate) {
    return request.post<MessageResponse>(`/conversations/${conversationId}/messages`, data)
  }
}

