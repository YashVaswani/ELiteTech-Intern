# Housing Price Prediction System 🏠📊

An end-to-end Machine Learning project that processes real estate data, trains an Ordinary Least Squares (OLS) Linear Regression model, generates diagnostic visualisations, and exposes an interactive Flask web portal with glassmorphic styling to predict house prices.

---

## 🌟 Key Features

- **Clean 3-Feature Model**: Simplified input schema focusing on the most critical real estate attributes (`area`, `bedrooms`, `bathrooms`).
- **Regional Market Calibration**: Includes a dynamic **Regional Market Index (RMI)** tool to scale predictions for Tier 1 Metros (1.0x), Tier 2 Cities (0.65x), and Tier 3 Suburbs/Towns (0.40x).
- **Indian Numbering Format**: Output values are formatted cleanly in **Lakhs and Crores** (e.g. `₹15.63 Lakh` or `₹1.12 Crore`) to match Indian real estate terminology.
- **Diagnostics & Visualization**: Outputs diagnostic plots (Actual vs. Predicted, Residual Distribution, and Feature Importance) directly to `reports/` upon model training.
- **Polished Glassmorphic Web UI**: A dark-theme Flask web app featuring error validation alerts, interactive calibration dropdowns, and an **About Model** dashboard.
- **Reproducible Design**: Pinned dependencies in `requirements.txt` and modular object-oriented directories.

---

## 📁 Project Directory Structure

```
Housing Price Prediction/
├── data/
│   ├── raw/                # Original, immutable data source (Housing.csv)
│   └── processed/          # Preprocessed data ready for training (Housing_cleaned.csv)
│
├── notebooks/
│   └── Housing_EDA.ipynb   # Jupyter Notebook with full Exploratory Data Analysis
│
├── src/                    # Pipeline scripts
│   ├── __init__.py
│   ├── data_preprocessing.py # Loads raw CSV, encodes binary/one-hot columns, saves cleaned data
│   ├── train_model.py      # Splits data, scales features, fits Linear Regression, evaluates, saves assets/plots
│   └── predict.py          # Standalone CLI prediction module for testing
│
├── models/                 # Saved Python objects (git-ignored except locally)
│   ├── linear_regression_model.pkl # Fitted OLS model
│   └── scaler.pkl          # Fitted StandardScaler
│
├── reports/                # Model evaluation plots
│   ├── actual_vs_predicted.png
│   ├── residuals_distribution.png
│   └── feature_importance.png
│
├── app/                    # Web Application
│   ├── static/
│   │   └── css/
│   │       └── style.css   # Main CSS stylesheet
│   ├── templates/
│   │   ├── index.html      # Main predictor dashboard template
│   │   └── about.html      # Model performance insights page
│   └── app.py              # Flask server and routing script
│
├── .gitignore
├── requirements.txt        # Pinned requirements file
└── README.md               # You are here
```

---

## 🚀 Quickstart Guide

### 1. Installation & Environment Setup
Ensure you have Python installed. Set up your virtual environment and install the pinned dependencies:
```bash
# Initialize and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install packages
pip install -r requirements.txt
```

### 2. Preprocess the Data
Execute the preprocessing pipeline. This cleans the raw data under `data/raw/Housing.csv` and outputs `data/processed/Housing_cleaned.csv`:
```bash
python src/data_preprocessing.py
```

### 3. Train the Model
Fit the Linear Regression model, compute diagnostic metrics, save evaluation plots to `reports/`, and save serialized assets to `models/`:
```bash
python src/train_model.py
```

### 4. Run CLI Predictions
Test inference directly via CLI with sample parameters:
```bash
python src/predict.py
```

### 5. Launch the Web Portal
Start the interactive local server to make predictions in your web browser:
```bash
python app/app.py
```
Open your browser and navigate to **`http://127.0.0.1:5000`**.

---

## 📊 Model Performance Summary

Evaluated on a 20% random test set:
- **R² Score (Coefficient of Determination)**: `0.4559` (The model explains approximately 45.6% of the target variance using the 3 features)
- **Root Mean Squared Error (RMSE)**: `₹1,658,324.60`
- **Mean Absolute Error (MAE)**: `₹1,265,275.67`

### Key Findings from EDA
- **Continuous Features**: The house area (square footage) has the strongest positive linear correlation (`0.54`) with pricing, followed closely by the number of bathrooms (`0.52`).
- **Amenities**: Multi-feature regression highlights that bedrooms and bathrooms are primary drivers alongside area.
- **Regional Calibration**: Introducing regional indexing allows the base Delhi-NCR model to extrapolate reliably to Tier 2/3 locations across India.
