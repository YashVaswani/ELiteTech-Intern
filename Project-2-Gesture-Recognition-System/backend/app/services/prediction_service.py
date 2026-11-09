import threading

import numpy as np

from app.ml.classifier import GestureClassifier
from app.ml.features import landmarks_to_feature_vector
from app.ml.landmarks import HandLandmarkExtractor
from app.schemas.prediction import Landmark, PredictionResponse


class PredictionService:
    def __init__(self) -> None:
        self._extractor = HandLandmarkExtractor()
        self._classifier = GestureClassifier()
        self._lock = threading.Lock()  # HandLandmarker isn't thread-safe

    def predict(self, image_rgb: np.ndarray) -> PredictionResponse | None:
        with self._lock:
            hands = self._extractor.extract(image_rgb)
            if not hands:
                return None
            landmarks = hands[0]
            features = landmarks_to_feature_vector(landmarks)
            gesture, confidence = self._classifier.predict(features)

        return PredictionResponse(
            gesture=gesture,
            confidence=confidence,
            landmarks=[Landmark(x=x, y=y, z=z) for x, y, z in landmarks],
        )
