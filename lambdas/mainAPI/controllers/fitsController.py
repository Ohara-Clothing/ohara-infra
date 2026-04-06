from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from usecases.fitsUsecase import FitsUsecase
from repositories.fitsRepository import FitsRepository
from models.dtos.fit import FitCreate, FitUpdate

fitsRouter = APIRouter()


@fitsRouter.get("/fits/")
async def get_all_fits(db: Session = Depends(get_db)):
    fit_repo = FitsRepository(db)
    fit_usecase = FitsUsecase(fit_repo)
    return fit_usecase.getAllFits()


@fitsRouter.post("/fits/")
async def create_fit(fit: FitCreate, db: Session = Depends(get_db)):
    fit_repo = FitsRepository(db)
    fit_usecase = FitsUsecase(fit_repo)
    return fit_usecase.createFit(fit)


@fitsRouter.patch("/fits/{fit_id}")
async def update_fit(fit_id: str, fit: FitUpdate, db: Session = Depends(get_db)):
    fit_repo = FitsRepository(db)
    fit_usecase = FitsUsecase(fit_repo)
    return fit_usecase.updateFit(fit_id, fit)


@fitsRouter.delete("/fits/{fit_id}")
async def delete_fit(fit_id: str, db: Session = Depends(get_db)):
    fit_repo = FitsRepository(db)
    fit_usecase = FitsUsecase(fit_repo)
    return fit_usecase.deleteFit(fit_id)

