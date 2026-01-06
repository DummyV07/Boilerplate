import request from '@/utils/request'
import axios from 'axios'

export interface Attachment {
  id: number
  filename: string
  stored_filename: string
  file_path: string
  file_size: number
  file_type: string
  file_extension: string
  recognition_result: string | null
  recognition_status: 'pending' | 'processing' | 'completed' | 'failed'
  recognition_error: string | null
  description: string | null
  tags: string | null
  source: string
  is_shared: boolean
  user_id: number
  created_at: string
  updated_at: string
}

export interface AttachmentListResponse {
  total: number
  items: Attachment[]
}

export interface UploadAttachmentParams {
  file: File
  description?: string
  tags?: string
}

export interface AttachmentUpdate {
  description?: string
  tags?: string
  is_shared?: boolean
}

export interface AttachmentListParams {
  skip?: number
  limit?: number
  search?: string
  user_id?: number
}

// 获取基础URL
const getBaseURL = () => {
  if (import.meta.env.DEV) {
    return '/api'
  }
  return import.meta.env.VITE_API_BASE_URL || '/api'
}

export const attachmentsApi = {
  // 上传附件
  async upload(params: UploadAttachmentParams): Promise<Attachment> {
    const formData = new FormData()
    formData.append('file', params.file)
    if (params.description) {
      formData.append('description', params.description)
    }
    if (params.tags) {
      formData.append('tags', params.tags)
    }

    const token = localStorage.getItem('token')
    const response = await axios.post(`${getBaseURL()}/attachments/upload`, formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // 获取附件列表
  list(params: AttachmentListParams = {}) {
    return request.get<AttachmentListResponse>('/attachments', { params })
  },

  // 获取附件详情
  get(id: number) {
    return request.get<Attachment>(`/attachments/${id}`)
  },

  // 下载附件
  async download(id: number): Promise<Blob> {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${getBaseURL()}/attachments/${id}/download`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      responseType: 'blob'
    })
    return response.data
  },

  // 更新附件
  update(id: number, data: AttachmentUpdate) {
    return request.patch<Attachment>(`/attachments/${id}`, data)
  },

  // 删除附件
  delete(id: number) {
    return request.delete(`/attachments/${id}`)
  }
}

// 管理员API
export interface AdminAttachmentListParams extends AttachmentListParams {
  file_type?: string
  recognition_status?: string
}

export interface AttachmentStats {
  total: number
  total_size: number
  total_size_mb: number
  status_stats: Record<string, number>
  type_stats: Record<string, number>
  user_stats: Record<string, number>
}

export const adminAttachmentsApi = {
  // 管理员获取附件列表
  list(params: AdminAttachmentListParams = {}) {
    return request.get<AttachmentListResponse>('/admin/attachments', { params })
  },

  // 管理员获取附件详情
  get(id: number) {
    return request.get<Attachment>('/admin/attachments/' + id)
  },

  // 获取统计信息
  getStats() {
    return request.get<AttachmentStats>('/admin/attachments/stats')
  }
}
