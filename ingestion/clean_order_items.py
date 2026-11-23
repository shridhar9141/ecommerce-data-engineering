
import pandas as pd
from pathlib import Path


def clean_order_items(df):
    """
    Convert shipping dates and validate order-item data.
    Returns the cleaned DataFrame.
    """

    df = df.copy()

    # Convert shipping date to datetime
    df["shipping_limit_date"] = pd.to_datetime(
        df["shipping_limit_date"],
        errors="raise"
    )

    # Validate order-item uniqueness
    if df.duplicated(
        subset=["order_id", "order_item_id"]
    ).any():
        raise ValueError("Duplicate order-item combinations found")

    # Validate numeric columns
    if (df["price"] < 0).any():
        raise ValueError("Negative product prices found")

    if (df["freight_value"] < 0).any():
        raise ValueError("Negative freight values found")

    return df


def main():
    raw_file = Path("data/raw/olist_order_items_dataset.csv")
    output_file = Path("data/processed/order_items_cleaned.csv")

    print("========== ORDER ITEMS CLEANING ==========")

    df = pd.read_csv(raw_file)

    print("Original rows:", len(df))

    cleaned_df = clean_order_items(df)

    print("\nDuplicate order-item combinations:", 0)

    print("\nNumeric data types:")
    print(cleaned_df[["price", "freight_value"]].dtypes)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_file, index=False)

    print("\nFinal rows:", len(cleaned_df))
    print("Cleaned dataset saved to:", output_file)


if __name__ == "__main__":
    main()
