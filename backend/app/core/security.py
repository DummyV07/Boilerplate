import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.core.database import get_db

logger = logging.getLogger(__name__)


# OAuth2 token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def _prepare_password(password: str) -> bytes:
    """准备密码字节，处理 bcrypt 的 72 字节限制"""
    password_bytes = password.encode('utf-8')
    # bcrypt 限制密码长度为 72 字节
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    return password_bytes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        password_bytes = _prepare_password(plain_password)
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    password_bytes = _prepare_password(password)
    # 生成盐并哈希密码
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # jose库会自动将datetime转换为timestamp
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.debug(f"Created access token for user_id: {data.get('sub')}")
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户（依赖注入）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_raw = payload.get("sub")
        if user_id_raw is None:
            logger.warning("Token missing 'sub' field")
            raise credentials_exception
        
        # 确保user_id是整数类型
        try:
            user_id = int(user_id_raw)
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid user_id type: {user_id_raw}, error: {e}")
            raise credentials_exception
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {e}")
        raise credentials_exception
    
    # 从数据库获取用户
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user

