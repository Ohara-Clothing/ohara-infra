from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
from .base import Base

class UserEntity(Base):
    __tablename__ = "users"
    
    userId = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    createdAt = Column(DateTime, default=datetime.now)
    confirmed = Column(Boolean, default=False)
