# Marketing Attribution and ROI Analytics System – Data Dictionary

This document explains the fields, data types, relationships and validation rules used in the project.

## 1. Campaign

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| campaign_id | TEXT (Primary Key) | Yes | Unique campaign ID. Format: CMP-2026-000001. |
| campaign_name | TEXT | Yes | Name of the campaign. |
| channel_id | TEXT (Foreign Key) | Yes | References an existing channel. |
| budget | REAL | Yes | Planned campaign budget. Must be non-negative. |
| currency | TEXT | Yes | Currency code, such as USD, INR or EUR. |
| start_date | TEXT (DATE) | Yes | Campaign start date. |
| end_date | TEXT (DATE) | Yes | Must be on or after start_date. |
| status | TEXT | Yes | Active, Completed or Paused. |

## 2. Channel

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| channel_id | TEXT (Primary Key) | Yes | Unique channel ID. |
| channel_name | TEXT | Yes | Email, Social Media, Search, Display or Offline. |

## 3. Creative

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| creative_id | TEXT (Primary Key) | Yes | Unique creative ID. |
| campaign_id | TEXT (Foreign Key) | Yes | References an existing campaign. |
| creative_name | TEXT | Yes | Name of the advertisement. |
| creative_type | TEXT | Yes | Image, Video, Text or Banner. |

## 4. Audience

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| audience_id | TEXT (Primary Key) | Yes | Unique audience ID. |
| audience_name | TEXT | Yes | Name of the audience group. |
| description | TEXT | No | Description of the audience. |

## 5. Contact

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| contact_id | TEXT (Primary Key) | Yes | Unique synthetic contact ID. |
| contact_name | TEXT | Yes | Synthetic contact name. |
| email | TEXT | Yes | Synthetic email address; unique. |
| created_at | TEXT (DATETIME) | Yes | Contact creation timestamp. |

## 6. Touchpoint

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| touchpoint_id | TEXT (Primary Key) | Yes | Unique ID. Format: TOUCH-CON-2026-000001-000001. |
| contact_id | TEXT (Foreign Key) | Yes | References an existing contact. |
| campaign_id | TEXT (Foreign Key) | Yes | References an existing campaign. |
| channel_id | TEXT (Foreign Key) | Yes | References an existing channel. |
| creative_id | TEXT (Foreign Key) | Yes | References an existing creative. |
| touchpoint_time | TEXT (DATETIME) | Yes | Date and time of interaction. |
| touch_type | TEXT | Yes | Impression, Click, Email or Offline. |

## 7. WebSession

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| session_id | TEXT (Primary Key) | Yes | Unique ID. Format: SES-2026-000001. |
| contact_id | TEXT (Foreign Key) | No | References a contact when identity is known; otherwise NULL. |
| session_time | TEXT (DATETIME) | Yes | Session date and time. |
| source | TEXT | Yes | Traffic source. |
| anonymous | INTEGER | Yes | 1 = anonymous, 0 = identified. |

## 8. Lead

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| lead_id | TEXT (Primary Key) | Yes | Unique ID. Format: LEAD-2026-000001. |
| contact_id | TEXT (Foreign Key) | Yes | References an existing contact. |
| session_id | TEXT (Foreign Key) | Yes | References an existing session. |
| created_at | TEXT (DATETIME) | Yes | Lead creation timestamp. |
| status | TEXT | Yes | New, Qualified or Converted. |

## 9. Opportunity

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| opportunity_id | TEXT (Primary Key) | Yes | Unique ID. Format: OPP-2026-000001. |
| lead_id | TEXT (Foreign Key) | Yes | References an existing lead. |
| contact_id | TEXT (Foreign Key) | Yes | References an existing contact. |
| created_at | TEXT (DATETIME) | Yes | Opportunity creation timestamp. |
| closed_at | TEXT (DATETIME) | No | Closing timestamp; required for closed opportunities. |
| status | TEXT | Yes | Open, Qualified, Proposal, Closed Won or Closed Lost. |

