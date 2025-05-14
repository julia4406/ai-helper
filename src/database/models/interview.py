from uuid import UUID

from sqlalchemy import ForeignKey, String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.schemas.interview import InterviewDetailSchema
from src.api.schemas.user_profile import UserProfileSchema
from src.database.models.base import Base, IdCreatedAtModelMixin


class Interview(Base, IdCreatedAtModelMixin):
    __tablename__ = "interviews"

    title: Mapped[str] = mapped_column(String)

    user_profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    user_profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="interviews"
    )

    def to_dto(self) -> InterviewDetailSchema:
        return InterviewDetailSchema(
            id=self.id,
            title=self.title,
            user_id=self.user_id,
            job_position=self.user_profile.job_position,
            experience=self.user_profile.experience,
            tech_stack=self.user_profile.tech_stack
        )
