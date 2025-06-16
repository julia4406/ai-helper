from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.api.schemas.user import UserDetailResponseSchema
from app.database.models.base import Base, IdCreatedAtModelMixin


class User(Base, IdCreatedAtModelMixin):
    __tablename__ = "users"

    fullname: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    telegram_id: Mapped[str] = mapped_column(nullable=True)

    user_profiles: Mapped[list["UserProfile"]] = relationship()

    def to_dto(self) -> UserDetailResponseSchema:
        return UserDetailResponseSchema(
            id=self.id,
            telegram_id=self.telegram_id,
            fullname=self.fullname,
            username=self.username
        )
