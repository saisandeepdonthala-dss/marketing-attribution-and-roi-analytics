
# Marketing Attribution and ROI Analytics System – Data Dictionary

This document explains the fields, data types, relationships and validation rules used in the project.

## 1. Campaign

| Field | Data Type | Required | Description |
|---|---|---|---|
| campaign_id | TEXT (Primary Key) | Yes | Unique campaign identifier. |
| campaign_name | TEXT | Yes | Name of the campaign. |
| channel_id | TEXT (Foreign Key) | Yes | References the channel used by the campaign. |
| budget | REAL | Yes | Planned campaign budget. |
| currency | TEXT | Yes | Currency used for the campaign budget. |
| start_date | TEXT (DATE) | Yes | Campaign start date. |
| end_date | TEXT (DATE) | Yes | Campaign end date. |
| status | TEXT | Yes | Campaign status. |

## 2. Channel

| Field | Data Type | Required | Description |
|---|---|---|---|
| channel_id | TEXT (Primary Key) | Yes | Unique channel identifier. |
| channel_name | TEXT | Yes | Name of the marketing channel. |

## 3. Creative

| Field | Data Type | Required | Description |
|---|---|---|---|
| creative_id | TEXT (Primary Key) | Yes | Unique creative identifier. |
| campaign_id | TEXT (Foreign Key) | Yes | References the related campaign. |
| creative_name | TEXT | Yes | Name of the advertisement creative. |
| creative_type | TEXT | Yes | Type of marketing creative. |

## 4. Audience

| Field | Data Type | Required | Description |
|---|---|---|---|
| audience_id | TEXT (Primary Key) | Yes | Unique audience identifier. |
| audience_name | TEXT | Yes | Name of the audience group. |
| description | TEXT | No | Additional audience information. |

## 5. Contact

| Field | Data Type | Required | Description |
|---|---|---|---|
| contact_id | TEXT (Primary Key) | Yes | Unique synthetic contact identifier. |
| contact_name | TEXT | Yes | Name assigned to the synthetic contact. |
| email | TEXT | Yes | Synthetic email address. |
| created_at | TEXT (DATETIME) | Yes | Contact creation timestamp. |

## 6. Touchpoint

| Field | Data Type | Required | Description |
|---|---|---|---|
| touchpoint_id | TEXT (Primary Key) | Yes | Unique touchpoint identifier. |
| contact_id | TEXT (Foreign Key) | Yes | References the associated contact. |
| campaign_id | TEXT (Foreign Key) | Yes | References the associated campaign. |
| channel_id | TEXT (Foreign Key) | Yes | References the marketing channel. |
| creative_id | TEXT (Foreign Key) | Yes | References the associated creative. |
| touchpoint_time | TEXT (DATETIME) | Yes | Date and time of the interaction. |
| touch_type | TEXT | Yes | Type of interaction recorded. |

## 7. WebSession

| Field | Data Type | Required | Description |
|---|---|---|---|
| session_id | TEXT (Primary Key) | Yes | Unique web session identifier. |
| contact_id | TEXT (Foreign Key) | No | Contact associated with the session, when identified. |
| session_time | TEXT (DATETIME) | Yes | Date and time of the session. |
| source | TEXT | Yes | Source of website traffic. |
| anonymous | INTEGER | Yes | Indicates whether the session is anonymous. |

## 8. Lead

| Field | Data Type | Required | Description |
|---|---|---|---|
| lead_id | TEXT (Primary Key) | Yes | Unique lead identifier. |
| contact_id | TEXT (Foreign Key) | Yes | References the associated contact. |
| session_id | TEXT (Foreign Key) | Yes | References the web session. |
| created_at | TEXT (DATETIME) | Yes | Lead creation timestamp. |
| status | TEXT | Yes | Current lead status. |

## 9. Opportunity

