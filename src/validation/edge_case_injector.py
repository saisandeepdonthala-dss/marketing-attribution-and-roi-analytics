
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
TEST_DB_PATH = BASE_DIR / "data" / "marketing_edge_cases.db"


def verify_edge_cases():
    connection = sqlite3.connect(TEST_DB_PATH)
    cursor = connection.cursor()

    checks = {
        "EDGE-001: Duplicate order": """
            SELECT COUNT(*) FROM orders
            WHERE order_id = 'EDGE-ORDER-001'
        """,
        "EDGE-002: Post-conversion touchpoint": """
            SELECT COUNT(*) FROM touchpoints
            WHERE touchpoint_id = 'EDGE-TOUCH-002'
        """,
        "EDGE-003: Currency mismatch": """
            SELECT COUNT(*) FROM cost_records
            WHERE cost_id = 'EDGE-COST-003'
        """,
        "EDGE-004: Campaign costs omitted": """
            SELECT COUNT(*)
            FROM attribution_results a
            WHERE a.attribution_model = 'Multi-Touch'
              AND NOT EXISTS (
                  SELECT 1 FROM cost_records c
                  WHERE c.campaign_id = a.campaign_id
              )
        """,
        "EDGE-005: Anonymous session linked": """
            SELECT COUNT(*) FROM web_sessions
            WHERE anonymous = 1
              AND contact_id IS NOT NULL
        """
    }

    print("\nEDGE-CASE VERIFICATION REPORT")
    print("=" * 55)

    passed = 0

    for name, query in checks.items():
        cursor.execute(query)
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"PASS - {name}: {count}")
            passed += 1
        else:
            print(f"FAIL - {name}: Not found")

    print("\nSummary:")
    print(f"Scenarios found: {passed}/5")

    connection.close()


if __name__ == "__main__":
    verify_edge_cases()
