import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate, ConversationResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户的所有对话"""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
    )
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
    
    return conversation_list


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建新对话"""
    new_conversation = Conversation(
        user_id=current_user.id,
        title=conversation_data.title
    )
    
    db.add(new_conversation)
    await db.commit()
    await db.refresh(new_conversation)
    
    logger.info(f"Conversation created: {new_conversation.id} by user {current_user.id}")
    
    return ConversationResponse(
        id=new_conversation.id,
        user_id=new_conversation.user_id,
        title=new_conversation.title,
        created_at=new_conversation.created_at,
        messages=[]
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取单个对话详情"""
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
    
    # 加载消息
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = messages_result.scalars().all()
    
    return ConversationResponse(
        id=conversation.id,
        user_id=conversation.user_id,
        title=conversation.title,
        created_at=conversation.created_at,
        messages=[{"id": m.id, "conversation_id": m.conversation_id, "role": m.role, "content": m.content, "created_at": m.created_at} for m in messages]
    )

