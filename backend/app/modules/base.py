"""AI 流水线节点基类与占位实现。"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any

from app.core.pipeline_trace import record_stage


class PipelineNode(ABC):
    """AI 处理节点基类，子类实现 process() 并自动记录链路追踪。"""

    node_name: str

    @abstractmethod
    async def process(self, trace_id: str, input_data: Any) -> Any:
        """处理输入并返回输出。"""

    async def run(self, trace_id: str, input_data: Any) -> Any:
        record_stage(
            trace_id,
            node=self.node_name,
            stage="input",
            summary=_summarize(input_data),
        )
        start = time.perf_counter()
        try:
            output = await self.process(trace_id, input_data)
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            record_stage(
                trace_id,
                node=self.node_name,
                stage="error",
                summary=str(exc),
                duration_ms=elapsed_ms,
            )
            raise
        elapsed_ms = (time.perf_counter() - start) * 1000
        record_stage(
            trace_id,
            node=self.node_name,
            stage="output",
            summary=_summarize(output),
            duration_ms=elapsed_ms,
        )
        return output


def _summarize(data: Any, max_len: int = 200) -> str:
    text = str(data)
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text
