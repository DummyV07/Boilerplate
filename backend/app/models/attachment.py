from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, BigInteger, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Attachment(Base):
    """附件模型"""
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False, comment="原始文件名")
    stored_filename = Column(String(255), nullable=False, unique=True, comment="存储的文件名")
    file_path = Column(String(500), nullable=False, comment="文件存储路径")
    file_size = Column(BigInteger, nullable=False, comment="文件大小（字节）")
    file_type = Column(String(100), nullable=False, comment="文件MIME类型")
    file_extension = Column(String(20), nullable=False, comment="文件扩展名")
    
    # 文件识别信息
    recognition_result = Column(Text, nullable=True, comment="文件识别结果（JSON格式）")
    recognition_status = Column(String(20), default="pending", nullable=False, comment="识别状态：pending, processing, completed, failed")
    recognition_error = Column(Text, nullable=True, comment="识别错误信息")
    
    # 文件元信息
    description = Column(Text, nullable=True, comment="文件描述")
    tags = Column(String(500), nullable=True, comment="文件标签（逗号分隔）")
    
    # 文件来源和权限
    source = Column(String(50), default="direct_upload", nullable=False, comment="文件来源：chat, admin, api, direct_upload")
    is_shared = Column(Integer, default=0, nullable=False, comment="是否共享：0-不共享，1-共享")
    
    # 用户关联
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="上传用户ID")
    
    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), nullable=False, comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="attachments")
