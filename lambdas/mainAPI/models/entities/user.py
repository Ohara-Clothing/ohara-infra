import uuid
from sqlalchemy import String, DateTime, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from .base import Base


class UserEntity(Base):
    __tablename__ = "users"

    userId: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()")
    )
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    confirmed: Mapped[bool] = mapped_column(default=True)
    profileImagekey: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    style: Mapped[str] = mapped_column(String, nullable=True)
    favoriteClothesIds: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(postgresql.JSONB),
        default=list,
        server_default=text("'[]'::jsonb"),
    )
    pinnedFitIds: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(postgresql.JSONB),
        default=list,
        server_default=text("'[]'::jsonb"),
    )

    clothes = relationship("ClothesEntity", back_populates="user", cascade="all, delete-orphan")
    fits = relationship("FitEntity", back_populates="user", cascade="all, delete-orphan")
