from fastapi import APIRouter

from . import auth, user, address, dishes, recipe, image, order

router = APIRouter()
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(address.router)
router.include_router(dishes.router)
router.include_router(recipe.router)
router.include_router(order.router)
router.include_router(image.router)