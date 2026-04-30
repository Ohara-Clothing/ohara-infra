from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class FitBase(BaseModel):
    name: str
    description: Optional[str] = None

class FitCreate(FitBase):
    clothesIds: list[str] = Field(default_factory=list)


class FitClothesUpdate(BaseModel):
    clothesIds: list[str]

class FitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    clothesIds: Optional[list[str]] = None

class Fit(FitBase):
    fitId: str
    userId: str
    createdAt: datetime
    model_config = ConfigDict(from_attributes=True)
