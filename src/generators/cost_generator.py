import random
from datetime import date, timedelta
from src.database.connection import get_connection

SEED = 20261022

def generate_costs():
    random.seed(SEED)
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT campaign_id, start_date, end_date, budget, currency
        FROM campaigns
    """)
    campaigns = cursor.fetchall()
    costs = []

    for campaign_id, start_date, end_date, budget, currency in campaigns:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        # Divide campaign spending into multiple records.
        number_of_records = random.randint(2, 5)
        for _ in range(number_of_records):
            days = (end - start).days
            cost_date = start + timedelta(
                days=random.randint(0, days)
            )

            amount = round(
                random.uniform(0.05, 0.20) * budget,
                2
            )

            cost_id = f"COST-{len(costs) + 1:06d}"
            costs.append((
                cost_id,
                campaign_id,
                amount,
                currency,
                cost_date.isoformat()
            ))

    cursor.executemany("""
        INSERT INTO cost_records (
            cost_id,
            campaign_id,
            cost_amount,
            currency,
            cost_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, costs)

    connection.commit()
    cursor.execute("SELECT COUNT(*) FROM cost_records")
    total = cursor.fetchone()[0]
    connection.close()
    print(f"Total campaign cost records in database: {total}")
    
if __name__ == "__main__":
    generate_costs()