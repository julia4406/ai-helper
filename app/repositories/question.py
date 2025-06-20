from sqlalchemy.orm import selectinload

from app.api.schemas.question import QuestionCreateSchema
from app.database.models import Question
from app.repositories.base import BaseRepository


class QuestionRepository(BaseRepository):
    model = Question

    async def create_question(self, question_data: QuestionCreateSchema):
        raw_question = await self.add(
            obj_data=question_data.model_dump(),
            load_options=[selectinload(self.model.answer)]
        )
        return raw_question.to_dto()
