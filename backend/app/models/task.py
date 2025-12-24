from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Task(Base):
    """任务模型（用于长任务处理）"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(String, unique=True, index=True, nullable=False)  # 唯一任务ID
    status = Column(String, nullable=False, default="pending")  # pending, processing, completed, failed
    result = Column(Text, nullable=True)  # 任务结果（JSON字符串）
    error_message = Column(Text, nullable=True)  # 错误信息
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="tasks")

