"""
data_preprocessing.py
=====================
This script handles the entire data-preprocessing pipeline for the
Housing Price Prediction project.

Pipeline overview:
    1. Load the raw CSV data from  data/raw/Housing.csv
    2. Display exploratory information (shape, dtypes, head, missing values,
       summary statistics) so we understand what we're working with.
    3. Encode binary categorical columns (yes/no → 1/0).
    4. One-hot encode the multi-class categorical column 'furnishingstatus'.
    5. Save the cleaned dataframe to  data/processed/Housing_cleaned.csv

Author : Auto-generated
Date   : 2026-07-21
"""

# ──────────────────────────────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────────────────────────────
import os  # For cross-platform file-path handling
import pandas as pd  # The workhorse library for tabular data in Python


# ──────────────────────────────────────────────────────────────────────
# Path constants
# ──────────────────────────────────────────────────────────────────────
# We derive the *project root* dynamically so the script works no matter
# where it's invoked from (e.g., IDE, terminal, scheduled job).
#
# __file__          → .../src/data_preprocessing.py
# dirname(__file__) → .../src
# dirname(dirname)  → ...  (project root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Raw data lives in  data/raw/  and cleaned output goes to  data/processed/
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "Housing.csv")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
CLEANED_DATA_PATH = os.path.join(PROCESSED_DIR, "Housing_cleaned.csv")


# ──────────────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ──────────────────────────────────────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.

    Parameters
    ----------
    filepath : str
        Absolute or relative path to the CSV file.

    Returns
    -------
    pd.DataFrame
        The loaded data as a DataFrame.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist at the given path.

    Notes
    -----
    • pandas.read_csv() automatically infers column types, but we will
      double-check them in the EDA step.
    • If the CSV is very large, consider using the `chunksize` parameter
      to read it in chunks — for this dataset it's small enough to load
      all at once.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"Could not find the data file at:\n  {filepath}\n"
            "Make sure Housing.csv is placed inside  data/raw/."
        )

    df = pd.read_csv(filepath)
    print(f"[OK] Data loaded successfully from:\n    {filepath}")
    return df


# ----------------------------------------------------------------------
# 2. EXPLORATORY DATA ANALYSIS (EDA) — quick look
# ──────────────────────────────────────────────────────────────────────
def display_basic_info(df: pd.DataFrame) -> None:
    """
    Print a concise summary of the DataFrame so we can sanity-check the
    data before transforming it.

    What we look for:
        • Shape          → how many rows and columns?
        • Data types     → are numeric columns really numeric?
        • Head           → do the first few rows look reasonable?
        • Missing values → any NaNs we need to handle?
        • Describe       → min/max/mean — any outliers jumping out?

    Parameters
    ----------
    df : pd.DataFrame
        The raw dataframe to inspect.
    """
    print("\n" + "=" * 60)
    print("  BASIC DATA INFORMATION")
    print("=" * 60)

    # --- 2a. Shape -----------------------------------------------------------
    # Shape returns a tuple: (number_of_rows, number_of_columns)
    print(f"\n[Shape]  {df.shape[0]} rows  ×  {df.shape[1]} columns")

    # --- 2b. Data types ------------------------------------------------------
    # Each column has a dtype (int64, float64, object, etc.).
    # 'object' usually means string/text — these are the columns we may
    # need to encode later.
    print("\n[Data Types]")
    print(df.dtypes.to_string())

    # --- 2c. First 5 rows ----------------------------------------------------
    # A quick visual check that values look sensible.
    print("\n[First 5 Rows]")
    print(df.head().to_string())

    # --- 2d. Missing values ---------------------------------------------------
    # Missing values (NaN) can cause models to crash or produce wrong results.
    # We count them per column so we know what to fix.
    missing = df.isnull().sum()
    print("\n[Missing Values per Column]")
    print(missing.to_string())

    total_missing = missing.sum()
    if total_missing == 0:
        print("  -> No missing values detected. Great!")
    else:
        print(f"  → Total missing values: {total_missing}")

    # --- 2e. Descriptive statistics -------------------------------------------
    # describe() gives count, mean, std, min, 25%, 50%, 75%, max for
    # numeric columns. For categorical columns use  include='all'.
    print("\n[Descriptive Statistics]")
    print(df.describe().to_string())

    print("\n" + "=" * 60)


