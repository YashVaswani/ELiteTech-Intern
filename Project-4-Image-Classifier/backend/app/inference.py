"""Loads the trained SVM pipeline once and serves predictions from it."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib
from PIL import Image

from ml.features import extract_features

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "model.joblib"


def is_model_available() -> bool:
    return MODEL_PATH.exists()


@lru_cache(maxsize=1)
def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No trained model at {MODEL_PATH}. Run `python -m ml.train` in backend/ first."
        )
    return joblib.load(MODEL_PATH)


def predict(image: Image.Image) -> dict:
    model = get_model()
    features = extract_features(image).reshape(1, -1)
    probabilities = model.predict_proba(features)[0]
    classes = model.classes_
    best_index = probabilities.argmax()
    return {
        "label": str(classes[best_index]),
        "confidence": float(probabilities[best_index]),
        "probabilities": {
            str(class_name): float(probability)
            for class_name, probability in zip(classes, probabilities, strict=True)
        },
    }
