"""应用配置管理"""

import multiprocessing

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    database_url: str = "sqlite+aiosqlite:///./data/template.db"
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    host: str = "0.0.0.0"
    port: int = 8000
    worker_processes: int = multiprocessing.cpu_count() * 2 + 1
    task_pool_workers: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
