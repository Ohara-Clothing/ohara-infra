from fastapi import APIRouter, Depends, Query, Request
from services.AWS.s3Service import AWS_S3
from usecases.imageUsecase import ImageUsecase
from repositories.authRepository import AuthRepository
from repositories.clothesRepository import ClothesRepository
from db import get_db
from sqlalchemy.orm import Session

imageRouter = APIRouter()

@imageRouter.get("/images/profile/upload-url")
async def get_user_upload_url(
    request: Request,
    content_type: str = Query(..., description="The MIME type of the file, e.g., image/jpeg"),
    s3: AWS_S3 = Depends(AWS_S3),
    db: Session = Depends(get_db),
):
    uc = ImageUsecase(s3, AuthRepository(db), ClothesRepository(db))
    return uc.get_user_profile_upload_url(request.headers.get("Authorization"), content_type)



@imageRouter.delete("/images/profile")
async def delete_profile_image(
    request: Request,
    s3: AWS_S3 = Depends(AWS_S3),
    db: Session = Depends(get_db),
):
    uc = ImageUsecase(s3, AuthRepository(db), ClothesRepository(db))
    return uc.delete_user_profile_image(request.headers.get("Authorization"))

@imageRouter.get("/images/clothes/{clothes_id}/upload-url")
async def get_clothes_upload_url(
    request: Request,
    clothes_id: str,
    content_type: str = Query(..., description="The MIME type of the file, e.g., image/png"),
    s3: AWS_S3 = Depends(AWS_S3),
    db: Session = Depends(get_db),
):
    uc = ImageUsecase(s3, AuthRepository(db), ClothesRepository(db))
    return uc.get_clothes_upload_url(request.headers.get("Authorization"), clothes_id, content_type)

@imageRouter.delete("/images/clothes/{clothes_id}")
async def delete_clothes_image(
    request: Request,
    clothes_id: str,
    s3: AWS_S3 = Depends(AWS_S3),
    db: Session = Depends(get_db),
):
    uc = ImageUsecase(s3, AuthRepository(db), ClothesRepository(db))
    return uc.delete_clothes_image(request.headers.get("Authorization"), clothes_id)
