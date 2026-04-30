from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from models.entities.fit import FitEntity
from models.entities.fit_clothes import FitClothesEntity
from models.entities.clothes import ClothesEntity
from models.dtos.fit import FitCreate, FitUpdate

class FitsRepository:
    def __init__(self, db: Session):
        self.db = db

    def getAllFits(self, user_id: str):
        return (
            self.db.query(FitEntity)
            .filter(FitEntity.userId == user_id)
            .options(
                selectinload(FitEntity.fit_clothes).selectinload(FitClothesEntity.clothes)
            )
            .all()
        )

    def getFitById(self, fit_id: str):
        return self.db.query(FitEntity).filter(FitEntity.fitId == fit_id).first()

    def createFit(self, fit: FitCreate, user_id: str):
        fit_data = fit.model_dump()
        clothes_ids = fit_data.pop("clothesIds", [])
        fit_data["userId"] = user_id
        db_fit = FitEntity(**fit_data)
        self.db.add(db_fit)
        self.db.commit()
        self.db.refresh(db_fit)
        if clothes_ids:
            self.setFitClothes(db_fit.fitId, clothes_ids)
        return db_fit

    def updateFit(self, fit_id: str, fit: FitUpdate):
        db_fit = self.getFitById(fit_id)
        if db_fit:
            update_data = fit.model_dump(exclude_unset=True)
            clothes_ids = update_data.pop("clothesIds", None)
            for key, value in update_data.items():
                setattr(db_fit, key, value)
            self.db.commit()
            self.db.refresh(db_fit)
            if clothes_ids is not None:
                self.setFitClothes(str(db_fit.fitId), clothes_ids)
        return db_fit

    def deleteFit(self, fit_id: str):
        db_fit = self.getFitById(fit_id)
        if db_fit:
            self.db.delete(db_fit)
            self.db.commit()
        return db_fit

    def setFitClothes(self, fit_id: str, clothes_ids: list[str]):
        fit = self.getFitById(fit_id)
        if not fit:
            return None

        unique_clothes_ids = list(dict.fromkeys(clothes_ids))

        valid_clothes = (
            self.db.query(ClothesEntity)
            .filter(ClothesEntity.clothesId.in_(unique_clothes_ids))
            .all()
        )
        valid_ids = {str(clothes.clothesId) for clothes in valid_clothes}
        missing_ids = [clothes_id for clothes_id in unique_clothes_ids if clothes_id not in valid_ids]
        if missing_ids:
            raise ValueError(f"Clothes not found: {', '.join(missing_ids)}")

        self.db.query(FitClothesEntity).filter(FitClothesEntity.fitId == fit.fitId).delete(
            synchronize_session=False
        )

        for clothes_id in unique_clothes_ids:
            self.db.add(
                FitClothesEntity(
                    fitId=fit.fitId,
                    clothesId=clothes_id,
                )
            )

        self.db.commit()
        self.db.refresh(fit)
        return fit
