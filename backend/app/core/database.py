from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings


# 创建异步引擎（针对 MySQL 优化）
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # 是否打印 SQL
    future=True,
    pool_size=settings.DB_POOL_SIZE,  # 连接池大小
    max_overflow=settings.DB_MAX_OVERFLOW,  # 最大溢出连接数
    pool_recycle=settings.DB_POOL_RECYCLE,  # 连接回收时间
    pool_pre_ping=True,  # 连接前检查连接是否有效（MySQL 推荐）
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 声明基类
Base = declarative_base()


async def get_db() -> AsyncSession:
    """数据库会话依赖注入"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """初始化数据库（创建表）"""
    # 导入所有模型以确保它们被注册到Base.metadata
    from app.models import User, Conversation, Message, Task, Attachment, Feedback
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

