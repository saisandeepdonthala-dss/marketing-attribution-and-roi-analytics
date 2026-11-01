
import sqlite3
from pathlib import Path

import pytest


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "marketing.db"

EXPECTED_TABLES = [
    "channels",
    "campaigns",
    "creatives",
    "audiences",
    "campaign_audiences",
    "contacts",
    "touchpoints",
    "web_sessions",
    "leads",
    "opportunities",
    "orders",
    "cost_records",
    "attribution_results",
]


@pytest.fixture
def connection():
    assert DB_PATH.exists(), "Marketing database does not exist."

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    yield conn

    conn.close()


def test_database_integrity(connection):
    result = connection.execute(
        "PRAGMA integrity_check"
    ).fetchone()[0]

    assert result == "ok"


def test_all_expected_tables_exist(connection):
    existing_tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }

    for table in EXPECTED_TABLES:
        assert table in existing_tables, f"Missing table: {table}"


def test_primary_keys_are_unique(connection):
    for table in EXPECTED_TABLES:
        columns = connection.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()

        primary_keys = [
            row[1]
            for row in sorted(columns, key=lambda row: row[5])
            if row[5] > 0
        ]

        assert primary_keys, f"No primary key defined for {table}"

        key_columns = ", ".join(
            f'"{column}"' for column in primary_keys
        )

        query = f"""
            SELECT {key_columns}
            FROM "{table}"
            GROUP BY {key_columns}
            HAVING COUNT(*) > 1
            LIMIT 1
        """

        duplicate = connection.execute(query).fetchone()

        assert duplicate is None, (
            f"Duplicate primary key in {table}: {duplicate}"
        )


def test_foreign_key_integrity(connection):
    violations = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    assert violations == [], f"Foreign key violations: {violations}"


def test_attribution_credits_are_valid(connection):
    invalid_credits = connection.execute("""
        SELECT COUNT(*)
        FROM attribution_results
        WHERE attribution_credit < 0
           OR attribution_credit > 1
    """).fetchone()[0]

    assert invalid_credits == 0


def test_attribution_credit_totals(connection):
    results = connection.execute("""
        SELECT opportunity_id, attribution_model,
               SUM(attribution_credit)
        FROM attribution_results
        GROUP BY opportunity_id, attribution_model
    """).fetchall()

    assert results, "No attribution results found."

    for opportunity_id, model, total_credit in results:
        assert abs(total_credit - 1.0) < 0.01, (
            f"Invalid credit total for {opportunity_id}, "
            f"{model}: {total_credit}"
        )
