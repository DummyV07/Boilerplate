from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskResponse(BaseModel):
    """任务响应模型"""
    id: int
    task_id: str
    status: str
    result: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskCreateResponse(BaseModel):
    """创建任务响应模型"""
    task_id: str
    status: str = "pending"

