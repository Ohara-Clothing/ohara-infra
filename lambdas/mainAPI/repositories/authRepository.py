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

    def updateUserConfirmationStatus(self, username: str):
        user = self.db.query(UserEntity).filter(UserEntity.username == username).first()
        if user:
            user.confirmed = True
            self.db.commit()
            self.db.refresh(user)
        return user

    def deleteUser(self, user_id: str):
        user = self.db.query(UserEntity).filter(UserEntity.userId == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
