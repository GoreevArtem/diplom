from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from database.db import get_db, SessionLocal
from database.models import Item, FoodBasket
from service.get_user import GETUSER
from utils.JWT import JWTBearer



class DishesService(GETUSER):
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db)
    ):
        super().__init__(token=token, session=session)

    def _serialize_basket(self, basket):
        serialized_basket = []
        for ordered_product in basket:
            item = ordered_product.item
            serialized_item = {
                "item_name": item.name,
                "item_calories": item.calories,
                "item_weight": item.weight,
                "item_type": item.type,
                "quantity": ordered_product.quantity
            }
            serialized_basket.append(serialized_item)
        return dict(zip(range(1, len(serialized_basket) + 1), serialized_basket))

    def get_nutrition(self, flag):
        data = self.session.query(Item).filter(Item.is_dish == flag).all()
        return dict(zip(range(1, len(data) + 1), data))
    
    def add_nutrition_to_basket(self, flag, item_id, quantity):
        user = self._get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        
        if self.session.query(Item).filter(Item.id == item_id, Item.is_dish == flag).first():
            ordered_product = self.session.query(FoodBasket).filter(
                FoodBasket.user_id == self.user_id,
                FoodBasket.item_id == item_id
            ).first()
            if ordered_product is None:
                ordered_product = FoodBasket(item_id=item_id, quantity=quantity, user_id = self.user_id)
                self.session.add(ordered_product)
                self.session.commit()
            else:
                ordered_product.quantity = quantity
                self.session.commit()
                self.session.refresh(ordered_product)
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
            
    def update_quantity_in_basket(self, item_id, new_quantity):
        user = self._get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        
        ordered_product = self.session.query(FoodBasket).filter(
            FoodBasket.item_id == item_id,
            FoodBasket.user_id == self.user_id
        ).first()
        if ordered_product:
            ordered_product.quantity = new_quantity
            self.session.commit()
            self.session.refresh(ordered_product)
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    def remove_from_basket(self, item_id):
        user = self._get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        ordered_product = self.session.query(FoodBasket).filter(
            FoodBasket.item_id == item_id,
            FoodBasket.user_id == self.user_id
        ).first()
        if ordered_product:
            self.session.delete(ordered_product)
            self.session.commit()
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        

    def get_basket(self):
        basket = self.session.query(FoodBasket).filter(FoodBasket.user_id == self.user_id).options(joinedload(FoodBasket.item)).all()
        if basket:
            return self._serialize_basket(basket)
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
