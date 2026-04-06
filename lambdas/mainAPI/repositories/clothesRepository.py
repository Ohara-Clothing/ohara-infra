from sqlalchemy.orm import Session
from models.entities.clothes import ClothesEntity
from models.dtos.clothes import ClothesCreate, ClothesUpdate

class ClothesRepository:
    def __init__(self, db: Session):
        self.db = db

    def getUserClothes(self):
        return self.db.query(ClothesEntity).all()

    def getClothesById(self, clothes_id: str):
        return self.db.query(ClothesEntity).filter(ClothesEntity.clothesId == clothes_id).first()

    def createClothes(self, clothes: ClothesCreate):
        db_clothes = ClothesEntity(**clothes.model_dump())
        self.db.add(db_clothes)
        self.db.commit()
        self.db.refresh(db_clothes)
        return db_clothes

    def updateClothes(self, clothes_id: str, clothes: ClothesUpdate):
        db_clothes = self.getClothesById(clothes_id)
        if db_clothes:
            update_data = clothes.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_clothes, key, value)
            self.db.commit()
            self.db.refresh(db_clothes)
        return db_clothes

    def deleteClothes(self, clothes_id: str):
        db_clothes = self.getClothesById(clothes_id)
        if db_clothes:
            self.db.delete(db_clothes)
            self.db.commit()
        return db_clothes