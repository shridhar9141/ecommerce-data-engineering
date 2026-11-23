
import pandas as pd
from pathlib import Path


DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]


def clean_orders(df):
    """
    Convert order timestamps and flag delivered orders
    with missing customer delivery dates.
    """

    df = df.copy()

    # Convert timestamp columns to datetime
    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(
            df[column],
            errors="raise"
        )

    # Create data quality flag
    df["delivered_missing_delivery_date"] = (
        (df["order_status"] == "delivered") &
        (df["order_delivered_customer_date"].isna())
    )

    return df


def main():
    raw_file = Path("data/raw/olist_orders_dataset.csv")
    output_file = Path("data/processed/orders_cleaned.csv")

    print("========== ORDER DATA CLEANING ==========")

    df = pd.read_csv(raw_file)

    print("Original rows:", len(df))

    cleaned_df = clean_orders(df)

    print("\nData types after conversion:")
    print(cleaned_df.dtypes)

    print("\nDelivered orders with missing delivery dates:")
    print(cleaned_df["delivered_missing_delivery_date"].sum())

    print("\nMissing values:")
    print(cleaned_df.isnull().sum())

    output_file.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_file, index=False)

    print("\nFinal rows:", len(cleaned_df))
    print("Cleaned dataset saved to:", output_file)


if __name__ == "__main__":
    main()
