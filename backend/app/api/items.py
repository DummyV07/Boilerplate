"""Item REST API"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_item_service
from app.schemas.item import ItemCreate, ItemRead
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
async def list_items(
    service: Annotated[ItemService, Depends(get_item_service)],
) -> list[ItemRead]:
    return await service.list_items()


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate,
    service: Annotated[ItemService, Depends(get_item_service)],
) -> ItemRead:
    return await service.create_item(payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_item_service)],
) -> None:
    await service.delete_item(item_id)
