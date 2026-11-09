import io

import numpy as np
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from PIL import Image, UnidentifiedImageError
from starlette.concurrency import run_in_threadpool

from app.api.deps import get_prediction_service
from app.schemas.prediction import PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter(tags=["predict"])

EMPTY_RESPONSE = PredictionResponse(gesture=None, confidence=None, landmarks=None)


def _decode_image(data: bytes) -> np.ndarray:
    try:
        return np.array(Image.open(io.BytesIO(data)).convert("RGB"))
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail="Could not decode image") from exc


@router.post("/predict/image", response_model=PredictionResponse)
async def predict_image(
    file: UploadFile = File(...),
    service: PredictionService = Depends(get_prediction_service),
) -> PredictionResponse:
    image_rgb = _decode_image(await file.read())
    result = await run_in_threadpool(service.predict, image_rgb)
    return result if result is not None else EMPTY_RESPONSE


@router.websocket("/predict/stream")
async def predict_stream(
    websocket: WebSocket,
    service: PredictionService = Depends(get_prediction_service),
) -> None:
    """Client sends raw JPEG/PNG bytes per frame; server replies with one
    PredictionResponse JSON per frame."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            try:
                image_rgb = _decode_image(data)
            except HTTPException:
                continue
            result = await run_in_threadpool(service.predict, image_rgb)
            await websocket.send_json((result or EMPTY_RESPONSE).model_dump())
    except WebSocketDisconnect:
        pass
