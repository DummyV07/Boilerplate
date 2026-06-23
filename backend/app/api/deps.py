"""FastAPI 依赖注入"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.item_repository import ItemRepository
from app.services.item_service import ItemService


async def get_item_service(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> ItemService:
    return ItemService(ItemRepository(session))
