from uuid import UUID

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.api.schemas.interview import (
    InterviewCreateSchema,
    InterviewDetailSchema
)
from src.database.models import Interview, Question
from src.repositories.base import BaseRepository


class InterviewRepository(BaseRepository):
    model = Interview

    async def create_interview(
            self, data: InterviewCreateSchema
    ) -> InterviewDetailSchema:
        logger.info(f"Creating interview(repo): {data}")
        new_interview = await self.add(
            obj_data=data.model_dump(exclude={"profile_id"}),
            load_options=[selectinload(self.model.questions)]
        )
        return new_interview.to_dto()

    async def get_interview_by_id(self, interview_id: UUID):
        logger.info(f"Getting interview by id: {interview_id}")
        interview = await self._session.execute(
            select(self.model)
            .where(self.model.id == interview_id)
            .options(
                selectinload(
                    self.model.questions
                )
            )
        )
        return interview.scalars().one_or_none().to_dto()
