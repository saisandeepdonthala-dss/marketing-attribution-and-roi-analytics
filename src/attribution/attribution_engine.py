
from datetime import datetime, timedelta

from src.database.connection import get_connection


ATTRIBUTION_WINDOW_DAYS = 90
SEED_YEAR = 2026


def calculate_attribution():
    connection = get_connection()
    cursor = connection.cursor()

    # Get closed-won opportunities that have orders.
    cursor.execute("""
        SELECT
            o.opportunity_id,
            o.contact_id,
            o.closed_at,
            SUM(ord.revenue) AS total_revenue
        FROM opportunities o
        INNER JOIN orders ord
            ON o.opportunity_id = ord.opportunity_id
        WHERE o.status = 'Closed Won'
          AND o.closed_at IS NOT NULL
        GROUP BY
            o.opportunity_id,
            o.contact_id,
            o.closed_at
        ORDER BY o.opportunity_id
    """)

    opportunities = cursor.fetchall()

    results = []

    for opportunity_id, contact_id, closed_at, revenue in opportunities:

        if not contact_id or not closed_at or revenue is None:
            continue

        conversion_date = datetime.fromisoformat(closed_at)

        # Consider only touchpoints from the 90 days
        # before conversion, including the conversion date.
        window_start = (
            conversion_date - timedelta(days=ATTRIBUTION_WINDOW_DAYS)
        )

        cursor.execute("""
            SELECT campaign_id, touchpoint_time
            FROM touchpoints
            WHERE contact_id = ?
              AND touchpoint_time >= ?
              AND touchpoint_time <= ?
            ORDER BY touchpoint_time ASC
        """, (
            contact_id,
            window_start.isoformat(),
            conversion_date.isoformat()
        ))

        touchpoints = cursor.fetchall()

        if not touchpoints:
            continue

        # First-Touch Attribution
        first_campaign = touchpoints[0][0]

        results.append((
            opportunity_id,
            first_campaign,
            "First-Touch",
            1.0,
            round(revenue, 2),
            conversion_date.isoformat()
        ))

        # Last-Touch Attribution
        last_campaign = touchpoints[-1][0]

        results.append((
            opportunity_id,
            last_campaign,
            "Last-Touch",
            1.0,
            round(revenue, 2),
            conversion_date.isoformat()
        ))

        # Multi-Touch Attribution
        # Give equal credit to each distinct campaign.
        campaign_ids = list(dict.fromkeys(
            campaign_id for campaign_id, _ in touchpoints
        ))

        credit = 1.0 / len(campaign_ids)

        for campaign_id in campaign_ids:
            results.append((
                opportunity_id,
                campaign_id,
                "Multi-Touch",
                credit,
                round(revenue * credit, 2),
                conversion_date.isoformat()
            ))

    # Remove previous attribution results before recalculating.
    cursor.execute("DELETE FROM attribution_results")

    # Insert new results with unique attribution IDs.
    if results:
        records_with_ids = [
            (
                f"ATTR-{SEED_YEAR}-{i:07d}",
                *record
            )
            for i, record in enumerate(results, start=1)
        ]

        cursor.executemany("""
            INSERT INTO attribution_results (
                attribution_id,
                opportunity_id,
                campaign_id,
                attribution_model,
                attribution_credit,
                attributed_revenue,
                attribution_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, records_with_ids)

    connection.commit()

    total = cursor.execute("""
        SELECT COUNT(*)
        FROM attribution_results
    """).fetchone()[0]

    connection.close()

    print("Attribution calculation completed!")
    print(f"Total attribution records: {total}")


if __name__ == "__main__":
    calculate_attribution()
