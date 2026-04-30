from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db import get_db
from usecases.clothesUsecase import ClothesUsecase
from repositories.clothesRepository import ClothesRepository
from repositories.authRepository import AuthRepository
from models.dtos.clothes import ClothesCreate, ClothesUpdate
from services.AWS.s3Service import AWS_S3

clothesRouter = APIRouter()


@clothesRouter.get("/clothes")
async def getClothes(request: Request, db: Session = Depends(get_db)):
    repo = ClothesRepository(db)
    user_repo = AuthRepository(db)
    usecase = ClothesUsecase(repo, user_repo)
    return await usecase.getClothesUsecase(request.headers.get("Authorization"))


@clothesRouter.post("/clothes")
async def createClothes(
    clothes: ClothesCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    repo = ClothesRepository(db)
    user_repo = AuthRepository(db)
    usecase = ClothesUsecase(repo, user_repo)
    return await usecase.createClothes(clothes, request.headers.get("Authorization"))


@clothesRouter.patch("/clothes/{clothes_id}")
async def updateClothes(
    clothes_id: str,
    clothes: ClothesUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    repo = ClothesRepository(db)
    user_repo = AuthRepository(db)
    usecase = ClothesUsecase(repo, user_repo)
    return await usecase.updateClothes(clothes_id, clothes, request.headers.get("Authorization"))


@clothesRouter.delete("/clothes/{clothes_id}")
async def deleteClothes(
    clothes_id: str,
    request: Request,
    db: Session = Depends(get_db),
    s3: AWS_S3 = Depends(AWS_S3),
):
    repo = ClothesRepository(db)
    user_repo = AuthRepository(db)
    usecase = ClothesUsecase(repo, user_repo, s3)
    return await usecase.deleteClothes(clothes_id, request.headers.get("Authorization"))
