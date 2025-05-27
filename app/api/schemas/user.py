from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, Field, model_validator


class UserCreateSchema(BaseModel):
    fullname: str
    username: str
    password: str
    telegram_id: Annotated[str | None, Field()] = None

    @model_validator(mode="after")
    def check_user_data(self) -> "UserCreateSchema":
        if not self.username or not self.password:
            raise ValueError("Username and Password cannot be empty!")
        return self


class UserCreateResponseSchema(BaseModel):
    id: UUID


class UserUpdateSchema(BaseModel):
    fullname: Annotated[str | None, Field()] = None
    username: Annotated[str | None, Field()] = None
    password: Annotated[str | None, Field()] = None
    telegram_id: Annotated[str | None, Field()] = None


class UserDetailResponseSchema(BaseModel):
    id: UUID
    fullname: str
    username: str
    telegram_id: Annotated[str | None, Field()] = None

    model_config = {"from_attributes": True}


class UserListResponseSchema(BaseModel):
    users: list[UserDetailResponseSchema]
