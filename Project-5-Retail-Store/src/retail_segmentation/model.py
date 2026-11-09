"""Build, train, and persist the K-means clustering pipeline.

Uses scikit-learn's KMeans directly rather than a hand-rolled implementation
- it's the standard, well-tested tool for this job (k-means++ init, multiple
restarts, optimized Lloyd's algorithm), so there is nothing to gain from
reimplementing it.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

FEATURE_COLUMNS = ["recency", "frequency", "monetary"]


def build_pipeline(n_clusters: int, random_state: int = 42) -> Pipeline:
    """Log-transform, standardize, then cluster RFM features with K-means.

    Recency/Frequency/Monetary are all right-skewed (a few customers spend
    far more or order far more often than the rest); log1p compresses that
    skew so those outliers don't single-handedly define the clusters.
    Scaling afterward is still required because the three features remain on
    different numeric scales, which would otherwise dominate the distance
    metric K-means uses.
    """
    return Pipeline(
        steps=[
            ("log", FunctionTransformer(np.log1p, feature_names_out="one-to-one")),
            ("scaler", StandardScaler()),
            (
                "kmeans",
                KMeans(n_clusters=n_clusters, init="k-means++", n_init=10, random_state=random_state),
            ),
        ]
    )


def train(rfm: pd.DataFrame, n_clusters: int, random_state: int = 42) -> Pipeline:
    """Fit the pipeline on RFM features and return it."""
    pipeline = build_pipeline(n_clusters, random_state)
    pipeline.fit(rfm[FEATURE_COLUMNS])
    return pipeline


def save_pipeline(pipeline: Pipeline, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, path)


def load_pipeline(path: str) -> Pipeline:
    return joblib.load(path)
