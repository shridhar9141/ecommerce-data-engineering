
import pandas as pd
from pathlib import Path


def clean_customers(df):
    """
    Clean customer data and apply data-quality validations.
    Returns the cleaned DataFrame.
    """

    # Work on a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Remove leading/trailing whitespace
    text_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ]

    for column in text_columns:
        df[column] = df[column].str.strip()

    # Standardize state codes
    df["customer_state"] = df["customer_state"].str.upper()

    # Validate required columns
    required_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix"
    ]

    for column in required_columns:
        if df[column].isna().any():
            raise ValueError(f"{column} contains missing values")

    # Validate customer IDs
    if not df["customer_id"].is_unique:
        raise ValueError("Duplicate customer IDs found")

    # Validate ZIP prefix format
    if not df["customer_zip_code_prefix"].str.fullmatch(r"\d+").all():
        raise ValueError("Invalid customer ZIP code prefix found")

    # Detect inconsistent customer locations
    location_counts = (
        df.groupby("customer_unique_id")[
            [
                "customer_zip_code_prefix",
                "customer_city",
                "customer_state"
            ]
        ].transform("nunique")
    )

    df["inconsistent_location_flag"] = (
        location_counts > 1
    ).any(axis=1)

    return df


def main():
    input_path = Path("data/raw/olist_customers_dataset.csv")
    output_path = Path("data/processed/customers_cleaned.csv")

    print("========== CUSTOMERS CLEANING ==========")

    # Read raw dataset
    df = pd.read_csv(
        input_path,
        dtype={"customer_zip_code_prefix": "str"}
    )

    original_rows = len(df)

    # Clean customer data
    cleaned_df = clean_customers(df)

    print("\nOriginal rows:", original_rows)
    print("Final rows:", len(cleaned_df))

    print("\nData types:")
    print(cleaned_df.dtypes)

    print("\nMissing values:")
    print(cleaned_df.isnull().sum())

    print("\nUnique customer IDs:", cleaned_df["customer_id"].nunique())

    print(
        "\nUnique actual customers:",
        cleaned_df["customer_unique_id"].nunique()
    )

    print(
        "\nRows flagged for inconsistent locations:",
        cleaned_df["inconsistent_location_flag"].sum()
    )

    # Save cleaned dataset
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved to:", output_path)


if __name__ == "__main__":
    main()