| Field | Data Type | Required | Description |
|---|---|---|---|
| opportunity_id | TEXT (Primary Key) | Yes | Unique opportunity identifier. |
| lead_id | TEXT (Foreign Key) | Yes | References the associated lead. |
| contact_id | TEXT (Foreign Key) | Yes | References the associated contact. |
| created_at | TEXT (DATETIME) | Yes | Opportunity creation timestamp. |
| closed_at | TEXT (DATETIME) | No | Opportunity closing timestamp, when applicable. |
| status | TEXT | Yes | Current opportunity status. |

## 10. Order

| Field | Data Type | Required | Description |
|---|---|---|---|
| order_id | TEXT (Primary Key) | Yes | Unique order identifier. |
| opportunity_id | TEXT (Foreign Key) | Yes | References the related opportunity. |
| revenue | REAL | Yes | Revenue recorded for the order. |
| currency | TEXT | Yes | Currency used for the revenue amount. |
| order_date | TEXT (DATE) | Yes | Date when the order was recorded. |

## 11. CostRecord

| Field | Data Type | Required | Description |
|---|---|---|---|
| cost_id | TEXT (Primary Key) | Yes | Unique cost record identifier. |
| campaign_id | TEXT (Foreign Key) | Yes | References the related campaign. |
| cost_amount | REAL | Yes | Marketing cost amount. |
| currency | TEXT | Yes | Currency used for the cost amount. |
| cost_date | TEXT (DATE) | Yes | Date when the cost was recorded. |

## 12. AttributionResult

| Field | Data Type | Required | Description |
|---|---|---|---|
| attribution_id | TEXT (Primary Key) | Yes | Unique attribution result identifier. |
| opportunity_id | TEXT (Foreign Key) | Yes | References the related opportunity. |
| campaign_id | TEXT (Foreign Key) | Yes | References the associated campaign. |
| attribution_model | TEXT | Yes | Attribution model used for calculation. |
| attribution_credit | REAL | Yes | Share of attribution credit assigned to the campaign. |
| attributed_revenue | REAL | Yes | Revenue credited to the campaign. |
| attribution_date | TEXT (DATETIME) | Yes | Date and time of attribution calculation. |

## 13. Campaign_Audiences

This bridge table connects campaigns and audiences.

| Field | Data Type | Required | Description |
|---|---|---|---|
| campaign_id | TEXT (Primary Key, Foreign Key) | Yes | References a campaign. |
| audience_id | TEXT (Primary Key, Foreign Key) | Yes | References an audience. |

The combination of campaign_id and audience_id identifies each campaign-audience relationship.

## Relationships and Cardinality

- Channel to Campaign: One-to-Many.
- Campaign to Creative: One-to-Many.
- Campaign to Audience: Many-to-Many through Campaign_Audiences.
- Contact to Touchpoint: One-to-Many.
- Campaign to Touchpoint: One-to-Many.
- Contact to WebSession: One-to-Many.
- Contact to Lead: One-to-Many.
- WebSession to Lead: One-to-Many.
- Lead to Opportunity: One-to-Many.
- Opportunity to Order: One-to-Many.
- Campaign to CostRecord: One-to-Many.
- Opportunity to AttributionResult: One-to-Many.
- Campaign to AttributionResult: One-to-Many.

## General Validation Rules

1. Primary keys should uniquely identify records.
2. Foreign keys should reference valid parent records.
3. Date fields should follow the expected chronological order.
4. Revenue and cost values should be checked for invalid negative amounts.
5. Attribution credit should be between 0 and 1.
6. Multi-Touch attribution credits should total 1 for each attributed opportunity.
7. Currency should be considered when comparing campaign spending and revenue.
8. Anonymous sessions should not be assigned to contacts without identity evidence.
9. Touchpoints occurring after conversion should not receive attribution credit.
10. Known data anomalies should be recorded in the ground-truth files.

## Data Generation and Reproducibility

- Data source: Synthetic data generated using Python.
- Random seed: 20261022.
- Database: SQLite.
- Processing libraries: Pandas and NumPy.
- Export formats: CSV, JSON and SQL.
- Consistent identifiers are used across generated datasets.
- A fixed random seed supports reproducible data generation.

All records in this project are synthetic and intended for development, testing and analytics.
