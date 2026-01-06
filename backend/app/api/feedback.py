import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.feedback import Feedback
from app.schemas.feedback import (
    FeedbackCreate,
    FeedbackResponse,
    FeedbackListResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/feedback", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """提交反馈"""
    try:
        feedback = Feedback(
            user_id=current_user.id,
            feedback_type=feedback_data.feedback_type,
            content=feedback_data.content,
            status="pending"
        )
        
        db.add(feedback)
        await db.commit()
        await db.refresh(feedback)
        
        logger.info(f"Feedback created: {feedback.id} by user {current_user.id}")
        return feedback
        
    except Exception as e:
        logger.error(f"Error creating feedback: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"提交反馈失败: {str(e)}"
        )


@router.get("/feedback", response_model=FeedbackListResponse)
async def list_feedback(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的反馈列表"""
    try:
        query = select(Feedback).where(Feedback.user_id == current_user.id)
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # 获取分页数据
        query = query.order_by(desc(Feedback.created_at))
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        feedbacks = result.scalars().all()
        
        return FeedbackListResponse(total=total, items=list(feedbacks))
        
    except Exception as e:
        logger.error(f"Error listing feedback: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取反馈列表失败: {str(e)}"
        )


@router.get("/feedback/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取反馈详情（只能查看自己的）"""
    result = await db.execute(
        select(Feedback).where(Feedback.id == feedback_id)
    )
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="反馈不存在"
        )
    
    # 检查权限：只能查看自己的反馈
    if feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此反馈"
        )
    
    return feedback
