from repositories.fitsRepository import FitsRepository
from utils.jsonReturnUtil import (
    jsonResponse,
)
from botocore.exceptions import (
    ClientError,
)


class FitsUsecase:
    def __init__(self, fitRepo: FitsRepository):
        self.db = fitRepo  # This would be the FitRepository instance

    def getAllFits(self):
        try:
            fits = self.db.getAllFits()
            return jsonResponse(fits, key="fits")
        except ClientError as err:
            # Handle specific client errors or re-raise
            raise err
        except Exception as e:
            # Handle other potential exceptions
            raise e

    # Add other use case methods here (e.g., create_fit, get_fit_by_id, update_fit, delete_fit)
