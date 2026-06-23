"""CPU 任务 API"""

import asyncio
from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/tasks", tags=["tasks"])


class ComputeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    op: Literal["fibonacci", "hash"]
    value: int = Field(..., ge=0, le=10_000)


class ComputeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    task_id: str
    result: int | str | dict[str, str]


@router.post("/compute", response_model=ComputeResponse)
async def compute_task(
    payload: ComputeRequest,
    request: Request,
) -> ComputeResponse:
    task_pool = request.app.state.task_pool
    task_id = task_pool.submit(payload.op, payload.value)
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(
            None,
            task_pool.get_result,
            task_id,
        )
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail=str(exc)) from exc
    return ComputeResponse(task_id=task_id, result=result)
