
from src.database.connection import reset_database

from src.database.schema import create_tables
from src.database.transaction_schema import create_transaction_tables
from src.database.finance_schema import create_finance_tables

from src.generators.master_data import create_master_data
from src.generators.campaign_generator import generate_campaigns
from src.generators.contact_generator import generate_contacts
from src.generators.touchpoint_generator import generate_touchpoints
from src.generators.session_generator import generate_sessions
from src.generators.lead_generator import generate_leads
from src.generators.opportunity_generator import generate_opportunities
from src.generators.order_generator import generate_orders
from src.generators.cost_generator import generate_costs

from src.validation.data_validator import validate_database
from src.attribution.attribution_engine import calculate_attribution
from src.analytics.roi_calculator import calculate_campaign_roi

from src.database.check_database import check_record_counts
from src.database.export_data import export_tables_to_csv
from src.database.export_json import export_tables_to_json
from src.database.export_sql import export_database_to_sql


def main():
    print("\nMARKETING ATTRIBUTION AND ROI ANALYTICS")
    print("=" * 55)

    # Step 0: Reset the working database
    print("\n0. Resetting working database...")
    reset_database()

    # Step 1: Create database tables
    print("\n1. Creating database tables...")
    create_tables()
    create_transaction_tables()
    create_finance_tables()

    # Step 2: Insert master data
    print("\n2. Creating master data...")
    create_master_data()

    # Step 3: Generate marketing data
    print("\n3. Generating marketing data...")
    generate_campaigns()
    generate_contacts()
    generate_touchpoints()
    generate_sessions()
    generate_leads()
    generate_opportunities()
    generate_orders()
    generate_costs()

    # Step 4: Validate database
    print("\n4. Validating database...")
    validate_database()

    # Step 5: Calculate attribution
    print("\n5. Calculating attribution...")
    calculate_attribution()

    # Step 6: Calculate campaign ROI
    print("\n6. Calculating campaign ROI...")
    calculate_campaign_roi()

    # Step 7: Display record counts
    print("\n7. Checking database records...")
    check_record_counts()

    # Step 8: Export data
    print("\n8. Exporting CSV files...")
    export_tables_to_csv()

    print("\n9. Exporting JSON files...")
    export_tables_to_json()

    print("\n10. Exporting SQL file...")
    export_database_to_sql()

    print("\n" + "=" * 55)
    print("MARKETING ANALYTICS PIPELINE COMPLETED")
    print("=" * 55)


if __name__ == "__main__":
    main()
