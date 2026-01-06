import request from '@/utils/request'

export interface Feedback {
  id: number
  user_id: number
  feedback_type: 'bug' | 'feature' | 'complaint' | 'other'
  content: string
  status: 'pending' | 'processing' | 'resolved' | 'closed'
  admin_comment: string | null
  created_at: string
  updated_at: string
}

export interface FeedbackListResponse {
  total: number
  items: Feedback[]
}

export interface FeedbackCreate {
  feedback_type: 'bug' | 'feature' | 'complaint' | 'other'
  content: string
}

export interface FeedbackUpdate {
  status?: 'pending' | 'processing' | 'resolved' | 'closed'
  admin_comment?: string
}

export interface FeedbackListParams {
  skip?: number
  limit?: number
}

export interface AdminFeedbackListParams extends FeedbackListParams {
  search?: string
  user_id?: number
  feedback_type?: string
  status?: string
}

export interface FeedbackStats {
  total: number
  status_stats: Record<string, number>
  type_stats: Record<string, number>
  user_stats: Record<string, number>
}

export const feedbackApi = {
  // 提交反馈
  create(data: FeedbackCreate) {
    return request.post<Feedback>('/feedback', data)
  },

  // 获取当前用户的反馈列表
  list(params: FeedbackListParams = {}) {
    return request.get<FeedbackListResponse>('/feedback', { params })
  },

  // 获取反馈详情
  get(id: number) {
    return request.get<Feedback>(`/feedback/${id}`)
  }
}

// 管理员API
export const adminFeedbackApi = {
  // 管理员获取反馈列表
  list(params: AdminFeedbackListParams = {}) {
    return request.get<FeedbackListResponse>('/admin/feedback', { params })
  },

  // 管理员获取反馈详情
  get(id: number) {
    return request.get<Feedback>('/admin/feedback/' + id)
  },

  // 管理员更新反馈
  update(id: number, data: FeedbackUpdate) {
    return request.patch<Feedback>('/admin/feedback/' + id, data)
  },

  // 获取统计信息
  getStats() {
    return request.get<FeedbackStats>('/admin/feedback/stats')
  }
}
