<template>
  <div class="feedback-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户反馈</span>
        </div>
      </template>

      <el-form :model="feedbackForm" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="反馈类型" prop="feedback_type">
          <el-select v-model="feedbackForm.feedback_type" placeholder="请选择反馈类型" style="width: 100%">
            <el-option label="Bug报告" value="bug" />
            <el-option label="功能建议" value="feature" />
            <el-option label="投诉" value="complaint" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>

        <el-form-item label="反馈内容" prop="content">
          <el-input
            v-model="feedbackForm.content"
            type="textarea"
            :rows="8"
            placeholder="请详细描述您的反馈内容..."
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitFeedback" :loading="submitting">
            提交反馈
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 我的反馈列表 -->
      <el-divider>我的反馈</el-divider>
      
      <el-table
        v-loading="loading"
        :data="myFeedbacks"
        stripe
        style="width: 100%"
        empty-text="暂无反馈记录"
      >
        <el-table-column prop="id" label="ID" width="80" />
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
        <el-table-column prop="admin_comment" label="管理员回复" min-width="200" show-overflow-tooltip />
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="viewFeedback(row)"
            >
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.limit"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadMyFeedbacks"
          @current-change="loadMyFeedbacks"
        />
      </div>
    </el-card>

    <!-- 反馈详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="反馈详情"
      width="700px"
    >
      <div v-if="selectedFeedback" class="detail-content">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="反馈类型">
            <el-tag :type="getFeedbackTypeTag(selectedFeedback.feedback_type)">
              {{ getFeedbackTypeText(selectedFeedback.feedback_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="反馈内容">
            {{ selectedFeedback.content }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getFeedbackStatusType(selectedFeedback.status)">
              {{ getFeedbackStatusText(selectedFeedback.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="管理员回复" v-if="selectedFeedback.admin_comment">
            {{ selectedFeedback.admin_comment }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ formatDate(selectedFeedback.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">
            {{ formatDate(selectedFeedback.updated_at) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { feedbackApi, type Feedback, type FeedbackCreate } from '@/api/feedback'

const formRef = ref<FormInstance>()
const loading = ref(false)
const submitting = ref(false)
const showDetailDialog = ref(false)
const selectedFeedback = ref<Feedback | null>(null)
const myFeedbacks = ref<Feedback[]>([])

const feedbackForm = ref<FeedbackCreate>({
  feedback_type: 'other',
  content: ''
})

const rules: FormRules = {
  feedback_type: [
    { required: true, message: '请选择反馈类型', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入反馈内容', trigger: 'blur' },
    { min: 10, message: '反馈内容至少10个字符', trigger: 'blur' }
  ]
}

const pagination = ref({
  page: 1,
  limit: 10,
  total: 0
})

onMounted(() => {
  loadMyFeedbacks()
})

const submitFeedback = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitting.value = true
        await feedbackApi.create(feedbackForm.value)
        ElMessage.success('反馈提交成功，感谢您的反馈！')
        resetForm()
        loadMyFeedbacks()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '提交失败，请重试')
      } finally {
        submitting.value = false
      }
    }
  })
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  feedbackForm.value = {
    feedback_type: 'other',
    content: ''
  }
}

const loadMyFeedbacks = async () => {
  try {
    loading.value = true
    const response = await feedbackApi.list({
      skip: (pagination.value.page - 1) * pagination.value.limit,
      limit: pagination.value.limit
    })
    myFeedbacks.value = response.items
    pagination.value.total = response.total
  } catch (error) {
    ElMessage.error('加载反馈列表失败')
    console.error('Failed to load feedback:', error)
  } finally {
    loading.value = false
  }
}

const viewFeedback = async (feedback: Feedback) => {
  try {
    const detail = await feedbackApi.get(feedback.id)
    selectedFeedback.value = detail
    showDetailDialog.value = true
  } catch (error) {
    ElMessage.error('获取反馈详情失败')
    console.error('Failed to get feedback details:', error)
  }
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString('zh-CN')
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
.feedback-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
</style>
