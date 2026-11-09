"""Pick the number of clusters using the elbow method and silhouette score."""

import pandas as pd
from sklearn.metrics import silhouette_score

from retail_segmentation.model import FEATURE_COLUMNS, build_pipeline


def score_k_range(rfm: pd.DataFrame, k_min: int, k_max: int, random_state: int = 42) -> pd.DataFrame:
    """Fit K-means for each k in [k_min, k_max] and record inertia + silhouette.

    Inertia (for the elbow plot) always decreases as k grows, so it can't
    pick k on its own; silhouette score (higher is better, range -1..1)
    penalizes overlapping clusters and is used to break the tie.
    """
    X = rfm[FEATURE_COLUMNS]
    records = []
    for k in range(k_min, k_max + 1):
        pipeline = build_pipeline(k, random_state)
        labels = pipeline.fit_predict(X)
        X_transformed = pipeline[:-1].transform(X)  # everything except the final KMeans step
        records.append(
            {
                "k": k,
                "inertia": pipeline.named_steps["kmeans"].inertia_,
                "silhouette": silhouette_score(X_transformed, labels),
            }
        )
    return pd.DataFrame(records)


def best_k(scores: pd.DataFrame) -> int:
    """Return the k with the highest silhouette score."""
    return int(scores.loc[scores["silhouette"].idxmax(), "k"])
