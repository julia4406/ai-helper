from abc import ABC
from uuid import UUID
from fastapi import HTTPException
from loguru import logger

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, obj_id: UUID):
        obj_query = await self._session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        obj = obj_query.scalars().one_or_none()
        return obj

    async def list(self):
        obj_list_query = await self._session.execute(
            select(self.model)
        )
        obj_list = obj_list_query.scalars().all()
        return obj_list

    async def update(self, obj_id: UUID, obj_new_data: dict):
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**{k: v for k, v in obj_new_data.items() if v is not None})
            .returning(self.model)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()

        obj = result.scalar()
        if obj:
            return obj

        raise HTTPException(status_code=404, detail="Object not found")

    async def add(self, obj_data: dict, load_options: list = None):
        stmt = insert(self.model).values(**obj_data).returning(self.model)
        if load_options:
            stmt = stmt.options(*load_options)

        new_obj = await self._session.scalar(stmt)
        logger.info(f"Created new obj {new_obj}")
        return new_obj

    async def delete(self, obj_id: UUID):
        obj_query = await self._session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        obj = obj_query.scalar()
        if obj:
            await self._session.execute(
                delete(self.model).where(self.model.id == obj_id)
            )
            await self._session.commit()
            return obj
        raise HTTPException(status_code=404, detail="Object not found")
