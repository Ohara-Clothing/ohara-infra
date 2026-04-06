from fastapi import HTTPException
from services.AWS.s3Service import AWS_S3
from utils.constants import S3KeyConstants
from utils.jsonReturnUtil import jsonResponse
import uuid

class ImageUsecase:
    def __init__(self, s3_service: AWS_S3):
        self.s3 = s3_service

    def get_user_profile_upload_url(self, user_id: str, content_type: str):
        extension = content_type.split('/')[-1] if '/' in content_type else content_type
        object_key = S3KeyConstants.USER_PROFILE_DIR.format(user_id=user_id, extension=extension)
        
        url_data = self.s3.generate_presigned_put_url(object_key, content_type)
        if not url_data:
            raise HTTPException(status_code=500, detail="Could not generate upload URL")
            
        return jsonResponse(url_data, key="presignedUrl")

    def get_clothes_upload_url(self, clothes_id: str, content_type: str):
        # We expect the frontend to pass the clothes_id (often a uuid generated on the frontend or backend prior to this call)
        extension = content_type.split('/')[-1] if '/' in content_type else content_type
        object_key = S3KeyConstants.CLOTHES_DIR.format(clothes_id=clothes_id, extension=extension)
        
        url_data = self.s3.generate_presigned_put_url(object_key, content_type)
        if not url_data:
            raise HTTPException(status_code=500, detail="Could not generate upload URL")
            
        return jsonResponse(url_data, key="presignedUrl")

    def get_view_url(self, image_key: str):
        url = self.s3.generate_presigned_get_url(image_key)
        if not url:
            raise HTTPException(status_code=404, detail="Could not generate view URL")
        return jsonResponse({"viewUrl": url}, key="presignedUrl")
