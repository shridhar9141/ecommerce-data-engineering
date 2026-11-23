
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_order_payments_dataset.csv")

df = pd.read_csv(file_path)

print("========== PAYMENTS INVESTIGATION ==========")

# Dataset overview
print("\nDataset shape:", df.shape)

# Missing values
print("\nMissing values:")
print(df.isnull().sum())

# Duplicate records
print("\nExact duplicate records:", df.duplicated().sum())

# Duplicate order-payment combinations
print("\nDuplicate order_id + payment_sequential:")
print(
    df.duplicated(
        subset=["order_id", "payment_sequential"]
    ).sum()
)

# Payment method distribution
print("\nPayment type distribution:")
print(df["payment_type"].value_counts())

# Payment value statistics
print("\nPayment value statistics:")
print(df["payment_value"].describe())

# Installment statistics
print("\nPayment installments statistics:")
print(df["payment_installments"].describe())

# Check invalid values
print("\nNegative payment values:")
print((df["payment_value"] < 0).sum())

print("\nZero payment values:")
print((df["payment_value"] == 0).sum())

print("\nZero installments:")
print((df["payment_installments"] == 0).sum())
