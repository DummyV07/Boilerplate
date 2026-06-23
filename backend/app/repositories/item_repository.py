"""Item 数据访问层"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item


class ItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_items(self) -> list[Item]:
        result = await self._session.execute(select(Item).order_by(Item.id.desc()))
        return list(result.scalars().all())

    async def get_by_id(self, item_id: int) -> Item | None:
        result = await self._session.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    async def create(self, title: str, description: str | None) -> Item:
        item = Item(title=title, description=description)
        self._session.add(item)
        await self._session.commit()
        await self._session.refresh(item)
        return item

    async def delete(self, item: Item) -> None:
        await self._session.delete(item)
        await self._session.commit()
