"""Trains an SVM classifier on the cat/dog dataset and saves it to backend/models/model.joblib.

Usage (from the backend/ directory, with the venv active):
    python -m ml.train
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from ml.dataset import load_dataset

BACKEND_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = BACKEND_DIR / "data" / "raw"
DEFAULT_MODEL_PATH = BACKEND_DIR / "models" / "model.joblib"
DEFAULT_METRICS_PATH = BACKEND_DIR / "models" / "metrics.json"

PARAM_GRID = {
    "svc__C": [1, 10, 100],
    "svc__gamma": ["scale", 0.01, 0.001],
    "svc__kernel": ["rbf"],
}


def train(data_dir: Path, model_path: Path, metrics_path: Path, cv: int) -> None:
    print(f"Loading images from {data_dir} ...")
    X, y = load_dataset(data_dir)
    print(f"Loaded {len(y)} images, feature dimension {X.shape[1]}.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("svc", SVC(probability=True, class_weight="balanced")),
        ]
    )

    search = GridSearchCV(pipeline, PARAM_GRID, cv=cv, n_jobs=-1, verbose=2)
    print("Running grid search over SVM hyperparameters ...")
    search.fit(X_train, y_train)

    print(f"Best params: {search.best_params_}")
    best_model = search.best_estimator_

    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    print(f"Test accuracy: {accuracy:.4f}")
    print(classification_report(y_test, y_pred))

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, model_path)
    metrics_path.write_text(
        json.dumps(
            {"accuracy": accuracy, "best_params": search.best_params_, "report": report},
            indent=2,
        )
    )
    print(f"Saved model to {model_path}")
    print(f"Saved metrics to {metrics_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--metrics-path", type=Path, default=DEFAULT_METRICS_PATH)
    parser.add_argument("--cv", type=int, default=3, help="Cross-validation folds for grid search")
    args = parser.parse_args()
    train(args.data_dir, args.model_path, args.metrics_path, args.cv)


if __name__ == "__main__":
    main()
