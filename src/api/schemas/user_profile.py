from datetime import datetime
from os import PathLike
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from fastapi import UploadFile, File


class UserProfileCreateSchema(BaseModel):
    user_id: UUID
    cv_file: UploadFile


class UserProfileSchema(BaseModel):
    job_position: Annotated[str | None, Field()] = None
    experience: Annotated[str | None, Field()] = None
    tech_stack: Annotated[str | None, Field()] = None


# TODO: Separate models for creating and reading profiles

class UserProfileDetailResponseSchema(BaseModel):
    id: UUID
    user_id: UUID
    job_position: str
    experience: float
    tech_stack: str
