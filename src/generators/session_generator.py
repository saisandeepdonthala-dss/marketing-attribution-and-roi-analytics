import random
from datetime import datetime, timedelta
from src.database.connection import get_connection

SEED = 20261022
TOTAL_SESSIONS = 20000

def generate_sessions():
    random.seed(SEED)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT contact_id FROM contacts")
    contacts = [row[0] for row in cursor.fetchall()]

    sources = [
        "Email",
        "Social Media",
        "Search",
        "Display",
        "Direct",
        "Offline"
    ]
    sessions = []

    for number in range(1, TOTAL_SESSIONS + 1):
        session_id = f"SES-2026-{number:06d}"

        # Some visitors will remain anonymous.
        is_anonymous = random.random() < 0.20
        if is_anonymous:
            contact_id = None
            anonymous = 1
        else:
            contact_id = random.choice(contacts)
            anonymous = 0

        start = datetime(2026, 1, 1)
        end = datetime(2026, 10, 31)
        days = (end - start).days

        session_date = start + timedelta(
            days=random.randint(0, days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        source = random.choice(sources)
        sessions.append((
            session_id,
            contact_id,
            session_date.isoformat(),
            source,
            anonymous
        ))

    cursor.executemany("""
        INSERT INTO web_sessions (
            session_id,
            contact_id,
            session_time,
            source,
            anonymous
        )
        VALUES (?, ?, ?, ?, ?)
    """, sessions)

    connection.commit()
    cursor.execute("SELECT COUNT(*) FROM web_sessions")
    total = cursor.fetchone()[0]
    connection.close()
    print(f"Total web sessions in database: {total}")

if __name__ == "__main__":
    generate_sessions()