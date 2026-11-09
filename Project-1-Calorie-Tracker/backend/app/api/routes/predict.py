from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.core.config import get_settings
from app.schemas.food import PredictionResult
from app.services.prediction_service import predict_food

router = APIRouter(prefix="/api", tags=["prediction"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/predict", response_model=PredictionResult)
async def predict(
    image: UploadFile = File(...),
    serving_grams: float | None = Form(default=None),
) -> PredictionResult:
    settings = get_settings()

    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported image type: {image.content_type}",
        )

    contents = await image.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image exceeds {settings.max_upload_mb}MB limit",
        )

    try:
        return predict_food(contents, serving_grams)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc
