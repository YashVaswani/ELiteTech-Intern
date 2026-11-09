import io

import numpy as np
import pytest
from PIL import Image


class StubModel:
    """Stands in for the trained SVM so API tests don't need a real model file."""

    classes_ = np.array(["cat", "dog"])

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        return np.array([[0.2, 0.8]] * len(features))


@pytest.fixture
def stub_model(monkeypatch):
    from app import inference

    monkeypatch.setattr(inference, "is_model_available", lambda: True)
    inference.get_model.cache_clear()
    monkeypatch.setattr(inference, "get_model", lambda: StubModel())
    return StubModel()


@pytest.fixture
def sample_image_bytes() -> bytes:
    image = Image.new("RGB", (128, 128), color=(120, 80, 40))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()
