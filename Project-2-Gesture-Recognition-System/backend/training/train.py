"""Train the gesture classifier from collected/synthetic landmark CSVs.

Run: cd backend && python -m training.train
"""

import csv
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split

from app.ml.features import landmarks_to_feature_vector

DATA_DIR = Path(__file__).parent / "data" / "processed"
OUTPUT_DIR = Path(__file__).parent / "outputs"
MODEL_PATH = Path(__file__).parents[1] / "app" / "ml" / "artifacts" / "gesture_classifier.joblib"


def _load_csv(path: Path) -> tuple[list, list]:
    if not path.exists():
        return [], []
    labels, features = [], []
    with path.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header[0] == "label"
        for row in reader:
            label = row[0]
            values = np.array(row[1:], dtype=np.float32).reshape(21, 3)
            labels.append(label)
            features.append(landmarks_to_feature_vector(values))
    return features, labels


def main() -> None:
    X: list = []
    y: list = []
    for csv_path in (DATA_DIR / "synthetic.csv", DATA_DIR / "collected.csv"):
        feats, labels = _load_csv(csv_path)
        X.extend(feats)
        y.extend(labels)
        if feats:
            print(f"Loaded {len(feats)} rows from {csv_path.name}")

    if not X:
        raise SystemExit(
            "No training data found. Run `python -m training.generate_synthetic_dataset` first."
        )

    X_arr, y_arr = np.array(X), np.array(y)
    print(f"Total: {len(X_arr)} samples across {len(set(y_arr))} classes")

    X_train, X_test, y_train, y_test = train_test_split(
        X_arr, y_arr, test_size=0.2, random_state=42, stratify=y_arr
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "classification_report.txt").write_text(report)

    try:
        import matplotlib.pyplot as plt

        ConfusionMatrixDisplay.from_predictions(y_test, y_pred, xticks_rotation=45)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=150)
        plt.close()
    except ImportError:
        print("matplotlib not installed - skipping confusion matrix plot")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model -> {MODEL_PATH}")


if __name__ == "__main__":
    main()
