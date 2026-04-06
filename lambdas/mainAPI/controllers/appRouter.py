from fastapi import APIRouter, responses
from fastapi.responses import HTMLResponse

from controllers.authController import authRouter
from controllers.clothesController import clothesRouter
from controllers.fitsController import fitsRouter
from controllers.imageController import imageRouter

app_router = APIRouter()


@app_router.get("/", response_class=HTMLResponse)
def welcomeOhara():
    return "<h1>Welcome to Ohara API</h1>"


app_router.include_router(authRouter, tags=["Auth Routes"])
app_router.include_router(clothesRouter, tags=["Clothes Routes"])
app_router.include_router(fitsRouter, tags=["Fits Routes"])
app_router.include_router(imageRouter, tags=["Image Routes"])
