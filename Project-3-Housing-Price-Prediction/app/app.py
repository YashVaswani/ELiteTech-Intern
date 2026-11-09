import os
import sys
import joblib

import numpy as np
from flask import Flask, render_template, request, send_from_directory

# Add project root to system path to enable absolute imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Import Indian market utilities and distance calculation
from src.utils import format_indian_currency, get_tier_multiplier, haversine_distance

# Initialize Flask application
app = Flask(__name__)

# Define paths
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "linear_regression_model.pkl")
SCALER_PATH = os.path.join(PROJECT_ROOT, "models", "scaler.pkl")

# Load model and scaler
# We load them once at startup so every prediction request is fast.
# joblib.dump() during the training step.
model = None
scaler = None
model_load_error = None

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    model_load_error = f"Error loading model files: {str(e)}. Please run python src/train_model.py first."

# Define feature order

# This list MUST match the exact column order used when the model was trained.
# Numeric features come first, followed by the calculated distance.
# Currently active features: area, bedrooms, bathrooms, distance_to_center_km.
FEATURE_ORDER = [
    "area",
    "bedrooms",
    "bathrooms",
    "distance_to_center_km",
]

MAJOR_CITIES = [
    {"name": "Mumbai", "lat": 19.0760, "lng": 72.8777, "tier": "tier-1"},
    {"name": "Delhi", "lat": 28.7041, "lng": 77.1025, "tier": "tier-1"},
    {"name": "Bangalore", "lat": 12.9716, "lng": 77.5946, "tier": "tier-1"},
    {"name": "Hyderabad", "lat": 17.3850, "lng": 78.4867, "tier": "tier-1"},
    {"name": "Chennai", "lat": 13.0827, "lng": 80.2707, "tier": "tier-1"},
    {"name": "Kolkata", "lat": 22.5726, "lng": 88.3639, "tier": "tier-1"},
    {"name": "Pune", "lat": 18.5204, "lng": 73.8567, "tier": "tier-2"},
    {"name": "Ahmedabad", "lat": 23.0225, "lng": 72.5714, "tier": "tier-2"},
    {"name": "Jaipur", "lat": 26.9124, "lng": 75.7873, "tier": "tier-2"},
    {"name": "Lucknow", "lat": 26.8467, "lng": 80.9462, "tier": "tier-2"},
    {"name": "Indore", "lat": 22.7196, "lng": 75.8577, "tier": "tier-2"},
    {"name": "Bhopal", "lat": 23.2599, "lng": 77.4126, "tier": "tier-2"},
    {"name": "Patna", "lat": 25.5941, "lng": 85.1376, "tier": "tier-2"},
    {"name": "Agra", "lat": 27.1767, "lng": 78.0081, "tier": "tier-2"},
    {"name": "Kochi", "lat": 9.9312, "lng": 76.2673, "tier": "tier-2"},
]

def get_nearest_city(lat, lng):
    min_dist = float('inf')
    nearest_city = None
    for city in MAJOR_CITIES:
        dist = haversine_distance(lat, lng, city['lat'], city['lng'])
        if dist < min_dist:
            min_dist = dist
            nearest_city = city
    return nearest_city, min_dist

# Routes

@app.route("/")
def home():
    """Serve the main page with the prediction form."""
    return render_template("index.html", prediction=None, error=model_load_error)

@app.route("/predict", methods=["POST"])
def predict():
    """Receive form data, preprocess it, run the model, and return the result."""
    if model_load_error:
        return render_template("index.html", prediction=None, error=model_load_error)

    try:
        # Parse and validate form data
        area_raw = request.form.get("area", "")
        bedrooms_raw = request.form.get("bedrooms", "")
        bathrooms_raw = request.form.get("bathrooms", "")
        lat_raw = request.form.get("latitude", "")
        lng_raw = request.form.get("longitude", "")

        if not (area_raw and bedrooms_raw and bathrooms_raw):
            raise ValueError("All fields (Area, Bedrooms, Bathrooms) are required.")

        area = float(area_raw)
        if area <= 0:
            raise ValueError("Area must be a positive number.")

        bedrooms = int(bedrooms_raw)
        if not (1 <= bedrooms <= 6):
            raise ValueError("Bedrooms must be between 1 and 6.")

        bathrooms = int(bathrooms_raw)
        if not (1 <= bathrooms <= 4):
            raise ValueError("Bathrooms must be between 1 and 4.")

        if not lat_raw or not lng_raw:
            raise ValueError("Please select a location on the map.")
            
        lat = float(lat_raw)
        lng = float(lng_raw)
        
        # Calculate distance to nearest major city
        nearest_city, distance_km = get_nearest_city(lat, lng)

        # Cap distance at 20km for the model to prevent negative extrapolation
        model_distance = min(distance_km, 20.0)

        # Prepare feature array
        features = np.array([[
            area,
            bedrooms,
            bathrooms,
            model_distance
        ]])

        # Scale features
        features_scaled = scaler.transform(features)

        # Generate prediction
        predicted_price = model.predict(features_scaled)[0]
        
        # Apply a sensible minimum price floor (e.g. 5 Lakhs) instead of 0
        predicted_price = max(500000, predicted_price)

        # Apply City Tier Multiplier for regional calibration
        multiplier = get_tier_multiplier(nearest_city['tier'])
        calibrated_price = predicted_price * multiplier

        # Format output
        formatted_price = format_indian_currency(calibrated_price)
        prediction_text = f"{formatted_price} (Approx {distance_km:.1f} km from {nearest_city['name']} Center)"

        return render_template("index.html", prediction=prediction_text)

    except Exception as e:
        return render_template("index.html", prediction=None, error=f"Validation/Processing Error: {str(e)}")

@app.route("/about")
def about():
    """Serve the about page with details on the model, its metrics, and plots."""
    return render_template("about.html")

@app.route("/reports/<path:filename>")
def serve_report(filename):
    """Serve reports files (plots) directly from the reports/ directory."""
    return send_from_directory(os.path.join(PROJECT_ROOT, "reports"), filename)

# Run development server

if __name__ == "__main__":
    # debug=True enables:
    #   - Auto-reload when you edit this file (no manual restart needed).
    #   - A helpful in-browser debugger if an error occurs.
    # WARNING: Never use debug=True in production!
    app.run(debug=True, port=5000)
