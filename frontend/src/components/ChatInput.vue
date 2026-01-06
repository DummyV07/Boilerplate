<template>
  <div class="chat-input-container">
    <!-- 文件列表 -->
    <div v-if="attachments.length > 0" class="attachments-list">
      <div v-for="(attachment, index) in attachments" :key="attachment.id || index" class="attachment-item">
        <el-icon class="file-icon"><Document /></el-icon>
        <span class="file-name">附件{{ index + 1 }}：{{ attachment.filename }}</span>
        <el-icon class="success-icon"><SuccessFilled /></el-icon>
        <el-icon class="remove-icon" @click="removeAttachment(index)"><Close /></el-icon>
      </div>
    </div>

    <div class="input-wrapper">
      <el-input
        v-model="inputText"
        type="textarea"
        :rows="4"
        :placeholder="placeholder"
        class="chat-textarea"
        @keydown.ctrl.enter="handleSend"
        @keydown.meta.enter="handleSend"
        :disabled="loading"
        resize="none"
      />
      <div class="input-footer">
        <div class="input-options">
          <!-- 可以在这里添加选项按钮，如"深度思考"、"联网搜索"等 -->
        </div>
        <div class="input-actions">
          <!-- 文件上传按钮 -->
          <div class="attachment-btn" @click="handleFileClick" title="上传文件">
            <el-icon :size="20"><Paperclip /></el-icon>
          </div>
          <!-- 隐藏的文件输入 -->
          <input
            ref="fileInputRef"
            type="file"
            multiple
            style="display: none"
            @change="handleFileChange"
          />
          <!-- 发送按钮 -->
          <el-button
            type="primary"
            :loading="loading"
            :disabled="!inputText.trim() && attachments.length === 0"
            class="send-btn"
            circle
            @click="handleSend"
            title="发送消息 (Ctrl+Enter)"
          >
            <el-icon :size="18"><ArrowUp /></el-icon>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 文件上传对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传文件"
      width="700px"
      :close-on-click-modal="false"
      @close="handleDialogClose"
    >
      <FileUpload
        default-source="chat"
        @success="handleUploadSuccess"
        @error="handleUploadError"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Paperclip, ArrowUp, Document, SuccessFilled, Close } from '@element-plus/icons-vue'
import FileUpload from './FileUpload.vue'
import type { Attachment } from '@/api/attachments'

interface Emits {
  (e: 'send', message: string, attachments?: Attachment[]): void
}

const emit = defineEmits<Emits>()

const inputText = ref('')
const loading = defineModel<boolean>('loading', { default: false })
const placeholder = defineModel<string>('placeholder', { default: '给 AI 发送消息...' })

const fileInputRef = ref<HTMLInputElement>()
const showUploadDialog = ref(false)
const attachments = ref<Attachment[]>([])

const handleSend = () => {
  if ((!inputText.value.trim() && attachments.value.length === 0) || loading.value) return
  
  const message = inputText.value.trim()
  const filesToSend = [...attachments.value]
  inputText.value = ''
  attachments.value = []
  emit('send', message, filesToSend)
}

const handleFileClick = () => {
  showUploadDialog.value = true
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    showUploadDialog.value = true
  }
}

const handleUploadSuccess = (attachment: Attachment) => {
  console.log('Upload success, attachment:', attachment)
  // 检查attachment是否是有效对象
  if (attachment && attachment.id) {
    // 添加到文件列表
    attachments.value.push(attachment)
    console.log('Attachments list updated:', attachments.value)
    // 延迟关闭对话框，让用户看到上传成功提示
    setTimeout(() => {
      showUploadDialog.value = false
    }, 500)
  } else {
    console.error('Invalid attachment object:', attachment)
  }
}

const handleUploadError = (error: any) => {
  console.error('Upload error:', error)
}

const handleDialogClose = () => {
  // 对话框关闭时，可以在这里清理
}

const removeAttachment = (index: number) => {
  attachments.value.splice(index, 1)
}

defineExpose({
  clear: () => {
    inputText.value = ''
    attachments.value = []
  }
})
</script>

<style scoped>
.chat-input-container {
  padding: 16px 20px;
  background: white;
  border-top: 1px solid #e5e7eb;
}

.attachments-list {
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.attachment-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  gap: 8px;
}

.file-icon {
  color: #f59e0b;
  font-size: 18px;
  flex-shrink: 0;
}

.file-name {
  flex: 1;
  font-size: 14px;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.success-icon {
  color: #10b981;
  font-size: 18px;
  flex-shrink: 0;
}

.remove-icon {
  color: #6b7280;
  font-size: 16px;
  cursor: pointer;
  flex-shrink: 0;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.remove-icon:hover {
  color: #ef4444;
  background: #fee2e2;
}

.input-wrapper {
  position: relative;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 12px;
  transition: all 0.2s;
}

.input-wrapper:focus-within {
  border-color: #409eff;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
}

:deep(.chat-textarea) {
  border: none;
  background: transparent;
}

:deep(.chat-textarea .el-textarea__inner) {
  border: none;
  background: transparent;
  box-shadow: none;
  padding: 0;
  font-size: 14px;
  line-height: 1.6;
  resize: none;
  color: #1f2937;
}

:deep(.chat-textarea .el-textarea__inner::placeholder) {
  color: #9ca3af;
}

:deep(.chat-textarea .el-textarea__inner:focus) {
  border: none;
  box-shadow: none;
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e5e7eb;
}

.input-options {
  display: flex;
  gap: 8px;
  flex: 1;
}

.input-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.attachment-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: white;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s;
  color: #6b7280;
}

.attachment-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
  color: #374151;
}

.attachment-btn:active {
  background: #e5e7eb;
}

.send-btn {
  width: 36px;
  height: 36px;
  padding: 0;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transform: translateY(-1px);
}

.send-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3);
}

.send-btn:disabled {
  background: #d1d5db;
  box-shadow: none;
  cursor: not-allowed;
}

.send-btn .el-icon {
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-input-container {
    padding: 12px 16px;
  }

  .input-wrapper {
    padding: 10px;
    border-radius: 12px;
  }

  .attachment-btn,
  .send-btn {
    width: 32px;
    height: 32px;
  }
}
</style>
