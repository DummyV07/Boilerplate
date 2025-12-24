from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.message import MessageResponse


class ConversationBase(BaseModel):
    """对话基础模型"""
    title: str


class ConversationCreate(ConversationBase):
    """创建对话模型"""
    pass


class ConversationResponse(ConversationBase):
    """对话响应模型"""
    id: int
    user_id: int
    created_at: datetime
    messages: Optional[List[MessageResponse]] = []
    
    class Config:
        from_attributes = True

