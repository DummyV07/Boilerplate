"""FastAPI 应用入口"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import items, tasks
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging_config import logger
from app.workers.task_pool import TaskPool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：初始化数据库与进程池。"""
    task_pool = TaskPool(num_workers=settings.task_pool_workers)
    task_pool.start()
    app.state.task_pool = task_pool

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Fullstack template backend started")

    yield

    task_pool.shutdown()
    logger.info("Fullstack template backend stopped")


app = FastAPI(
    title="Fullstack Template API",
    description="FastAPI + Vue 3 全栈项目模版",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
