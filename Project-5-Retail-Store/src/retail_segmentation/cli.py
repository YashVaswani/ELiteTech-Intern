"""Command-line entry point: `retail-segment train` / `retail-segment predict`.

Plain argparse (standard library) is enough for two subcommands - no need
for a third-party CLI framework.
"""

import argparse
from pathlib import Path

import pandas as pd

from retail_segmentation.config import load_config
from retail_segmentation.data import generate_synthetic_transactions, load_transactions
from retail_segmentation.evaluate import best_k, score_k_range
from retail_segmentation.features import compute_rfm
from retail_segmentation.model import FEATURE_COLUMNS, load_pipeline, save_pipeline, train
from retail_segmentation.segments import label_segments, segment_summary
from retail_segmentation.viz import plot_clusters_pca, plot_k_selection


def run_train(cfg: dict) -> None:
    raw_path = Path(cfg["data"]["raw_path"])
    if raw_path.exists():
        print(f"Loading existing transactions from {raw_path}")
        transactions = load_transactions(str(raw_path))
    else:
        print(f"No transaction file found, generating synthetic data at {raw_path}")
        transactions = generate_synthetic_transactions(
            n_customers=cfg["data"]["n_customers"],
            snapshot_date=cfg["data"]["snapshot_date"],
            random_state=cfg["random_state"],
        )
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        transactions.to_csv(raw_path, index=False)

    rfm = compute_rfm(transactions, snapshot_date=cfg["data"]["snapshot_date"])
    Path(cfg["features"]["processed_path"]).parent.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(cfg["features"]["processed_path"], index=False)
    print(f"Computed RFM features for {len(rfm)} customers -> {cfg['features']['processed_path']}")

    k_min, k_max = cfg["model"]["k_range"]
    scores = score_k_range(rfm, k_min, k_max, random_state=cfg["random_state"])
    k = best_k(scores)
    print(f"Evaluated k={k_min}..{k_max}; best k by silhouette score = {k}")
    plot_k_selection(scores, f"{cfg['reports']['figures_dir']}/k_selection.png")
    Path(cfg["reports"]["k_scores_path"]).parent.mkdir(parents=True, exist_ok=True)
    scores.to_csv(cfg["reports"]["k_scores_path"], index=False)

    pipeline = train(rfm, n_clusters=k, random_state=cfg["random_state"])
    save_pipeline(pipeline, cfg["model"]["artifact_path"])
    print(f"Saved trained pipeline -> {cfg['model']['artifact_path']}")

    rfm["cluster"] = pipeline.named_steps["kmeans"].labels_
    labeled = label_segments(rfm)
    labeled.to_csv(cfg["model"]["labeled_output_path"], index=False)
    print(f"Saved segmented customers -> {cfg['model']['labeled_output_path']}")

    transformed = pipeline[:-1].transform(labeled[FEATURE_COLUMNS])
    plot_clusters_pca(transformed, labeled["cluster"], f"{cfg['reports']['figures_dir']}/clusters_pca.png")

    print("\nSegment summary:")
    print(segment_summary(labeled).to_string(index=False))


def run_predict(cfg: dict, recency: float, frequency: float, monetary: float) -> None:
    pipeline = load_pipeline(cfg["model"]["artifact_path"])
    labeled = pd.read_csv(cfg["model"]["labeled_output_path"])

    row = pd.DataFrame([{"recency": recency, "frequency": frequency, "monetary": monetary}])
    cluster = int(pipeline.predict(row[FEATURE_COLUMNS])[0])

    segment_by_cluster = labeled.drop_duplicates("cluster").set_index("cluster")["segment"]
    segment = segment_by_cluster.get(cluster, f"Segment {cluster}")
    print(f"cluster={cluster} segment={segment}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="retail-segment", description=__doc__)
    parser.add_argument("--config", default=None, help="Path to config.yaml (default: configs/config.yaml)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("train", help="Run the full pipeline: data -> RFM -> K-means -> segments")

    predict_parser = subparsers.add_parser("predict", help="Assign a segment to one customer's RFM values")
    predict_parser.add_argument("--recency", type=float, required=True, help="Days since last purchase")
    predict_parser.add_argument("--frequency", type=float, required=True, help="Number of orders")
    predict_parser.add_argument("--monetary", type=float, required=True, help="Total amount spent")

    args = parser.parse_args()
    cfg = load_config(args.config) if args.config else load_config()

    if args.command == "train":
        run_train(cfg)
    elif args.command == "predict":
        run_predict(cfg, args.recency, args.frequency, args.monetary)


if __name__ == "__main__":
    main()
