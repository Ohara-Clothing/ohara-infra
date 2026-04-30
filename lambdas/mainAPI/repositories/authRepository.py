from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.entities.user import UserEntity
from models.dtos.user import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def putUser(self, user_data: User):
        new_user = UserEntity(
            userId=user_data.userId, username=user_data.username, email=user_data.email
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def upsertUser(self, user_data: User):
        user = (
            self.getUserById(user_data.userId)
            or self.getUserByEmail(user_data.email)
            or self.getUserByUsername(user_data.username)
        )
        if user:
            user.username = user_data.username
            user.email = user_data.email
            self.db.commit()
            self.db.refresh(user)
            return user

        try:
            return self.putUser(user_data)
        except IntegrityError:
            self.db.rollback()
            user = self.getUserByEmail(user_data.email) or self.getUserByUsername(user_data.username)
            if not user:
                raise

            user.username = user_data.username
            user.email = user_data.email
            self.db.commit()
            self.db.refresh(user)
            return user

    def updateUserConfirmationStatus(self, username: str):
        user = self.db.query(UserEntity).filter(UserEntity.username == username).first()
        if user:
            user.confirmed = True
            self.db.commit()
            self.db.refresh(user)
        return user

    def getUserByUsername(self, username: str):
        return self.db.query(UserEntity).filter(UserEntity.username == username).first()

    def getUserByEmail(self, email: str):
        return self.db.query(UserEntity).filter(UserEntity.email == email).first()

    def getUserById(self, user_id: str):
        return self.db.query(UserEntity).filter(UserEntity.userId == user_id).first()

    def deleteUser(self, user_id: str):
        user = self.db.query(UserEntity).filter(UserEntity.userId == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
        return user

    def updateUserProfile(self, user_id: str, profile_data: dict):
        user = self.getUserById(user_id)
        if not user:
            return None

        for key, value in profile_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user
