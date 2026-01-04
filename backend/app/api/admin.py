import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.attachment import Attachment
from app.schemas.attachment import AttachmentResponse, AttachmentListResponse

logger = logging.getLogger(__name__)

router = APIRouter()


def is_admin(user: User) -> bool:
    """检查用户是否为管理员（可以根据需要扩展）"""
    # 这里简化处理，可以根据实际需求添加管理员字段或角色系统
    # 暂时返回False，需要时可以扩展
    return False


@router.get("/admin/attachments", response_model=AttachmentListResponse)
async def admin_list_attachments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    file_type: Optional[str] = Query(None),
    recognition_status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员获取所有附件列表（完整信息）"""
    # 注意：这里简化处理，实际应该检查管理员权限
    # 暂时允许所有登录用户访问，生产环境需要添加权限检查
    
    try:
        query = select(Attachment).options(selectinload(Attachment.user))
        
        # 按用户ID过滤
        if user_id:
            query = query.where(Attachment.user_id == user_id)
        
        # 按文件类型过滤
        if file_type:
            query = query.where(Attachment.file_type.contains(file_type))
        
        # 按识别状态过滤
        if recognition_status:
            query = query.where(Attachment.recognition_status == recognition_status)
        
        # 搜索功能
        if search:
            query = query.where(
                or_(
                    Attachment.filename.contains(search),
                    Attachment.description.contains(search),
                    Attachment.tags.contains(search),
                    Attachment.stored_filename.contains(search)
                )
            )
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据，按创建时间倒序
        query = query.order_by(desc(Attachment.created_at))
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        attachments = result.scalars().all()
        
        return AttachmentListResponse(total=total, items=list(attachments))
        
    except Exception as e:
        logger.error(f"Error listing attachments in admin: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取附件列表失败: {str(e)}"
        )


@router.get("/admin/attachments/{attachment_id}", response_model=AttachmentResponse)
async def admin_get_attachment(
    attachment_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员获取附件详情（完整信息）"""
    result = await db.execute(
        select(Attachment).options(selectinload(Attachment.user)).where(Attachment.id == attachment_id)
    )
    attachment = result.scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="附件不存在"
        )
    
    return attachment


@router.get("/admin/attachments/stats")
async def admin_attachments_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取附件统计信息"""
    try:
        # 总文件数
        total_result = await db.execute(select(func.count(Attachment.id)))
        total = total_result.scalar()
        
        # 按识别状态统计
        status_result = await db.execute(
            select(Attachment.recognition_status, func.count(Attachment.id))
            .group_by(Attachment.recognition_status)
        )
        status_stats = {row[0]: row[1] for row in status_result.all()}
        
        # 按文件类型统计（前10个）
        type_result = await db.execute(
            select(Attachment.file_type, func.count(Attachment.id))
            .group_by(Attachment.file_type)
            .order_by(desc(func.count(Attachment.id)))
            .limit(10)
        )
        type_stats = {row[0]: row[1] for row in type_result.all()}
        
        # 总文件大小
        size_result = await db.execute(select(func.sum(Attachment.file_size)))
        total_size = size_result.scalar() or 0
        
        # 按用户统计（前10个）
        user_result = await db.execute(
            select(Attachment.user_id, func.count(Attachment.id))
            .group_by(Attachment.user_id)
            .order_by(desc(func.count(Attachment.id)))
            .limit(10)
        )
        user_stats = {str(row[0]): row[1] for row in user_result.all()}
        
        return {
            "total": total,
            "total_size": total_size,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "status_stats": status_stats,
            "type_stats": type_stats,
            "user_stats": user_stats
        }
        
    except Exception as e:
        logger.error(f"Error getting attachment stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计信息失败: {str(e)}"
        )
