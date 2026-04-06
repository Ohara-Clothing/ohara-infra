from sqlalchemy.orm import Session
from models.entities.fit import FitEntity


class FitsRepository:
    def __init__(self, db: Session):
        self.db = db

    def getAllFits(self):
        return self.db.query(FitEntity).all()

    # Add other repository methods here (e.g., get_fit_by_id, create_fit, update_fit, delete_fit)
