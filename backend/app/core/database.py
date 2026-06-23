"""数据库连接管理"""

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# 创建数据库目录
os.makedirs(os.path.dirname(settings.database_url.split("///")[-1]), exist_ok=True)

# 创建异步引擎
engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
)

# 创建会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 声明基类
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
