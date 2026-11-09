from pydantic import BaseModel


class Landmark(BaseModel):
    x: float
    y: float
    z: float


class PredictionResponse(BaseModel):
    gesture: str | None
    confidence: float | None
    landmarks: list[Landmark] | None
