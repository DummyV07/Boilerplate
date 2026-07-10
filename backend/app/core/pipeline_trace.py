"""AI 流水线链路追踪（模版级内存存储，后期可换 Redis/DB）。"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

_trace_store: dict[str, list[TraceStageRecord]] = {}


@dataclass
class TraceStageRecord:
    node: str
    stage: str
    summary: str
    duration_ms: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def generate_trace_id() -> str:
    return uuid.uuid4().hex[:16]


def record_stage(
    trace_id: str,
    *,
    node: str,
    stage: str,
    summary: str,
    duration_ms: float | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    if trace_id not in _trace_store:
        _trace_store[trace_id] = []
    _trace_store[trace_id].append(
        TraceStageRecord(
            node=node,
            stage=stage,
            summary=summary,
            duration_ms=duration_ms,
            metadata=metadata or {},
        )
    )


def get_trace(trace_id: str) -> list[TraceStageRecord] | None:
    stages = _trace_store.get(trace_id)
    if not stages:
        return None
    return list(stages)


def clear_traces() -> None:
    """测试辅助：清空内存存储。"""
    _trace_store.clear()
