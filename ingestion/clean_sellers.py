
import pandas as pd
from pathlib import Path


def clean_sellers(df):
    """
    Clean seller text columns and validate seller data.
    """

    df = df.copy()

    # Clean text columns
    text_columns = [
        "seller_id",
        "seller_city",
        "seller_state"
    ]

    for column in text_columns:
        df[column] = df[column].str.strip()

    # Standardize state codes
    df["seller_state"] = df["seller_state"].str.upper()

    # Validate required fields
    required_columns = [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state"
    ]

    for column in required_columns:
        if df[column].isna().any():
            raise ValueError(f"Missing values found in {column}")

    # Validate seller IDs
    if not df["seller_id"].is_unique:
        raise ValueError("Duplicate seller IDs found")

    # Validate ZIP code prefixes
    if not df["seller_zip_code_prefix"].str.fullmatch(r"\d+").all():
        raise ValueError("Invalid seller ZIP code prefix found")

    return df


def main():
    input_path = Path("data/raw/olist_sellers_dataset.csv")
    output_path = Path("data/processed/sellers_cleaned.csv")

    print("========== SELLERS CLEANING ==========")

    df = pd.read_csv(
        input_path,
        dtype={"seller_zip_code_prefix": "str"}
    )

    original_rows = len(df)

    cleaned_df = clean_sellers(df)

    print("\nOriginal rows:", original_rows)
    print("Final rows:", len(cleaned_df))

    print("\nData types:")
    print(cleaned_df.dtypes)

    print("\nMissing values:")
    print(cleaned_df.isnull().sum())

    print("\nUnique sellers:", cleaned_df["seller_id"].nunique())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved to:", output_path)


if __name__ == "__main__":
    main()
