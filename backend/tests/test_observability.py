"""可观测性与链路追踪测试。"""

import pytest
from httpx import AsyncClient

from app.core.pipeline_trace import clear_traces, generate_trace_id, record_stage
from app.modules import ASRNode, LLMNode, TTSNode


@pytest.fixture(autouse=True)
def _clear_trace_store():
    clear_traces()
    yield
    clear_traces()


@pytest.mark.asyncio
async def test_metrics_returns_pipeline_metrics(client: AsyncClient) -> None:
    response = await client.get("/metrics")
    assert response.status_code == 200
    body = response.text
    assert "pipeline_node_total" in body
    assert "pipeline_node_duration_seconds" in body


@pytest.mark.asyncio
async def test_health_asr_node(client: AsyncClient) -> None:
    response = await client.get("/health/asr")
    assert response.status_code == 200
    data = response.json()
    assert data["node"] == "asr"
    assert data["status"] == "stub"


@pytest.mark.asyncio
async def test_health_unknown_node_returns_404(client: AsyncClient) -> None:
    response = await client.get("/health/unknown")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_pipeline_trace_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/v1/pipeline/trace/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_pipeline_trace_returns_stages(client: AsyncClient) -> None:
    trace_id = generate_trace_id()
    record_stage(trace_id, node="asr", stage="input", summary="audio stream")
    record_stage(
        trace_id,
        node="asr",
        stage="output",
        summary="hello world",
        duration_ms=120.5,
    )

    response = await client.get(f"/api/v1/pipeline/trace/{trace_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["trace_id"] == trace_id
    assert len(data["stages"]) == 2
    assert data["stages"][0]["node"] == "asr"
    assert data["stages"][0]["stage"] == "input"


@pytest.mark.asyncio
async def test_pipeline_node_records_trace() -> None:
    trace_id = generate_trace_id()
    node = ASRNode()
    await node.run(trace_id, "test audio")

    from app.core.pipeline_trace import get_trace

    stages = get_trace(trace_id)
    assert stages is not None
    assert len(stages) == 2
    assert stages[0].stage == "input"
    assert stages[1].stage == "output"


@pytest.mark.asyncio
async def test_full_pipeline_stub_chain() -> None:
    trace_id = generate_trace_id()
    asr = ASRNode()
    llm = LLMNode()
    tts = TTSNode()

    text = await asr.run(trace_id, "audio bytes")
    reply = await llm.run(trace_id, text)
    audio = await tts.run(trace_id, reply)

    assert "[asr stub]" in text
    assert "[llm stub]" in reply
    assert "[tts stub]" in audio

    from app.core.pipeline_trace import get_trace

    stages = get_trace(trace_id)
    assert stages is not None
    assert len(stages) == 6  # 3 nodes × (input + output)
