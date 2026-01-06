from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AttachmentBase(BaseModel):
    """附件基础Schema"""
    description: Optional[str] = Field(None, description="文件描述")
    tags: Optional[str] = Field(None, description="文件标签（逗号分隔）")
    source: Optional[str] = Field("direct_upload", description="文件来源：chat, admin, api, direct_upload")
    is_shared: Optional[bool] = Field(False, description="是否共享")


class AttachmentCreate(AttachmentBase):
    """创建附件Schema"""
    pass


class AttachmentResponse(AttachmentBase):
    """附件响应Schema"""
    id: int
    filename: str
    stored_filename: str
    file_path: str
    file_size: int
    file_type: str
    file_extension: str
    recognition_result: Optional[str] = None
    recognition_status: str
    recognition_error: Optional[str] = None
    user_id: int
    source: str
    is_shared: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AttachmentListResponse(BaseModel):
    """附件列表响应Schema"""
    total: int
    items: list[AttachmentResponse]


class AttachmentUpdate(BaseModel):
    """更新附件Schema"""
    description: Optional[str] = None
    tags: Optional[str] = None
    is_shared: Optional[bool] = None
