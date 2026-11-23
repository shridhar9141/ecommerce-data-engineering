
import os

import pytest
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import URL, create_engine, text


# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


# Expected Gold layer tables and row counts
GOLD_TABLES = {
    "dim_customers": 96096,
    "customer_records": 99441,
    "dim_products": 32951,
    "dim_sellers": 3095,
    "dim_orders": 99441,
    "dim_date": 774,
    "fact_order_items": 112650,
    "fact_payments": 103886,
    "fact_reviews": 99224,
}


@pytest.fixture(scope="module")
def db_engine():
    """Create a PostgreSQL connection for integration tests."""

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
        pytest.skip(
            f"Missing database configuration: {missing_vars}"
        )

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
        yield engine
    finally:
        engine.dispose()


@pytest.mark.parametrize(
    "table_name, expected_rows",
    GOLD_TABLES.items(),
)
def test_gold_table_row_count(
    db_engine, table_name, expected_rows
):
    """Verify Gold layer table row counts."""

    with db_engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT COUNT(*) FROM gold.{table_name}")
        )

        actual_rows = result.scalar_one()

    assert actual_rows == expected_rows, (
        f"gold.{table_name}: expected {expected_rows} rows, "
        f"but found {actual_rows}"
    )
