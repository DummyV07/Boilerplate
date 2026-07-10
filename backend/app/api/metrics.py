"""Prometheus 指标导出（对接 Grafana，零额外依赖）。"""

from fastapi import APIRouter
from starlette.responses import Response

from app.modules import KNOWN_NODES

router = APIRouter(tags=["observability"])

# 模版级静态指标：后期可替换为 prometheus-client 或 OpenTelemetry
_METRICS_BODY = "\n".join(
    [
        "# HELP pipeline_node_total AI pipeline node invocation count",
        "# TYPE pipeline_node_total counter",
        *[f'pipeline_node_total{{node="{n}",status="stub"}} 0' for n in KNOWN_NODES],
        "",
        "# HELP pipeline_node_duration_seconds AI pipeline node processing duration",
        "# TYPE pipeline_node_duration_seconds histogram",
        'pipeline_node_duration_seconds_bucket{node="asr",status="stub",le="+Inf"} 0',
        "",
        "# HELP pipeline_request_total End-to-end pipeline request count",
        "# TYPE pipeline_request_total counter",
        'pipeline_request_total{final_status="ok"} 0',
        "",
    ]
)


@router.get("/metrics")
async def metrics() -> Response:
    return Response(content=_METRICS_BODY, media_type="text/plain; version=0.0.4; charset=utf-8")
