<template>
  <div class="chat-container">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="250px" class="sidebar">
        <div class="sidebar-header">
          <h3>AI 对话</h3>
          <el-button type="primary" size="small" @click="handleNewConversation">
            <el-icon :size="16"><Plus /></el-icon>
            新建对话
          </el-button>
        </div>
        
        <el-menu
          :default-active="currentConversationId?.toString()"
          @select="handleSelectConversation"
        >
          <el-menu-item
            v-for="conv in conversations"
            :key="conv.id"
            :index="conv.id.toString()"
          >
            <span>{{ conv.title }}</span>
          </el-menu-item>
        </el-menu>
        
        <div class="sidebar-footer">
          <el-button type="danger" size="small" @click="handleLogout">
            退出登录
          </el-button>
        </div>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-main class="chat-main">
        <div v-if="!currentConversation" class="empty-state">
          <el-empty description="选择一个对话或创建新对话开始聊天" />
        </div>
        
        <div v-else class="chat-content">
          <!-- 消息列表 -->
          <div class="messages-container" ref="messagesContainerRef">
            <MessageBubble
              v-for="message in messages"
              :key="message.id"
              :message="message"
            />
            <LoadingSpinner v-if="isLoading" />
          </div>
          
          <!-- 输入框 -->
          <ChatInput
            v-model:loading="isSending"
            @send="handleSendMessage"
          />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useConversationsStore } from '@/store/conversations'
import { messagesApi } from '@/api/messages'
import { tasksApi, type Task } from '@/api/tasks'
import { poll } from '@/utils/polling'
import MessageBubble from '@/components/MessageBubble.vue'
import ChatInput from '@/components/ChatInput.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { Message } from '@/api/conversations'

const router = useRouter()
const authStore = useAuthStore()
const conversationsStore = useConversationsStore()

const messagesContainerRef = ref<HTMLElement>()
const isSending = ref(false)
const isLoading = ref(false)
const currentConversationId = ref<number | null>(null)

const conversations = computed(() => conversationsStore.conversations)
const currentConversation = computed(() => conversationsStore.currentConversation)
const messages = computed(() => currentConversation.value?.messages || [])

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainerRef.value) {
      messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight
    }
  })
}

// 监听消息变化，自动滚动
watch(messages, () => {
  scrollToBottom()
}, { deep: true })

// 初始化
onMounted(async () => {
  authStore.init()
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  await conversationsStore.fetchConversations()
  
  // 如果有对话，选择第一个
  if (conversations.value.length > 0) {
    await handleSelectConversation(conversations.value[0].id.toString())
  }
})

// 选择对话
const handleSelectConversation = async (conversationId: string) => {
  const id = parseInt(conversationId)
  currentConversationId.value = id
  await conversationsStore.fetchConversation(id)
  scrollToBottom()
}

// 新建对话
const handleNewConversation = async () => {
  const title = `对话 ${new Date().toLocaleString('zh-CN')}`
  try {
    const conversation = await conversationsStore.createConversation(title)
    if (conversation) {
      currentConversationId.value = conversation.id
    }
    scrollToBottom()
  } catch (error) {
    ElMessage.error('创建对话失败')
  }
}

// 发送消息
const handleSendMessage = async (content: string) => {
  if (!currentConversation.value) {
    ElMessage.warning('请先创建或选择一个对话')
    return
  }
  
  isSending.value = true
  isLoading.value = true
  
  try {
    // 发送消息（返回202和task_id）
    const response = await messagesApi.sendMessage(
      currentConversation.value.id,
      {
        role: 'user',
        content
      }
    ) as unknown as { task_id: string; status: string; message: string }
    
    // 立即显示用户消息（临时）
    const tempUserMessage: Message = {
      id: Date.now(),
      conversation_id: currentConversation.value.id,
      role: 'user',
      content,
      created_at: new Date().toISOString()
    }
    
    if (!currentConversation.value.messages) {
      currentConversation.value.messages = []
    }
    currentConversation.value.messages.push(tempUserMessage)
    
    // 开始轮询任务状态
    poll(
      async () => {
        const task = await tasksApi.getTaskStatus(response.task_id) as unknown as Task
        return task
      },
      {
        interval: 1000,
        maxAttempts: 60,
        shouldStop: (task) => task.status === 'completed' || task.status === 'failed',
        onSuccess: async (task) => {
          isLoading.value = false
          
          if (task.status === 'completed') {
            // 重新获取对话以获取最新消息
            await conversationsStore.fetchConversation(currentConversation.value!.id)
            ElMessage.success('消息已发送')
          } else if (task.status === 'failed') {
            ElMessage.error(task.error_message || '消息发送失败')
            // 移除临时消息
            if (currentConversation.value?.messages) {
              const index = currentConversation.value.messages.findIndex(
                m => m.id === tempUserMessage.id
              )
              if (index > -1) {
                currentConversation.value.messages.splice(index, 1)
              }
            }
          }
        },
        onError: (error) => {
          isLoading.value = false
          ElMessage.error('获取消息状态失败')
          console.error('Polling error:', error)
        },
        onTimeout: () => {
          isLoading.value = false
          ElMessage.warning('请求超时，请稍后刷新查看')
        }
      }
    )
    
  } catch (error: any) {
    isLoading.value = false
    ElMessage.error(error.message || '发送消息失败')
  } finally {
    isSending.value = false
  }
}

// 退出登录
const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.sidebar {
  background: #f5f5f5;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.sidebar-header h3 {
  margin: 0 0 12px 0;
  color: #333;
}

.sidebar-footer {
  padding: 16px;
  margin-top: auto;
  border-top: 1px solid #e0e0e0;
}

.chat-main {
  display: flex;
  flex-direction: column;
  padding: 0;
  background: white;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.chat-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #fafafa;
}

.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>

