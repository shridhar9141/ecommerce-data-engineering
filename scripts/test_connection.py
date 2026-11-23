
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Load environment variables
load_dotenv()

# Read database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

try:
    # Safely construct database URL
    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME
    )

    # Create SQLAlchemy engine
    engine = create_engine(database_url)

    # Test connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))

        print("Successfully connected to PostgreSQL!")
        print(f"Database: {DB_NAME}")
        print("Connection Status: SUCCESS")
        print(f"PostgreSQL Version: {result.scalar()}")

    engine.dispose()

except Exception as error:
    print("Database connection failed!")
    print(f"Error: {error}")
