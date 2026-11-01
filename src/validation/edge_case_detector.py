
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "marketing_edge_cases.db"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def detect_edge_cases():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    checks = {
        "EDGE-001 - Duplicate Revenue": """
            SELECT opportunity_id
            FROM orders
            GROUP BY opportunity_id
            HAVING COUNT(*) > 1
        """,

        "EDGE-002 - Touchpoint After Conversion": """
            SELECT t.touchpoint_id
            FROM touchpoints t
            JOIN opportunities o
              ON t.contact_id = o.contact_id
            WHERE t.touchpoint_id = 'EDGE-TOUCH-002'
              AND o.status = 'Closed Won'
              AND t.touchpoint_time > o.closed_at
        """,

        "EDGE-003 - Currency Mismatch": """
            SELECT cr.cost_id
            FROM cost_records cr
            JOIN campaigns c
              ON cr.campaign_id = c.campaign_id
            WHERE cr.currency != c.currency
        """,

        "EDGE-004 - Missing Campaign Costs": """
            SELECT DISTINCT a.campaign_id
            FROM attribution_results a
            WHERE a.attribution_model = 'Multi-Touch'
              AND NOT EXISTS (
                  SELECT 1
                  FROM cost_records cr
                  WHERE cr.campaign_id = a.campaign_id
              )
        """,

        "EDGE-005 - Unsupported Anonymous Identity": """
            SELECT session_id
            FROM web_sessions
            WHERE anonymous = 1
              AND contact_id IS NOT NULL
        """
    }

    report_lines = [
        "MARKETING ATTRIBUTION - EDGE CASE DETECTION REPORT",
        "=" * 60,
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        ""
    ]

    total_detected = 0
    detected_categories = 0

    for case_name, query in checks.items():
        cursor.execute(query)
        records = cursor.fetchall()

        count = len(records)
        total_detected += count

        if count > 0:
            detected_categories += 1

        status = "DETECTED" if count > 0 else "NOT DETECTED"

        report_lines.append(case_name)
        report_lines.append(f"Status: {status}")
        report_lines.append(f"Records found: {count}")
        report_lines.append("-" * 45)

    report_lines.extend([
        "",
        f"Categories detected: {detected_categories}/5",
        f"Total problematic records: {total_detected}"
    ])

    report_text = "\n".join(report_lines)

    print("\n" + report_text)

    report_path = REPORT_DIR / "edge_case_detection_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_text)

    print(f"\nReport saved to: {report_path}")

    connection.close()


if __name__ == "__main__":
    detect_edge_cases()
