from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from fastapi import UploadFile, File


class UserProfileCreateSchema(BaseModel):
    user_id: UUID
    cv_file: UploadFile

# TODO: Separate models for creating and reading profiles

class UserProfileSchema(BaseModel):
    id: Annotated[UUID | None, Field()] = None
    user_id: UUID
    job_position: Annotated[str | None, Field()] = None
    experience: Annotated[float | None, Field()] = None
    # TODO: Can be improved by using JSON field
    tech_stack: Annotated[str | None, Field()] = None
