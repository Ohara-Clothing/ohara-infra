from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException

clothesRouter = APIRouter()


@clothesRouter.get("/clothes")
async def getClothes():
    return
