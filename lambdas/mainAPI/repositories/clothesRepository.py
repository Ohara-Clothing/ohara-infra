from sqlalchemy.orm import Session
from models.entities.clothes import ClothesEntity
from models.dtos.clothes import ClothesCreate, ClothesUpdate

class ClothesRepository:
    def __init__(self, db: Session):
        self.db = db

    def getUserClothes(self, user_id: str):
        return self.db.query(ClothesEntity).filter(ClothesEntity.userId == user_id).all()

    def getClothesById(self, clothes_id: str, user_id: str):
        return (
            self.db.query(ClothesEntity)
            .filter(ClothesEntity.clothesId == clothes_id, ClothesEntity.userId == user_id)
            .first()
        )

    def createClothes(self, clothes: ClothesCreate, user_id: str):
        db_clothes = ClothesEntity(userId=user_id, **clothes.model_dump())
        self.db.add(db_clothes)
        self.db.commit()
        self.db.refresh(db_clothes)
        return db_clothes

    def updateClothes(self, clothes_id: str, clothes: ClothesUpdate, user_id: str):
        db_clothes = self.getClothesById(clothes_id, user_id)
        if db_clothes:
            update_data = clothes.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_clothes, key, value)
            self.db.commit()
            self.db.refresh(db_clothes)
        return db_clothes

    def deleteClothes(self, clothes_id: str, user_id: str):
        db_clothes = self.getClothesById(clothes_id, user_id)
        if db_clothes:
            self.db.delete(db_clothes)
            self.db.commit()
        return db_clothes
