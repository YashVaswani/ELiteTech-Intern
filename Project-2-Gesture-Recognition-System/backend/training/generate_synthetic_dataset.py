"""Generate a synthetic landmark dataset so the classifier has something to
train on out of the box. Run collect_webcam_data.py and mix in real samples
for production-grade accuracy — see training/README.md.
"""

import argparse
import csv
from pathlib import Path

import numpy as np

from training.hand_model import generate_landmarks

# extension per finger in [0, 1]: 1.0 = fully extended, ~0.05 = curled into a fist
GESTURE_FINGER_STATES = {
    "open_palm": {"thumb": 1.0, "index": 1.0, "middle": 1.0, "ring": 1.0, "pinky": 1.0},
    "fist": {"thumb": 0.1, "index": 0.05, "middle": 0.05, "ring": 0.05, "pinky": 0.05},
    "thumbs_up": {"thumb": 1.0, "index": 0.05, "middle": 0.05, "ring": 0.05, "pinky": 0.05},
    "thumbs_down": {"thumb": 1.0, "index": 0.05, "middle": 0.05, "ring": 0.05, "pinky": 0.05},
    "peace": {"thumb": 0.2, "index": 1.0, "middle": 1.0, "ring": 0.05, "pinky": 0.05},
    "ok": {"thumb": 0.45, "index": 0.45, "middle": 1.0, "ring": 1.0, "pinky": 1.0},
    "pointing": {"thumb": 0.1, "index": 1.0, "middle": 0.05, "ring": 0.05, "pinky": 0.05},
}
BASE_ROTATION_DEG = {"thumbs_down": 180.0}

OUT_PATH = Path(__file__).parent / "data" / "processed" / "synthetic.csv"


def main(samples_per_class: int) -> None:
    rng = np.random.default_rng(42)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    header = ["label"] + [f"{axis}{i}" for i in range(21) for axis in ("x", "y", "z")]
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for label, states in GESTURE_FINGER_STATES.items():
            base_rotation = BASE_ROTATION_DEG.get(label, 0.0)
            for _ in range(samples_per_class):
                jitter = rng.normal(0, 8)
                landmarks = generate_landmarks(states, rng, rotate_deg=base_rotation + jitter)
                writer.writerow([label, *landmarks.flatten().tolist()])

    print(f"Wrote {samples_per_class * len(GESTURE_FINGER_STATES)} rows -> {OUT_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples-per-class", type=int, default=300)
    args = parser.parse_args()
    main(args.samples_per_class)
