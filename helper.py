import matplotlib.pyplot as plt

def plot_sales_forecast(df_monthly, forecast_df, model_name='AutoARIMA'):
    """ 
    Plots the original sales data and the forecasted sales.

    Parameters:
    df_monthly (DataFrame): Historical sales data with columns ['ds', 'y'].
    forecast_df (DataFrame): Forecasted sales data with columns ['ds', 'AutoARIMA'].

    """
    plt.figure(figsize=(10, 6))
    plt.plot(df_monthly['ds'], df_monthly['y'], label='Original Penjualan', color='blue')
    plt.plot(forecast_df['ds'], forecast_df[model_name], label='Forecasted Penjualan', color='red', linestyle='--')

    plt.title('Sales Forecast vs Actual Sales')
    plt.xlabel('Date')
    plt.ylabel('Penjualan')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage:
# plot_sales_forecast(df_monthly, forecast_df)

def plot_sales(df_monthly):
    """ 
    Plots the original sales data and the forecasted sales.

    Parameters:
    df_monthly (DataFrame): Historical sales data with columns ['ds', 'y'].
    forecast_df (DataFrame): Forecasted sales data with columns ['ds', 'AutoARIMA'].

    """
    plt.figure(figsize=(10, 6))
    plt.plot(df_monthly['ds'], df_monthly['y'], label='Original Penjualan', color='blue')

    plt.title('Actual Sales')
    plt.xlabel('Date')
    plt.ylabel('Penjualan')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_one_df_column(df, column_name):
    plt.figure(figsize=(10, 6))
    plt.plot(df['ds'], df[column_name], label=column_name)
    plt.title(column_name)
    plt.xlabel('Date')
    plt.ylabel(column_name)
    plt.legend()
    plt.grid(True)
    plt.show()  

def check_stationary_timeseries(df):
    from statsmodels.tsa.stattools import adfuller
    result = adfuller(df['y'])
    print(f'ADF Statistic: {result[0]}')
    print(f'p-value: {result[1]}')
