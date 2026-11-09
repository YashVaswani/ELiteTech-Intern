"""
train_model.py
==============
End-to-end script that trains a Linear Regression model on the cleaned
Housing dataset, evaluates it on a held-out test set, persists the trained
artefacts (model + scaler), and generates three diagnostic plots.

Workflow
--------
1. Load cleaned CSV  →  2. Define X / y  →  3. Train / Test split
4. Scale features    →  5. Fit model     →  6. Evaluate (MAE, MSE, RMSE, R²)
7. Save model & scaler  →  8. Generate plots

Author : Housing-Price-Prediction team
Date   : 2026-07-21
"""
# Imports

import os                       # For constructing OS-agnostic file paths
import numpy as np              # Numerical operations (e.g. sqrt)
import pandas as pd             # Data loading and manipulation

# Scikit-learn utilities
from sklearn.model_selection import train_test_split   # Validation
from sklearn.preprocessing import StandardScaler       # Feature scaling
from sklearn.linear_model import LinearRegression      # Base Model
from sklearn.metrics import (                          # Evaluation metrics
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

import joblib                   # Efficient serialisation for sklearn objects
import matplotlib.pyplot as plt # Plotting library
from utils import haversine_distance # Shared distance calculation

# Path configuration – everything is relative to the *project root*,
# which is assumed to be one directory above this script's location.

# __file__ resolves to  <project_root>/src/train_model.py
# os.path.dirname twice gives us <project_root>
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Input data
CLEANED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "Housing_cleaned_geo.csv")

# Output directories / files
MODELS_DIR  = os.path.join(PROJECT_ROOT, "models")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

MODEL_PATH  = os.path.join(MODELS_DIR, "linear_regression_model.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")

ACTUAL_VS_PRED_PLOT = os.path.join(REPORTS_DIR, "actual_vs_predicted.png")
RESIDUALS_PLOT      = os.path.join(REPORTS_DIR, "residuals_distribution.png")
FEATURE_IMP_PLOT    = os.path.join(REPORTS_DIR, "feature_importance.png")

