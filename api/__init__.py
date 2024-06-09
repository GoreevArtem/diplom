from fastapi import APIRouter

from . import auth, user, address, dishes

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(address.router)
router.include_router(dishes.router)