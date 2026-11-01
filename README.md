# Marketing Attribution and ROI Analytics System

## Project Overview

This project is a Python-based Marketing Attribution and ROI Analytics System. It brings together campaign data, customer interactions, website sessions, leads, opportunities, orders, and campaign costs to understand how marketing campaigns contribute to revenue.
The project uses synthetic data to demonstrate how marketing performance can be measured and compared using different attribution models.

## Main Features
Generates marketing data for 500 campaigns, 50,000 contacts, and 200,000 touchpoints.
Connects campaigns, customers, web sessions, leads, opportunities, and orders.
Implements First-Touch, Last-Touch, and Multi-Touch attribution.
Calculates campaign ROI and ROAS.
Validates database records and relationships.
Creates separate test data for five business edge cases.
Detects data quality and attribution issues.
Exports database tables into CSV, JSON, and SQL formats.

## Technology Stack
Python
SQLite
Pandas
NumPy
Matplotlib
SQL

## Project Structure

```text
marketing-attribution-system/
│
├── data/
│   ├── raw/
│   ├── processed/
│   │   ├── csv/
│   │   ├── json/
│   │   └── sql/
│   ├── ground_truth/
│   ├── marketing.db
│   ├── marketing_baseline_backup.db
│   └── marketing_edge_cases.db
│
├── src/
│   ├── generators/
│   ├── database/
│   ├── attribution/
│   ├── validation/
│   └── analytics/
│
├── reports/
├── docs/
├── tests/
├── prompts/
├── main.py
└── requirements.txt
```

## Attribution Models

### First-Touch Attribution
Assigns 100% of the conversion revenue to the first eligible campaign touchpoint.

### Last-Touch Attribution
Assigns 100% of the conversion revenue to the last eligible campaign touchpoint before conversion.

### Multi-Touch Attribution
Distributes conversion credit equally among the distinct campaigns in the eligible customer journey.

The current attribution window is 90 days before opportunity closure. Touchpoints after conversion are excluded.

## ROI and ROAS

**ROI:**

ROI = ((Attributed Revenue - Campaign Spend) / Campaign Spend) × 100

**ROAS:**

ROAS = Attributed Revenue / Campaign Spend

The ROI report uses Multi-Touch attributed revenue for campaign-level comparisons.

## Data Generation

The project uses a fixed random seed:

`20261022`

This supports repeatable synthetic data generation.

## Edge Cases

Five business scenarios are documented and tested in a separate database:

1. Revenue counted more than once.
2. Touchpoint occurring after conversion.
3. Campaign cost currency mismatch.
4. Missing campaign cost records.
5. Anonymous session linked without identity evidence.

The edge-case detection report is saved in:

`reports/edge_case_detection_report.txt`

## How to Run

Activate the Python virtual environment:

```powershell
.\venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the data validation:

```powershell
python -m src.validation.data_validator
```

Run attribution:

```powershell
python -m src.attribution.attribution_engine
```

Generate campaign ROI:

```powershell
python -m src.analytics.roi_calculator
```

Run edge-case detection:

```powershell
python -m src.validation.edge_case_detector
```

Export CSV:

```powershell
python -m src.database.export_data
```

Export JSON:

```powershell
python -m src.database.export_json
```

Export SQL:

```powershell
python -m src.database.export_sql
```

## Current Validation Results

- Database validation: 0 issues in the baseline dataset.
- Attribution records generated: 7,000.
- Edge-case categories verified: 5 out of 5.
- CSV exports: 13 tables.
- JSON exports: 13 tables.
- SQL export: completed successfully.

These are the results from the current project run.

## Data Source

All records are synthetically generated for this project. No real customer or business information is used.