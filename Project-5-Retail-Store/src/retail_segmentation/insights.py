"""Shared, plotting-library-agnostic analysis helpers.

Kept separate from `viz.py` (which depends on matplotlib) so the API layer
can reuse this logic without pulling in a plotting dependency it doesn't
otherwise need.
"""

import numpy as np
from sklearn.decomposition import PCA


def pca_2d(transformed_features) -> tuple[np.ndarray, np.ndarray]:
    """Project the model's (log + scaled) feature space onto 2 components.

    Using the same transformed space K-means clusters on - rather than raw
    RFM values - keeps this consistent with what the model actually saw.
    Returns (coordinates, explained_variance_ratio_per_component).
    """
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(transformed_features)
    return coords, pca.explained_variance_ratio_
