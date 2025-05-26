from loguru import logger

from src.api.schemas.answer import AnswerCreateSchema
from src.database.models.answer import Answer
from src.repositories.base import BaseRepository


class AnswerRepository(BaseRepository):
    model = Answer

    async def create_answer(self, answer_data: AnswerCreateSchema):
        logger.info(f"Creating answer: {answer_data}")
        new_answer = await self.add(
            obj_data=answer_data.model_dump()
        )

        return new_answer.to_dto()

    async def update_answer(self, answer_id, new_answer_data: dict):
        updated_answer = await self.update(
            obj_id=answer_id,
            obj_new_data=new_answer_data
        )

        return updated_answer.to_dto()
