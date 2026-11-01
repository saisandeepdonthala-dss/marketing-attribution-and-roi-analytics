
import json
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "data" / "ground_truth"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

edge_cases = [
    {
        "case_id": "EDGE-001",
        "case_name": "Revenue Counted More Than Once",
        "description": "The same order revenue is counted more than once during campaign revenue aggregation.",
        "expected_detection": "Duplicate revenue must be identified during reconciliation.",
        "severity": "High"
    },
    {
        "case_id": "EDGE-002",
        "case_name": "Touchpoint After Conversion",
        "description": "A campaign touchpoint occurs after an opportunity is converted.",
        "expected_detection": "The post-conversion touchpoint must not receive attribution credit.",
        "severity": "High"
    },
    {
        "case_id": "EDGE-003",
        "case_name": "Spend Currency Mismatch",
        "description": "A campaign cost record uses a currency different from the campaign currency.",
        "expected_detection": "The mismatch must be reported instead of silently combining amounts.",
        "severity": "High"
    },
    {
        "case_id": "EDGE-004",
        "case_name": "Campaign Costs Omitted",
        "description": "A campaign has no cost records even though it has attributed revenue.",
        "expected_detection": "The campaign must be flagged as having missing cost data.",
        "severity": "Medium"
    },
    {
        "case_id": "EDGE-005",
        "case_name": "Anonymous Session Linked Without Evidence",
        "description": "An anonymous web session is linked to a contact without a valid identity-matching record.",
        "expected_detection": "The unsupported identity link must be reported.",
        "severity": "High"
    }
]

# Export JSON
json_file = OUTPUT_DIR / "edge_case_ground_truth.json"

with open(json_file, "w", encoding="utf-8") as file:
    json.dump(edge_cases, file, indent=4)

# Export CSV
csv_file = OUTPUT_DIR / "edge_case_ground_truth.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=edge_cases[0].keys())
    writer.writeheader()
    writer.writerows(edge_cases)

print("Edge-case ground truth created successfully!")
print(f"Total documented edge cases: {len(edge_cases)}")
print(f"JSON saved to: {json_file}")
print(f"CSV saved to: {csv_file}")
