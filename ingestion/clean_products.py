
import pandas as pd
from pathlib import Path


def clean_products(df):
    """
    Clean product data by handling missing categories.
    Returns the cleaned DataFrame.
    """

    df = df.copy()

    # Fill missing product categories
    df["product_category_name"] = (
        df["product_category_name"].fillna("unknown")
    )

    return df


def main():
    raw_file = Path("data/raw/olist_products_dataset.csv")
    output_file = Path("data/processed/products_cleaned.csv")

    print("========== PRODUCT DATA CLEANING ==========")

    # Read raw dataset
    df = pd.read_csv(raw_file)

    print("Original rows:", len(df))

    # Clean product data
    cleaned_df = clean_products(df)

    print("\nMissing values after cleaning:")
    print(cleaned_df.isnull().sum())

    # Save cleaned dataset
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_file, index=False)

    print("\nCleaned dataset saved to:", output_file)
    print("Final rows:", len(cleaned_df))


if __name__ == "__main__":
    main()
