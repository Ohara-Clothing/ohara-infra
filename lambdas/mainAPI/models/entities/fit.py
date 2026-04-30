import uuid
from sqlalchemy import String, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from .base import Base

class FitEntity(Base):
    __tablename__ = "fits"

    fitId: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()")
    )
    userId: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.userId"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("UserEntity", back_populates="fits")
    fit_clothes = relationship("FitClothesEntity", back_populates="fit", cascade="all, delete-orphan")
