from fastapi import APIRouter, Depends, Query
from services.AWS.s3Service import AWS_S3
from usecases.imageUsecase import ImageUsecase

imageRouter = APIRouter()

@imageRouter.get("/images/upload-url/user/{user_id}")
async def get_user_upload_url(
    user_id: str, 
    content_type: str = Query(..., description="The MIME type of the file, e.g., image/jpeg"),
    s3: AWS_S3 = Depends(AWS_S3)
):
    uc = ImageUsecase(s3)
    return uc.get_user_profile_upload_url(user_id, content_type)

@imageRouter.get("/images/upload-url/clothes/{clothes_id}")
async def get_clothes_upload_url(
    clothes_id: str,
    content_type: str = Query(..., description="The MIME type of the file, e.g., image/png"),
    s3: AWS_S3 = Depends(AWS_S3)
):
    uc = ImageUsecase(s3)
    return uc.get_clothes_upload_url(clothes_id, content_type)

@imageRouter.get("/images/view-url/")
async def get_view_url(
    image_key: str = Query(..., description="The S3 object key, e.g., clothes/123/image.jpg"),
    s3: AWS_S3 = Depends(AWS_S3)
):
    uc = ImageUsecase(s3)
    return uc.get_view_url(image_key)
