# Marketing Attribution System - Data Dictionary

# 1. Campaign
campaign_id: Unique ID for each campaign.
campaign_name: Name of the campaign.
channel_id: Channel used for the campaign.
budget: Planned campaign budget.
currency: Budget currency (USD, INR, EUR).
start_date: Campaign start date.
end_date: Campaign end date.
status: Active, Completed or Paused.

# 2. Channel
channel_id: Unique channel ID.
channel_name: Email, Social Media, Search, Display or Offline.

# 3. Creative
creative_id: Unique creative ID.
creative_name: Name of the advertisement.
campaign_id: Related campaign ID.
creative_type: Image, Video, Text or Banner.

# 4. Audience
audience_id: Unique audience ID.
audience_name: Audience group name.
description: Audience details.

# 5. Contact
contact_id: Unique contact ID.
contact_name: Synthetic contact name.
email: Synthetic email address.
created_at: Contact creation date.

# 6. Touchpoint
touchpoint_id: Unique touchpoint ID.
contact_id: Related contact ID.
campaign_id: Related campaign ID.
channel_id: Related channel ID.
creative_id: Related creative ID.
touchpoint_time: Date and time of interaction.
touch_type: Click, Impression, Email or Offline.

# 7. WebSession
session_id: Unique session ID.
contact_id: Optional contact ID.
session_time: Session date and time.
source: Traffic source.
anonymous: Whether the visitor is anonymous.

# 8. Lead
lead_id: Unique lead ID.
contact_id: Related contact ID.
session_id: Related session ID.
created_at: Lead creation date.
status: New, Qualified or Converted.

# 9. Opportunity
opportunity_id: Unique opportunity ID.
lead_id: Related lead ID.
contact_id: Related contact ID.
created_at: Opportunity creation date.
closed_at: Opportunity closing date.
status: Open, Won or Lost.

# 10. Order
order_id: Unique order ID.
opportunity_id: Related opportunity ID.
revenue: Order revenue amount.
currency: Revenue currency.
order_date: Order date.

# 11. CostRecord
cost_id: Unique cost record ID.
campaign_id: Related campaign ID.
cost_amount: Campaign spending amount.
currency: Spending currency.
cost_date: Date of spending.

# 12. AttributionResult
attribution_id: Unique attribution ID.
opportunity_id: Related opportunity ID.
campaign_id: Related campaign ID.
attribution_model: First-touch, Last-touch or Multi-touch.
attributed_revenue: Revenue assigned to the campaign.
attribution_date: Date of calculation.