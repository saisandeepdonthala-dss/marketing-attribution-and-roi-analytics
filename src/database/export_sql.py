import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "marketing.db"
EXPORT_DIR = BASE_DIR / "data" / "processed" / "sql"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = EXPORT_DIR / "marketing_seed_data.sql"

def export_database_to_sql():
    connection = sqlite3.connect(DB_PATH)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("-- Marketing Attribution System SQL Export\n")
        file.write("-- Generated from the baseline database\n\n")

        for line in connection.iterdump():
            file.write(line + "\n")

    connection.close()

    print("\nSQL EXPORT COMPLETED")
    print("=" * 45)
    print(f"SQL file: {OUTPUT_FILE}")
    print(f"File size: {OUTPUT_FILE.stat().st_size / 1024:.2f} KB")


if __name__ == "__main__":
    export_database_to_sql()
