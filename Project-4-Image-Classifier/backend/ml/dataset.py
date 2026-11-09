"""Loads a labeled image folder into feature/label arrays for training.

Expects the layout produced by scripts/organize_dataset.py:

    data/raw/
        cat/*.jpg
        dog/*.jpg
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from ml.features import extract_features, load_image

CLASSES = ("cat", "dog")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_dataset(data_dir: Path) -> tuple[np.ndarray, np.ndarray]:
    """Walk data_dir/<class>/* and return (X, y) with y as class-name strings."""
    features: list[np.ndarray] = []
    labels: list[str] = []

    for class_name in CLASSES:
        class_dir = data_dir / class_name
        if not class_dir.is_dir():
            raise FileNotFoundError(
                f"Expected a '{class_name}' folder inside {data_dir}. "
                "Run scripts/organize_dataset.py first — see backend/data/README.md."
            )
        image_paths = sorted(p for p in class_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
        if not image_paths:
            raise FileNotFoundError(f"No images found in {class_dir}.")

        for image_path in image_paths:
            image = load_image(str(image_path))
            features.append(extract_features(image))
            labels.append(class_name)

    return np.stack(features), np.array(labels)
