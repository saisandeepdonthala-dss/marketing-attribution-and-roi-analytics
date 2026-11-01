from src.database.connection import get_connection

def validate_database():
    connection = get_connection()
    cursor = connection.cursor()

    issues = []

    print("\nDATA VALIDATION REPORT")
    print("=" * 55)

    # 1. Check primary key duplicates.
    primary_key_checks = {
        "campaigns": "campaign_id",
        "contacts": "contact_id",
        "touchpoints": "touchpoint_id",
        "web_sessions": "session_id",
        "leads": "lead_id",
        "opportunities": "opportunity_id",
        "orders": "order_id",
        "cost_records": "cost_id"
    }

    for table, column in primary_key_checks.items():
        cursor.execute(f"""
            SELECT COUNT(*) - COUNT(DISTINCT {column})
            FROM {table}
        """)
        duplicates = cursor.fetchone()[0]
        if duplicates > 0:
            issues.append(
                f"{table}: {duplicates} duplicate primary keys"
            )

    # 2. Check foreign key violations.
    tables = [
        "campaigns",
        "creatives",
        "campaign_audiences",
        "touchpoints",
        "web_sessions",
        "leads",
        "opportunities",
        "orders",
        "cost_records",
        "attribution_results"
    ]

    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_check({table})")
        violations = cursor.fetchall()
        if violations:
            issues.append(
                f"{table}: {len(violations)} foreign key violations"
            )

    # 3. Check campaign date order.
    cursor.execute("""
        SELECT COUNT(*)
        FROM campaigns
        WHERE end_date < start_date
    """)

    invalid_campaign_dates = cursor.fetchone()[0]
    if invalid_campaign_dates:
        issues.append(
            f"{invalid_campaign_dates} campaigns have invalid dates"
        )

    # 4. Check opportunity date order.
    cursor.execute("""
        SELECT COUNT(*)
        FROM opportunities
        WHERE closed_at IS NOT NULL
          AND closed_at < created_at
    """)

    invalid_opportunity_dates = cursor.fetchone()[0]
    if invalid_opportunity_dates:
        issues.append(
            f"{invalid_opportunity_dates} opportunities have invalid dates"
        )

    # 5. Check orders with negative revenue.
    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE revenue < 0
    """)
    invalid_revenue = cursor.fetchone()[0]
    if invalid_revenue:
        issues.append(
            f"{invalid_revenue} orders have negative revenue"
        )

    # 6. Check negative campaign costs.
    cursor.execute("""
        SELECT COUNT(*)
        FROM cost_records
        WHERE cost_amount < 0
    """)
    invalid_costs = cursor.fetchone()[0]
    if invalid_costs:
        issues.append(
            f"{invalid_costs} cost records have negative amounts"
        )

    # 7. Check attribution credit.
    cursor.execute("""
        SELECT COUNT(*)
        FROM attribution_results
        WHERE attribution_credit < 0
           OR attribution_credit > 1
    """)
    invalid_credits = cursor.fetchone()[0]
    if invalid_credits:
        issues.append(
            f"{invalid_credits} attribution records have invalid credits"
        )

    # 8. Check total multi-touch credit per opportunity.
    cursor.execute("""
        SELECT opportunity_id, SUM(attribution_credit)
        FROM attribution_results
        WHERE attribution_model = 'Multi-Touch'
        GROUP BY opportunity_id
        HAVING ABS(SUM(attribution_credit) - 1.0) > 0.000001
    """)

    incorrect_credit = cursor.fetchall()

    if incorrect_credit:
        issues.append(
            f"{len(incorrect_credit)} opportunities have incorrect "
            "multi-touch credit totals"
        )

    # Print report.
    if issues:
        print("\nValidation completed with issues:\n")

        for issue in issues:
            print(f"- {issue}")
    else:
        print("\nAll current validation checks passed!")
    print(f"\nTotal issues found: {len(issues)}")
    connection.close()

if __name__ == "__main__":
    validate_database()
