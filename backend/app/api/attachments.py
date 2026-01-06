import logging
import uuid
import json
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, delete
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.attachment import Attachment
from app.schemas.attachment import (
    AttachmentResponse,
    AttachmentListResponse,
    AttachmentUpdate,
    AttachmentCreate
)
from app.services.file_recognition_service import file_recognition_service
import aiofiles
import mimetypes

logger = logging.getLogger(__name__)

router = APIRouter()

# 允许的文件扩展名
ALLOWED_EXTENSIONS = set(settings.ALLOWED_EXTENSIONS.split(","))


def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return Path(filename).suffix.lower()


def is_allowed_file(filename: str) -> bool:
    """检查文件是否允许上传"""
    ext = get_file_extension(filename)
    return ext in ALLOWED_EXTENSIONS


def generate_stored_filename(original_filename: str) -> str:
    """生成存储的文件名"""
    ext = get_file_extension(original_filename)
    unique_id = str(uuid.uuid4())
    return f"{unique_id}{ext}"


@router.post("/attachments/upload", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    source: Optional[str] = Form("direct_upload"),
    is_shared: Optional[bool] = Form(False),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """上传附件"""
    try:
        # 检查文件扩展名
        if not is_allowed_file(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件类型。允许的类型: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # 读取文件内容
        file_content = await file.read()
        file_size = len(file_content)
        
        # 检查文件大小
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件大小超过限制（最大 {settings.MAX_FILE_SIZE / 1024 / 1024}MB）"
            )
        
        # 生成存储文件名
        stored_filename = generate_stored_filename(file.filename)
        file_path = Path(settings.UPLOAD_DIR) / stored_filename
        
        # 保存文件
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        
        logger.info(f"File saved: {file_path}, size: {file_size} bytes")
        
        # 获取文件MIME类型
        file_type, _ = mimetypes.guess_type(file.filename)
        if not file_type:
            file_type = file.content_type or "application/octet-stream"
        
        file_extension = get_file_extension(file.filename)
        
        # 创建附件记录
        attachment = Attachment(
            filename=file.filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_size=file_size,
            file_type=file_type,
            file_extension=file_extension,
            description=description,
            tags=tags,
            source=source or "direct_upload",
            is_shared=1 if is_shared else 0,
            user_id=current_user.id,
            recognition_status="pending"
        )
        
        db.add(attachment)
        await db.commit()
        await db.refresh(attachment)
        
        # 异步进行文件识别
        try:
            attachment.recognition_status = "processing"
            await db.commit()
            
            recognition_result = await file_recognition_service.recognize_file(
                str(file_path),
                file_type,
                file_extension
            )
            
            attachment.recognition_result = json.dumps(recognition_result, ensure_ascii=False)
            attachment.recognition_status = "completed"
            await db.commit()
            
            logger.info(f"File recognition completed for attachment {attachment.id}")
        except Exception as e:
            logger.error(f"File recognition failed: {e}", exc_info=True)
            attachment.recognition_status = "failed"
            attachment.recognition_error = str(e)
            await db.commit()
        
        await db.refresh(attachment)
        return attachment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )


@router.get("/attachments", response_model=AttachmentListResponse)
async def list_attachments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取附件列表（支持分页和搜索）"""
    try:
        query = select(Attachment)
        
        # 普通用户可以查看自己的文件和共享的文件
        # 管理员可以查看所有文件
        if current_user.is_admin:
            # 管理员可以查看所有文件，如果指定了user_id则过滤
            if user_id:
                query = query.where(Attachment.user_id == user_id)
        else:
            # 普通用户只能查看自己的文件或共享的文件
            query = query.where(
                or_(
                    Attachment.user_id == current_user.id,
                    Attachment.is_shared == 1
                )
            )
        
        # 搜索功能
        if search:
            query = query.where(
                or_(
                    Attachment.filename.contains(search),
                    Attachment.description.contains(search),
                    Attachment.tags.contains(search)
                )
            )
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据
        query = query.order_by(Attachment.created_at.desc())
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        attachments = result.scalars().all()
        
        return AttachmentListResponse(total=total, items=list(attachments))
        
    except Exception as e:
        logger.error(f"Error listing attachments: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取附件列表失败: {str(e)}"
        )


@router.get("/attachments/{attachment_id}", response_model=AttachmentResponse)
async def get_attachment(
    attachment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取附件详情"""
    result = await db.execute(
        select(Attachment).where(Attachment.id == attachment_id)
    )
    attachment = result.scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="附件不存在"
        )
    
    # 检查权限：可以查看自己的文件或共享的文件，管理员可以查看所有文件
    if not current_user.is_admin and attachment.user_id != current_user.id and attachment.is_shared != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此附件"
        )
    
    return attachment


@router.get("/attachments/{attachment_id}/download")
async def download_attachment(
    attachment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """下载附件"""
    result = await db.execute(
        select(Attachment).where(Attachment.id == attachment_id)
    )
    attachment = result.scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="附件不存在"
        )
    
    # 检查权限：可以下载自己的文件或共享的文件，管理员可以下载所有文件
    if not current_user.is_admin and attachment.user_id != current_user.id and attachment.is_shared != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权下载此附件"
        )
    
    file_path = Path(attachment.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )
    
    return FileResponse(
        path=str(file_path),
        filename=attachment.filename,
        media_type=attachment.file_type
    )


@router.patch("/attachments/{attachment_id}", response_model=AttachmentResponse)
async def update_attachment(
    attachment_id: int,
    update_data: AttachmentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新附件信息"""
    result = await db.execute(
        select(Attachment).where(Attachment.id == attachment_id)
    )
    attachment = result.scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="附件不存在"
        )
    
    # 检查权限
    if attachment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此附件"
        )
    
    # 更新字段
    if update_data.description is not None:
        attachment.description = update_data.description
    if update_data.tags is not None:
        attachment.tags = update_data.tags
    if update_data.is_shared is not None:
        attachment.is_shared = 1 if update_data.is_shared else 0
    
    await db.commit()
    await db.refresh(attachment)
    
    return attachment


@router.delete("/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
    attachment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除附件"""
    result = await db.execute(
        select(Attachment).where(Attachment.id == attachment_id)
    )
    attachment = result.scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="附件不存在"
        )
    
    # 检查权限
    if attachment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此附件"
        )
    
    # 删除文件
    file_path = Path(attachment.file_path)
    if file_path.exists():
        try:
            file_path.unlink()
            logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
    
    # 删除数据库记录
    await db.execute(delete(Attachment).where(Attachment.id == attachment_id))
    await db.commit()
    
    return
