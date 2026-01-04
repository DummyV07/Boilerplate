<template>
  <div class="admin-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>附件管理</span>
          <el-button type="primary" @click="showUploadDialog = true">
            <el-icon><plus /></el-icon>
            上传文件
          </el-button>
        </div>
      </template>

      <!-- 统计信息 -->
      <div class="stats-section" v-if="stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-label">总文件数</div>
              <div class="stat-value">{{ stats.total }}</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-label">总存储大小</div>
              <div class="stat-value">{{ stats.total_size_mb }} MB</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-label">已完成识别</div>
              <div class="stat-value">{{ stats.status_stats?.completed || 0 }}</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-label">识别中</div>
              <div class="stat-value">{{ stats.status_stats?.processing || 0 }}</div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 搜索和筛选 -->
      <div class="filter-section">
        <el-form :inline="true" :model="filterForm">
          <el-form-item label="搜索">
            <el-input
              v-model="filterForm.search"
              placeholder="文件名、描述、标签"
              clearable
              @clear="loadAttachments"
              @keyup.enter="loadAttachments"
              style="width: 200px"
            />
          </el-form-item>
          <el-form-item label="文件类型">
            <el-input
              v-model="filterForm.file_type"
              placeholder="MIME类型"
              clearable
              @clear="loadAttachments"
              style="width: 150px"
            />
          </el-form-item>
          <el-form-item label="识别状态">
            <el-select
              v-model="filterForm.recognition_status"
              placeholder="全部"
              clearable
              @change="loadAttachments"
              style="width: 150px"
            >
              <el-option label="待处理" value="pending" />
              <el-option label="处理中" value="processing" />
              <el-option label="已完成" value="completed" />
              <el-option label="失败" value="failed" />
            </el-select>
          </el-form-item>
          <el-form-item label="用户ID">
            <el-input-number
              v-model="filterForm.user_id"
              :min="1"
              clearable
              @clear="loadAttachments"
              style="width: 120px"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="loadAttachments">搜索</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 文件列表 -->
      <el-table
        v-loading="loading"
        :data="attachments"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="filename" label="文件名" min-width="200" show-overflow-tooltip />
        <el-table-column prop="file_type" label="文件类型" width="150" />
        <el-table-column label="文件大小" width="120">
          <template #default="{ row }">
            {{ formatFileSize(row.file_size) }}
          </template>
        </el-table-column>
        <el-table-column prop="user_id" label="用户ID" width="100" />
        <el-table-column label="识别状态" width="120">
          <template #default="{ row }">
            <el-tag
              :type="getStatusType(row.recognition_status)"
              size="small"
            >
              {{ getStatusText(row.recognition_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
        <el-table-column prop="tags" label="标签" width="150" show-overflow-tooltip />
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewDetails(row)"
            >
              详情
            </el-button>
            <el-button
              type="success"
              size="small"
              @click="downloadFile(row)"
            >
              下载
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="deleteFile(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.limit"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadAttachments"
          @current-change="loadAttachments"
        />
      </div>
    </el-card>

    <!-- 上传对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传文件"
      width="800px"
      @close="handleUploadClose"
    >
      <FileUpload
        @success="handleUploadSuccess"
        @error="handleUploadError"
      />
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="文件详情"
      width="800px"
    >
      <div v-if="selectedAttachment" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="ID">
            {{ selectedAttachment.id }}
          </el-descriptions-item>
          <el-descriptions-item label="文件名">
            {{ selectedAttachment.filename }}
          </el-descriptions-item>
          <el-descriptions-item label="存储文件名">
            {{ selectedAttachment.stored_filename }}
          </el-descriptions-item>
          <el-descriptions-item label="文件类型">
            {{ selectedAttachment.file_type }}
          </el-descriptions-item>
          <el-descriptions-item label="文件大小">
            {{ formatFileSize(selectedAttachment.file_size) }}
          </el-descriptions-item>
          <el-descriptions-item label="文件扩展名">
            {{ selectedAttachment.file_extension }}
          </el-descriptions-item>
          <el-descriptions-item label="用户ID">
            {{ selectedAttachment.user_id }}
          </el-descriptions-item>
          <el-descriptions-item label="识别状态">
            <el-tag :type="getStatusType(selectedAttachment.recognition_status)">
              {{ getStatusText(selectedAttachment.recognition_status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ selectedAttachment.description || '无' }}
          </el-descriptions-item>
          <el-descriptions-item label="标签" :span="2">
            {{ selectedAttachment.tags || '无' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ formatDate(selectedAttachment.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ formatDate(selectedAttachment.updated_at) }}
          </el-descriptions-item>
          <el-descriptions-item
            v-if="selectedAttachment.recognition_error"
            label="识别错误"
            :span="2"
          >
            <el-alert
              :title="selectedAttachment.recognition_error"
              type="error"
              :closable="false"
            />
          </el-descriptions-item>
          <el-descriptions-item
            v-if="selectedAttachment.recognition_result"
            label="识别结果"
            :span="2"
          >
            <pre class="recognition-result">{{ formatRecognitionResult(selectedAttachment.recognition_result) }}</pre>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { adminAttachmentsApi, attachmentsApi, type Attachment } from '@/api/attachments'
import FileUpload from '@/components/FileUpload.vue'

const loading = ref(false)
const attachments = ref<Attachment[]>([])
const stats = ref<any>(null)
const showUploadDialog = ref(false)
const showDetailDialog = ref(false)
const selectedAttachment = ref<Attachment | null>(null)

const filterForm = ref({
  search: '',
  file_type: '',
  recognition_status: '',
  user_id: undefined as number | undefined
})

const pagination = ref({
  page: 1,
  limit: 20,
  total: 0
})

onMounted(() => {
  loadStats()
  loadAttachments()
})

const loadStats = async () => {
  try {
    stats.value = await adminAttachmentsApi.getStats()
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const loadAttachments = async () => {
  try {
    loading.value = true
    const params: any = {
      skip: (pagination.value.page - 1) * pagination.value.limit,
      limit: pagination.value.limit
    }
    if (filterForm.value.search) {
      params.search = filterForm.value.search
    }
    if (filterForm.value.file_type) {
      params.file_type = filterForm.value.file_type
    }
    if (filterForm.value.recognition_status) {
      params.recognition_status = filterForm.value.recognition_status
    }
    if (filterForm.value.user_id) {
      params.user_id = filterForm.value.user_id
    }

    const response = await adminAttachmentsApi.list(params)
    attachments.value = response.items
    pagination.value.total = response.total
  } catch (error) {
    ElMessage.error('加载附件列表失败')
    console.error('Failed to load attachments:', error)
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.value = {
    search: '',
    file_type: '',
    recognition_status: '',
    user_id: undefined
  }
  pagination.value.page = 1
  loadAttachments()
}

const viewDetails = async (attachment: Attachment) => {
  try {
    const detail = await adminAttachmentsApi.get(attachment.id)
    selectedAttachment.value = detail
    showDetailDialog.value = true
  } catch (error) {
    ElMessage.error('获取文件详情失败')
    console.error('Failed to get attachment details:', error)
  }
}

const downloadFile = async (attachment: Attachment) => {
  try {
    const blob = await attachmentsApi.download(attachment.id)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = attachment.filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
    ElMessage.success('下载开始')
  } catch (error) {
    ElMessage.error('下载文件失败')
    console.error('Failed to download file:', error)
  }
}

const deleteFile = async (attachment: Attachment) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除文件 "${attachment.filename}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await attachmentsApi.delete(attachment.id)
    ElMessage.success('删除成功')
    loadAttachments()
    loadStats()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除文件失败')
      console.error('Failed to delete file:', error)
    }
  }
}

const handleUploadSuccess = () => {
  ElMessage.success('文件上传成功')
  loadAttachments()
  loadStats()
}

const handleUploadError = (error: any) => {
  console.error('Upload error:', error)
}

const handleUploadClose = () => {
  // 对话框关闭时的处理
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const getStatusType = (status: string): string => {
  const map: Record<string, string> = {
    pending: 'info',
    processing: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string): string => {
  const map: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成',
    failed: '失败'
  }
  return map[status] || status
}

const formatRecognitionResult = (result: string): string => {
  try {
    const obj = JSON.parse(result)
    return JSON.stringify(obj, null, 2)
  } catch {
    return result
  }
}
</script>

<style scoped>
.admin-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-section {
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.filter-section {
  margin-bottom: 20px;
}

.pagination-section {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.detail-content {
  max-height: 600px;
  overflow-y: auto;
}

.recognition-result {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-size: 12px;
  max-height: 300px;
  overflow-y: auto;
}
</style>
