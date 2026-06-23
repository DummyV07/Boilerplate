"""CPU 任务 API 测试"""

from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_compute_fibonacci(client: AsyncClient) -> None:
    mock_pool = MagicMock()
    mock_pool.submit.return_value = "task-123"
    mock_pool.get_result.return_value = 55
    app.state.task_pool = mock_pool

    response = await client.post(
        "/api/tasks/compute",
        json={"op": "fibonacci", "value": 10},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "task-123"
    assert data["result"] == 55
    mock_pool.submit.assert_called_once_with("fibonacci", 10)
