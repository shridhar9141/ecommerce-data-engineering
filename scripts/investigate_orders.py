
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_orders_dataset.csv")

df = pd.read_csv(file_path)

print("========== ORDER DATA INVESTIGATION ==========")

# 1. Order status distribution
print("\nOrder status distribution:")
print(df["order_status"].value_counts())

# 2. Missing values by column
print("\nMissing values:")
print(df.isnull().sum())

# 3. Missing delivery dates by order status
print("\nMissing delivery customer date by status:")
print(
    df.groupby("order_status")[
        "order_delivered_customer_date"
    ].apply(lambda x: x.isnull().sum())
)

# 4. Total orders by status
print("\nTotal orders by status:")
print(df.groupby("order_status")["order_id"].count())

# 5. Check duplicate order IDs
print("\nDuplicate order IDs:")
print(df["order_id"].duplicated().sum())
