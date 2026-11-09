from pathlib import Path

import joblib
import numpy as np

MODEL_PATH = Path(__file__).parent / "artifacts" / "gesture_classifier.joblib"


class GestureClassifier:
    def __init__(self) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"{MODEL_PATH} not found. Run backend/training/train.py first.")
        self._model = joblib.load(MODEL_PATH)

    def predict(self, feature_vector: np.ndarray) -> tuple[str, float]:
        proba = self._model.predict_proba([feature_vector])[0]
        idx = int(np.argmax(proba))
        return str(self._model.classes_[idx]), float(proba[idx])
