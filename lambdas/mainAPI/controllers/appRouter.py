from fastapi import APIRouter

from controllers.authController import authRouter
from controllers.clothesController import clothesRouter

app_router = APIRouter()

app_router.include_router(authRouter, tags=["Auth"])
app_router.include_router(clothesRouter, tags=["Clothes"])
