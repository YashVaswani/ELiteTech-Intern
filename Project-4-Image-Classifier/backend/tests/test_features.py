import numpy as np
from PIL import Image

from ml.features import extract_features, feature_vector_size


def test_feature_vector_is_fixed_length():
    black = Image.new("RGB", (200, 150), color=(0, 0, 0))
    white = Image.new("RGB", (64, 64), color=(255, 255, 255))

    black_features = extract_features(black)
    white_features = extract_features(white)

    assert black_features.shape == white_features.shape
    assert black_features.shape[0] == feature_vector_size()


def test_feature_vector_distinguishes_different_images():
    red = Image.new("RGB", (128, 128), color=(255, 0, 0))
    blue = Image.new("RGB", (128, 128), color=(0, 0, 255))

    assert not np.allclose(extract_features(red), extract_features(blue))
