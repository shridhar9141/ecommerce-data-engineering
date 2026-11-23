
import pandas as pd
from pathlib import Path

file_path = Path("data/raw/olist_order_payments_dataset.csv")

df = pd.read_csv(file_path)

print("========== PAYMENT ANOMALIES ==========")

# 1. Investigate zero payment values
print("\nZero payment records:")
print(df[df["payment_value"] == 0])

# 2. Investigate zero installments
print("\nZero installment records:")
print(df[df["payment_installments"] == 0])

# 3. Investigate undefined payment types
print("\nUndefined payment type records:")
print(df[df["payment_type"] == "not_defined"])

# 4. Payment value by payment type
print("\nPayment value by payment type:")
print(
    df.groupby("payment_type")["payment_value"]
    .agg(["count", "min", "mean", "max"])
)
