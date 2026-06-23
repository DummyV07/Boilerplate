"""Gunicorn 生产环境配置"""
import multiprocessing

from app.core.config import settings

bind = f"{settings.host}:{settings.port}"
workers = settings.worker_processes or multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = settings.log_level.lower()
