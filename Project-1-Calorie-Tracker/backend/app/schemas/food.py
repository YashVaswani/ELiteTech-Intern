from pydantic import BaseModel


class NutritionInfo(BaseModel):
    food_name: str
    serving_grams: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float


class PredictionCandidate(BaseModel):
    food_name: str
    confidence: float


class PredictionResult(BaseModel):
    top_prediction: PredictionCandidate
    alternatives: list[PredictionCandidate]
    nutrition: NutritionInfo


class FoodItemOut(BaseModel):
    food_name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
