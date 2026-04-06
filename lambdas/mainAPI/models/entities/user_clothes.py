from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base

class UserClothesEntity(Base):
    __tablename__ = "user_clothes"

    userClothesId = Column(String, primary_key=True, index=True)
    userId = Column(String, ForeignKey("users.userId"), nullable=False)
    clothesId = Column(String, ForeignKey("clothes.clothesId"), nullable=False)
    quantity = Column(Integer, default=1)
    addedAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("UserEntity", back_populates="user_clothes")
    clothes = relationship("ClothesEntity", back_populates="user_clothes")
