from fastapi import APIRouter

from app.ml.gestures import GESTURE_CLASSES

router = APIRouter(tags=["gestures"])


@router.get("/gestures")
def list_gestures() -> dict[str, list[str]]:
    return {"gestures": GESTURE_CLASSES}
