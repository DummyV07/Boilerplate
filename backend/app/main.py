import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.database import init_db
from app.api import auth, conversations, messages, tasks

# 配置日志
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # 关闭时清理资源
    logger.info("Shutting down...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 异常处理中间件
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# 注册路由
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(conversations.router, prefix=settings.API_V1_STR, tags=["conversations"])
app.include_router(messages.router, prefix=settings.API_V1_STR, tags=["messages"])
app.include_router(tasks.router, prefix=settings.API_V1_STR, tags=["tasks"])


@app.get("/")
async def root():
    """根路径"""
    return {"message": "AI Chat API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )

