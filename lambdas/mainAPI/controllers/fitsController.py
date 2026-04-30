from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db import get_db
from usecases.fitsUsecase import FitsUsecase
from repositories.fitsRepository import FitsRepository
from repositories.authRepository import AuthRepository
from models.dtos.fit import FitCreate, FitUpdate, FitClothesUpdate

fitsRouter = APIRouter()


@fitsRouter.get("/fits/")
async def get_all_fits(request: Request, db: Session = Depends(get_db)):
    fit_repo = FitsRepository(db)
    user_repo = AuthRepository(db)
    fit_usecase = FitsUsecase(fit_repo, user_repo)
    return fit_usecase.getAllFits(request.headers.get("Authorization"))


@fitsRouter.post("/fits/")
async def create_fit(
    fit: FitCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    fit_repo = FitsRepository(db)
    user_repo = AuthRepository(db)
    fit_usecase = FitsUsecase(fit_repo, user_repo)
    return fit_usecase.createFit(fit, request.headers.get("Authorization"))


@fitsRouter.patch("/fits/{fit_id}")
async def update_fit(
    fit_id: str,
    fit: FitUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    fit_repo = FitsRepository(db)
    user_repo = AuthRepository(db)
    fit_usecase = FitsUsecase(fit_repo, user_repo)
    return fit_usecase.updateFit(fit_id, fit, request.headers.get("Authorization"))


@fitsRouter.delete("/fits/{fit_id}")
async def delete_fit(
    fit_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    fit_repo = FitsRepository(db)
    user_repo = AuthRepository(db)
    fit_usecase = FitsUsecase(fit_repo, user_repo)
    return fit_usecase.deleteFit(fit_id, request.headers.get("Authorization"))


@fitsRouter.put("/fits/{fit_id}/clothes")
async def set_fit_clothes(
    fit_id: str,
    payload: FitClothesUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    fit_repo = FitsRepository(db)
    user_repo = AuthRepository(db)
    fit_usecase = FitsUsecase(fit_repo, user_repo)
    return fit_usecase.setFitClothes(fit_id, payload, request.headers.get("Authorization"))
