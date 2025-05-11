from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, Field


class UserProfileDetailResponseSchema:
    id: UUID
    user_id: UUID
    job_position: str
    experience: float
    tech_stack: str
