"""FastAPI app exposing the cat/dog SVM classifier over HTTP."""

from __future__ import annotations

import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from app import inference
from app.config import settings
from app.schemas import HealthResponse, PredictionResponse

app = FastAPI(
    title="Cat vs Dog Classifier",
    description="Classical SVM (HOG + colour histogram features) served over a REST API.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", model_loaded=inference.is_model_available())


@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(file: UploadFile = File(...)) -> PredictionResponse:
    if not inference.is_model_available():
        raise HTTPException(
            status_code=503, detail="Model not trained yet. Run `python -m ml.train`."
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported file type. Use JPEG, PNG or WebP.")

    contents = await file.read()
    if len(contents) > settings.max_upload_bytes:
        max_mb = settings.max_upload_bytes // (1024 * 1024)
        raise HTTPException(status_code=413, detail=f"File too large (max {max_mb}MB).")

    try:
        image = Image.open(io.BytesIO(contents))
        image.load()
        image = image.convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file.") from exc

    return PredictionResponse(**inference.predict(image))
