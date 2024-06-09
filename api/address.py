from typing import Dict, List, Optional

from fastapi import Depends, APIRouter, status

from scheme import scheme
from service.address import AddressService
from utils.JWT import JWTBearer

router = APIRouter(
    prefix='/address',
    tags=['address'],
)


@router.get('/get_addresses',
            dependencies=[Depends(JWTBearer())],
            status_code=status.HTTP_200_OK,
            response_model=Optional[Dict[int, scheme.Address]])
def get_address(
        address_service: AddressService = Depends()
):
    return address_service.get_address()


@router.put(
    '/add_address',
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_201_CREATED)
def add_address(
        payload: scheme.Address,
        address_service: AddressService = Depends()
):
    address_service.add_address(payload)


@router.delete(
    '/delete_address',
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
        payload: scheme.Address,
        address_service: AddressService = Depends()
):
    address_service.delete_address(payload)
