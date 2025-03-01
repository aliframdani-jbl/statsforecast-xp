from helper.database import fetch_aggregated_sales
from helper.helper import output_csv

table_name = "sales_cube_1161"

# Get Monthly Aggregated Sales
# monthly_sales = fetch_aggregated_sales(table_name, interval='month')
# print(f"Fetched {len(monthly_sales)} monthly records.")

# Get Weekly Aggregated Sales
weekly_sales = fetch_aggregated_sales(table_name, interval='week')
print(f"Fetched {len(weekly_sales)} weekly records.")

weekly_sales['unique_id'] = "sales_forecast"

output_csv(weekly_sales, './weekly_1161_all.csv')