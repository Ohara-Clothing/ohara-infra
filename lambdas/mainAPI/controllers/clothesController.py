from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException
from sqlalchemy.orm import Session
from db import get_db
from usecases.clothesUsecase import ClothesUsecase
from repositories.clothesRepository import ClothesRepository

clothesRouter = APIRouter()


@clothesRouter.get("/clothes")
async def getClothes(db: Session = Depends(get_db)):
    repo = ClothesRepository(db)
    usecase = ClothesUsecase(repo)
    return await usecase.getClothesUsecase()