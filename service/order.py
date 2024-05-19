from fastapi import Depends

from database.db import get_db, SessionLocal
from service.get_user import GETUSER
from utils.JWT import JWTBearer


class OrderService(GETUSER):
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        super().__init__(token=token, session=session)





