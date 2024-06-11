from typing import Dict, Union
from fastapi import APIRouter, status

from scheme.scheme import Recipe
from database.db import post_singleton

router = APIRouter(
    prefix='/recipes',
    tags=['recipes'],
)

# Создание нового рецепта
@router.post("/recipes", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
def create_recipe(recipe: Recipe):
    return post_singleton.add_post(recipe)

# Получение рецептов
@router.get("/recipes",
            status_code=status.HTTP_200_OK,
            response_model=Dict[int, Recipe]
            )
def get_recipes():
    return post_singleton.get_posts()

@router.get("/recipe",
            status_code=status.HTTP_200_OK,
            response_model=Recipe
            )
def get_recipes(recipe_id: str):
    return post_singleton.get_post(recipe_id)


# Обновление рецепта
@router.put("/recipes", status_code=status.HTTP_204_NO_CONTENT)
def update_recipe(recipe_id: str,
 recipe: Recipe):
    return post_singleton.update_post(recipe_id, recipe)

# Удаление рецепта
@router.delete("/recipes", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: str):
    return post_singleton.delete_post(recipe_id)