from datetime import datetime

from fastapi import HTTPException
from fastapi import status, Depends

from database import models
from database.db import SessionLocal, get_db
from scheme import scheme
from utils import hash_pwd
from utils.JWT import JWTBearer


class UserService:

    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        self.token = token
        self.user_id = JWTBearer.decodeJWT(token).get("user_id")
        self.session = session

    def __get_user_by_id(
            self
    ):
        user = self.session.query(models.User).get(self.user_id)
        if user is not None:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not authenticated',
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_me(
            self
    ):
        return self.__get_user_by_id()

    def delete_me(
            self,
    ):
        user = self.__get_user_by_id()
        self.session.delete(user)
        self.session.commit()

    def update_email(
            self,
            payload: scheme.UpdateUserEmailSchema
    ):
        user = self.__get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if payload.email is not None:
            user_email = self.session.query(models.User).filter(models.User.email == payload.email).first()
            if (user_email is not None) and (payload.email == user_email.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Email already exist',
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user.email = payload.email

        user.updated_at = datetime.now()

        self.session.commit()
        self.session.refresh(user)

    def update_password(
            self,
            payload: scheme.UpdateUserPasswordSchema
    ):
        user = self.__get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if payload.password is not None:
            if hash_pwd.verify_password(payload.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='The old password has been entered',
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user.password = hash_pwd.hash_password(payload.password)

        user.updated_at = datetime.now()

        self.session.commit()
        self.session.refresh(user)