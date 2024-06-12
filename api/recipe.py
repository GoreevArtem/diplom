from typing import Dict
from fastapi import APIRouter, status

from scheme.scheme import Recipe
from database.db import post_singleton

router = APIRouter(
    prefix='/recipes',
    tags=['recipes'],
)

# Создание нового рецепта
@router.post("/create_recipe", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
async def create_recipe(recipe: Recipe):
    return post_singleton.add_post(recipe)

# Получение рецептов
@router.get("/get_all_recipes",
            status_code=status.HTTP_200_OK
            )
async def get_recipes():
    return post_singleton.get_posts()

@router.get("/get_recipe/{recipe_id}",
            status_code=status.HTTP_200_OK,
            )
async def get_recipes(recipe_id: str):
    return post_singleton.get_post(recipe_id)


# Обновление рецепта
@router.patch("/update_recipe/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_recipe(recipe_id: str, recipe: Recipe):
    return post_singleton.update_post(recipe_id, recipe)

# Удаление рецепта
@router.delete("/delete_recipe/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def  delete_recipe(recipe_id: str):
    return post_singleton.delete_post(recipe_id)

# Удаление всех постов
@router.delete("/delete_all_recipes", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_recipe():
    return post_singleton.delete_all_posts()