import logging
import aiohttp
from typing import List, Dict, Optional
from aiohttp import ClientError, ClientTimeout

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """AI服务（调用Ollama API）"""
    
    def __init__(self):
        self.api_url = settings.OLLAMA_API_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = ClientTimeout(total=300)  # 5分钟超时
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        生成AI响应
        
        Args:
            messages: 当前消息列表 [{"role": "user", "content": "..."}]
            conversation_history: 历史对话（可选）
        
        Returns:
            AI生成的响应文本
        """
        try:
            # 构建请求体
            all_messages = []
            if conversation_history:
                all_messages.extend(conversation_history)
            all_messages.extend(messages)
            
            payload = {
                "model": self.model,
                "messages": all_messages,
                "stream": False  # 非流式响应
            }
            
            url = f"{self.api_url}/api/chat"
            
            logger.info(f"Calling Ollama API: {url} with model {self.model}")
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        ai_response = result.get("message", {}).get("content", "")
                        logger.info(f"AI response received, length: {len(ai_response)}")
                        return ai_response
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama API error: {response.status} - {error_text}")
                        raise Exception(f"Ollama API error: {response.status}")
        
        except ClientError as e:
            logger.error(f"Network error calling Ollama API: {e}", exc_info=True)
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating AI response: {e}", exc_info=True)
            raise
    
    async def check_ollama_available(self) -> bool:
        """检查Ollama服务是否可用"""
        try:
            url = f"{self.api_url}/api/tags"
            async with aiohttp.ClientSession(timeout=ClientTimeout(total=5)) as session:
                async with session.get(url) as response:
                    return response.status == 200
        except Exception as e:
            logger.warning(f"Ollama service check failed: {e}")
            return False


# 创建全局实例
ai_service = AIService()

