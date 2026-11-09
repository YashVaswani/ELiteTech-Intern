"""Collect real hand-landmark training samples from your webcam.

Run: cd backend && python -m training.collect_webcam_data

Hold a gesture in frame and press its number key to label the current
frame's landmarks. Press 'q' to quit. Appends to data/processed/collected.csv
in the same format generate_synthetic_dataset.py produces, so train.py can
mix both real and synthetic data.
"""

import csv
from pathlib import Path

import cv2

from app.ml.gestures import GESTURE_CLASSES
from app.ml.landmarks import HandLandmarkExtractor

OUT_PATH = Path(__file__).parent / "data" / "processed" / "collected.csv"
KEY_TO_GESTURE = {str(i + 1): g for i, g in enumerate(GESTURE_CLASSES)}


def _ensure_header(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    header = ["label"] + [f"{axis}{i}" for i in range(21) for axis in ("x", "y", "z")]
    with path.open("w", newline="") as f:
        csv.writer(f).writerow(header)


def main() -> None:
    _ensure_header(OUT_PATH)
    extractor = HandLandmarkExtractor(num_hands=1)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam (index 0)")

    counts = dict.fromkeys(GESTURE_CLASSES, 0)
    print("Keys:", ", ".join(f"{k}={v}" for k, v in KEY_TO_GESTURE.items()), "| q=quit")

    try:
        while True:
            ok, frame_bgr = cap.read()
            if not ok:
                break
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            hands = extractor.extract(frame_rgb)

            display = frame_bgr.copy()
            if hands:
                h, w = display.shape[:2]
                for x, y, _z in hands[0]:
                    cv2.circle(display, (int(x * w), int(y * h)), 3, (0, 255, 0), -1)

            counts_text = " ".join(f"{g}:{c}" for g, c in counts.items())
            cv2.putText(
                display, counts_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1
            )
            cv2.imshow("collect_webcam_data - number key to label, q to quit", display)

            key = cv2.waitKey(1) & 0xFF
            char = chr(key) if key != 0xFF else ""
            if char == "q":
                break
            if char in KEY_TO_GESTURE:
                if not hands:
                    print("No hand detected - not saved")
                    continue
                label = KEY_TO_GESTURE[char]
                with OUT_PATH.open("a", newline="") as f:
                    row_landmarks = [v for point in hands[0] for v in point]
                    csv.writer(f).writerow([label, *row_landmarks])
                counts[label] += 1
                print(f"Saved {label} (total {counts[label]})")
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
