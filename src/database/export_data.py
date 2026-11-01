import sqlite3
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "marketing.db"
EXPORT_DIR = BASE_DIR / "data" / "processed" / "csv"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def export_tables_to_csv():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = [row[0] for row in cursor.fetchall()]

    print("\nCSV EXPORT REPORT")
    print("=" * 50)

    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        output_file = EXPORT_DIR / f"{table}.csv"
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(rows)
        print(f"{table}: {len(rows):,} records exported")
    connection.close()
    print("\nCSV export completed successfully!")
    print(f"Export folder: {EXPORT_DIR}")

if __name__ == "__main__":
    export_tables_to_csv()
