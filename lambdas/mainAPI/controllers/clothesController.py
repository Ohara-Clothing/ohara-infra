from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from usecases.clothesUsecase import ClothesUsecase
from repositories.clothesRepository import ClothesRepository
from models.dtos.clothes import ClothesCreate, ClothesUpdate

clothesRouter = APIRouter()


@clothesRouter.get("/clothes")
async def getClothes(db: Session = Depends(get_db)):
    repo = ClothesRepository(db)
    usecase = ClothesUsecase(repo)
    return await usecase.getClothesUsecase()


@clothesRouter.post("/clothes")
async def createClothes(clothes: ClothesCreate, db: Session = Depends(get_db)):
    repo = ClothesRepository(db)
    usecase = ClothesUsecase(repo)
    return await usecase.createClothes(clothes)


@clothesRouter.patch("/clothes/{clothes_id}")
async def updateClothes(
    clothes_id: str, clothes: ClothesUpdate, db: Session = Depends(get_db)
):
    repo = ClothesRepository(db)
    usecase = ClothesUsecase(repo)
    return await usecase.updateClothes(clothes_id, clothes)


@clothesRouter.delete("/clothes/{clothes_id}")
async def deleteClothes(clothes_id: str, db: Session = Depends(get_db)):
    repo = ClothesRepository(db)
    usecase = ClothesUsecase(repo)
    return await usecase.deleteClothes(clothes_id)
