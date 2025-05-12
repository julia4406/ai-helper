from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.schemas.user_profile import UserProfileDetailResponseSchema
from src.database.models.base import Base, IdCreatedAtModelMixin


class UserProfile(Base, IdCreatedAtModelMixin):
    __tablename__ = "user_profiles"

    job_position: Mapped[str] = mapped_column(nullable=True)
    experience: Mapped[float] = mapped_column(default=0.5)
    tech_stack: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    def to_dto(self) -> UserProfileDetailResponseSchema:
        return UserProfileDetailResponseSchema(
            id=self.id,
            user_id=self.user_id,
            job_position=self.job_position,
            experience=self.experience,
            tech_stack=self.tech_stack
        )
