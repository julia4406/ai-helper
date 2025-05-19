from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from src.api.schemas.interview import InterviewDetailSchema
from src.database.models.base import Base, IdCreatedAtModelMixin


class Interview(Base, IdCreatedAtModelMixin):
    __tablename__ = "interviews"

    title: Mapped[str] = mapped_column()
    job_position: Mapped[str] = mapped_column()
    experience: Mapped[float] = mapped_column()
    tech_stack: Mapped[str] = mapped_column()


    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    questions: Mapped[list["Question"]] = relationship()

    # TODO can be remade
    # user_profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    # user_profile: Mapped["UserProfile"] = relationship(
    #     "UserProfile", back_populates="interviews"
    # )

    def to_dto(self) -> InterviewDetailSchema:
        return InterviewDetailSchema(
            id=self.id,
            title=self.title,
            user_id=self.user_id,
            job_position=self.job_position,
            experience=self.experience,
            tech_stack=self.tech_stack
        )
