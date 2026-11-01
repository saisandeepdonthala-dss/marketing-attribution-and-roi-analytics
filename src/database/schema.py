from src.database.connection import get_connection

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Marketing channels
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            channel_id TEXT PRIMARY KEY,
            channel_name TEXT NOT NULL UNIQUE
        )
    """)

    # Marketing campaigns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            campaign_id TEXT PRIMARY KEY,
            campaign_name TEXT NOT NULL,
            channel_id TEXT NOT NULL,
            budget REAL NOT NULL CHECK (budget >= 0),
            currency TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (channel_id)
                REFERENCES channels(channel_id),
            CHECK (end_date >= start_date)
        )
    """)

    # Advertisement creatives
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS creatives (
            creative_id TEXT PRIMARY KEY,
            campaign_id TEXT NOT NULL,
            creative_name TEXT NOT NULL,
            creative_type TEXT NOT NULL,
            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(campaign_id)
        )
    """)

    # Target audiences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audiences (
            audience_id TEXT PRIMARY KEY,
            audience_name TEXT NOT NULL,
            description TEXT
        )
    """)

    # Campaign and audience relationship
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaign_audiences (
            campaign_id TEXT NOT NULL,
            audience_id TEXT NOT NULL,
            PRIMARY KEY (campaign_id, audience_id),
            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(campaign_id),
            FOREIGN KEY (audience_id)
                REFERENCES audiences(audience_id)
        )
    """)

    # Contacts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            contact_id TEXT PRIMARY KEY,
            contact_name TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()
    print("Master tables created successfully!")


if __name__ == "__main__":
    create_tables()