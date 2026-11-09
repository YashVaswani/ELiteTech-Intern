"""Rebuild app/data/nutrition.json from the official USDA FoodData Central export.

The bundled nutrition.json ships with hand-curated estimates so the app works
offline with zero setup. For production-grade accuracy, use this script to
replace it with real USDA data — no API key needed, since it reads the
public bulk CSV export rather than calling the rate-limited API.

Usage:
    1. Download & unzip "Foundation Foods" CSV from
       https://fdc.nal.usda.gov/download-datasets (no login/API key required).
    2. python scripts/import_usda.py --usda-dir /path/to/unzipped/csv

Matching is best-effort (normalized substring match between the Food-101
category name and the USDA food description). Anything unmatched keeps its
existing estimate and is printed so you can fill it in manually.
"""

import argparse
import csv
import json
from pathlib import Path

NUTRIENT_IDS = {
    "calories": "1008",  # Energy (kcal)
    "protein_g": "1003",  # Protein
    "carbs_g": "1005",  # Carbohydrate, by difference
    "fat_g": "1004",  # Total lipid (fat)
}

DATA_PATH = Path(__file__).resolve().parent.parent / "app" / "data" / "nutrition.json"


def load_usda_food_nutrients(usda_dir: Path) -> dict[str, dict[str, float]]:
    foods: dict[str, str] = {}
    with (usda_dir / "food.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            foods[row["fdc_id"]] = row["description"].lower()

    per_food: dict[str, dict[str, float]] = {}
    with (usda_dir / "food_nutrient.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fdc_id, nutrient_id = row["fdc_id"], row["nutrient_id"]
            description = foods.get(fdc_id)
            if description is None:
                continue
            for key, target_id in NUTRIENT_IDS.items():
                if nutrient_id == target_id:
                    per_food.setdefault(description, {})[key] = float(row["amount"])

    return per_food


def best_match(food_name: str, usda_foods: dict[str, dict[str, float]]) -> dict[str, float] | None:
    query = food_name.replace("_", " ")
    candidates = [desc for desc in usda_foods if query in desc or desc in query]
    if not candidates:
        return None
    # Prefer the shortest matching description as the closest/most generic match.
    best = min(candidates, key=len)
    return usda_foods[best]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--usda-dir", required=True, type=Path, help="Path to unzipped USDA CSV export"
    )
    args = parser.parse_args()

    with DATA_PATH.open(encoding="utf-8") as f:
        nutrition = json.load(f)

    usda_foods = load_usda_food_nutrients(args.usda_dir)

    unmatched = []
    for food_name in list(nutrition.keys()):
        if food_name.startswith("_"):
            continue
        match = best_match(food_name, usda_foods)
        if match and all(k in match for k in NUTRIENT_IDS):
            nutrition[food_name] = {k: round(match[k], 1) for k in NUTRIENT_IDS}
        else:
            unmatched.append(food_name)

    nutrition["_meta"]["source"] = "USDA FoodData Central (https://fdc.nal.usda.gov/)"

    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(nutrition, f, indent=2)
        f.write("\n")

    print(f"Updated {DATA_PATH}")
    if unmatched:
        print(f"\n{len(unmatched)} foods kept their previous estimate (no confident USDA match):")
        for name in unmatched:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
