from fastapi import Depends, APIRouter, status

from service.dishes import DishesService
from utils.JWT import JWTBearer

router = APIRouter(
    prefix='/backet',
    tags=['backet'],
)

@router.get('/get_all_nutrition',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
def get_products(
        flag: bool,
        dishes_service: DishesService = Depends()
):
    return dishes_service.get_nutrition(flag=flag)


@router.put('/add_nutrition_to_basket',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_201_CREATED)
def add_nutrition_to_basket(
        flag: bool,
        item_id: float,
        quantity: int,
        dishes_service: DishesService = Depends()
):
    dishes_service.add_nutrition_to_basket(flag=flag, item_id=item_id, quantity=quantity)


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