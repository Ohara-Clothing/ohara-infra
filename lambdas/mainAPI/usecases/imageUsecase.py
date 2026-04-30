from fastapi import HTTPException
from services.AWS.s3Service import AWS_S3
from utils.constants import S3KeyConstants
from utils.jsonReturnUtil import jsonResponse
from repositories.authRepository import AuthRepository
from repositories.clothesRepository import ClothesRepository
from utils.jwtUtil import usernameFromAccessToken

class ImageUsecase:
    def __init__(
        self,
        s3_service: AWS_S3,
        user_repo: AuthRepository,
        clothes_repo: ClothesRepository,
    ):
        self.s3 = s3_service
        self.user_repo = user_repo
        self.clothes_repo = clothes_repo

    def _resolve_current_user(self, authorization_header: str | None):
        if not authorization_header or not authorization_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authorization token")

        access_token = authorization_header.removeprefix("Bearer ").strip()
        username = usernameFromAccessToken(access_token)
        if not username:
            raise HTTPException(status_code=401, detail="Invalid authorization token")

        user = self.user_repo.getUserByUsername(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def get_user_profile_upload_url(self, authorization_header: str | None, content_type: str):
        user = self._resolve_current_user(authorization_header)
        object_key = S3KeyConstants.USER_PROFILE_IMAGE.format(user_id=user.userId)
        url_data = self.s3.generate_presigned_put_url(object_key, content_type)
        if not url_data:
            raise HTTPException(status_code=500, detail="Could not generate upload URL")

        self.user_repo.updateUserProfile(str(user.userId), {"profileImagekey": object_key})
        return jsonResponse(url_data, key="presignedUrl")

    def get_user_profile_view_url(self, authorization_header: str | None):
        user = self._resolve_current_user(authorization_header)
        object_key = user.profileImagekey or S3KeyConstants.USER_PROFILE_IMAGE.format(
            user_id=user.userId
        )
        url = self.s3.generate_presigned_get_url(object_key)
        if not url:
            raise HTTPException(status_code=404, detail="Could not generate view URL")
        return jsonResponse({"viewUrl": url}, key="presignedUrl")

    def delete_user_profile_image(self, authorization_header: str | None):
        user = self._resolve_current_user(authorization_header)
        object_key_prefix = (
            user.profileImagekey
            or S3KeyConstants.USER_PROFILE_IMAGE.format(user_id=user.userId)
        )
        self.s3.delete_objects_by_prefix(object_key_prefix)
        self.user_repo.updateUserProfile(str(user.userId), {"profileImagekey": None})
        return jsonResponse({"message": "Profile image deleted successfully"}, key="data")

    def get_clothes_upload_url(self, authorization_header: str | None, clothes_id: str, content_type: str):
        user = self._resolve_current_user(authorization_header)
        clothes = self.clothes_repo.getClothesById(clothes_id, str(user.userId))
        if not clothes:
            raise HTTPException(status_code=404, detail="Clothes not found")

        object_key = S3KeyConstants.CLOTHES_IMAGE.format(clothes_id=clothes_id)
        url_data = self.s3.generate_presigned_put_url(object_key, content_type)
        if not url_data:
            raise HTTPException(status_code=500, detail="Could not generate upload URL")

        return jsonResponse(url_data, key="presignedUrl")

    def get_clothes_view_url(self, authorization_header: str | None, clothes_id: str):
        user = self._resolve_current_user(authorization_header)
        clothes = self.clothes_repo.getClothesById(clothes_id, str(user.userId))
        if not clothes:
            raise HTTPException(status_code=404, detail="Clothes not found")

        object_key = S3KeyConstants.CLOTHES_IMAGE.format(clothes_id=clothes_id)
        url = self.s3.generate_presigned_get_url(object_key)
        if not url:
            raise HTTPException(status_code=404, detail="Could not generate view URL")
        return jsonResponse({"viewUrl": url}, key="presignedUrl")

    def delete_clothes_image(self, authorization_header: str | None, clothes_id: str):
        user = self._resolve_current_user(authorization_header)
        clothes = self.clothes_repo.getClothesById(clothes_id, str(user.userId))
        if not clothes:
            raise HTTPException(status_code=404, detail="Clothes not found")

        object_key_prefix = S3KeyConstants.CLOTHES_IMAGE.format(clothes_id=clothes_id)
        self.s3.delete_objects_by_prefix(object_key_prefix)
        return jsonResponse({"message": "Clothes image deleted successfully"}, key="data")
