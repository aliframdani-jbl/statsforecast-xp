import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def get_db_config():
    """Loads DB credentials from environment variables."""
    return {
        "host": os.getenv("DB_HOST"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT", 5432)
    }

def fetch_aggregated_sales(table_name, interval='month'):
    """
    Fetches aggregated sales data (weekly or monthly).
    
    Parameters:
        table_name (str): The database table name.
        interval (str): 'week' or 'month' for aggregation.
    
    Returns:
        list of tuples: Aggregated sales data.
    """
    db_config = get_db_config()

    if interval not in ['week', 'month']:
        raise ValueError("Interval must be 'week' or 'month'")

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = f"""
            SELECT 
                DATE_TRUNC(%s, transaction_date) AS period, 
                SUM(penjualan) AS total_sales,
                SUM(margin) AS total_margin
            FROM {table_name}
            GROUP BY period
            ORDER BY period ASC;
        """

        cursor.execute(query, (interval,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        
        df = pd.DataFrame(result, columns=["period", "total_sales", "total_margin"])
        return df

    except Exception as e:
        print(f"Database Error: {e}")
        return []

# Example Usage
# if __name__ == "__main__":
#     table_name = "sales_cube_1161"
    
#     # Get Monthly Aggregated Sales
#     monthly_sales = fetch_aggregated_sales(table_name, interval='month')
#     print(f"Fetched {len(monthly_sales)} monthly records.")

#     # Get Weekly Aggregated Sales
#     weekly_sales = fetch_aggregated_sales(table_name, interval='week')
#     print(f"Fetched {len(weekly_sales)} weekly records.")
