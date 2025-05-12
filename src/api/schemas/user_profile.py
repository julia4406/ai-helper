from datetime import datetime
from os import PathLike
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from fastapi import UploadFile, File


class UserProfileCreateSchema(BaseModel):
    user_id: UUID
    cv_file: UploadFile


class UserProfileCreateResponseSchema(BaseModel):
    ...


class UserProfileDetailResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    job_position: str
    experience: float
    tech_stack: str
    created_at: datetime
