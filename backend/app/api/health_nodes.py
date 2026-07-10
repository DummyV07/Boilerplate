"""AI 节点健康检查。"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from app.modules import KNOWN_NODES

router = APIRouter(tags=["observability"])

KNOWN_NODES_SET = frozenset(KNOWN_NODES)


class NodeHealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node: str
    status: str
    message: str


@router.get("/health/{node}", response_model=NodeHealthResponse)
async def node_health(node: str) -> NodeHealthResponse:
    if node not in KNOWN_NODES_SET:
        raise HTTPException(status_code=404, detail=f"Unknown node: {node}")
    return NodeHealthResponse(
        node=node,
        status="stub",
        message=f"{node} node placeholder ready",
    )
