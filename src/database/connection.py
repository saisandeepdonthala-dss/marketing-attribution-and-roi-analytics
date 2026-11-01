
import sqlite3
from pathlib import Path


# Find the main project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Create the database folder
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)

# Main database file location
DB_PATH = DB_DIR / "marketing.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)

    # Enable foreign key checking
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def reset_database():
    """Remove the existing database and create a fresh empty one."""

    if DB_PATH.exists():
        DB_PATH.unlink()
        print("Existing database removed.")

    connection = get_connection()
    connection.close()

    print("Fresh database connection created.")


if __name__ == "__main__":
    connection = get_connection()

    print("Database connection successful!")
    print(f"Database location: {DB_PATH}")

    connection.close()
