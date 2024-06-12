import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse


router = APIRouter(
    prefix='/images',
    tags=['images'],
)

@router.get("/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join("images", image_name)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path, media_type="image/jpeg")