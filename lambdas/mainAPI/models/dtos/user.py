from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class User(BaseModel):
    userId: str
    username: str
    email: EmailStr
    createdAt: datetime = Field(default_factory=datetime.now)
    confirmed: bool = False
    description: Optional[str] = None
    style: Optional[str] = None
    favoriteClothesIds: list[str] = Field(default_factory=list)
    pinnedFitIds: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserConfirm(BaseModel):
    username: str
    confirmationCode: str


class UserDelete(BaseModel):
    username: str
    accessCode: str


class UserConfirmPasswordChange(BaseModel):
    username: str
    password: str
    confirmationCode: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserProfileUpdate(BaseModel):
    description: Optional[str] = None
    style: Optional[str] = None
    favoriteClothesIds: Optional[list[str]] = None
    pinnedFitIds: Optional[list[str]] = None


class UserProfileResponse(BaseModel):
    user: User
