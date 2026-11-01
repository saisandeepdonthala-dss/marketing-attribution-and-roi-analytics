
# Source Manifest

## Project
Marketing Attribution and ROI Analytics System

## Data Source
All records used in this project are synthetically generated for development, testing, and analytics purposes.

No real customer information or confidential business data is used.

## Data Generation
- Generation method: Python-based synthetic data generation
- Random seed: 20261022
- Database: SQLite
- Data processing: Pandas and NumPy
- SQL exports: SQLite database dump

## Generated Data

| Entity | Records |
|---|---:|
| Channels | 5 |
| Campaigns | 500 |
| Creatives | 500 |
| Audiences | 4 |
| Campaign-Audience Assignments | 744 |
| Contacts | 50,000 |
| Touchpoints | 200,000 |
| Web Sessions | 20,000 |
| Leads | 15,000 |
| Opportunities | 10,000 |
| Orders | 2,517 |
| Cost Records | 1,757 |
| Attribution Results | 7,000 |

## Data Outputs

- CSV: data/processed/csv/
- JSON: data/processed/json/
- SQL: data/processed/sql/marketing_seed_data.sql
- Edge-case ground truth: data/ground_truth/

## Edge Cases

Five controlled edge cases were injected into a separate testing database:
1. Duplicate revenue
2. Touchpoint after conversion
3. Currency mismatch
4. Missing campaign costs
5. Unsupported anonymous identity link

## Reproducibility

The fixed random seed is 20261022. The generators use this seed to support repeatable synthetic data generation.

## Data Privacy

The project uses synthetic records and does not contain real personal or financial customer records.
