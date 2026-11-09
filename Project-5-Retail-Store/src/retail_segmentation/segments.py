"""Turn anonymous cluster ids into business-readable segment names.

K-means only outputs cluster indices (0, 1, 2, ...); this ranks clusters by
a simple RFM value score and maps them onto descriptive labels a store
manager can act on. Pure ranking arithmetic - no extra model needed.
"""

import pandas as pd

# Ordered from most to least valuable. Extra clusters beyond this list fall
# back to a generic "Segment N" label instead of guessing a business meaning.
_LABELS_BEST_TO_WORST = [
    "Champions",
    "Loyal Customers",
    "Potential Loyalists",
    "New Customers",
    "At Risk",
    "Hibernating",
]


def label_segments(rfm_with_cluster: pd.DataFrame) -> pd.DataFrame:
    """Add a `segment` column derived from each cluster's average RFM profile."""
    stats = rfm_with_cluster.groupby("cluster")[["recency", "frequency", "monetary"]].mean()

    z = (stats - stats.mean()) / stats.std(ddof=0).replace(0, 1)
    # Higher frequency/monetary and lower recency (days since last order) = more valuable.
    value_score = z["frequency"] + z["monetary"] - z["recency"]
    ranked_clusters = value_score.sort_values(ascending=False).index.tolist()

    label_map = {}
    for rank, cluster_id in enumerate(ranked_clusters):
        label_map[cluster_id] = (
            _LABELS_BEST_TO_WORST[rank] if rank < len(_LABELS_BEST_TO_WORST) else f"Segment {rank + 1}"
        )

    # A single best-to-worst rank can't tell "new" from "low-value": both
    # have below-average frequency/monetary, but a new customer is also
    # *recent*. Re-tag any such cluster explicitly, unless that would
    # collide with a label another cluster already holds.
    medians = rfm_with_cluster[["recency", "frequency", "monetary"]].median()
    is_recent_but_light = (
        (stats["recency"] < medians["recency"])
        & (stats["frequency"] < medians["frequency"])
        & (stats["monetary"] < medians["monetary"])
    )
    for cluster_id, flagged in is_recent_but_light.items():
        if flagged and "New Customers" not in label_map.values():
            label_map[cluster_id] = "New Customers"

    result = rfm_with_cluster.copy()
    result["segment"] = result["cluster"].map(label_map)
    return result


def segment_summary(labeled: pd.DataFrame) -> pd.DataFrame:
    """One row per segment: customer count and average RFM, sorted by value."""
    summary = (
        labeled.groupby("segment")
        .agg(
            customers=("customer_id", "count"),
            avg_recency_days=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
        )
        .round(1)
        .sort_values("avg_monetary", ascending=False)
    )
    return summary.reset_index()
