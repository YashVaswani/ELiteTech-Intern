from pathlib import Path

import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

MODEL_PATH = Path(__file__).parent / "artifacts" / "hand_landmarker.task"


class HandLandmarkExtractor:
    """Wraps MediaPipe's HandLandmarker task. Not thread-safe per instance —
    callers must serialize access (see PredictionService)."""

    def __init__(self, num_hands: int = 1) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"{MODEL_PATH} not found. Run `python -m app.ml.download_model` first."
            )
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
            running_mode=RunningMode.IMAGE,
            num_hands=num_hands,
        )
        self._landmarker = HandLandmarker.create_from_options(options)

    def extract(self, image_rgb: np.ndarray) -> list[list[tuple[float, float, float]]]:
        """Returns one list of 21 (x, y, z) landmarks per detected hand."""
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        result = self._landmarker.detect(mp_image)
        return [[(lm.x, lm.y, lm.z) for lm in hand] for hand in result.hand_landmarks]
