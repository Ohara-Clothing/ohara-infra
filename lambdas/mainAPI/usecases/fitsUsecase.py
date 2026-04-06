from fastapi import HTTPException
from botocore.exceptions import ClientError
from utils.jsonReturnUtil import jsonResponse
from repositories.fitsRepository import FitsRepository
from models.dtos.fit import FitCreate, FitUpdate

class FitsUsecase:
    def __init__(self, fitRepo: FitsRepository):
        self.repo = fitRepo

    def getAllFits(self):
        try:
            fits = self.repo.getAllFits()
            return jsonResponse(fits, key="fits")
        except ClientError as err:
            raise err
        except Exception as e:
            raise e

    def createFit(self, fit: FitCreate):
        try:
            new_fit = self.repo.createFit(fit)
            return jsonResponse(new_fit, key="fit")
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    def updateFit(self, fit_id: str, fit: FitUpdate):
        try:
            updated_fit = self.repo.updateFit(fit_id, fit)
            if not updated_fit:
                raise HTTPException(status_code=404, detail="Fit not found")
            return jsonResponse(updated_fit, key="fit")
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))

    def deleteFit(self, fit_id: str):
        try:
            deleted_fit = self.repo.deleteFit(fit_id)
            if not deleted_fit:
                raise HTTPException(status_code=404, detail="Fit not found")
            return jsonResponse({"message": "Fit deleted successfully"}, key="data")
        except Exception as err:
            raise HTTPException(status_code=400, detail=str(err))