
import pandas as pd
from pathlib import Path


def clean_geolocation(df):
    """
    Remove only exact duplicate geolocation records.
    Preserve different coordinates for the same ZIP prefix.
    """

    df_cleaned = df.drop_duplicates().copy()

    return df_cleaned


def main():
    raw_file = Path("data/raw/olist_geolocation_dataset.csv")
    output_file = Path("data/processed/geolocation_cleaned.csv")

    print("========== GEOLOCATION CLEANING ==========")

    df = pd.read_csv(raw_file)

    original_rows = len(df)
    duplicate_count = df.duplicated().sum()

    print("Original rows:", original_rows)
    print("Exact duplicates:", duplicate_count)

    df_cleaned = clean_geolocation(df)

    print("\n========== CLEANING RESULTS ==========")
    print("Rows after cleaning:", len(df_cleaned))
    print("Rows removed:", original_rows - len(df_cleaned))
    print("Remaining duplicates:", df_cleaned.duplicated().sum())

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_file, index=False)

    print("\nCleaned dataset saved to:", output_file)


if __name__ == "__main__":
    main()
