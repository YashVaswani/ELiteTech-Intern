"""Save the two plots a reviewer needs to trust the clustering: how k was
chosen, and what the resulting clusters look like."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: never try to open a GUI window
import matplotlib.pyplot as plt
import pandas as pd

from retail_segmentation.insights import pca_2d


def plot_k_selection(scores: pd.DataFrame, out_path: str) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    ax1.plot(scores["k"], scores["inertia"], marker="o")
    ax1.set_title("Elbow method")
    ax1.set_xlabel("k (clusters)")
    ax1.set_ylabel("Inertia")

    ax2.plot(scores["k"], scores["silhouette"], marker="o", color="darkorange")
    ax2.set_title("Silhouette score")
    ax2.set_xlabel("k (clusters)")
    ax2.set_ylabel("Silhouette score")

    fig.tight_layout()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_clusters_pca(transformed_features, cluster_labels, out_path: str) -> None:
    """Project the model's (log + scaled) feature space to 2D with PCA.

    Projecting the raw RFM values would let Monetary's much larger scale
    dominate both axes; using the same transformed space the pipeline
    clusters on keeps the plot consistent with what K-means actually saw.
    """
    coords, variance_ratio = pca_2d(transformed_features)

    fig, ax = plt.subplots(figsize=(6, 5))
    scatter = ax.scatter(coords[:, 0], coords[:, 1], c=cluster_labels, cmap="tab10", s=12, alpha=0.7)
    ax.set_title("Customer segments (PCA projection)")
    ax.set_xlabel(f"PC1 ({variance_ratio[0]:.0%} variance)")
    ax.set_ylabel(f"PC2 ({variance_ratio[1]:.0%} variance)")
    legend = ax.legend(*scatter.legend_elements(), title="Cluster", loc="best", fontsize=8)
    ax.add_artist(legend)

    fig.tight_layout()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
