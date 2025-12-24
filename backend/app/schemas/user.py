from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """创建用户模型"""
    password: str


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token模型"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token数据模型"""
    user_id: Optional[int] = None

