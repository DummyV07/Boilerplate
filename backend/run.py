"""应用启动脚本"""
import uvicorn

from app.core.config import settings
from app.core.logging_config import logger

if __name__ == "__main__":
    logger.info(f"启动开发服务器: {settings.host}:{settings.port}")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
