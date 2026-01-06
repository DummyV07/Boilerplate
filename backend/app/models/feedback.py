from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Feedback(Base):
    """用户反馈模型"""
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    feedback_type = Column(String(50), nullable=False, comment="反馈类型：bug, feature, complaint, other")
    content = Column(Text, nullable=False, comment="反馈内容")
    status = Column(String(20), default="pending", nullable=False, comment="处理状态：pending, processing, resolved, closed")
    admin_comment = Column(Text, nullable=True, comment="管理员回复")
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="feedbacks")
