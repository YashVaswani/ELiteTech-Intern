import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371.0 * c

def format_indian_currency(amount: float, prefix: str = "₹") -> str:
    """
    Format a floating-point number into Indian Rupees (INR) with Lakh/Crore naming conventions.
    
    Examples:
        5712050.50 -> ₹57.12 Lakh
        13300000.00 -> ₹1.33 Crore
        95000.00 -> ₹95,000.00
    """
    amount = float(amount)
    if amount >= 10000000:
        return f"{prefix}{amount / 10000000:.2f} Crore"
    elif amount >= 100000:
        return f"{prefix}{amount / 100000:.2f} Lakh"
    else:
        return f"{prefix}{amount:,.2f}"


def get_tier_multiplier(tier_name: str) -> float:
    """
    Get the price multiplier based on the city tier to calibrate the model
    to different Indian real estate markets.
    """
    tier_name = tier_name.strip().lower()
    if tier_name == "tier-2":
        return 0.65
    elif tier_name == "tier-3":
        return 0.40
    else:
        return 1.0
