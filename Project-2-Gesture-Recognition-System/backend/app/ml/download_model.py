"""Download the MediaPipe HandLandmarker model asset.

Free, Apache-2.0-licensed model hosted by Google as part of the open-source
MediaPipe project. ~8MB, downloaded once into app/ml/artifacts/.
"""

import urllib.request
from pathlib import Path

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)
DEST = Path(__file__).parent / "artifacts" / "hand_landmarker.task"


def main() -> None:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.exists():
        print(f"Already present: {DEST}")
        return
    print(f"Downloading {MODEL_URL} -> {DEST}")
    urllib.request.urlretrieve(MODEL_URL, DEST)
    print("Done.")


if __name__ == "__main__":
    main()
