from src.database.connection import get_connection

def check_record_counts():
    connection = get_connection()
    cursor = connection.cursor()
    
    tables = [
        "channels",
        "campaigns",
        "creatives",
        "audiences",
        "contacts",
        "touchpoints",
        "web_sessions",
        "leads",
        "opportunities",
        "orders",
        "cost_records",
        "attribution_results"
    ]

    print("\nDATABASE RECORD SUMMARY")
    print("-----------------------")

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count:,}")
        
    connection.close()

if __name__ == "__main__":
    check_record_counts()