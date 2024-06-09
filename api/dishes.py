from typing import List, Optional

from fastapi import Depends, APIRouter, status

from scheme import scheme
from service.dishes import DishesService
from utils.JWT import JWTBearer

router = APIRouter(
    prefix='/backet',
    tags=['backet'],
)


@router.get('/get_all_dishes',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
def get_address(
        dishes_service: DishesService = Depends()
):
    return dishes_service.get_nutrition(flag=True)

@router.get('/get_products',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
def get_address(
        dishes_service: DishesService = Depends()
):
    return dishes_service.get_nutrition(flag=False)


@router.put('/add_dish_to_basket',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_201_CREATED)
def add_dish_to_basket(
        item_id,
        quantity,
        dishes_service: DishesService = Depends()
):
    dishes_service.add_dish_to_basket(item_id, quantity)


@router.patch('/update_quantity_in_basket',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_204_NO_CONTENT)
def update_quantity_in_basket(
        item_id,
        new_quantity,
        dishes_service: DishesService = Depends()
):
    dishes_service.update_quantity_in_basket(item_id, new_quantity)


@router.delete('/remove_from_basket',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_204_NO_CONTENT)
def remove_from_basket(
        item_id,
        dishes_service: DishesService = Depends()
):
    dishes_service.remove_from_basket(item_id)


@router.get('/get_basket',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
def get_basket(
        dishes_service: DishesService = Depends()
):
    return dishes_service.get_basket()