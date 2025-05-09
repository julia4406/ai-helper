from abc import ABC

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self):
        pass

    async def list(self):
        obj_list_query = await self._session.execute(
          select(self.model)
        )
        obj_list = obj_list_query.scalars().all()
        return obj_list

    async def update(self):
        pass

    async def add(self, obj_data: dict):
        new_obj = await self._session.scalar(
            insert(self.model).values(**obj_data).returning(self.model)
        )
        return new_obj

    async def delete(self):
        pass
