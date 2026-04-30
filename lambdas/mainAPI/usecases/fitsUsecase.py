from fastapi import HTTPException
from botocore.exceptions import ClientError
from utils.jsonReturnUtil import jsonResponse
from repositories.fitsRepository import FitsRepository
from repositories.authRepository import AuthRepository
from models.dtos.fit import FitCreate, FitUpdate, FitClothesUpdate
from utils.jwtUtil import userIdFromAccessToken, usernameFromAccessToken

class FitsUsecase:
    def __init__(self, fitRepo: FitsRepository, userRepo: AuthRepository):
        self.repo = fitRepo
        self.user_repo = userRepo

    def getAllFits(self, authorization_header: str | None):
        try:
            user = self._resolve_current_user(authorization_header)
            fits = self.repo.getAllFits(str(user.userId))
            fits_payload = []
            for fit in fits:
                fits_payload.append(
                    {
                        "fitId": str(fit.fitId),
                        "userId": str(fit.userId),
                        "name": fit.name,
                        "description": fit.description,
                        "createdAt": fit.createdAt,
                        "clothes": [
                            {
                                "clothesId": str(fit_clothes.clothes.clothesId),
                                "clothesType": fit_clothes.clothes.clothesType,
                                "color": fit_clothes.clothes.color,
                                "size": fit_clothes.clothes.size,
                                "brand": fit_clothes.clothes.brand,
                                "price": fit_clothes.clothes.price,
                            }
                            for fit_clothes in fit.fit_clothes
                            if fit_clothes.clothes
                        ],
                    }
                )
            return jsonResponse(fits_payload, key="fits")
        except ClientError as err:
            raise err
        except HTTPException:
            raise
        except Exception as e:
            raise e

    def createFit(self, fit: FitCreate, authorization_header: str | None):
        try:
            if not authorization_header or not authorization_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing authorization token")

            access_token = authorization_header.removeprefix("Bearer ").strip()
            username = usernameFromAccessToken(access_token)
            if not username:
                raise HTTPException(status_code=401, detail="Invalid authorization token")

            user = self.user_repo.getUserByUsername(username)
            if not user:
                fallback_user_id = userIdFromAccessToken(access_token)
                if fallback_user_id:
                    user = self.user_repo.getUserById(fallback_user_id)

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            new_fit = self.repo.createFit(fit, str(user.userId))
            return jsonResponse(new_fit, key="fit")
        except HTTPException:
            raise
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    def _resolve_current_user(self, authorization_header: str | None):
        if not authorization_header or not authorization_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authorization token")

        access_token = authorization_header.removeprefix("Bearer ").strip()
        username = usernameFromAccessToken(access_token)
        if not username:
            raise HTTPException(status_code=401, detail="Invalid authorization token")

        user = self.user_repo.getUserByUsername(username)
        if not user:
            fallback_user_id = userIdFromAccessToken(access_token)
            if fallback_user_id:
                user = self.user_repo.getUserById(fallback_user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def updateFit(self, fit_id: str, fit: FitUpdate, authorization_header: str | None):
        try:
            self._resolve_current_user(authorization_header)
            updated_fit = self.repo.updateFit(fit_id, fit)
            if not updated_fit:
                raise HTTPException(status_code=404, detail="Fit not found")
            return jsonResponse(updated_fit, key="fit")
        except HTTPException:
            raise
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    def deleteFit(self, fit_id: str, authorization_header: str | None):
        try:
            self._resolve_current_user(authorization_header)
            deleted_fit = self.repo.deleteFit(fit_id)
            if not deleted_fit:
                raise HTTPException(status_code=404, detail="Fit not found")
            return jsonResponse({"message": "Fit deleted successfully"}, key="data")
        except HTTPException:
            raise
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    def setFitClothes(self, fit_id: str, payload: FitClothesUpdate, authorization_header: str | None):
        try:
            self._resolve_current_user(authorization_header)
            updated_fit = self.repo.setFitClothes(fit_id, payload.clothesIds)
            if not updated_fit:
                raise HTTPException(status_code=404, detail="Fit not found")
            return jsonResponse({"message": "Fit clothes updated successfully"}, key="data")
        except HTTPException:
            raise
        except ValueError as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))
