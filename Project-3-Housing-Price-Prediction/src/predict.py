"""
predict.py — Standalone Command-Line Housing Price Prediction Script
====================================================================

Purpose
-------
This script provides a convenient way to predict housing prices *without*
re-training the model.  It:

  1. Loads the previously-trained Linear Regression model from disk.
  2. Loads the fitted StandardScaler that was used during training.
  3. Accepts raw, human-readable feature values (e.g. "yes"/"no" strings,
     furnishing status text) and converts them into the numeric format
     the model expects.
  4. Returns and prints the predicted price.

Usage
-----
    python src/predict.py

You can also import the ``predict_price`` function from other modules:

    from src.predict import predict_price
    price = predict_price(area=7000, bedrooms=4, ...)

Prerequisites
-------------
* The model file  ``models/linear_regression_model.pkl`` must exist.
* The scaler file ``models/scaler.pkl`` must exist.
  Both are created by the training pipeline (``src/train.py``).

Author : Housing-Price-Prediction Team
Date   : 2026-07-21
"""

# Imports

import os
import joblib          # For deserialising the saved model & scaler
import numpy as np     # For building the feature array

# Import Indian market utilities
try:
    from src.utils import format_indian_currency, get_tier_multiplier
except ModuleNotFoundError:
    from utils import format_indian_currency, get_tier_multiplier


# Path Configuration

# We compute every path relative to the *project root* so the script
# works regardless of where it is invoked from.
#
#   PROJECT_ROOT/
#   ├── models/
#   │   ├── linear_regression_model.pkl
#   │   └── scaler.pkl
#   └── src/
#       └── predict.py          ← you are here
#
# os.path.dirname(__file__)  → …/src
# os.path.join(…, '..')      → …/src/..  (i.e. the project root)
# os.path.abspath(…)         → clean absolute path without ".."

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Full paths to the serialised artefacts
MODEL_PATH  = os.path.join(PROJECT_ROOT, 'models', 'linear_regression_model.pkl')
SCALER_PATH = os.path.join(PROJECT_ROOT, 'models', 'scaler.pkl')

# Helper – Load a pickle file

def _load_pickle(filepath: str):
    """
    Load and return a Python object from a ``.pkl`` file.

    Parameters
    ----------
    filepath : str
        Absolute path to the pickle file.

    Returns
    -------
    object
        The deserialised Python object (model, scaler, etc.).

    Raises
    ------
    FileNotFoundError
        If the file does not exist — usually means the training
        pipeline has not been run yet.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Required file not found: {filepath}\n"
            "Please run the training pipeline first to generate this file."
        )
    return joblib.load(filepath)

# Core Prediction Function

def predict_price(
    area: int,
    bedrooms: int,
    bathrooms: int,
    distance_km: float,
    city_tier: str = "tier-1",
) -> float:
    """
    Predict the price of a house in Indian Rupees (INR) given its raw feature values
    and the targeted city tier market.

    Parameters
    ----------
    area : int
        Total area of the house in square feet (e.g. 5000).
    bedrooms : int
        Number of bedrooms (e.g. 3).
    bathrooms : int
        Number of bathrooms (e.g. 2).
    distance_km : float
        Distance to the nearest major city center in kilometers.
    city_tier : str
        The city tier ("tier-1", "tier-2", "tier-3") to apply price calibration.

    Returns
    -------
    float
        The predicted, calibrated house price in Indian Rupees (INR).
    """

    model  = _load_pickle(MODEL_PATH)
    scaler = _load_pickle(SCALER_PATH)

    features = np.array([[
        area,                                # 0
        bedrooms,                            # 1
        bathrooms,                           # 2
        distance_km                          # 3
    ]])

    features_scaled = scaler.transform(features)

    predicted_price = model.predict(features_scaled)[0]

    multiplier = get_tier_multiplier(city_tier)
    calibrated_price = predicted_price * multiplier

    return float(calibrated_price)

# CLI Entry Point

if __name__ == '__main__':
    # Sample prediction with representative feature values
    sample_inputs = {
        'area':              5000,
        'bedrooms':          3,
        'bathrooms':         2,
        'distance_km':       10.5,
    }

    print("=" * 60)
    print("  Housing Price Prediction — Sample Inference")
    print("=" * 60)

    # Pretty-print the input features so the user can verify them
    print("\n[INPUTS] Input Features:")
    print("-" * 40)
    for feature_name, feature_value in sample_inputs.items():
        # Right-align the feature name for a clean table-like look
        print(f"  {feature_name:>25s} : {feature_value}")
    print("-" * 40)

    # Run the prediction
    try:
        # Predict standard Tier 1 price
        price_t1 = predict_price(**sample_inputs, city_tier="tier-1")
        price_t2 = predict_price(**sample_inputs, city_tier="tier-2")
        price_t3 = predict_price(**sample_inputs, city_tier="tier-3")
        
        print(f"\n[SUCCESS] Predicted Prices:")
        print(f"  Tier 1 Metro (1.0x) : {format_indian_currency(price_t1, prefix='Rs. ')}")
        print(f"  Tier 2 City  (0.65x): {format_indian_currency(price_t2, prefix='Rs. ')}")
        print(f"  Tier 3 Town  (0.40x): {format_indian_currency(price_t3, prefix='Rs. ')}")
    except FileNotFoundError as e:
        # Friendly message if model artefacts are missing
        print(f"\n[ERROR] Error: {e}")
    except Exception as e:
        # Catch-all for unexpected errors (shape mismatches, etc.)
        print(f"\n[ERROR] Unexpected error during prediction: {e}")

    print("\n" + "=" * 60)
