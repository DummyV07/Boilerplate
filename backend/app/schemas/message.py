from datetime import datetime
from pydantic import BaseModel


class MessageBase(BaseModel):
    """消息基础模型"""
    role: str  # "user" or "assistant"
    content: str


class MessageCreate(MessageBase):
    """创建消息模型"""
    pass


class MessageResponse(MessageBase):
    """消息响应模型"""
    id: int
    conversation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

