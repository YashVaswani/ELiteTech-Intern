from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FoodLogCreate(BaseModel):
    food_name: str
    serving_grams: float = Field(gt=0, default=150.0)
    confidence: float | None = None


class FoodLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    food_name: str
    serving_grams: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    confidence: float | None
    logged_at: datetime


class DailySummary(BaseModel):
    date: str
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    goal_calories: float
    entries: list[FoodLogOut]
