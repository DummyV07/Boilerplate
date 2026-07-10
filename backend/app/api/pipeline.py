"""AI 流水线链路追踪 API。"""

from fastapi import APIRouter, HTTPException

from app.core.pipeline_trace import get_trace
from app.schemas.pipeline import TraceResponse, TraceStage

router = APIRouter(prefix="/v1/pipeline", tags=["pipeline"])


@router.get("/trace/{trace_id}", response_model=TraceResponse)
async def get_pipeline_trace(trace_id: str) -> TraceResponse:
    stages = get_trace(trace_id)
    if stages is None:
        raise HTTPException(status_code=404, detail=f"Trace not found: {trace_id}")
    return TraceResponse(
        trace_id=trace_id,
        stages=[
            TraceStage(
                node=s.node,
                stage=s.stage,
                summary=s.summary,
                duration_ms=s.duration_ms,
                timestamp=s.timestamp,
            )
            for s in stages
        ],
    )
