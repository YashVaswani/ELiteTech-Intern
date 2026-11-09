from functools import lru_cache

from app.services.prediction_service import PredictionService


@lru_cache
def get_prediction_service() -> PredictionService:
    return PredictionService()
