from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from usecases.fitsUsecase import FitsUsecase
from repositories.fitsRepository import FitsRepository

fitsRouter = APIRouter()


@fitsRouter.get("/fits/")
async def get_all_fits(db: Session = Depends(get_db)):
    fit_repo = FitsRepository(db)
    fit_usecase = FitsUsecase(fit_repo)
    return fit_usecase.getAllFits()


# Add other fit endpoints here (e.g., create, get by id, update, delete)

