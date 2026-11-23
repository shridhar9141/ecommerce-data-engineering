
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL


# 1. Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load database credentials
load_dotenv(PROJECT_ROOT / ".env")


# 2. Database configuration
required_vars = [
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]

missing_vars = [
    var for var in required_vars if not os.getenv(var)
]

if missing_vars:
    raise ValueError(
        f"Missing environment variables: {missing_vars}"
    )


# 3. Create PostgreSQL connection
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(db_url, pool_pre_ping=True)


try:
    # 4. Read cleaned customer dataset
    csv_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "customers_cleaned.csv"
    )

    # Check whether CSV exists
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Customer dataset not found: {csv_path}"
        )

    df = pd.read_csv(csv_path)

    # Check whether dataset is empty
    if df.empty:
        raise ValueError(
            f"Customer dataset is empty: {csv_path}"
        )

    print("========== CUSTOMER DATA LOADING ==========")
    print("CSV rows:", len(df))


    # 5. Load data into PostgreSQL
    # Transaction automatically commits or rolls back.
    with engine.begin() as connection:

        # Clear existing rows before reloading
        connection.execute(
            text("TRUNCATE TABLE staging.customers")
        )

        # Insert customer records
        df.to_sql(
            name="customers",
            schema="staging",
            con=connection,
            if_exists="append",
            index=False,
            chunksize=1000,
            method="multi",
        )

        # Verify database row count
        result = connection.execute(
            text(
                "SELECT COUNT(*) FROM staging.customers"
            )
        )

        database_rows = result.scalar_one()

        # Validate before transaction commits
        if database_rows != len(df):
            raise ValueError(
                "CSV and database row counts do not match! "
                f"CSV={len(df)}, DB={database_rows}"
            )


    # 6. Display loading results
    print("Rows loaded:", database_rows)
    print("Customer data loaded successfully!")


finally:
    # 7. Dispose database connections
    engine.dispose()
    print("Database connection resources released.")
