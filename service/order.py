from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from database.db import get_db, SessionLocal
from database.models import FoodBasket, Order
from service.get_user import GETUSER
from utils.JWT import JWTBearer


class OrderService(GETUSER):
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        super().__init__(token=token, session=session)

    def create_order(self, address_id: int, food_basket_id: int):
        if not self.user_id:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
               
        food_basket = self.session.query(FoodBasket).filter(FoodBasket.user_id == self.user_id).all()
        if not food_basket:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        for item in food_basket:
            new_order = Order(
                status="Pending",
                user_id=self.user_id,
                address_id=address_id,
                food_basket_id=item.id
            )
            self.session.add(new_order)

        self.session.commit()

        return new_order.id
    
    def get_order(self, address_id: int):
        if not self.user_id:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        orders = self.session.query(Order).options(
            joinedload(Order.food_basket),
            joinedload(Order.address),
        ).filter(Order.user_id == self.user_id, Order.address_id == address_id).all()

        if not orders:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        return dict(zip(range(1, len(orders) + 1), orders))