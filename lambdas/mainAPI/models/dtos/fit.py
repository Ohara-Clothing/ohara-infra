from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FitBase(BaseModel):
    name: str
    description: Optional[str] = None

class FitCreate(FitBase):
    fitId: str
    userId: str

class FitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Fit(FitBase):
    fitId: str
    userId: str
    createdAt: datetime
    model_config = ConfigDict(from_attributes=True)
