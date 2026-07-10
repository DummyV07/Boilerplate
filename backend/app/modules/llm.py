"""LLM（大语言模型）节点占位。"""

from typing import Any

from app.modules.base import PipelineNode


class LLMNode(PipelineNode):
    node_name = "llm"

    async def process(self, trace_id: str, input_data: Any) -> str:
        # TODO: 接入真实 LLM 服务
        return f"[llm stub] response to: {input_data}"
