import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "marketing.db"
EXPORT_DIR = BASE_DIR / "data" / "processed" / "json"

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def export_tables_to_json():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = [row["name"] for row in cursor.fetchall()]

    print("\nJSON EXPORT REPORT")
    print("=" * 50)

    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        records = [
            dict(row) for row in cursor.fetchall()
        ]
        output_file = EXPORT_DIR / f"{table}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)

        print(f"{table}: {len(records):,} records exported")

    connection.close()

    print("\nJSON export completed successfully!")
    print(f"Export folder: {EXPORT_DIR}")


if __name__ == "__main__":
    export_tables_to_json()
