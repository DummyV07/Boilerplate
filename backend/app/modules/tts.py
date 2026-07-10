"""TTS（语音合成）节点占位。"""

from typing import Any

from app.modules.base import PipelineNode


class TTSNode(PipelineNode):
    node_name = "tts"

    async def process(self, trace_id: str, input_data: Any) -> str:
        # TODO: 接入真实 TTS 服务
        return f"[tts stub] audio for: {input_data}"
