import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.schemas.message import MessageCreate
from app.schemas.task import TaskCreateResponse
from app.services.task_service import task_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/conversations/{conversation_id}/messages", status_code=status.HTTP_202_ACCEPTED)
async def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发送消息（异步处理，立即返回202）
    
    如果AI响应时间超过2秒，返回202 Accepted和task_id，由前端轮询获取结果
    """
    # 验证对话是否存在且属于当前用户
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # 创建任务并立即返回task_id
    task_id = await task_service.create_task(
        db=db,
        user_id=current_user.id,
        conversation_id=conversation_id,
        user_message=message_data.content
    )
    
    logger.info(f"Message task created: {task_id} for conversation {conversation_id}")
    
    # 返回202 Accepted和task_id
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "task_id": task_id,
            "status": "pending",
            "message": "Message is being processed"
        }
    )

