from uuid import UUID

from pydantic import BaseModel


class QuestionCreateSchema(BaseModel):
    text: str
    interview_id: UUID
