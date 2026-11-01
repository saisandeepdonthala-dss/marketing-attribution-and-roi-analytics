import random
from collections import defaultdict
from bisect import bisect_right
from datetime import date, datetime, time, timedelta
from src.database.connection import get_connection

SEED = 20261022
TOTAL_TOUCHPOINTS = 200000

TOUCH_TYPES = [
    "Impression",
    "Click",
    "Email",
    "Offline"
]


def generate_touchpoints():
    random.seed(SEED)
    connection = get_connection()
    cursor = connection.cursor()

    # Get contacts and their creation dates
    cursor.execute("""
        SELECT contact_id, created_at
        FROM contacts
        ORDER BY created_at
    """)
    contacts = cursor.fetchall()
    contact_dates = [
        date.fromisoformat(row[1]) for row in contacts
    ]

    # Get campaigns and their related information
    cursor.execute("""
        SELECT
            c.campaign_id,
            c.channel_id,
            c.start_date,
            c.end_date,
            cr.creative_id
        FROM campaigns c
        JOIN creatives cr
        ON c.campaign_id = cr.campaign_id
    """)
    campaigns = cursor.fetchall()

    # Store generated touchpoints
    touchpoints = []

    # Keep a separate counter for each contact
    contact_counters = defaultdict(int)
    for number in range(TOTAL_TOUCHPOINTS):
        campaign = random.choice(campaigns)
        campaign_id = campaign[0]
        channel_id = campaign[1]
        start_date = date.fromisoformat(campaign[2])
        end_date = date.fromisoformat(campaign[3])
        creative_id = campaign[4]

        # Select a contact created before the campaign ends
        eligible_count = bisect_right(
            contact_dates,
            end_date
        )

        if eligible_count == 0:
            continue
        contact_index = random.randrange(eligible_count)
        contact_id = contacts[contact_index][0]
        contact_created = contact_dates[contact_index]

        # Touchpoint must happen during the campaign
        earliest_date = max(start_date, contact_created)
        if earliest_date > end_date:
            continue
        days = (end_date - earliest_date).days
        touch_date = earliest_date + timedelta(
            days=random.randint(0, days)
        )

        touch_time = datetime.combine(
            touch_date,
            time(
                random.randint(8, 21),
                random.randint(0, 59)
            )
        )

        contact_counters[contact_id] += 1
        touchpoint_id = (
            f"TOUCH-{contact_id}-"
            f"{contact_counters[contact_id]:06d}"
        )
        touch_type = random.choice(TOUCH_TYPES)
        touchpoints.append((
            touchpoint_id,
            contact_id,
            campaign_id,
            channel_id,
            creative_id,
            touch_time.isoformat(),
            touch_type
        ))

        # Insert in batches to avoid keeping everything in memory
        if len(touchpoints) >= 10000:
            cursor.executemany("""
                INSERT INTO touchpoints (
                    touchpoint_id,
                    contact_id,
                    campaign_id,
                    channel_id,
                    creative_id,
                    touchpoint_time,
                    touch_type
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, touchpoints)
            connection.commit()
            touchpoints.clear()

    if touchpoints:
        cursor.executemany("""
            INSERT INTO touchpoints (
                touchpoint_id,
                contact_id,
                campaign_id,
                channel_id,
                creative_id,
                touchpoint_time,
                touch_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, touchpoints)
        connection.commit()

    cursor.execute("SELECT COUNT(*) FROM touchpoints")
    total = cursor.fetchone()[0]
    connection.close()
    print(f"Total touchpoints in database: {total}")


if __name__ == "__main__":
    generate_touchpoints()