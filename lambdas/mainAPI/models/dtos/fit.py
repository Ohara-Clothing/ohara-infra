import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

from models.dtos.clothes import Clothes


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


class FitClothesResponse(Clothes):
    fitClothesId: uuid.UUID


class FitResponse(FitBase):
    fitId: uuid.UUID
    userId: uuid.UUID
    createdAt: datetime
    clothes: list[FitClothesResponse] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
