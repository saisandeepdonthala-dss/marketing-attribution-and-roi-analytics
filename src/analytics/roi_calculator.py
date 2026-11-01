from src.database.connection import get_connection

def calculate_campaign_roi():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            c.campaign_id,
            c.campaign_name,
            c.currency,
            COALESCE(SUM(cr.cost_amount), 0) AS total_spend
        FROM campaigns c
        LEFT JOIN cost_records cr
            ON c.campaign_id = cr.campaign_id
            AND c.currency = cr.currency
        GROUP BY
            c.campaign_id,
            c.campaign_name,
            c.currency
    """)

    campaigns = cursor.fetchall()

    print("\nCAMPAIGN ROI REPORT")
    print("=" * 75)

    for campaign_id, campaign_name, currency, total_spend in campaigns:
        cursor.execute("""
            SELECT
                COALESCE(SUM(attributed_revenue), 0)
            FROM attribution_results
            WHERE campaign_id = ?
              AND attribution_model = 'Multi-Touch'
        """, (campaign_id,))

        total_revenue = cursor.fetchone()[0]

        if total_spend > 0:
            roi = (
                (total_revenue - total_spend) / total_spend
            ) * 100

            roas = total_revenue / total_spend
        else:
            roi = None
            roas = None

        roi_text = f"{roi:.2f}%" if roi is not None else "N/A"
        roas_text = f"{roas:.2f}" if roas is not None else "N/A"

        print(f"\nCampaign: {campaign_id}")
        print(f"Name: {campaign_name}")
        print(f"Currency: {currency}")
        print(f"Total Spend: {total_spend:.2f}")
        print(f"Attributed Revenue: {total_revenue:.2f}")
        print(f"ROI: {roi_text}")
        print(f"ROAS: {roas_text}")

    connection.close()

if __name__ == "__main__":
    calculate_campaign_roi()
