
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_orders_dataset.csv")

df = pd.read_csv(file_path)

print("========== DELIVERED ORDER INVESTIGATION ==========")

# Find delivered orders with missing customer delivery dates
problem_orders = df[
    (df["order_status"] == "delivered") &
    (df["order_delivered_customer_date"].isnull())
]

print("\nNumber of affected orders:", len(problem_orders))

print("\nAffected order records:")
print(problem_orders.to_string(index=False))

# Check missing carrier delivery dates for these orders
print("\nMissing carrier delivery dates:")
print(problem_orders["order_delivered_carrier_date"].isnull().sum())

# Check missing approval timestamps for these orders
print("\nMissing approval timestamps:")
print(problem_orders["order_approved_at"].isnull().sum())
