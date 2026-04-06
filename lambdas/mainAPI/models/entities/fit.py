from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class FitEntity(Base):
    __tablename__ = "fits"

    fitId = Column(String, primary_key=True, index=True)
    userId = Column(String, ForeignKey("users.userId"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    createdAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("UserEntity", back_populates="fits")
    fit_clothes = relationship("FitClothesEntity", back_populates="fit", cascade="all, delete-orphan")
