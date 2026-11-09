from app.core.config import get_settings
from app.ml.model import get_classifier
from app.schemas.food import PredictionCandidate, PredictionResult
from app.services.nutrition_service import get_nutrition_for_grams, is_known_food


def predict_food(image_bytes: bytes, serving_grams: float | None = None) -> PredictionResult:
    settings = get_settings()
    grams = serving_grams or settings.default_serving_grams

    classifier = get_classifier()
    predictions = classifier.predict(image_bytes, top_k=settings.ml_top_k)

    known = [(label, conf) for label, conf in predictions if is_known_food(label)]
    if not known:
        raise LookupError(
            f"None of the predicted labels {[p[0] for p in predictions]} have nutrition data"
        )
    top_label, top_conf = known[0]

    nutrition = get_nutrition_for_grams(top_label, grams)

    return PredictionResult(
        top_prediction=PredictionCandidate(food_name=top_label, confidence=round(top_conf, 4)),
        alternatives=[
            PredictionCandidate(food_name=label, confidence=round(conf, 4))
            for label, conf in predictions
            if label != top_label
        ],
        nutrition=nutrition,
    )
