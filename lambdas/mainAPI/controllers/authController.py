from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException
from botocore.exceptions import ClientError
from models.dtos.user import (
    UserConfirmPasswordChange,
    UserCreate,
    UserLogin,
    UserConfirm,
    UserDelete,
)

from usecases.authUsecase import AuthUsecase
from repositories.authRepository import AuthRepository
from services.AWS.cognitoService import AWS_Cognito
from db import get_db

authRouter = APIRouter()

@authRouter.get("/getUsers")
async def getUser(
    cognito: AWS_Cognito = Depends(AWS_Cognito), db: Session = Depends(get_db)
):
    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.listUsers()
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)


@authRouter.post("/createUser")
async def createUser(
    credentials: UserCreate,
    cognito: AWS_Cognito = Depends(AWS_Cognito),
    db: Session = Depends(get_db),
):
    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.createUser(credentials)
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)


@authRouter.post("/confirmUser")
async def confirmUser(
    credentials: UserConfirm,
    cognito: AWS_Cognito = Depends(AWS_Cognito),
    db: Session = Depends(get_db),
):
    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.confirmUser(credentials)
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)


@authRouter.post("/login")
async def loginUser(
    credentials: UserLogin,
    cognito: AWS_Cognito = Depends(AWS_Cognito),
    db: Session = Depends(get_db),
):
    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.loginUser(credentials)
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)


@authRouter.post("/logout")
async def logoutUser(
    accessToken: str,
    cognito: AWS_Cognito = Depends(AWS_Cognito),
    db: Session = Depends(get_db),
):
    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.logoutUser(accessToken)
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)


@authRouter.post("/refreshToken")
async def refreshToken(
    request: Request,
    cognito: AWS_Cognito = Depends(AWS_Cognito),
    db: Session = Depends(get_db),
):
    refreshToken = request.cookies.get("refresh_token")

    if not refreshToken:
        raise HTTPException(status_code=401, detail="No Refresh Token")

    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.refreshAccessToken(refreshToken)
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)


@authRouter.post("/deleteUser")
async def deleteUser(
    credentials: UserDelete,
    cognito: AWS_Cognito = Depends(AWS_Cognito),
    db: Session = Depends(get_db),
):
    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.deleteUser(credentials)
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)


@authRouter.post("/forgetPass")
async def forgetPass(
    username: str,
    cognito: AWS_Cognito = Depends(AWS_Cognito),
    db: Session = Depends(get_db),
):
    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.forgotPassword(username)
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)


@authRouter.post("/forgetPassConfirm")
async def confirmForgetPass(
    credentials: UserConfirmPasswordChange,
    cognito: AWS_Cognito = Depends(AWS_Cognito),
    db: Session = Depends(get_db),
):
    try:
        repo = AuthRepository(db)
        uc = AuthUsecase(cognito, repo)
        return uc.confirmForgotPassword(credentials)
    except ClientError as err:
        errorMessage = err.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=errorMessage)