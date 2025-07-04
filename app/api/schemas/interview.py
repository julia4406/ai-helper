from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.api.schemas.question import QuestionDetailSchema
from app.api.schemas.user_profile import UserProfileSchema


class InterviewDetailSchema(BaseModel):
    id: UUID
    is_active: bool
    title: str
    feedback: Annotated[str | None, Field()] = None
    user_id: UUID
    job_position: str
    experience: float
    tech_stack: str
    questions: list["QuestionDetailSchema"]


class InterviewCreateSchema(BaseModel):
    title: Annotated[str | None, Field()] = None
    job_position: Annotated[str | None, Field()] = None
    experience: Annotated[float | None, Field()] = None
    tech_stack: Annotated[str | None, Field()] = None
    user_id: Annotated[UUID | None, Field()] = None
    telegram_id: Annotated[str | None, Field()] = None
    profile_id: Annotated[UUID | None, Field()] = None

    @model_validator(mode="after")
    def validate_id_presence(self):
        if not self.telegram_id and not self.user_id:
            raise ValueError("Impossible to identify user!"
                             " Please login or register.")
        return self

    @model_validator(mode="after")
    def set_title_if_none(self) -> "InterviewCreateSchema":
        if not self.title:
            self.set_title()
        return self

    @model_validator(mode="after")
    def check_profile_or_args(self) -> "InterviewCreateSchema":
        if not self.profile_id:
            if not self.job_position or not self.experience or not self.tech_stack:
                raise ValueError("You must provide either profile_id or "
                                 "job_position, experience and tech_stack")
        return self

    def set_title(self):
        self.title = f"Interview {self.job_position} - {self.experience} y."

    def load_from_user_profile(self, user_profile: UserProfileSchema):
        self.job_position = user_profile.job_position
        self.experience = user_profile.experience
        self.tech_stack = user_profile.tech_stack
        self.set_title()

class InterviewFinishResponseSchema(BaseModel):
    id: UUID
    feedback: str