## 10. Order

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| order_id | TEXT (Primary Key) | Yes | Unique order ID. |
| opportunity_id | TEXT (Foreign Key) | Yes | References an existing opportunity. |
| revenue | REAL | Yes | Revenue amount; must be non-negative. |
| currency | TEXT | Yes | Currency code for the revenue. |
| order_date | TEXT (DATE) | Yes | Order date; should be consistent with the opportunity lifecycle. |

## 11. CostRecord

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| cost_id | TEXT (Primary Key) | Yes | Unique cost record ID. |
| campaign_id | TEXT (Foreign Key) | Yes | References an existing campaign. |
| cost_amount | REAL | Yes | Campaign spending amount; must be non-negative. |
| currency | TEXT | Yes | Currency code; should match campaign currency for direct reconciliation. |
| cost_date | TEXT (DATE) | Yes | Date on which the cost was recorded. |

## 12. AttributionResult

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| attribution_id | TEXT (Primary Key) | Yes | Unique attribution result ID. |
| opportunity_id | TEXT (Foreign Key) | Yes | References an existing opportunity. |
| campaign_id | TEXT (Foreign Key) | Yes | References an existing campaign. |
| attribution_model | TEXT | Yes | First-Touch, Last-Touch or Multi-Touch. |
| attribution_credit | REAL | Yes | Attribution credit between 0 and 1. |
| attributed_revenue | REAL | Yes | Revenue assigned to the campaign; must be non-negative. |
| attribution_date | TEXT (DATETIME) | Yes | Date and time of attribution calculation. |

## 13. Bridge Table: Campaign_Audiences

This table connects campaigns and audiences through a many-to-many relationship.

| Field | Data Type | Required | Description and Validation |
|---|---|---|---|
| campaign_id | TEXT (Primary Key, Foreign Key) | Yes | References an existing campaign. |
| audience_id | TEXT (Primary Key, Foreign Key) | Yes | References an existing audience. |

The combination of campaign_id and audience_id must be unique.

## Relationships and Cardinality

- Channel to Campaign: One-to-Many (1:N).
- Campaign to Creative: One-to-Many (1:N).
- Campaign to Audience: Many-to-Many (N:M), using Campaign_Audiences.
- Contact to Touchpoint: One-to-Many (1:N).
- Campaign to Touchpoint: One-to-Many (1:N).
- Contact to WebSession: One-to-Many (1:N), with optional contact identity.
- Contact to Lead: One-to-Many (1:N).
- WebSession to Lead: One-to-Many (1:N).
- Lead to Opportunity: One-to-Many (1:N).
- Opportunity to Order: One-to-Many (1:N).
- Campaign to CostRecord: One-to-Many (1:N).
- Opportunity to AttributionResult: One-to-Many (1:N).
- Campaign to AttributionResult: One-to-Many (1:N).

## General Validation Rules

1. Primary keys must be unique and must not be NULL.
2. Foreign keys must reference valid parent records.
3. Campaign and opportunity dates must follow valid chronological order.
4. Revenue and cost values must not be negative.
5. Attribution credit must be between 0 and 1.
6. Multi-Touch attribution credits must total 1 for each attributed opportunity.
7. Currency must be checked before comparing campaign spending and revenue.
8. Anonymous sessions must not be linked to contacts without supporting identity evidence.
9. Touchpoints after conversion must not be included in attribution.
10. Known anomalies must be documented separately in the ground-truth files.

## Data Generation and Reproducibility

- Data source: Synthetic records generated using Python.
- Random seed: 20261022.
- Database: SQLite.
- Processing libraries: Pandas and NumPy.
- Output formats: CSV, JSON and SQL.
- IDs use consistent naming conventions and zero-padded counters.
- The same seed and generation settings support repeatable results.

All records are synthetic and intended for development, testing and analytics.
