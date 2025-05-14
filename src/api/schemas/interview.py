from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class InterviewDetailSchema(BaseModel):
    id: UUID
    title: str
    user_id: UUID
    job_position: str
    experience: float
    tech_stack: str


class InterviewCreateSchema(BaseModel):
    title: Annotated[str | None, Field()] = None
    job_position: Annotated[str | None, Field()] = None
    experience: Annotated[float | None, Field()] = None
    tech_stack: Annotated[str | None, Field()] = None
    user_id: Annotated[UUID, Field()]
