from fastapi import HTTPException
from fastapi import status, Depends
from sqlalchemy import and_

from database import models
from database.db import SessionLocal, get_db
from scheme import scheme
from service.get_user import GETUSER
from utils.JWT import JWTBearer


class AddressService(GETUSER):

    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        super().__init__(token=token, session=session)

    def add_address(
            self,
            payload: scheme.Address
    ):
        user = self._get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        addr = self.session.query(models.Address).filter(and_(
            models.Address.user_id == self.user_id,
            models.Address.address == str.lower(payload.address)
        )).first()
        if addr is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="address already exist"
            )

        new_address = models.Address()
        new_address.user_id = self.user_id
        new_address.address = str.lower(payload.address)

        self.session.add(new_address)
        self.session.commit()
        self.session.refresh(user)

    def get_address(
            self,
    ):
        user = self._get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        addr = self.session.query(models.Address).filter(
            models.Address.user_id == self.user_id
        ).all()
        if addr is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="addresses not found"
            )
        return addr

    def delete_address(
            self,
            payload: scheme.Address
    ):
        user = self._get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        addr = self.session.query(models.Address).filter(and_(
            models.Address.user_id == self.user_id,
            models.Address.address == str.lower(payload.address)
        )).first()
        if addr is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="address not found"
            )

        self.session.delete(addr)
        self.session.commit()
        self.session.refresh(user)
