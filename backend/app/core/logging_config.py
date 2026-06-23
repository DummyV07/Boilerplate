"""日志配置"""

import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings

# 创建日志目录
log_dir = Path(settings.log_file).parent
log_dir.mkdir(parents=True, exist_ok=True)

# 移除默认处理器
logger.remove()

CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 添加控制台输出
logger.add(
    sys.stderr,
    format=CONSOLE_FORMAT,
    level=settings.log_level,
    colorize=True,
)

# 添加文件输出（按大小轮转）
logger.add(
    settings.log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=settings.log_level,
    rotation="100 MB",
    retention="10 days",
    compression="zip",
    encoding="utf-8",
)
