"""A minimal procedural hand-pose model used only to bootstrap a synthetic
training set (see generate_synthetic_dataset.py). Produces 21 (x, y, z)
points in the same layout MediaPipe HandLandmarker returns: wrist, then
4 joints each for thumb, index, middle, ring, pinky.

This is a geometric approximation, not real hand data — it exists so the
project has a working classifier out of the box. Replace/augment it with
real recordings via collect_webcam_data.py for production accuracy.
"""

import numpy as np

FINGER_BASE_ANGLES_DEG = {
    "thumb": -55.0,
    "index": -20.0,
    "middle": 0.0,
    "ring": 18.0,
    "pinky": 38.0,
}
FINGER_SEGMENT_LENGTHS = {
    "thumb": (0.18, 0.14, 0.12),
    "index": (0.22, 0.14, 0.11),
    "middle": (0.24, 0.15, 0.12),
    "ring": (0.22, 0.14, 0.11),
    "pinky": (0.18, 0.11, 0.09),
}
PALM_RADIUS = 0.28
FINGER_ORDER = ["thumb", "index", "middle", "ring", "pinky"]


def _build_finger(
    base_angle_deg: float, seg_lengths: tuple, extension: float, rng: np.random.Generator
):
    """extension in [0, 1]: 1 = straight, 0 = fully curled toward the palm."""
    angle = np.radians(base_angle_deg + rng.normal(0, 3))
    pos = np.array([np.sin(angle), -np.cos(angle)]) * PALM_RADIUS
    bend_per_joint = np.radians(95 * (1 - extension) + rng.normal(0, 4))
    points = [pos.copy()]
    for length in seg_lengths:
        angle += bend_per_joint
        direction = np.array([np.sin(angle), -np.cos(angle)])
        pos = pos + direction * length * rng.normal(1.0, 0.03)
        points.append(pos.copy())
    return points  # [MCP, PIP, DIP, TIP]


def generate_landmarks(
    finger_extension: dict, rng: np.random.Generator, rotate_deg: float = 0.0
) -> np.ndarray:
    """finger_extension: {finger_name: extension in [0, 1]}. Returns (21, 3) array."""
    wrist = np.zeros(2)
    landmarks_2d = [wrist]
    for finger in FINGER_ORDER:
        pts = _build_finger(
            FINGER_BASE_ANGLES_DEG[finger],
            FINGER_SEGMENT_LENGTHS[finger],
            finger_extension[finger],
            rng,
        )
        landmarks_2d.extend(pts)

    pts_2d = np.array(landmarks_2d)
    if rotate_deg:
        theta = np.radians(rotate_deg)
        rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        pts_2d = pts_2d @ rot.T

    z = rng.normal(0, 0.02, size=(pts_2d.shape[0], 1))
    return np.hstack([pts_2d, z])
