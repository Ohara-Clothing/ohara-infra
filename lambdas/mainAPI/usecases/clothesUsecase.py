from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from utils.jsonReturnUtil import jsonResponse


class ClothesUsecase:
    def __init__(self, clothesRepo):
        self.repo = clothesRepo

    async def getClothesUsecase(self):
        try:
            clothes = self.repo.getUserClothes()
            return jsonResponse(clothes, key="clothes")
        except ClientError as err:
            raise err
