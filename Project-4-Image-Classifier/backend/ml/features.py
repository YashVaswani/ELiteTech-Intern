"""Turns an image into the fixed-length numeric vector the SVM trains and predicts on.

Uses HOG (shape/edge structure) plus per-channel colour histograms (colour
distribution) — a standard, cheap classical-CV feature set. No CNN, no
learned embeddings: everything here is deterministic and library-provided.
"""

from __future__ import annotations

import numpy as np
from PIL import Image
from skimage.color import rgb2gray
from skimage.feature import hog

IMAGE_SIZE = (128, 128)
HOG_ORIENTATIONS = 9
HOG_PIXELS_PER_CELL = (8, 8)
HOG_CELLS_PER_BLOCK = (2, 2)
COLOR_HIST_BINS = 32


def load_image(path: str) -> Image.Image:
    """Load an image file from disk as RGB, resized to the model's input size."""
    return Image.open(path).convert("RGB").resize(IMAGE_SIZE)


def prepare_image(image: Image.Image) -> Image.Image:
    """Normalize an already-open PIL image (e.g. from an upload) to the model's input size."""
    return image.convert("RGB").resize(IMAGE_SIZE)


def extract_features(image: Image.Image) -> np.ndarray:
    """Extract a 1D HOG + colour-histogram feature vector from a resized RGB image."""
    image = prepare_image(image)
    arr = np.asarray(image, dtype=np.float64) / 255.0

    gray = rgb2gray(arr)
    hog_features = hog(
        gray,
        orientations=HOG_ORIENTATIONS,
        pixels_per_cell=HOG_PIXELS_PER_CELL,
        cells_per_block=HOG_CELLS_PER_BLOCK,
        feature_vector=True,
    )

    color_hist = np.concatenate(
        [
            np.histogram(arr[..., channel], bins=COLOR_HIST_BINS, range=(0.0, 1.0))[0]
            for channel in range(3)
        ]
    ).astype(np.float64)
    color_hist /= color_hist.sum() + 1e-9

    return np.concatenate([hog_features, color_hist])


def feature_vector_size() -> int:
    """Return the length of the feature vector produced by extract_features."""
    return extract_features(Image.new("RGB", IMAGE_SIZE)).shape[0]
