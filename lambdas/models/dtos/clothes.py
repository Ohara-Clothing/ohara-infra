from typing import Optional
from pydantic import BaseModel, ConfigDict


class Clothes(BaseModel):
    clothesId: str
    clotheType: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
