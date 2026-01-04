import logging
import json
import mimetypes
from pathlib import Path
from typing import Dict, Optional, Any
import aiofiles

logger = logging.getLogger(__name__)


class FileRecognitionService:
    """文件识别服务"""
    
    # 支持的图片格式
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.ico'}
    
    # 支持的文档格式
    DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.md', '.rtf'}
    
    # 支持的其他格式
    OTHER_EXTENSIONS = {'.zip', '.rar', '.7z', '.tar', '.gz'}
    
    def __init__(self):
        self.all_supported_extensions = (
            self.IMAGE_EXTENSIONS | 
            self.DOCUMENT_EXTENSIONS | 
            self.OTHER_EXTENSIONS
        )
    
    async def recognize_file(
        self, 
        file_path: str, 
        file_type: str,
        file_extension: str
    ) -> Dict[str, Any]:
        """
        识别文件内容
        
        Args:
            file_path: 文件路径
            file_type: MIME类型
            file_extension: 文件扩展名
            
        Returns:
            识别结果字典
        """
        try:
            result = {
                "file_type": file_type,
                "file_extension": file_extension,
                "category": self._get_file_category(file_extension),
                "details": {}
            }
            
            # 根据文件类型进行不同的识别
            if file_extension.lower() in self.IMAGE_EXTENSIONS:
                result["details"] = await self._recognize_image(file_path)
            elif file_extension.lower() in self.DOCUMENT_EXTENSIONS:
                result["details"] = await self._recognize_document(file_path, file_extension)
            elif file_extension.lower() in self.OTHER_EXTENSIONS:
                result["details"] = await self._recognize_archive(file_path, file_extension)
            else:
                result["details"] = {
                    "message": "文件类型暂不支持详细识别",
                    "mime_type": file_type
                }
            
            # 获取文件的实际MIME类型（使用mimetypes）
            try:
                detected_mime, _ = mimetypes.guess_type(file_path)
                result["detected_mime_type"] = detected_mime or file_type
            except Exception as e:
                logger.warning(f"Failed to detect MIME type: {e}")
                result["detected_mime_type"] = file_type
            
            return result
            
        except Exception as e:
            logger.error(f"Error recognizing file {file_path}: {e}", exc_info=True)
            raise
    
    def _get_file_category(self, extension: str) -> str:
        """获取文件类别"""
        ext = extension.lower()
        if ext in self.IMAGE_EXTENSIONS:
            return "image"
        elif ext in self.DOCUMENT_EXTENSIONS:
            return "document"
        elif ext in self.OTHER_EXTENSIONS:
            return "archive"
        else:
            return "other"
    
    async def _recognize_image(self, file_path: str) -> Dict[str, Any]:
        """识别图片文件"""
        try:
            # 尝试使用PIL识别图片
            try:
                from PIL import Image
                with Image.open(file_path) as img:
                    return {
                        "format": img.format,
                        "mode": img.mode,
                        "size": {
                            "width": img.width,
                            "height": img.height
                        },
                        "has_transparency": img.mode in ('RGBA', 'LA', 'P') and 'transparency' in img.info,
                        "color_space": img.mode
                    }
            except ImportError:
                # 如果PIL未安装，返回基本信息
                file_size = Path(file_path).stat().st_size
                return {
                    "type": "image",
                    "file_size_bytes": file_size,
                    "message": "Pillow未安装，无法获取详细图片信息"
                }
        except Exception as e:
            logger.error(f"Error recognizing image: {e}")
            file_size = Path(file_path).stat().st_size
            return {
                "error": str(e),
                "file_size_bytes": file_size,
                "message": "无法识别图片信息"
            }
    
    async def _recognize_document(self, file_path: str, extension: str) -> Dict[str, Any]:
        """识别文档文件"""
        result = {
            "extension": extension,
            "type": "document"
        }
        
        # 对于文本文件，尝试读取内容预览
        if extension.lower() in {'.txt', '.md'}:
            try:
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    content = await f.read(1000)  # 读取前1000个字符
                    result["preview"] = content[:500]  # 只返回前500个字符
                    result["preview_length"] = len(content)
            except UnicodeDecodeError:
                result["encoding"] = "binary_or_unsupported_encoding"
            except Exception as e:
                logger.warning(f"Error reading text file: {e}")
                result["error"] = str(e)
        
        # 获取文件大小
        file_size = Path(file_path).stat().st_size
        result["file_size_bytes"] = file_size
        
        return result
    
    async def _recognize_archive(self, file_path: str, extension: str) -> Dict[str, Any]:
        """识别压缩文件"""
        file_size = Path(file_path).stat().st_size
        return {
            "extension": extension,
            "type": "archive",
            "file_size_bytes": file_size,
            "message": "压缩文件，需要解压后才能查看内容"
        }
    
    def is_supported(self, file_extension: str) -> bool:
        """检查文件扩展名是否支持"""
        return file_extension.lower() in self.all_supported_extensions


# 创建全局实例
file_recognition_service = FileRecognitionService()
