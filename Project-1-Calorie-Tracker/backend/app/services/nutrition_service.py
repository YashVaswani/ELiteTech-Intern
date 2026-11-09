import json
from functools import lru_cache
from pathlib import Path

from app.schemas.food import FoodItemOut, NutritionInfo

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "nutrition.json"


@lru_cache
def _load_table() -> dict[str, dict[str, float]]:
    with DATA_PATH.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def normalize_food_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def list_foods() -> list[FoodItemOut]:
    table = _load_table()
    return [
        FoodItemOut(
            food_name=name,
            calories_per_100g=values["calories"],
            protein_per_100g=values["protein_g"],
            carbs_per_100g=values["carbs_g"],
            fat_per_100g=values["fat_g"],
        )
        for name, values in sorted(table.items())
    ]


def get_nutrition_for_grams(food_name: str, grams: float) -> NutritionInfo:
    table = _load_table()
    key = normalize_food_name(food_name)
    values = table.get(key)
    if values is None:
        raise KeyError(f"Unknown food: {food_name}")

    factor = grams / 100.0
    return NutritionInfo(
        food_name=key,
        serving_grams=grams,
        calories=round(values["calories"] * factor, 1),
        protein_g=round(values["protein_g"] * factor, 1),
        carbs_g=round(values["carbs_g"] * factor, 1),
        fat_g=round(values["fat_g"] * factor, 1),
    )


def is_known_food(food_name: str) -> bool:
    return normalize_food_name(food_name) in _load_table()
