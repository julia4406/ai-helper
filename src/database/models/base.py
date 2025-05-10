from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class IdModelMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), server_default=func.now(), nullable=False
    )
