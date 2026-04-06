from sqlalchemy.orm import Session
from db import SessionLocal
from models.entities.clothes import ClothesEntity

class ClothesRepository:
    def __init__(self, db: Session):
        self.db = db

    def getUserClothes(self):
        # This method needs to be implemented based on how you associate clothes with users.
        # For now, it will return all clothes.
        return self.db.query(ClothesEntity).all()

    # You would add other methods here like get_clothes_by_id, create_clothes, update_clothes, etc.
