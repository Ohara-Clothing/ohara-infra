from sqlalchemy import Column, String, DateTime
from typing import Literal
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from .base import Base


class UserEntity(Base):
    __tablename__ = "users"

    userId = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    createdAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    confirmed: Mapped[bool] = mapped_column(default=True)
    profileImagekey = Column(String, nullable=True)

    user_clothes = relationship("UserClothesEntity", back_populates="user", cascade="all, delete-orphan")
    fits = relationship("FitEntity", back_populates="user", cascade="all, delete-orphan")

