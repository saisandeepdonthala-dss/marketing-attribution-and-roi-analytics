from src.database.connection import get_connection


def create_finance_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Customer orders and revenue
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            opportunity_id TEXT NOT NULL,
            revenue REAL NOT NULL CHECK (revenue >= 0),
            currency TEXT NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (opportunity_id)
                REFERENCES opportunities(opportunity_id)
        )
    """)

    # Campaign spending records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cost_records (
            cost_id TEXT PRIMARY KEY,
            campaign_id TEXT NOT NULL,
            cost_amount REAL NOT NULL CHECK (cost_amount >= 0),
            currency TEXT NOT NULL,
            cost_date TEXT NOT NULL,
            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(campaign_id)
        )
    """)

    # Attribution results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attribution_results (
            attribution_id TEXT PRIMARY KEY,
            opportunity_id TEXT NOT NULL,
            campaign_id TEXT NOT NULL,
            attribution_model TEXT NOT NULL,
            attribution_credit REAL NOT NULL
                CHECK (attribution_credit >= 0 AND attribution_credit <= 1),
            attributed_revenue REAL NOT NULL
                CHECK (attributed_revenue >= 0),
            attribution_date TEXT NOT NULL,
            FOREIGN KEY (opportunity_id)
                REFERENCES opportunities(opportunity_id),
            FOREIGN KEY (campaign_id)
                REFERENCES campaigns(campaign_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Financial and attribution tables created successfully!")


if __name__ == "__main__":
    create_finance_tables()