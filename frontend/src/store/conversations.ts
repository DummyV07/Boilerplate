import { defineStore } from 'pinia'
import { ref } from 'vue'
import { conversationsApi, type Conversation } from '@/api/conversations'

export const useConversationsStore = defineStore('conversations', () => {
  const conversations = ref<Conversation[]>([])
  const currentConversation = ref<Conversation | null>(null)

  // 获取所有对话
  const fetchConversations = async () => {
    try {
      const data = await conversationsApi.getConversations()
      conversations.value = data
    } catch (error) {
      console.error('获取对话列表失败', error)
    }
  }

  // 创建对话
  const createConversation = async (title: string) => {
    try {
      const data = await conversationsApi.createConversation({ title })
      conversations.value.unshift(data)
      currentConversation.value = data
      return data
    } catch (error) {
      console.error('创建对话失败', error)
      throw error
    }
  }

  // 获取对话详情
  const fetchConversation = async (id: number) => {
    try {
      const data = await conversationsApi.getConversation(id)
      currentConversation.value = data
      return data
    } catch (error) {
      console.error('获取对话详情失败', error)
      throw error
    }
  }

  // 设置当前对话
  const setCurrentConversation = (conversation: Conversation | null) => {
    currentConversation.value = conversation
  }

  return {
    conversations,
    currentConversation,
    fetchConversations,
    createConversation,
    fetchConversation,
    setCurrentConversation
  }
})

