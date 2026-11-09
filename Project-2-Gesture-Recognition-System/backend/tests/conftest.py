import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_prediction_service
from app.main import app
from app.schemas.prediction import Landmark, PredictionResponse


class FakePredictionService:
    def predict(self, image_rgb: np.ndarray) -> PredictionResponse | None:
        return PredictionResponse(
            gesture="open_palm",
            confidence=0.99,
            landmarks=[Landmark(x=0.0, y=0.0, z=0.0) for _ in range(21)],
        )


@pytest.fixture
def client():
    app.dependency_overrides[get_prediction_service] = lambda: FakePredictionService()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
