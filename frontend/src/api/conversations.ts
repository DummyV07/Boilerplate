import request from '@/utils/request'

export interface Conversation {
  id: number
  user_id: number
  title: string
  created_at: string
  messages?: Message[]
}

export interface Message {
  id: number
  conversation_id: number
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface ConversationCreate {
  title: string
}

export const conversationsApi = {
  // 获取所有对话
  getConversations() {
    return request.get<Conversation[]>('/conversations')
  },

  // 创建对话
  createConversation(data: ConversationCreate) {
    return request.post<Conversation>('/conversations', data)
  },

  // 获取单个对话
  getConversation(id: number) {
    return request.get<Conversation>(`/conversations/${id}`)
  }
}

