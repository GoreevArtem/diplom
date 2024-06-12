from fastapi import APIRouter, Depends, status
from service import order
from utils.JWT import JWTBearer

router = APIRouter(
    prefix='/order',
    tags=['order'],
)

@router.put('/create_order',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_201_CREATED)
def create_order(
        address_id: int,
        food_basket_id: int,
        order_service: order.OrderService = Depends()
):
    return order_service.create_order(address_id, food_basket_id)

@router.get('/get_order',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK)
def get_basket(
        address_id: int,
        order_service: order.OrderService = Depends()
):
    return order_service.get_order(address_id)