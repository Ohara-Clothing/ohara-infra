from fastapi import HTTPException
from botocore.exceptions import ClientError
from models.dtos.user import (
    UserCreate,
    UserLogin,
    UserConfirm,
    UserConfirmPasswordChange,
    UserDelete,
    UserProfileUpdate,
)
from models.dtos.user import User
from fastapi.responses import JSONResponse
from utils.jsonReturnUtil import jsonResponse
from utils.jwtUtil import (
    usernameFromIdToken,
    userIdFromIdToken,
    emailFromIdToken,
    usernameFromAccessToken,
    userIdFromAccessToken,
)
from utils.cookieUtil import createRefreshTokenCookie, deleteRefreshTokenCookie
from repositories.authRepository import AuthRepository
from services.AWS.s3Service import AWS_S3


class AuthUsecase:
    def __init__(self, cognito_service, userRepo: AuthRepository, s3_service: AWS_S3 | None = None):
        self.auth = cognito_service
        self.repo = userRepo
        self.s3 = s3_service or AWS_S3()

    def listUsers(self):
        try:
            users = self.auth.listUsers()
            return jsonResponse(users, key="users")
        except ClientError as err:
            raise err

    def createUser(self, credentials: UserCreate):
        try:
            user = self.auth.createUser(credentials)

            try:
                user_data = User(
                    userId=user["UserSub"],
                    username=credentials.username,
                    email=credentials.email,
                )
                self.repo.upsertUser(user_data)
            except Exception as sync_err:
                print(f"Warning: could not sync local user row after Cognito signup: {sync_err}")

            return jsonResponse(user, key="user")

        except ClientError as err:
            raise err

    def confirmUser(self, credentials: UserConfirm):
        try:
            user = self.auth.confirmUser(credentials)
            self.repo.updateUserConfirmationStatus(credentials.username)

            return jsonResponse(user, key="user")
        except ClientError as err:
            raise err

    def loginUser(self, credentials: UserLogin):
        try:
            loginResponse = self.auth.loginUser(credentials)
            token = loginResponse["AuthenticationResult"]

            idToken = token["IdToken"]
            username = usernameFromIdToken(idToken)
            user_id = userIdFromIdToken(idToken)
            email = emailFromIdToken(idToken)
            if username and user_id:
                user = self.repo.getUserByUsername(username) or self.repo.getUserByEmail(email or "")
                if not user:
                    if not email:
                        cognito_user = self.auth.getUser(username)
                        user_attributes = {
                            attr["Name"]: attr["Value"]
                            for attr in cognito_user.get("UserAttributes", [])
                        }
                        email = user_attributes.get("email")

                    if not email:
                        raise HTTPException(
                            status_code=400,
                            detail="Could not determine user email from Cognito token",
                        )

                    self.repo.upsertUser(
                        User(
                            userId=user_id,
                            username=username,
                            email=email,
                        )
                    )

            response = JSONResponse(
                content={
                    "accessToken": token["AccessToken"],
                    "idToken": idToken,
                    "expiration": token["ExpiresIn"],
                    "username": username,
                }
            )

            refreshToken = token["RefreshToken"]
            createRefreshTokenCookie(response, refreshToken)

            return response

        except ClientError as err:
            raise err

    def refreshAccessToken(self, refresh_token):
        try:
            loginResponse = self.auth.refreshAccessToken(refresh_token)
            token = loginResponse["AuthenticationResult"]

            idToken = token["IdToken"]
            username = usernameFromIdToken(idToken)

            response = JSONResponse(
                content={
                    "accessToken": token["AccessToken"],
                    "idToken": idToken,
                    "expiration": token["ExpiresIn"],
                    "username": username,
                }
            )

            return response

        except ClientError as err:
            raise err

    def forgotPassword(self, username):
        try:
            user = self.auth.forgotPassword(username)
            return jsonResponse(user, key="user")

        except ClientError as err:
            raise err

    def confirmForgotPassword(self, credentials: UserConfirmPasswordChange):
        try:
            user = self.auth.confirmForgotPassword(credentials)
            return jsonResponse(user, key="user")

        except ClientError as err:
            raise err

    def deleteUser(self, credentials: UserDelete):
        try:
            user_data = self.auth.getUser(credentials.username)
            user_id = user_data["UserAttributes"][2]["Value"]
            user = self.repo.getUserById(user_id)

            if user:
                if user.profileImagekey:
                    self.s3.delete_objects_by_prefix(user.profileImagekey)

                for clothes in user.clothes:
                    self.s3.delete_objects_by_prefix(f"clothes/{clothes.clothesId}/")

            userDelete = self.auth.deleteUserCognito(credentials.accessCode)
            self.repo.deleteUser(user_id)

            return jsonResponse(userDelete, key="user")

        except ClientError as err:
            raise err

    def logoutUser(self, accessToken):
        try:
            response = self.auth.logoutUser(accessToken)
            deleteRefreshTokenCookie(
                response=JSONResponse(content={"message": "Logout successful"})
            )

            return response

        except ClientError as err:
            raise err

    def _resolve_current_user(self, authorization_header: str | None):
        if not authorization_header or not authorization_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authorization token")

        access_token = authorization_header.removeprefix("Bearer ").strip()
        username = usernameFromAccessToken(access_token)
        if not username:
            raise HTTPException(status_code=401, detail="Invalid authorization token")

        user = self.repo.getUserByUsername(username)
        if not user:
            fallback_user_id = userIdFromAccessToken(access_token)
            if fallback_user_id:
                user = self.repo.getUserById(fallback_user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def getMyProfile(self, authorization_header: str | None):
        try:
            user = self._resolve_current_user(authorization_header)
            return jsonResponse(user, key="user")
        except HTTPException:
            raise
        except ClientError as err:
            raise err

    def updateMyProfile(self, authorization_header: str | None, profile: UserProfileUpdate):
        try:
            user = self._resolve_current_user(authorization_header)
            update_data = profile.model_dump(exclude_unset=True)
            updated_user = self.repo.updateUserProfile(str(user.userId), update_data)
            if not updated_user:
                raise HTTPException(status_code=404, detail="User not found")
            return jsonResponse(updated_user, key="user")
        except HTTPException:
            raise
        except ClientError as err:
            raise err
