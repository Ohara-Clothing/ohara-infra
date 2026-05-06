import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class ClothesBase(BaseModel):
    clothesType: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[Decimal] = None


class ClothesCreate(ClothesBase):
    imageKey: Optional[str] = None


class ClothesUpdate(ClothesBase):
    pass


class Clothes(ClothesBase):
    clothesId: uuid.UUID
    imageKey: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
