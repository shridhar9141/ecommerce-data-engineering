
import pandas as pd
from pathlib import Path


def clean_payments(df):
    """
    Convert payment data types, validate payment records,
    and create a zero-installments quality flag.
    """

    df = df.copy()

    # Convert data types
    df["payment_sequential"] = df["payment_sequential"].astype("int64")
    df["payment_installments"] = df["payment_installments"].astype("int64")

    df["payment_value"] = pd.to_numeric(
        df["payment_value"],
        errors="raise"
    )

    # Add data quality flag
    df["zero_installments_flag"] = (
        df["payment_installments"] == 0
    )

    # Validate required values
    if df["order_id"].isna().any():
        raise ValueError("Missing order IDs found")

    if df["payment_value"].isna().any():
        raise ValueError("Missing payment values found")

    # Validate payment values
    if (df["payment_value"] < 0).any():
        raise ValueError("Negative payment values found")

    # Validate payment uniqueness
    if df.duplicated(
        subset=["order_id", "payment_sequential"]
    ).any():
        raise ValueError("Duplicate payment combinations found")

    return df


def main():
    input_path = Path("data/raw/olist_order_payments_dataset.csv")
    output_path = Path("data/processed/payments_cleaned.csv")

    print("========== PAYMENTS CLEANING ==========")

    df = pd.read_csv(input_path)
    original_rows = len(df)

    cleaned_df = clean_payments(df)

    print("\nOriginal rows:", original_rows)
    print("Final rows:", len(cleaned_df))

    print("\nData types:")
    print(cleaned_df.dtypes)

    print("\nZero installment records:")
    print(cleaned_df["zero_installments_flag"].sum())

    print("\nPayment types:")
    print(cleaned_df["payment_type"].value_counts())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_path, index=False)

    print("\nCleaned dataset saved to:", output_path)


if __name__ == "__main__":
    main()
