"""Item CRUD 测试"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_item_crud(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/items",
        json={"title": "Test Item", "description": "A test description"},
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Test Item"
    assert created["id"] is not None

    list_response = await client.get("/api/items")
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert items[0]["title"] == "Test Item"

    delete_response = await client.delete(f"/api/items/{created['id']}")
    assert delete_response.status_code == 204

    empty_response = await client.get("/api/items")
    assert empty_response.json() == []


@pytest.mark.asyncio
async def test_delete_not_found(client: AsyncClient) -> None:
    response = await client.delete("/api/items/9999")
    assert response.status_code == 404
