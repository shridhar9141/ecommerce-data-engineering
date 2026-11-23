
import pandas as pd
from pathlib import Path


def clean_category_translation(df):
    """
    Clean category names and validate translation records.
    """

    df = df.copy()

    # Remove leading and trailing whitespace
    df["product_category_name"] = (
        df["product_category_name"].str.strip()
    )

    df["product_category_name_english"] = (
        df["product_category_name_english"].str.strip()
    )

    # Validate required columns
    required_columns = [
        "product_category_name",
        "product_category_name_english"
    ]

    for column in required_columns:
        if df[column].isna().any():
            raise ValueError(f"Missing values found in {column}")

    # Validate uniqueness
    if not df["product_category_name"].is_unique:
        raise ValueError("Duplicate Portuguese category names found")

    if not df["product_category_name_english"].is_unique:
        raise ValueError("Duplicate English category names found")

    return df


def main():
    input_path = Path(
        "data/raw/product_category_name_translation.csv"
    )

    output_path = Path(
        "data/processed/category_translation_cleaned.csv"
    )

    print("========== CATEGORY TRANSLATION CLEANING ==========")

    df = pd.read_csv(input_path)
    original_rows = len(df)

    cleaned_df = clean_category_translation(df)

    print("\nOriginal rows:", original_rows)
    print("Final rows:", len(cleaned_df))

    print("\nData types:")
    print(cleaned_df.dtypes)

    print("\nMissing values:")
    print(cleaned_df.isnull().sum())

    print(
        "\nUnique Portuguese categories:",
        cleaned_df["product_category_name"].nunique()
    )

    print(
        "Unique English categories:",
        cleaned_df["product_category_name_english"].nunique()
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved to:", output_path)


if __name__ == "__main__":
    main()
