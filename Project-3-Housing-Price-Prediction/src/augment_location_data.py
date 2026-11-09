import os
import pandas as pd
import numpy as np

# Set paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INPUT_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "Housing_cleaned.csv")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "Housing_cleaned_geo.csv")

# Indore coordinates
INDORE_LAT = 22.7196
INDORE_LNG = 75.8577

def augment_data():
    print(f"Loading data from {INPUT_PATH}...")
    df = pd.read_csv(INPUT_PATH)
    
    # Calculate an approximate "premium" factor (price per sqft) to correlate with distance
    # Higher premium = closer to city center
    price_per_sqft = df['price'] / df['area']
    
    # Normalize between 0 and 1
    min_pps = price_per_sqft.min()
    max_pps = price_per_sqft.max()
    normalized_pps = (price_per_sqft - min_pps) / (max_pps - min_pps)
    
    # Generate distances (in km). Max distance ~15km, min ~0.5km.
    # Higher premium means lower distance.
    # distance = 15 - (normalized_pps * 14) + noise
    np.random.seed(42) # For reproducibility
    noise = np.random.normal(0, 1.5, len(df))
    distances_km = 15.0 - (normalized_pps * 14.0) + noise
    distances_km = np.clip(distances_km, 0.5, 20.0)
    
    latitudes = []
    longitudes = []
    
    for dist in distances_km:
        # 1 km is roughly 0.009 degrees of latitude/longitude
        dist_deg = dist * 0.009
        
        # Pick a random angle around the city center
        angle = np.random.uniform(0, 2 * np.pi)
        
        # Calculate offset
        lat_offset = dist_deg * np.cos(angle)
        lng_offset = dist_deg * np.sin(angle)
        
        latitudes.append(INDORE_LAT + lat_offset)
        longitudes.append(INDORE_LNG + lng_offset)
        
    df['latitude'] = latitudes
    df['longitude'] = longitudes
    
    print(f"Generated synthetic coordinates around Indore (Lat: {INDORE_LAT}, Lng: {INDORE_LNG}).")
    print(f"Saving augmented data to {OUTPUT_PATH}...")
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print("Done!")

if __name__ == "__main__":
    augment_data()
