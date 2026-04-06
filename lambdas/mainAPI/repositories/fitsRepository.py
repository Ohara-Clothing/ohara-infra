from sqlalchemy.orm import Session
from models.entities.fit import FitEntity
from models.dtos.fit import FitCreate, FitUpdate

class FitsRepository:
    def __init__(self, db: Session):
        self.db = db

    def getAllFits(self):
        return self.db.query(FitEntity).all()

    def getFitById(self, fit_id: str):
        return self.db.query(FitEntity).filter(FitEntity.fitId == fit_id).first()

    def createFit(self, fit: FitCreate):
        db_fit = FitEntity(**fit.model_dump())
        self.db.add(db_fit)
        self.db.commit()
        self.db.refresh(db_fit)
        return db_fit

    def updateFit(self, fit_id: str, fit: FitUpdate):
        db_fit = self.getFitById(fit_id)
        if db_fit:
            update_data = fit.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_fit, key, value)
            self.db.commit()
            self.db.refresh(db_fit)
        return db_fit

    def deleteFit(self, fit_id: str):
        db_fit = self.getFitById(fit_id)
        if db_fit:
            self.db.delete(db_fit)
            self.db.commit()
        return db_fit