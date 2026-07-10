"""AI 流水线节点包。"""

from app.modules.asr import ASRNode
from app.modules.llm import LLMNode
from app.modules.tts import TTSNode

KNOWN_NODES: tuple[str, ...] = ("asr", "llm", "tts")

__all__ = ["ASRNode", "LLMNode", "TTSNode", "KNOWN_NODES"]
