import numpy as np


def landmarks_to_feature_vector(landmarks) -> np.ndarray:
    """Turn 21 (x, y, z) hand landmarks into a translation- and scale-invariant
    feature vector: wrist-relative coordinates, scaled by the largest
    displacement. Used identically at training time and inference time so the
    classifier always sees the same feature space."""
    pts = np.asarray(landmarks, dtype=np.float32)
    pts = pts - pts[0]
    scale = np.abs(pts).max()
    if scale > 0:
        pts = pts / scale
    return pts.flatten()
