import os
from typing import Optional
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""
    
    # 数据库配置
    # MySQL 连接格式: mysql+asyncmy://用户名:密码@主机:端口/数据库名
    # 示例: mysql+asyncmy://root:password@localhost:3306/chat_db
    DATABASE_URL: str = "mysql+asyncmy://root:123456@localhost:3306/chat_db"
    
    # 数据库连接池配置
    DB_POOL_SIZE: int = 10  # 连接池大小
    DB_MAX_OVERFLOW: int = 20  # 连接池最大溢出数
    DB_POOL_RECYCLE: int = 3600  # 连接回收时间（秒）
    DB_ECHO: bool = False  # 是否打印 SQL 语句（开发时可设为 True）
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Ollama配置
    OLLAMA_API_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3:0.6b"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # 应用配置
    PROJECT_NAME: str = "AI Chat API"
    API_V1_STR: str = "/api"
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"  # 文件上传目录
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 最大文件大小（100MB）
    ALLOWED_EXTENSIONS: str = ".jpg,.jpeg,.png,.gif,.bmp,.webp,.pdf,.doc,.docx,.txt,.md,.zip,.rar,.7z"  # 允许的文件扩展名
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建日志目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 创建上传目录
settings = Settings()
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(exist_ok=True)

