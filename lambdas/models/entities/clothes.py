from sqlalchemy import Column, String
from .base import Base

class ClothesEntity(Base):
    __tablename__ = "clothes"
    
    clothesId = Column(String, primary_key=True, index=True)
    clotheType = Column(String, nullable=True)
