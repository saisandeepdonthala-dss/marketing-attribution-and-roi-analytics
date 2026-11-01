import random
from datetime import date, timedelta

from src.database.connection import get_connection


SEED = 20261022
TOTAL_CONTACTS = 50000

FIRST_NAMES = [
    "Arun", "Rahul", "Priya", "Sneha", "Kiran",
    "Ananya", "Vikram", "Meera", "Ravi", "Neha",
    "Suresh", "Divya", "Amit", "Pooja", "Rohan"
]

LAST_NAMES = [
    "Sharma", "Reddy", "Kumar", "Patel", "Rao",
    "Singh", "Verma", "Gupta", "Das", "Nair"
]


def generate_contacts():
    random.seed(SEED)
    connection = get_connection()
    cursor = connection.cursor()
    contacts = []
    start_date = date(2025, 1, 1)
    end_date = date(2026, 10, 31)
    total_days = (end_date - start_date).days

    for number in range(1, TOTAL_CONTACTS + 1):

        contact_id = f"CON-2026-{number:06d}"

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        contact_name = f"{first_name} {last_name}"
        email = f"{contact_id.lower()}@example.com"
        created_at = start_date + timedelta(
            days=random.randint(0, total_days)
        )

        contacts.append((
            contact_id,
            contact_name,
            email,
            created_at.isoformat()
        ))

    cursor.executemany("""
        INSERT INTO contacts (
            contact_id,
            contact_name,
            email,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, contacts)

    connection.commit()
    connection.close()

    print(f"Contacts created: {len(contacts)}")


if __name__ == "__main__":
    generate_contacts()