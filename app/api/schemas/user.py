from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    fullname: str
    username: str
    password: str


class UserCreateResponseSchema(BaseModel):
    id: UUID


class UserUpdateSchema(BaseModel):
    fullname: Annotated[str | None, Field()] = None
    username: Annotated[str | None, Field()] = None
    password: Annotated[str | None, Field()] = None


class UserDetailResponseSchema(BaseModel):
    id: UUID
    fullname: str
    username: str

    model_config = {"from_attributes": True}


class UserListResponseSchema(BaseModel):
    users: list[UserDetailResponseSchema]