def load_data(filepath: str) -> pd.DataFrame:
    """Read the cleaned CSV into a pandas DataFrame."""
    print(f"[INFO] Loading cleaned data from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"[INFO] Dataset shape: {df.shape}  ({df.shape[0]} rows × {df.shape[1]} columns)")
    return df

# 2. Feature / Target Definition

def define_features_and_target(df: pd.DataFrame):
    """Separate the DataFrame into a feature matrix X and target vector y."""

    # Calculate distance to Indore center
    INDORE_LAT = 22.7196
    INDORE_LNG = 75.8577
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['distance_to_center_km'] = haversine_distance(
            df['latitude'], df['longitude'], INDORE_LAT, INDORE_LNG
        )
    else:
        # Fallback if somehow using old dataset
        df['distance_to_center_km'] = 0.0

    feature_columns = [
        "area",
        "bedrooms",
        "bathrooms",
        "distance_to_center_km",
    ]

    target_column = "price"

    X = df[feature_columns]
    y = df[target_column]

    print(f"[INFO] Features ({len(feature_columns)}): {feature_columns}")
    print(f"[INFO] Target: {target_column}")
    return X, y

def split_data(X: pd.DataFrame, y: pd.Series, test_size: float = 0.20, random_state: int = 42):
    """Split features and target into training and testing subsets."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
    )
    print(f"[INFO] Training set size : {X_train.shape[0]} samples")
    print(f"[INFO] Testing  set size : {X_test.shape[0]} samples")
    return X_train, X_test, y_train, y_test

def scale_features(X_train: pd.DataFrame, X_test: pd.DataFrame):
    """Apply StandardScaler so every feature has mean ≈ 0 and std ≈ 1."""
    scaler = StandardScaler()

    # fit_transform: learns mean/std from training data AND applies the transform
    X_train_scaled = scaler.fit_transform(X_train)

    # transform only: uses the *training* mean/std — no information from test set
    X_test_scaled = scaler.transform(X_test)

    print("[INFO] Features scaled with StandardScaler (fit on train set only).")
    return X_train_scaled, X_test_scaled, scaler

def train_model(X_train_scaled: np.ndarray, y_train: pd.Series):
    """Fit an Ordinary Least Squares (OLS) Linear Regression model."""
    print("[INFO] Training LinearRegression model...")
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    print("[INFO] Linear Regression model trained successfully.")
    
    return model

def evaluate_model(model, X_test_scaled: np.ndarray, y_test: pd.Series):
    """Compute and print regression evaluation metrics on the test set."""
    # Generate predictions on the unseen test set
    y_pred = model.predict(X_test_scaled)

    # Calculate each metric
    mae  = mean_absolute_error(y_test, y_pred)
    mse  = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)  # sklearn ≥1.4 deprecated squared param; manual sqrt is safest
    r2   = r2_score(y_test, y_pred)

    metrics = {
        "MAE":      mae,
        "MSE":      mse,
        "RMSE":     rmse,
        "R² Score": r2,
    }

    # ── Pretty-print the results ──
    print("\n" + "=" * 55)
    print("       MODEL EVALUATION METRICS (Test Set)")
    print("=" * 55)
    print(f"  Mean Absolute Error  (MAE)  : {mae:,.2f}")
    print(f"  Mean Squared Error   (MSE)  : {mse:,.2f}")
    print(f"  Root Mean Sq. Error  (RMSE) : {rmse:,.2f}")
    print(f"  R² Score                    : {r2:.4f}")
    print("=" * 55 + "\n")

    return y_pred, metrics

def save_artefacts(model, scaler, model_path: str, scaler_path: str):
    """Persist the trained model and the fitted scaler to disk."""
    # Create the models/ directory if it does not exist yet
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    joblib.dump(model, model_path)
    print(f"[INFO] Trained model saved to : {model_path}")

    joblib.dump(scaler, scaler_path)
    print(f"[INFO] Fitted scaler saved to : {scaler_path}")

def plot_actual_vs_predicted(y_test: pd.Series, y_pred: np.ndarray, save_path: str):
    """Scatter plot of Actual vs Predicted prices."""
    plt.style.use("seaborn-v0_8-whitegrid")  # Clean, modern style
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(y_test, y_pred, alpha=0.6, edgecolors="k", linewidths=0.5,
               color="#4C72B0", label="Predictions")

    # Reference line: y = x (perfect predictions)
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], color="red",
            linestyle="--", linewidth=2, label="Ideal (y = x)")

    ax.set_xlabel("Actual Price", fontsize=13)
    ax.set_ylabel("Predicted Price", fontsize=13)
    ax.set_title("Actual vs Predicted Housing Prices", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11)
    fig.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"[INFO] Plot saved: {save_path}")


def plot_residuals_distribution(y_test: pd.Series, y_pred: np.ndarray, save_path: str):
    """Histogram of residuals (errors = actual − predicted)."""
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(8, 6))

    residuals = y_test.values - y_pred  # Positive → under-predicted

    ax.hist(residuals, bins=30, color="#55A868", edgecolor="black",
            alpha=0.75)

    # Draw a vertical line at zero for reference
    ax.axvline(x=0, color="red", linestyle="--", linewidth=2, label="Zero Error")

    ax.set_xlabel("Residual (Actual − Predicted)", fontsize=13)
    ax.set_ylabel("Frequency", fontsize=13)
    ax.set_title("Distribution of Prediction Residuals", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11)
    fig.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"[INFO] Plot saved: {save_path}")


def plot_feature_importance(model, feature_names: list, save_path: str):
    """Horizontal bar chart of feature importance based on linear coefficients."""
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 7))

    coefficients = model.coef_

    # Sort features by absolute coefficient (most important first)
    sorted_indices = np.argsort(np.abs(coefficients))
    sorted_coefs = coefficients[sorted_indices]
    sorted_names = [feature_names[i] for i in sorted_indices]

    colors = ["#C44E52" if c < 0 else "#4C72B0" for c in sorted_coefs]
    ax.barh(sorted_names, sorted_coefs, color=colors, edgecolor="black",
            linewidth=0.5)

    ax.set_xlabel("Coefficient Value (Standardised)", fontsize=13)
    ax.set_ylabel("Feature", fontsize=13)
    ax.set_title("Feature Importance (Linear Regression)",
                 fontsize=15, fontweight="bold")

    # Add a vertical line at zero for clarity
    ax.axvline(x=0, color="grey", linestyle="-", linewidth=0.8)
    fig.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"[INFO] Plot saved: {save_path}")

def main():
    """Execute the full training pipeline."""
    df = load_data(CLEANED_DATA_PATH)
    X, y = define_features_and_target(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    model = train_model(X_train_scaled, y_train)
    y_pred, metrics = evaluate_model(model, X_test_scaled, y_test)
    
    save_artefacts(model, scaler, MODEL_PATH, SCALER_PATH)

    # Generate and save diagnostic plots
    plot_actual_vs_predicted(y_test, y_pred, ACTUAL_VS_PRED_PLOT)
    plot_residuals_distribution(y_test, y_pred, RESIDUALS_PLOT)
    
    feature_cols = X.columns.tolist()
    plot_feature_importance(model, feature_cols, FEATURE_IMP_PLOT)

    print("\n[SUCCESS] Training pipeline completed successfully!")

if __name__ == "__main__":
    main()
