<template>
  <div class="admin-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>后台管理</span>
        </div>
      </template>

      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <!-- 附件管理 -->
        <el-tab-pane label="附件管理" name="attachments">
          <div class="tab-header">
            <el-button type="primary" @click="showUploadDialog = true">
              <el-icon><plus /></el-icon>
              上传文件
            </el-button>
          </div>

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
        </el-tab-pane>

        <!-- 聊天记录管理 -->
        <el-tab-pane label="聊天记录管理" name="conversations">
          <div class="tab-content">
            <!-- 统计信息 -->
            <div class="stats-section" v-if="conversationStats">
              <el-row :gutter="20">
                <el-col :span="8">
                  <div class="stat-item">
                    <div class="stat-label">总对话数</div>
                    <div class="stat-value">{{ conversationStats.total }}</div>
                  </div>
                </el-col>
                <el-col :span="8">
                  <div class="stat-item">
                    <div class="stat-label">总消息数</div>
                    <div class="stat-value">{{ conversationStats.total_messages }}</div>
                  </div>
                </el-col>
              </el-row>
            </div>

            <!-- 搜索和筛选 -->
            <div class="filter-section">
              <el-form :inline="true" :model="conversationFilterForm">
                <el-form-item label="搜索">
                  <el-input
                    v-model="conversationFilterForm.search"
                    placeholder="对话标题"
                    clearable
                    @clear="loadConversations"
                    @keyup.enter="loadConversations"
                    style="width: 200px"
                  />
                </el-form-item>
                <el-form-item label="用户ID">
                  <el-input-number
                    v-model="conversationFilterForm.user_id"
                    :min="1"
                    clearable
                    @clear="loadConversations"
                    style="width: 120px"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="loadConversations">搜索</el-button>
                  <el-button @click="resetConversationFilter">重置</el-button>
                </el-form-item>
              </el-form>
            </div>

            <!-- 对话列表 -->
            <el-table
              v-loading="conversationLoading"
              :data="conversations"
              stripe
              style="width: 100%"
            >
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
              <el-table-column prop="user_id" label="用户ID" width="100" />
              <el-table-column label="消息数" width="100">
                <template #default="{ row }">
                  {{ row.messages?.length || 0 }}
                </template>
              </el-table-column>
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
                    @click="viewConversationDetails(row)"
                  >
                    详情
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click="deleteConversation(row)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="pagination-section">
              <el-pagination
                v-model:current-page="conversationPagination.page"
                v-model:page-size="conversationPagination.limit"
                :page-sizes="[10, 20, 50, 100]"
                :total="conversationPagination.total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="loadConversations"
                @current-change="loadConversations"
              />
            </div>
          </div>
        </el-tab-pane>

        <!-- 用户反馈管理 -->
        <el-tab-pane label="用户反馈管理" name="feedback">
          <div class="tab-content">
            <!-- 统计信息 -->
            <div class="stats-section" v-if="feedbackStats">
              <el-row :gutter="20">
                <el-col :span="6">
                  <div class="stat-item">
                    <div class="stat-label">总反馈数</div>
                    <div class="stat-value">{{ feedbackStats.total }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <div class="stat-label">待处理</div>
                    <div class="stat-value">{{ feedbackStats.status_stats?.pending || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <div class="stat-label">处理中</div>
                    <div class="stat-value">{{ feedbackStats.status_stats?.processing || 0 }}</div>
                  </div>
                </el-col>
                <el-col :span="6">
                  <div class="stat-item">
                    <div class="stat-label">已解决</div>
                    <div class="stat-value">{{ feedbackStats.status_stats?.resolved || 0 }}</div>
                  </div>
                </el-col>
              </el-row>
            </div>

            <!-- 搜索和筛选 -->
            <div class="filter-section">
              <el-form :inline="true" :model="feedbackFilterForm">
                <el-form-item label="搜索">
                  <el-input
                    v-model="feedbackFilterForm.search"
                    placeholder="反馈内容"
                    clearable
                    @clear="loadFeedback"
                    @keyup.enter="loadFeedback"
                    style="width: 200px"
                  />
                </el-form-item>
                <el-form-item label="反馈类型">
                  <el-select
                    v-model="feedbackFilterForm.feedback_type"
                    placeholder="全部"
                    clearable
                    @change="loadFeedback"
                    style="width: 150px"
                  >
                    <el-option label="Bug" value="bug" />
                    <el-option label="功能建议" value="feature" />
                    <el-option label="投诉" value="complaint" />
                    <el-option label="其他" value="other" />
                  </el-select>
                </el-form-item>
                <el-form-item label="状态">
                  <el-select
                    v-model="feedbackFilterForm.status"
                    placeholder="全部"
                    clearable
                    @change="loadFeedback"
                    style="width: 150px"
                  >
                    <el-option label="待处理" value="pending" />
                    <el-option label="处理中" value="processing" />
                    <el-option label="已解决" value="resolved" />
                    <el-option label="已关闭" value="closed" />
                  </el-select>
                </el-form-item>
                <el-form-item label="用户ID">
                  <el-input-number
                    v-model="feedbackFilterForm.user_id"
                    :min="1"
                    clearable
                    @clear="loadFeedback"
                    style="width: 120px"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="loadFeedback">搜索</el-button>
                  <el-button @click="resetFeedbackFilter">重置</el-button>
                </el-form-item>
              </el-form>
            </div>

            <!-- 反馈列表 -->
            <el-table
              v-loading="feedbackLoading"
              :data="feedbacks"
              stripe
              style="width: 100%"
            >
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="user_id" label="用户ID" width="100" />
              <el-table-column label="反馈类型" width="120">
                <template #default="{ row }">
                  <el-tag :type="getFeedbackTypeTag(row.feedback_type)">
                    {{ getFeedbackTypeText(row.feedback_type) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="content" label="反馈内容" min-width="200" show-overflow-tooltip />
              <el-table-column label="状态" width="120">
                <template #default="{ row }">
                  <el-tag :type="getFeedbackStatusType(row.status)">
                    {{ getFeedbackStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="创建时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-button
                    type="primary"
                    size="small"
                    @click="viewFeedbackDetails(row)"
                  >
                    处理
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="pagination-section">
              <el-pagination
                v-model:current-page="feedbackPagination.page"
                v-model:page-size="feedbackPagination.limit"
                :page-sizes="[10, 20, 50, 100]"
                :total="feedbackPagination.total"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="loadFeedback"
                @current-change="loadFeedback"
              />
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
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

    <!-- 附件详情对话框 -->
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
          <el-descriptions-item label="文件来源">
            {{ selectedAttachment.source }}
          </el-descriptions-item>
          <el-descriptions-item label="是否共享">
            <el-tag :type="selectedAttachment.is_shared ? 'success' : 'info'">
              {{ selectedAttachment.is_shared ? '是' : '否' }}
            </el-tag>
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

    <!-- 对话详情对话框 -->
    <el-dialog
      v-model="showConversationDetailDialog"
      title="对话详情"
      width="900px"
    >
      <div v-if="selectedConversation" class="detail-content">
        <el-descriptions :column="2" border style="margin-bottom: 20px">
          <el-descriptions-item label="ID">
            {{ selectedConversation.id }}
          </el-descriptions-item>
          <el-descriptions-item label="用户ID">
            {{ selectedConversation.user_id }}
          </el-descriptions-item>
          <el-descriptions-item label="标题" :span="2">
            {{ selectedConversation.title }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ formatDate(selectedConversation.created_at) }}
          </el-descriptions-item>
        </el-descriptions>
        <h4>消息列表</h4>
        <el-table :data="selectedConversation.messages || []" stripe style="margin-top: 10px">
          <el-table-column prop="role" label="角色" width="100">
            <template #default="{ row }">
              <el-tag :type="row.role === 'user' ? 'primary' : 'success'">
                {{ row.role === 'user' ? '用户' : '助手' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="content" label="内容" show-overflow-tooltip />
          <el-table-column label="时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>

    <!-- 反馈处理对话框 -->
    <el-dialog
      v-model="showFeedbackDetailDialog"
      title="处理反馈"
      width="700px"
    >
      <div v-if="selectedFeedback" class="detail-content">
        <el-form :model="feedbackUpdateForm" label-width="100px">
          <el-form-item label="反馈ID">
            <span>{{ selectedFeedback.id }}</span>
          </el-form-item>
          <el-form-item label="用户ID">
            <span>{{ selectedFeedback.user_id }}</span>
          </el-form-item>
          <el-form-item label="反馈类型">
            <el-tag :type="getFeedbackTypeTag(selectedFeedback.feedback_type)">
              {{ getFeedbackTypeText(selectedFeedback.feedback_type) }}
            </el-tag>
          </el-form-item>
          <el-form-item label="反馈内容">
            <el-input
              v-model="selectedFeedback.content"
              type="textarea"
              :rows="4"
              readonly
            />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="feedbackUpdateForm.status" style="width: 100%">
              <el-option label="待处理" value="pending" />
              <el-option label="处理中" value="processing" />
              <el-option label="已解决" value="resolved" />
              <el-option label="已关闭" value="closed" />
            </el-select>
          </el-form-item>
          <el-form-item label="管理员回复">
            <el-input
              v-model="feedbackUpdateForm.admin_comment"
              type="textarea"
              :rows="4"
              placeholder="请输入回复内容"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="updateFeedback">保存</el-button>
            <el-button @click="showFeedbackDetailDialog = false">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { adminAttachmentsApi, attachmentsApi, type Attachment } from '@/api/attachments'
import { adminConversationsApi, type Conversation } from '@/api/conversations'
import { adminFeedbackApi, type Feedback } from '@/api/feedback'
import FileUpload from '@/components/FileUpload.vue'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref('attachments')

// 附件管理相关
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

// 聊天记录管理相关
const conversationLoading = ref(false)
const conversations = ref<Conversation[]>([])
const conversationStats = ref<any>(null)
const showConversationDetailDialog = ref(false)
const selectedConversation = ref<Conversation | null>(null)

const conversationFilterForm = ref({
  search: '',
  user_id: undefined as number | undefined
})

const conversationPagination = ref({
  page: 1,
  limit: 20,
  total: 0
})

// 反馈管理相关
const feedbackLoading = ref(false)
const feedbacks = ref<Feedback[]>([])
const feedbackStats = ref<any>(null)
const showFeedbackDetailDialog = ref(false)
const selectedFeedback = ref<Feedback | null>(null)
const feedbackUpdateForm = ref({
  status: '',
  admin_comment: ''
})

const feedbackFilterForm = ref({
  search: '',
  feedback_type: '',
  status: '',
  user_id: undefined as number | undefined
})

const feedbackPagination = ref({
  page: 1,
  limit: 20,
  total: 0
})

const handleTabChange = (tabName: string) => {
  if (tabName === 'attachments') {
    loadStats()
    loadAttachments()
  } else if (tabName === 'conversations') {
    loadConversationStats()
    loadConversations()
  } else if (tabName === 'feedback') {
    loadFeedbackStats()
    loadFeedback()
  }
}

onMounted(async () => {
  // 检查认证
  authStore.init()
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  // 刷新用户信息
  await authStore.fetchUserInfo()
  
  if (activeTab.value === 'attachments') {
    loadStats()
    loadAttachments()
  }
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

// ==================== 聊天记录管理 ====================

const loadConversationStats = async () => {
  try {
    conversationStats.value = await adminConversationsApi.getStats()
  } catch (error) {
    console.error('Failed to load conversation stats:', error)
  }
}

const loadConversations = async () => {
  try {
    conversationLoading.value = true
    const params: any = {
      skip: (conversationPagination.value.page - 1) * conversationPagination.value.limit,
      limit: conversationPagination.value.limit
    }
    if (conversationFilterForm.value.search) {
      params.search = conversationFilterForm.value.search
    }
    if (conversationFilterForm.value.user_id) {
      params.user_id = conversationFilterForm.value.user_id
    }

    const response = await adminConversationsApi.list(params)
    conversations.value = response.items
    conversationPagination.value.total = response.total
  } catch (error) {
    ElMessage.error('加载对话列表失败')
    console.error('Failed to load conversations:', error)
  } finally {
    conversationLoading.value = false
  }
}

const resetConversationFilter = () => {
  conversationFilterForm.value = {
    search: '',
    user_id: undefined
  }
  conversationPagination.value.page = 1
  loadConversations()
}

const viewConversationDetails = async (conversation: Conversation) => {
  try {
    const detail = await adminConversationsApi.get(conversation.id)
    selectedConversation.value = detail
    showConversationDetailDialog.value = true
  } catch (error) {
    ElMessage.error('获取对话详情失败')
    console.error('Failed to get conversation details:', error)
  }
}

const deleteConversation = async (conversation: Conversation) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除对话 "${conversation.title}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await adminConversationsApi.delete(conversation.id)
    ElMessage.success('删除成功')
    loadConversations()
    loadConversationStats()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除对话失败')
      console.error('Failed to delete conversation:', error)
    }
  }
}

// ==================== 反馈管理 ====================

const loadFeedbackStats = async () => {
  try {
    feedbackStats.value = await adminFeedbackApi.getStats()
  } catch (error) {
    console.error('Failed to load feedback stats:', error)
  }
}

const loadFeedback = async () => {
  try {
    feedbackLoading.value = true
    const params: any = {
      skip: (feedbackPagination.value.page - 1) * feedbackPagination.value.limit,
      limit: feedbackPagination.value.limit
    }
    if (feedbackFilterForm.value.search) {
      params.search = feedbackFilterForm.value.search
    }
    if (feedbackFilterForm.value.feedback_type) {
      params.feedback_type = feedbackFilterForm.value.feedback_type
    }
    if (feedbackFilterForm.value.status) {
      params.status = feedbackFilterForm.value.status
    }
    if (feedbackFilterForm.value.user_id) {
      params.user_id = feedbackFilterForm.value.user_id
    }

    const response = await adminFeedbackApi.list(params)
    feedbacks.value = response.items
    feedbackPagination.value.total = response.total
  } catch (error) {
    ElMessage.error('加载反馈列表失败')
    console.error('Failed to load feedback:', error)
  } finally {
    feedbackLoading.value = false
  }
}

const resetFeedbackFilter = () => {
  feedbackFilterForm.value = {
    search: '',
    feedback_type: '',
    status: '',
    user_id: undefined
  }
  feedbackPagination.value.page = 1
  loadFeedback()
}

const viewFeedbackDetails = async (feedback: Feedback) => {
  try {
    const detail = await adminFeedbackApi.get(feedback.id)
    selectedFeedback.value = detail
    feedbackUpdateForm.value = {
      status: detail.status,
      admin_comment: detail.admin_comment || ''
    }
    showFeedbackDetailDialog.value = true
  } catch (error) {
    ElMessage.error('获取反馈详情失败')
    console.error('Failed to get feedback details:', error)
  }
}

const updateFeedback = async () => {
  if (!selectedFeedback.value) return
  
  try {
    await adminFeedbackApi.update(selectedFeedback.value.id, {
      status: feedbackUpdateForm.value.status as any,
      admin_comment: feedbackUpdateForm.value.admin_comment || undefined
    })
    ElMessage.success('更新成功')
    showFeedbackDetailDialog.value = false
    loadFeedback()
    loadFeedbackStats()
  } catch (error) {
    ElMessage.error('更新反馈失败')
    console.error('Failed to update feedback:', error)
  }
}

const getFeedbackTypeTag = (type: string): string => {
  const map: Record<string, string> = {
    bug: 'danger',
    feature: 'success',
    complaint: 'warning',
    other: 'info'
  }
  return map[type] || 'info'
}

const getFeedbackTypeText = (type: string): string => {
  const map: Record<string, string> = {
    bug: 'Bug',
    feature: '功能建议',
    complaint: '投诉',
    other: '其他'
  }
  return map[type] || type
}

const getFeedbackStatusType = (status: string): string => {
  const map: Record<string, string> = {
    pending: 'info',
    processing: 'warning',
    resolved: 'success',
    closed: 'danger'
  }
  return map[status] || 'info'
}

const getFeedbackStatusText = (status: string): string => {
  const map: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已解决',
    closed: '已关闭'
  }
  return map[status] || status
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

.tab-header {
  margin-bottom: 20px;
}

.tab-content {
  padding-top: 10px;
}
</style>
