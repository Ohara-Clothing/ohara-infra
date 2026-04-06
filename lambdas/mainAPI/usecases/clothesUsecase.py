from fastapi import HTTPException
from botocore.exceptions import ClientError
from utils.jsonReturnUtil import jsonResponse
from repositories.clothesRepository import ClothesRepository
from models.dtos.clothes import ClothesCreate, ClothesUpdate

class ClothesUsecase:
    def __init__(self, clothesRepo: ClothesRepository):
        self.repo = clothesRepo

    async def getClothesUsecase(self):
        try:
            clothes = self.repo.getUserClothes()
            return jsonResponse(clothes, key="clothes")
        except ClientError as err:
            raise err

    async def createClothes(self, clothes: ClothesCreate):
        try:
            new_clothes = self.repo.createClothes(clothes)
            return jsonResponse(new_clothes, key="clothes")
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    async def updateClothes(self, clothes_id: str, clothes: ClothesUpdate):
        try:
            updated_clothes = self.repo.updateClothes(clothes_id, clothes)
            if not updated_clothes:
                raise HTTPException(status_code=404, detail="Clothes not found")
            return jsonResponse(updated_clothes, key="clothes")
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    async def deleteClothes(self, clothes_id: str):
        try:
            deleted_clothes = self.repo.deleteClothes(clothes_id)
            if not deleted_clothes:
                raise HTTPException(status_code=404, detail="Clothes not found")
            return jsonResponse({"message": "Clothes deleted successfully"}, key="data")
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))