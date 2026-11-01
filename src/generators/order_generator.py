import random
from datetime import datetime, timedelta
from src.database.connection import get_connection

SEED = 20261022

def generate_orders():
    random.seed(SEED)

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT opportunity_id, closed_at
        FROM opportunities
        WHERE status = 'Closed Won'
    """)

    won_opportunities = cursor.fetchall()
    orders = []
    for number, (opportunity_id, closed_at) in enumerate(
        won_opportunities, start=1
    ):
        closed_date = datetime.fromisoformat(closed_at)

        order_date = closed_date + timedelta(
            days=random.randint(0, 15)
        )
        revenue = round(random.uniform(500, 15000), 2)
        orders.append((
            f"ORD-2026-{number:06d}",
            opportunity_id,
            revenue,
            "USD",
            order_date.isoformat()
        ))

    cursor.executemany("""
        INSERT INTO orders (
            order_id,
            opportunity_id,
            revenue,
            currency,
            order_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, orders)

    connection.commit()
    cursor.execute("SELECT COUNT(*) FROM orders")
    total = cursor.fetchone()[0]
    connection.close()
    print(f"Total orders in database: {total}")

if __name__ == "__main__":
    generate_orders()