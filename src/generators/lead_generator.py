import random
from collections import defaultdict
from datetime import datetime, timedelta
from src.database.connection import get_connection

SEED = 20261022
TOTAL_LEADS = 15000

def generate_leads():
    random.seed(SEED)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT contact_id, created_at
        FROM contacts
    """)
    contacts = cursor.fetchall()
    cursor.execute("""
        SELECT session_id, contact_id, session_time
        FROM web_sessions
        WHERE contact_id IS NOT NULL
    """)
    session_rows = cursor.fetchall()

    # Group sessions by contact.
    contact_sessions = defaultdict(list)
    for session_id, contact_id, session_time in session_rows:
        contact_sessions[contact_id].append(
            (session_id, datetime.fromisoformat(session_time))
        )

    selected_contacts = random.sample(contacts, TOTAL_LEADS)
    leads = []
    end_date = datetime(2026, 10, 31, 23, 59)
    for number, (contact_id, contact_created) in enumerate(
        selected_contacts, start=1
    ):
        contact_date = datetime.fromisoformat(contact_created)
        earliest = max(
            contact_date,
            datetime(2026, 1, 1)
        )

        if earliest > end_date:
            lead_date = contact_date
        else:
            days = (end_date - earliest).days
            lead_date = earliest + timedelta(
                days=random.randint(0, days),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

        # Use only a session belonging to this contact
        # that happened before the lead was created.
        eligible_sessions = [
            session for session in contact_sessions[contact_id]
            if session[1] <= lead_date
        ]

        session_id = (
            random.choice(eligible_sessions)[0]
            if eligible_sessions and random.random() < 0.70
            else None
        )

        status = random.choice([
            "New",
            "Qualified",
            "Disqualified",
            "Converted"
        ])

        lead_id = f"LEAD-2026-{number:06d}"
        leads.append((
            lead_id,
            contact_id,
            session_id,
            lead_date.isoformat(),
            status
        ))

    cursor.executemany("""
        INSERT INTO leads (
            lead_id,
            contact_id,
            session_id,
            created_at,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, leads)
    connection.commit()
    cursor.execute("SELECT COUNT(*) FROM leads")
    total = cursor.fetchone()[0]
    connection.close()
    print(f"Total leads in database: {total}")


if __name__ == "__main__":
    generate_leads()