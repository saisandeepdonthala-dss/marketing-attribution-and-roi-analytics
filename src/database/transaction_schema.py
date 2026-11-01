from src.database.connection import get_connection

def create_transaction_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Customer marketing interactions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS touchpoints (
            touchpoint_id TEXT PRIMARY KEY,
            contact_id TEXT NOT NULL,
            campaign_id TEXT NOT NULL,
            channel_id TEXT NOT NULL,
            creative_id TEXT,
            touchpoint_time TEXT NOT NULL,
            touch_type TEXT NOT NULL,
            FOREIGN KEY (contact_id)
                REFERENCES contacts(contact_id),
            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(campaign_id),
            FOREIGN KEY (channel_id)
                REFERENCES channels(channel_id),
            FOREIGN KEY (creative_id)
                REFERENCES creatives(creative_id)
        )
    """)

    # Website visits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS web_sessions (
            session_id TEXT PRIMARY KEY,
            contact_id TEXT,
            session_time TEXT NOT NULL,
            source TEXT,
            anonymous INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (contact_id)
                REFERENCES contacts(contact_id)
        )
    """)

    # Marketing leads
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id TEXT PRIMARY KEY,
            contact_id TEXT NOT NULL,
            session_id TEXT,
            created_at TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (contact_id)
                REFERENCES contacts(contact_id),
            FOREIGN KEY (session_id)
                REFERENCES web_sessions(session_id)
        )
    """)

    # Sales opportunities
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            opportunity_id TEXT PRIMARY KEY,
            lead_id TEXT NOT NULL,
            contact_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            closed_at TEXT,
            status TEXT NOT NULL,
            FOREIGN KEY (lead_id)
                REFERENCES leads(lead_id),
            FOREIGN KEY (contact_id)
                REFERENCES contacts(contact_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Transaction tables created successfully!")


if __name__ == "__main__":
    create_transaction_tables()