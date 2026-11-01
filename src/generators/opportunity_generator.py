import random
from datetime import datetime, timedelta
from src.database.connection import get_connection

SEED = 20261022
TOTAL_OPPORTUNITIES = 10000

def generate_opportunities():
    random.seed(SEED)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT lead_id, contact_id, created_at
        FROM leads
    """)
    leads = cursor.fetchall()

    selected_leads = random.sample(leads, TOTAL_OPPORTUNITIES)
    opportunities = []
    statuses = [
        "Open",
        "Qualified",
        "Proposal",
        "Closed Won",
        "Closed Lost"
    ]

    for number, (lead_id, contact_id, lead_created) in enumerate(
        selected_leads, start=1
    ):
        lead_date = datetime.fromisoformat(lead_created)

        # Opportunity creation must happen after the lead date.
        opportunity_date = lead_date + timedelta(
            days=random.randint(1, 30)
        )

        status = random.choices(
            statuses,
            weights=[20, 20, 20, 25, 15],
            k=1
        )[0]
        closed_at = None

        if status in ["Closed Won", "Closed Lost"]:
            closed_at = (
                opportunity_date + timedelta(
                    days=random.randint(1, 60)
                )
            ).isoformat()
        opportunity_id = f"OPP-2026-{number:06d}"

        opportunities.append((
            opportunity_id,
            lead_id,
            contact_id,
            opportunity_date.isoformat(),
            closed_at,
            status
        ))

    cursor.executemany("""
        INSERT INTO opportunities (
            opportunity_id,
            lead_id,
            contact_id,
            created_at,
            closed_at,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, opportunities)
    connection.commit()
    cursor.execute("SELECT COUNT(*) FROM opportunities")
    total = cursor.fetchone()[0]
    connection.close()
    print(f"Total opportunities in database: {total}")

if __name__ == "__main__":
    generate_opportunities()