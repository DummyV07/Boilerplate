from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FeedbackBase(BaseModel):
    """反馈基础Schema"""
    feedback_type: str = Field(..., description="反馈类型：bug, feature, complaint, other")
    content: str = Field(..., description="反馈内容", min_length=1)


class FeedbackCreate(FeedbackBase):
    """创建反馈Schema"""
    pass


class FeedbackUpdate(BaseModel):
    """更新反馈Schema（管理员使用）"""
    status: Optional[str] = Field(None, description="处理状态：pending, processing, resolved, closed")
    admin_comment: Optional[str] = Field(None, description="管理员回复")


class FeedbackResponse(FeedbackBase):
    """反馈响应Schema"""
    id: int
    user_id: int
    status: str
    admin_comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackListResponse(BaseModel):
    """反馈列表响应Schema"""
    total: int
    items: list[FeedbackResponse]
