
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_order_items_dataset.csv")

df = pd.read_csv(file_path)

print("========== ORDER ITEMS INVESTIGATION ==========")

# Dataset overview
print("\nDataset shape:", df.shape)

# Missing values
print("\nMissing values:")
print(df.isnull().sum())

# Duplicate records
print("\nDuplicate records:", df.duplicated().sum())

# Duplicate order-item combinations
print("\nDuplicate order_id + order_item_id combinations:")
print(
    df.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

# Numeric column statistics
print("\nPrice statistics:")
print(df["price"].describe())

print("\nFreight value statistics:")
print(df["freight_value"].describe())

# Check negative values
print("\nNegative prices:", (df["price"] < 0).sum())
print("Negative freight values:", (df["freight_value"] < 0).sum())

# Check shipping date
print("\nShipping limit date data type:")
print(df["shipping_limit_date"].dtype)
