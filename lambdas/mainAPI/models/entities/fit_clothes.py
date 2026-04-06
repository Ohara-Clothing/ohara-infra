from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class FitClothesEntity(Base):
    __tablename__ = "fit_clothes"

    fitClothesId = Column(String, primary_key=True, index=True)
    fitId = Column(String, ForeignKey("fits.fitId"), nullable=False)
    clothesId = Column(String, ForeignKey("clothes.clothesId"), nullable=False)

    fit = relationship("FitEntity", back_populates="fit_clothes")
    clothes = relationship("ClothesEntity", back_populates="fit_clothes")
