import os
from typing import Optional
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./chat.db"
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建日志目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

settings = Settings()

