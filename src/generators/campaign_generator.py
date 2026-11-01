import random
from datetime import date, timedelta

from src.database.connection import get_connection

SEED = 20261022
TOTAL_CAMPAIGNS = 500


def generate_campaigns():
    random.seed(SEED)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT channel_id FROM channels")
    channels = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT audience_id FROM audiences")
    audiences = [row[0] for row in cursor.fetchall()]

    campaign_records = []
    creative_records = []
    audience_records = []
    campaign_names = [
        "Summer Sale",
        "Product Launch",
        "Customer Retention",
        "Brand Awareness",
        "Festival Promotion",
        "New Customer Offer",
        "Winter Campaign",
        "Website Traffic"
    ]

    creative_types = ["Image", "Video", "Text", "Banner"]

    start_limit = date(2026, 1, 1)
    end_limit = date(2026, 10, 31)
    for number in range(1, TOTAL_CAMPAIGNS + 1):
        campaign_id = f"CMP-2026-{number:06d}"
        channel_id = random.choice(channels)
        campaign_name = (
            f"{random.choice(campaign_names)} {number}"
        )
        budget = round(random.uniform(5000, 100000), 2)
        start_offset = random.randint(
            0, (end_limit - start_limit).days - 30
        )
        start_date = start_limit + timedelta(days=start_offset)
        duration = random.randint(15, 90)
        end_date = start_date + timedelta(days=duration)

        if end_date > end_limit:
            end_date = end_limit

        campaign_records.append((
            campaign_id,
            campaign_name,
            channel_id,
            budget,
            "USD",
            start_date.isoformat(),
            end_date.isoformat(),
            "Completed"
        ))

        # Create one advertisement for each campaign
        creative_id = f"CRE-2026-{number:06d}"

        creative_records.append((
            creative_id,
            campaign_id,
            f"Creative {number}",
            random.choice(creative_types)
        ))

        # Assign one or two audience groups
        selected_audiences = random.sample(
            audiences,
            k=random.randint(1, 2)
        )

        for audience_id in selected_audiences:
            audience_records.append((
                campaign_id,
                audience_id
            ))

    cursor.executemany("""
        INSERT INTO campaigns (
            campaign_id, campaign_name, channel_id,
            budget, currency, start_date, end_date, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, campaign_records)

    cursor.executemany("""
        INSERT INTO creatives (
            creative_id, campaign_id, creative_name, creative_type
        )
        VALUES (?, ?, ?, ?)
    """, creative_records)

    cursor.executemany("""
        INSERT INTO campaign_audiences (
            campaign_id, audience_id
        )
        VALUES (?, ?)
    """, audience_records)

    connection.commit()
    connection.close()

    print(f"Campaigns created: {len(campaign_records)}")
    print(f"Creatives created: {len(creative_records)}")
    print(f"Audience assignments: {len(audience_records)}")


if __name__ == "__main__":
    generate_campaigns()