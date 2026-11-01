from src.database.connection import get_connection


def create_master_data():

    connection = get_connection()
    cursor = connection.cursor()

    # Marketing channels
    channels = [
        ("CH-001", "Email"),
        ("CH-002", "Social Media"),
        ("CH-003", "Search"),
        ("CH-004", "Display"),
        ("CH-005", "Offline")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO channels
        (channel_id, channel_name)
        VALUES (?, ?)
    """, channels)

    # Target audience groups
    audiences = [
        ("AUD-001", "New Customers", "People who have not purchased before"),
        ("AUD-002", "Existing Customers", "People who have purchased before"),
        ("AUD-003", "Website Visitors", "People who visited the website"),
        ("AUD-004", "Potential Buyers", "People interested in purchasing")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO audiences
        (audience_id, audience_name, description)
        VALUES (?, ?, ?)
    """, audiences)

    connection.commit()
    connection.close()

    print("Marketing channels and audiences added successfully!")


if __name__ == "__main__":
    create_master_data()