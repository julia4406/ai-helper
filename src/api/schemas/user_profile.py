from os import PathLike
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from fastapi import UploadFile


class UserProfileCreateSchema(BaseModel):
    id: UUID


class UserProfileCreateResponseSchema(BaseModel):
    ...


class UserProfileDetailResponseSchema:
    id: UUID
    user_id: UUID
    job_position: str
    experience: float
    tech_stack: str
