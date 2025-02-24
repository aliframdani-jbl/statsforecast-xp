import pandas as pd

def predict(df_monthly, model):
    # Prepare exogenous variables for prediction
    future_horizon = 24

    # Generate future dates
    future_dates = pd.date_range(start=df_monthly['ds'].max() + pd.Timedelta(days=1), periods=future_horizon, freq='MS')

    moving_avg_margin = df_monthly['margin'].rolling(window=3, min_periods=1).mean().iloc[-1]
    
    # Prepare future exogenous DataFrame with 'unique_id' (if only one time series, set to 1)
    future_X = pd.DataFrame({
        'ds': future_dates,  
        'margin': moving_avg_margin, 
        'unique_id': 'sales_forecast'
    })
    print("Future exogenous variables: ")
    print(future_X)

    forecast_df = model.predict(h=future_horizon, X_df=future_X, level=[90])
    
    print(forecast_df.head(20))

    # plot_sales_forecast(df_monthly, forecast_df)
    # sf.plot(df_monthly, forecast_df, level=[90]).show()
    
    return forecast_df
