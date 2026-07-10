"""链路追踪 Pydantic 模型。"""

from pydantic import BaseModel, ConfigDict


class TraceStage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node: str
    stage: str
    summary: str
    duration_ms: float | None = None
    timestamp: str


class TraceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trace_id: str
    stages: list[TraceStage]
