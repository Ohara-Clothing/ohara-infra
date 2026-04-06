from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from .base import Base

class ClothesEntity(Base):
    __tablename__ = "clothes"

    clothesId = Column(String, primary_key=True, index=True)
    clothesType = Column(String, nullable=True)
    color = Column(String, nullable=True)
    size = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    imageKey = Column(String, nullable=True)

    user_clothes = relationship("UserClothesEntity", back_populates="clothes")
    fit_clothes = relationship("FitClothesEntity", back_populates="clothes")