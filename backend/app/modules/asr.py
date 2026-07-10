"""ASR（语音识别）节点占位。"""

from typing import Any

from app.modules.base import PipelineNode


class ASRNode(PipelineNode):
    node_name = "asr"

    async def process(self, trace_id: str, input_data: Any) -> str:
        # TODO: 接入真实 ASR 服务
        return f"[asr stub] transcribed: {input_data}"
