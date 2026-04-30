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
    pass


class ClothesUpdate(ClothesBase):
    pass


class Clothes(ClothesBase):
    clothesId: str
    model_config = ConfigDict(from_attributes=True)