# ──────────────────────────────────────────────────────────────────────
# 3. ENCODE BINARY CATEGORICAL COLUMNS  (yes/no → 1/0)
# ──────────────────────────────────────────────────────────────────────
def encode_binary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert binary categorical columns that contain 'yes'/'no' strings
    into numeric 1/0 values.

    Why do we do this?
        Machine-learning models work with numbers, not text.  A column
        like ``mainroad`` with values 'yes' and 'no' must be turned into
        1 and 0 before we can feed it to a regression model.

    Columns affected:
        mainroad, guestroom, basement, hotwaterheating,
        airconditioning, prefarea

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with the raw yes/no columns.

    Returns
    -------
    pd.DataFrame
        DataFrame with the binary columns converted to integers.

    Notes
    -----
    • We use pandas `.map()` which replaces values based on a dictionary.
    • If a column contained something other than 'yes' or 'no' (e.g., NaN
      or a typo like 'Yes'), .map() would turn it into NaN — that's a
      useful signal that something unexpected is in the data.
    """
    # List of columns that are binary yes/no
    binary_columns = [
        "mainroad",
        "guestroom",
        "basement",
        "hotwaterheating",
        "airconditioning",
        "prefarea",
    ]

    # Mapping dictionary: 'yes' → 1, 'no' → 0
    yes_no_map = {"yes": 1, "no": 0}

    for col in binary_columns:
        if col in df.columns:
            df[col] = df[col].map(yes_no_map)
            print(f"  • Encoded '{col}' : yes → 1, no → 0")
        else:
            # Warn (but don't crash) if a column is missing — the dataset
            # schema might have changed.
            print(f"  [WARN] Column '{col}' not found in DataFrame - skipping.")

    print("[OK] Binary encoding complete.")
    return df


# ──────────────────────────────────────────────────────────────────────
# 4. ONE-HOT ENCODE 'furnishingstatus'
# ──────────────────────────────────────────────────────────────────────
def one_hot_encode_furnishing(df: pd.DataFrame) -> pd.DataFrame:
    """
    One-hot encode the 'furnishingstatus' column and drop the first
    category to avoid the *dummy-variable trap* (multicollinearity).

    Background for interns:
        'furnishingstatus' has 3 unique values:
            furnished, semi-furnished, unfurnished

        One-hot encoding creates a new binary (0/1) column for each
        category.  However, if we keep ALL 3 dummy columns, any one of
        them is perfectly predictable from the other two (they always
        sum to 1).  That redundancy — called *multicollinearity* — can
        cause problems for linear models.  Dropping one column (the
        "reference" category) fixes this.

        pd.get_dummies(drop_first=True) drops the first category
        alphabetically, which is 'furnished'.  So we end up with:
            • furnishingstatus_semi-furnished  (1 if semi-furnished, else 0)
            • furnishingstatus_unfurnished     (1 if unfurnished, else 0)
        If BOTH are 0, the house is furnished (the dropped category).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the 'furnishingstatus' column.

    Returns
    -------
    pd.DataFrame
        DataFrame with 'furnishingstatus' replaced by dummy columns.
    """
    if "furnishingstatus" not in df.columns:
        print("  [WARN] Column 'furnishingstatus' not found - skipping one-hot encoding.")
        return df

    # pd.get_dummies() creates indicator/dummy columns.
    # - columns=["furnishingstatus"]  →  only encode this column
    # - drop_first=True               →  drop one category to avoid
    #                                     multicollinearity
    # - dtype=int                      →  produce 0/1 integers instead of
    #                                     True/False booleans
    df = pd.get_dummies(
        df,
        columns=["furnishingstatus"],
        drop_first=True,
        dtype=int,
    )

    print("[OK] One-hot encoded 'furnishingstatus' (drop_first=True).")
    print("    New dummy columns created:")
    # Show the user which new columns appeared
    for col in df.columns:
        if col.startswith("furnishingstatus_"):
            print(f"      • {col}")

    return df


# ──────────────────────────────────────────────────────────────────────
# 5. SAVE CLEANED DATA
# ──────────────────────────────────────────────────────────────────────
def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Persist the cleaned DataFrame to a CSV file.

    Parameters
    ----------
    df : pd.DataFrame
        The fully preprocessed DataFrame.
    output_path : str
        Destination file path (absolute).

    Notes
    -----
    • We pass `index=False` so pandas does NOT write the row numbers as
      an extra unnamed column — that would create a useless 'Unnamed: 0'
      column when the file is read back in.
    • os.makedirs(..., exist_ok=True) creates the output directory if it
      doesn't exist yet, and does nothing if it already exists.
    """
    # Make sure the output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"[OK] Cleaned data saved to:\n    {output_path}")


# ──────────────────────────────────────────────────────────────────────
# MAIN — orchestrate the full pipeline
# ──────────────────────────────────────────────────────────────────────
def main() -> None:
    """
    Run the complete data-preprocessing pipeline end-to-end.

    Steps executed:
        1. Load raw data
        2. Display EDA summary
        3. Encode binary columns
        4. One-hot encode furnishingstatus
        5. Save cleaned data
    """
    print("=" * 60)
    print("  HOUSING DATA PREPROCESSING PIPELINE")
    print("=" * 60)

    # Step 1 — Load
    print("\n>>> Step 1: Loading raw data …")
    df = load_data(RAW_DATA_PATH)

    # Step 2 — EDA
    print("\n>>> Step 2: Displaying basic information …")
    display_basic_info(df)

    # Step 3 — Binary encoding
    print("\n>>> Step 3: Encoding binary categorical columns …")
    df = encode_binary_columns(df)

    # Step 4 — One-hot encoding
    print("\n>>> Step 4: One-hot encoding 'furnishingstatus' …")
    df = one_hot_encode_furnishing(df)

    # Quick sanity check after transformations
    print("\n>>> Post-processing check:")
    print(f"    Shape after encoding: {df.shape}")
    print(f"    Columns: {list(df.columns)}")
    print(f"    Data types:\n{df.dtypes.to_string()}")

    # Step 5 — Save
    print("\n>>> Step 5: Saving cleaned data …")
    save_cleaned_data(df, CLEANED_DATA_PATH)

    print("\n" + "=" * 60)
    print("  PREPROCESSING COMPLETE")
    print("=" * 60)


# ──────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────
# The  if __name__ == '__main__'  guard ensures that main() only runs
# when this file is executed directly (e.g., `python data_preprocessing.py`).
# If another script *imports* this module to reuse a function (like
# encode_binary_columns), main() will NOT run automatically.
if __name__ == "__main__":
    main()
