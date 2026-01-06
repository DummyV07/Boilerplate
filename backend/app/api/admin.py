import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, delete
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user, get_admin_user
from app.models.user import User
from app.models.attachment import Attachment
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.feedback import Feedback
from app.schemas.attachment import AttachmentResponse, AttachmentListResponse
from app.schemas.conversation import ConversationResponse
from app.schemas.feedback import FeedbackResponse, FeedbackListResponse, FeedbackUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/admin/attachments", response_model=AttachmentListResponse)
async def admin_list_attachments(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    file_type: Optional[str] = Query(None),
    recognition_status: Optional[str] = Query(None),
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员获取所有附件列表（完整信息）"""
    
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
    current_user: User = Depends(get_admin_user),
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
    current_user: User = Depends(get_admin_user),
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


# ==================== 聊天记录管理 ====================

@router.get("/admin/conversations")
async def admin_list_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员获取所有对话列表"""
    try:
        query = select(Conversation).options(selectinload(Conversation.user))
        
        # 按用户ID过滤
        if user_id:
            query = query.where(Conversation.user_id == user_id)
        
        # 搜索功能
        if search:
            query = query.where(Conversation.title.contains(search))
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据，按创建时间倒序
        query = query.order_by(desc(Conversation.created_at))
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        conversations = result.scalars().all()
        
        # 加载消息
        conversation_list = []
        for conv in conversations:
            messages_result = await db.execute(
                select(Message)
                .where(Message.conversation_id == conv.id)
                .order_by(Message.created_at)
            )
            messages = messages_result.scalars().all()
            
            conv_dict = {
                "id": conv.id,
                "user_id": conv.user_id,
                "title": conv.title,
                "created_at": conv.created_at,
                "messages": [{"id": m.id, "conversation_id": m.conversation_id, "role": m.role, "content": m.content, "created_at": m.created_at} for m in messages]
            }
            conversation_list.append(conv_dict)
        
        return {"total": total, "items": conversation_list}
        
    except Exception as e:
        logger.error(f"Error listing conversations in admin: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取对话列表失败: {str(e)}"
        )


@router.get("/admin/conversations/{conversation_id}")
async def admin_get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员获取对话详情"""
    result = await db.execute(
        select(Conversation).options(selectinload(Conversation.user)).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )
    
    # 加载消息
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = messages_result.scalars().all()
    
    return {
        "id": conversation.id,
        "user_id": conversation.user_id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "messages": [{"id": m.id, "conversation_id": m.conversation_id, "role": m.role, "content": m.content, "created_at": m.created_at} for m in messages]
    }


@router.delete("/admin/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员删除对话"""
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="对话不存在"
        )
    
    # 删除对话（关联的消息会级联删除）
    await db.execute(delete(Conversation).where(Conversation.id == conversation_id))
    await db.commit()
    
    logger.info(f"Conversation {conversation_id} deleted by admin {current_user.id}")


@router.get("/admin/conversations/stats")
async def admin_conversations_stats(
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """获取对话统计信息"""
    try:
        # 总对话数
        total_result = await db.execute(select(func.count(Conversation.id)))
        total = total_result.scalar()
        
        # 总消息数
        message_result = await db.execute(select(func.count(Message.id)))
        total_messages = message_result.scalar()
        
        # 按用户统计（前10个）
        user_result = await db.execute(
            select(Conversation.user_id, func.count(Conversation.id))
            .group_by(Conversation.user_id)
            .order_by(desc(func.count(Conversation.id)))
            .limit(10)
        )
        user_stats = {str(row[0]): row[1] for row in user_result.all()}
        
        return {
            "total": total,
            "total_messages": total_messages,
            "user_stats": user_stats
        }
        
    except Exception as e:
        logger.error(f"Error getting conversation stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计信息失败: {str(e)}"
        )


# ==================== 反馈管理 ====================

@router.get("/admin/feedback", response_model=FeedbackListResponse)
async def admin_list_feedback(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    feedback_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员获取所有反馈列表"""
    try:
        query = select(Feedback).options(selectinload(Feedback.user))
        
        # 按用户ID过滤
        if user_id:
            query = query.where(Feedback.user_id == user_id)
        
        # 按反馈类型过滤
        if feedback_type:
            query = query.where(Feedback.feedback_type == feedback_type)
        
        # 按状态过滤
        if status:
            query = query.where(Feedback.status == status)
        
        # 搜索功能
        if search:
            query = query.where(Feedback.content.contains(search))
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据，按创建时间倒序
        query = query.order_by(desc(Feedback.created_at))
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        feedbacks = result.scalars().all()
        
        return FeedbackListResponse(total=total, items=list(feedbacks))
        
    except Exception as e:
        logger.error(f"Error listing feedback in admin: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取反馈列表失败: {str(e)}"
        )


@router.get("/admin/feedback/{feedback_id}", response_model=FeedbackResponse)
async def admin_get_feedback(
    feedback_id: int,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员获取反馈详情"""
    result = await db.execute(
        select(Feedback).options(selectinload(Feedback.user)).where(Feedback.id == feedback_id)
    )
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    return feedback


@router.patch("/admin/feedback/{feedback_id}", response_model=FeedbackResponse)
async def admin_update_feedback(
    feedback_id: int,
    update_data: FeedbackUpdate,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """管理员更新反馈（更新状态和添加回复）"""
    result = await db.execute(
        select(Feedback).where(Feedback.id == feedback_id)
    )
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    # 更新字段
    if update_data.status is not None:
        feedback.status = update_data.status
    if update_data.admin_comment is not None:
        feedback.admin_comment = update_data.admin_comment
    
    await db.commit()
    await db.refresh(feedback)
    
    logger.info(f"Feedback {feedback_id} updated by admin {current_user.id}")
    return feedback


@router.get("/admin/feedback/stats")
async def admin_feedback_stats(
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """获取反馈统计信息"""
    try:
        # 总反馈数
        total_result = await db.execute(select(func.count(Feedback.id)))
        total = total_result.scalar()
        
        # 按状态统计
        status_result = await db.execute(
            select(Feedback.status, func.count(Feedback.id))
            .group_by(Feedback.status)
        )
        status_stats = {row[0]: row[1] for row in status_result.all()}
        
        # 按类型统计
        type_result = await db.execute(
            select(Feedback.feedback_type, func.count(Feedback.id))
            .group_by(Feedback.feedback_type)
        )
        type_stats = {row[0]: row[1] for row in type_result.all()}
        
        # 按用户统计（前10个）
        user_result = await db.execute(
            select(Feedback.user_id, func.count(Feedback.id))
            .group_by(Feedback.user_id)
            .order_by(desc(func.count(Feedback.id)))
            .limit(10)
        )
        user_stats = {str(row[0]): row[1] for row in user_result.all()}
        
        return {
            "total": total,
            "status_stats": status_stats,
            "type_stats": type_stats,
            "user_stats": user_stats
        }
        
    except Exception as e:
        logger.error(f"Error getting feedback stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计信息失败: {str(e)}"
        )
