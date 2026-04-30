from fastapi import HTTPException
from botocore.exceptions import ClientError
from utils.jsonReturnUtil import jsonResponse
from repositories.clothesRepository import ClothesRepository
from repositories.authRepository import AuthRepository
from models.dtos.clothes import ClothesCreate, ClothesUpdate
from services.AWS.s3Service import AWS_S3
from utils.jwtUtil import usernameFromAccessToken

class ClothesUsecase:
    def __init__(
        self,
        clothesRepo: ClothesRepository,
        userRepo: AuthRepository,
        s3_service: AWS_S3 | None = None,
    ):
        self.repo = clothesRepo
        self.user_repo = userRepo
        self.s3 = s3_service or AWS_S3()

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

    async def getClothesUsecase(self, authorization_header: str | None):
        try:
            user = self._resolve_current_user(authorization_header)
            clothes = self.repo.getUserClothes(str(user.userId))
            return jsonResponse(clothes, key="clothes")
        except HTTPException:
            raise
        except ClientError as err:
            raise err

    async def createClothes(self, clothes: ClothesCreate, authorization_header: str | None):
        try:
            user = self._resolve_current_user(authorization_header)
            new_clothes = self.repo.createClothes(clothes, str(user.userId))
            return jsonResponse(new_clothes, key="clothes")
        except HTTPException:
            raise
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    async def updateClothes(
        self, clothes_id: str, clothes: ClothesUpdate, authorization_header: str | None
    ):
        try:
            user = self._resolve_current_user(authorization_header)
            updated_clothes = self.repo.updateClothes(clothes_id, clothes, str(user.userId))
            if not updated_clothes:
                raise HTTPException(status_code=404, detail="Clothes not found")
            return jsonResponse(updated_clothes, key="clothes")
        except HTTPException:
            raise
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    async def deleteClothes(self, clothes_id: str, authorization_header: str | None):
        try:
            user = self._resolve_current_user(authorization_header)
            clothes = self.repo.getClothesById(clothes_id, str(user.userId))
            if not clothes:
                raise HTTPException(status_code=404, detail="Clothes not found")

            self.s3.delete_objects_by_prefix(f"clothes/{clothes_id}/")
            deleted_clothes = self.repo.deleteClothes(clothes_id, str(user.userId))
            if not deleted_clothes:
                raise HTTPException(status_code=404, detail="Clothes not found")
            return jsonResponse({"message": "Clothes deleted successfully"}, key="data")
        except HTTPException:
            raise
        except ClientError as err:
            raise HTTPException(status_code=500, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))
