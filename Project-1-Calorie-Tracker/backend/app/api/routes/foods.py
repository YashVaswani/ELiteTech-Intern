from fastapi import APIRouter, HTTPException, status

from app.schemas.food import FoodItemOut, NutritionInfo
from app.services.nutrition_service import get_nutrition_for_grams, list_foods

router = APIRouter(prefix="/api/foods", tags=["foods"])


@router.get("", response_model=list[FoodItemOut])
def get_foods() -> list[FoodItemOut]:
    return list_foods()


@router.get("/{food_name}", response_model=NutritionInfo)
def get_food(food_name: str, grams: float = 100.0) -> NutritionInfo:
    try:
        return get_nutrition_for_grams(food_name, grams)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
