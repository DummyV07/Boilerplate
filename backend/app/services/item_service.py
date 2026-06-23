"""Item 业务逻辑"""

from fastapi import HTTPException, status

from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemRead


class ItemService:
    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    async def list_items(self) -> list[ItemRead]:
        items = await self._repository.list_items()
        return [ItemRead.model_validate(item) for item in items]

    async def create_item(self, payload: ItemCreate) -> ItemRead:
        item = await self._repository.create(payload.title, payload.description)
        return ItemRead.model_validate(item)

    async def delete_item(self, item_id: int) -> None:
        item = await self._repository.get_by_id(item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item_id} not found",
            )
        await self._repository.delete(item)
