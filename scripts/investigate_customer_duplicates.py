
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_customers_dataset.csv")

df = pd.read_csv(file_path)

print("========== CUSTOMER DUPLICATE ANALYSIS ==========")

# Count unique customers
print("\nTotal customer records:", len(df))

print(
    "Unique customer IDs:",
    df["customer_id"].nunique()
)

print(
    "Unique customer unique IDs:",
    df["customer_unique_id"].nunique()
)

# Find customers with multiple customer IDs
customer_order_counts = (
    df.groupby("customer_unique_id")["customer_id"]
    .nunique()
)

repeated_customers = customer_order_counts[
    customer_order_counts > 1
]

print(
    "\nCustomers with multiple customer IDs:",
    len(repeated_customers)
)

print("\nMaximum customer IDs per unique customer:")
print(customer_order_counts.max())

# Check location consistency
location_counts = (
    df.groupby("customer_unique_id")[
        ["customer_zip_code_prefix", "customer_city", "customer_state"]
    ]
    .nunique()
)

inconsistent_locations = location_counts[
    (location_counts > 1).any(axis=1)
]

print(
    "\nCustomers with inconsistent location records:",
    len(inconsistent_locations)
)

print("\nSample inconsistent customer locations:")
print(inconsistent_locations.head(10))

# Check state values
print("\nUnique state codes:", df["customer_state"].nunique())
