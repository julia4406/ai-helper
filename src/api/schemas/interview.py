from uuid import UUID

from pydantic import BaseModel


class InterviewDetailSchema(BaseModel):
    id: UUID
    title: str
    user_id: UUID
    job_position: str
    experience: float
    tech_stack: str
