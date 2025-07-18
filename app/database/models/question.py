from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.api.schemas.question import QuestionDetailSchema
from app.database.models.base import Base, IdCreatedAtModelMixin


class Question(Base, IdCreatedAtModelMixin):
    __tablename__ = "questions"

    text: Mapped[str]
    interview_id: Mapped[UUID] = mapped_column(ForeignKey("interviews.id"))

    answer: Mapped["Answer"] = relationship()

    def to_dto(self) -> QuestionDetailSchema:
        return QuestionDetailSchema(
            id=self.id,
            text=self.text,
            answer=self.answer.to_dto() if self.answer else None,
            interview_id=self.interview_id,
        )
