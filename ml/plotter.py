from statsforecast import StatsForecast
import matplotlib.pyplot as plt

def plot_sales_forecast(train_df, forecast_df, test_df, model_names=None):
    """ 
    Plots the original sales data and multiple forecasted sales.

    Parameters:
    df_monthly (DataFrame): Historical sales data with columns ['ds', 'y'].
    forecast_df (DataFrame): Forecasted sales data with 'ds' and one or more model columns.
    model_names (list): List of model names to plot. If None, it defaults to the third column in forecast_df.
    """

    if model_names is None:
        model_names = [forecast_df.columns[2]]  # Default to the third column

    plt.figure(figsize=(10, 6))

    # Plot original sales data
    plt.plot(train_df['ds'], train_df['y'], label='Original Sales', color='blue')
    
    if test_df is not None:
        plt.plot(test_df['ds'], test_df['y'], label='Actual Sales', color='red')

    # Plot forecasted values for each model
    for model in model_names:
        plt.plot(forecast_df['ds'], forecast_df[model], label=f'Forecast - {model}', linestyle='--')

    # Formatting
    plt.title('Sales Forecast vs Actual Sales')
    plt.xlabel('Date')
    plt.ylabel('Penjualan')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example Usage:
# plot_forecast(df_monthly, forecast_df, model_names=['AutoARIMA', 'Prophet', 'SARIMA'])

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

def statsforecast_plot(df, forecast_df=None):
    if forecast_df is None:
        fig = StatsForecast.plot(df)
    else:
        fig = StatsForecast.plot(df, forecast_df, level=[90])

    # snippet that will reopen closed figure
    new_fig = plt.figure(figsize=(16,4))
    new_manager = new_fig.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)
    plt.legend()
    # wait for user interactions
    plt.show()  
    
def plot_forecast(forecast_df):
    forecast_df.plot()
