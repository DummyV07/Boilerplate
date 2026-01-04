<template>
  <div class="file-upload">
    <el-upload
      ref="uploadRef"
      :action="uploadUrl"
      :headers="uploadHeaders"
      :data="uploadData"
      :before-upload="beforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-progress="handleProgress"
      :show-file-list="false"
      :auto-upload="false"
      drag
      multiple
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        将文件拖到此处，或<em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          支持的文件类型：图片、文档、压缩包等（最大100MB）
        </div>
      </template>
    </el-upload>

    <div v-if="fileList.length > 0" class="file-list">
      <div v-for="(file, index) in fileList" :key="index" class="file-item">
        <div class="file-info">
          <el-icon><document /></el-icon>
          <span class="file-name">{{ file.name }}</span>
          <span class="file-size">({{ formatFileSize(file.size) }})</span>
        </div>
        <div class="file-actions">
          <el-input
            v-model="file.description"
            placeholder="文件描述（可选）"
            size="small"
            style="width: 200px; margin-right: 10px"
          />
          <el-input
            v-model="file.tags"
            placeholder="标签（可选，逗号分隔）"
            size="small"
            style="width: 200px; margin-right: 10px"
          />
          <el-button
            type="primary"
            size="small"
            :loading="file.uploading"
            @click="uploadFile(file, index)"
          >
            {{ file.uploading ? '上传中...' : '上传' }}
          </el-button>
          <el-button
            size="small"
            @click="removeFile(index)"
            :disabled="file.uploading"
          >
            移除
          </el-button>
        </div>
        <el-progress
          v-if="file.uploading"
          :percentage="file.progress"
          :status="file.status"
        />
        <div v-if="file.result" class="upload-result">
          <el-alert
            :title="file.result.success ? '上传成功' : '上传失败'"
            :type="file.result.success ? 'success' : 'error'"
            :description="file.result.message"
            show-icon
            :closable="false"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Document } from '@element-plus/icons-vue'
import { attachmentsApi } from '@/api/attachments'
import type { UploadFile, UploadFiles, UploadInstance } from 'element-plus'

interface FileItem {
  file: File
  name: string
  size: number
  description: string
  tags: string
  uploading: boolean
  progress: number
  status?: 'success' | 'exception'
  result?: {
    success: boolean
    message: string
    data?: any
  }
}

const emit = defineEmits<{
  success: [attachment: any]
  error: [error: any]
}>()

const uploadRef = ref<UploadInstance>()
const fileList = ref<FileItem[]>([])

const uploadUrl = computed(() => {
  // 不使用action，手动上传
  return ''
})

const uploadHeaders = computed(() => {
  const token = localStorage.getItem('token')
  return {
    Authorization: `Bearer ${token}`
  }
})

const uploadData = computed(() => ({} as any))

const beforeUpload = (file: File) => {
  // 检查文件大小（100MB）
  const maxSize = 100 * 1024 * 1024
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过100MB')
    return false
  }

  // 添加到文件列表
  fileList.value.push({
    file,
    name: file.name,
    size: file.size,
    description: '',
    tags: '',
    uploading: false,
    progress: 0
  })

  return false // 阻止自动上传
}

const uploadFile = async (fileItem: FileItem, index: number) => {
  try {
    fileItem.uploading = true
    fileItem.progress = 0
    fileItem.status = undefined
    fileItem.result = undefined

    // 模拟上传进度
    const progressInterval = setInterval(() => {
      if (fileItem.progress < 90) {
        fileItem.progress += 10
      }
    }, 200)

    const attachment = await attachmentsApi.upload({
      file: fileItem.file,
      description: fileItem.description || undefined,
      tags: fileItem.tags || undefined
    })

    clearInterval(progressInterval)
    fileItem.progress = 100
    fileItem.status = 'success'
    fileItem.result = {
      success: true,
      message: '上传成功',
      data: attachment
    }
    fileItem.uploading = false

    ElMessage.success('文件上传成功')
    emit('success', attachment)
  } catch (error: any) {
    fileItem.progress = 0
    fileItem.status = 'exception'
    fileItem.result = {
      success: false,
      message: error.response?.data?.detail || error.message || '上传失败'
    }
    fileItem.uploading = false

    ElMessage.error(fileItem.result.message)
    emit('error', error)
  }
}

const removeFile = (index: number) => {
  fileList.value.splice(index, 1)
}

const handleSuccess = () => {
  // 不使用默认的成功处理
}

const handleError = () => {
  // 不使用默认的错误处理
}

const handleProgress = () => {
  // 不使用默认的进度处理
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}
</script>

<style scoped>
.file-upload {
  width: 100%;
}

.file-list {
  margin-top: 20px;
}

.file-item {
  padding: 15px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  margin-bottom: 10px;
  background: #fff;
}

.file-info {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.file-info .el-icon {
  margin-right: 8px;
  font-size: 20px;
  color: #409eff;
}

.file-name {
  font-weight: 500;
  margin-right: 8px;
}

.file-size {
  color: #909399;
  font-size: 12px;
}

.file-actions {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.upload-result {
  margin-top: 10px;
}

:deep(.el-upload) {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
}
</style>
