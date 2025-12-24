import asyncio
import logging
import uuid
import json
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from app.models.message import Message
from app.models.conversation import Conversation
from app.services.ai_service import ai_service

logger = logging.getLogger(__name__)


class TaskService:
    """任务服务（处理长任务）"""
    
    @staticmethod
    async def create_task(
        db: AsyncSession,
        user_id: int,
        conversation_id: int,
        user_message: str
    ) -> str:
        """
        创建任务并立即返回task_id
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            conversation_id: 对话ID
            user_message: 用户消息
        
        Returns:
            task_id: 任务ID
        """
        # 生成唯一任务ID
        task_id = str(uuid.uuid4())
        
        # 创建任务记录
        task = Task(
            user_id=user_id,
            task_id=task_id,
            status="pending",
            result=None
        )
        
        db.add(task)
        await db.commit()
        await db.refresh(task)
        
        logger.info(f"Task created: {task_id} for user {user_id}")
        
        # 后台异步执行任务
        asyncio.create_task(
            TaskService._execute_task(db, task_id, conversation_id, user_message)
        )
        
        return task_id
    
    @staticmethod
    async def _execute_task(
        db: AsyncSession,
        task_id: str,
        conversation_id: int,
        user_message: str
    ):
        """
        后台执行任务（异步）
        
        Args:
            db: 数据库会话（注意：这个会话会在函数开始时关闭，需要创建新会话）
            task_id: 任务ID
            conversation_id: 对话ID
            user_message: 用户消息
        """
        # 创建新的数据库会话（因为原会话可能已关闭）
        from app.core.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as new_db:
            try:
                # 更新任务状态为processing
                result = await new_db.execute(select(Task).where(Task.task_id == task_id))
                task = result.scalar_one_or_none()
                
                if not task:
                    logger.error(f"Task not found: {task_id}")
                    return
                
                task.status = "processing"
                await new_db.commit()
                
                logger.info(f"Task {task_id} started processing")
                
                # 获取对话历史
                conversation_result = await new_db.execute(
                    select(Conversation).where(Conversation.id == conversation_id)
                )
                conversation = conversation_result.scalar_one_or_none()
                
                if not conversation:
                    raise Exception(f"Conversation {conversation_id} not found")
                
                # 获取历史消息
                messages_result = await new_db.execute(
                    select(Message)
                    .where(Message.conversation_id == conversation_id)
                    .order_by(Message.created_at)
                )
                history_messages = messages_result.scalars().all()
                
                # 构建历史对话格式
                conversation_history = []
                for msg in history_messages:
                    conversation_history.append({
                        "role": msg.role,
                        "content": msg.content
                    })
                
                # 保存用户消息
                user_msg = Message(
                    conversation_id=conversation_id,
                    role="user",
                    content=user_message
                )
                new_db.add(user_msg)
                await new_db.commit()
                
                # 调用AI服务
                ai_response = await ai_service.generate_response(
                    messages=[{"role": "user", "content": user_message}],
                    conversation_history=conversation_history if conversation_history else None
                )
                
                # 保存AI响应
                assistant_msg = Message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=ai_response
                )
                new_db.add(assistant_msg)
                
                # 更新任务状态为completed
                task.status = "completed"
                task.result = json.dumps({
                    "message_id": assistant_msg.id,
                    "content": ai_response
                })
                await new_db.commit()
                
                logger.info(f"Task {task_id} completed successfully")
            
            except Exception as e:
                logger.error(f"Task {task_id} failed: {e}", exc_info=True)
                
                # 更新任务状态为failed
                try:
                    result = await new_db.execute(select(Task).where(Task.task_id == task_id))
                    task = result.scalar_one_or_none()
                    if task:
                        task.status = "failed"
                        task.error_message = str(e)
                        await new_db.commit()
                except Exception as commit_error:
                    logger.error(f"Failed to update task status: {commit_error}", exc_info=True)
    
    @staticmethod
    async def get_task_status(
        db: AsyncSession,
        task_id: str,
        user_id: int
    ) -> Optional[Task]:
        """
        获取任务状态
        
        Args:
            db: 数据库会话
            task_id: 任务ID
            user_id: 用户ID（用于验证权限）
        
        Returns:
            Task对象或None
        """
        result = await db.execute(
            select(Task).where(
                Task.task_id == task_id,
                Task.user_id == user_id
            )
        )
        return result.scalar_one_or_none()


# 创建全局实例
task_service = TaskService()

