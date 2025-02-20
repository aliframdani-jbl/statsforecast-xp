import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS
import matplotlib.pyplot as plt 
from helper import plot_sales_forecast, check_stationary_timeseries, plot_sales

# df = pd.read_csv('https://datasets-nixtla.s3.amazonaws.com/air-passengers.csv', parse_dates=['ds'])
# plot_sales(df)
# exit(0)

df = pd.read_csv('../../merge_csv/merged_sales_cube_9985.csv', parse_dates=['transaction_date'], low_memory=False)
print(df.columns)
df['diskon'] = np.where(df['diskon'] == 0, 0, (df['penjualan'] - df['diskon']) / df['penjualan'] * 100)

df["transaction_date"] = pd.to_datetime(df["transaction_date"])

df = df[['transaction_date', 'penjualan', 
         'diskon'
        ]].rename(columns={
    'transaction_date': 'ds',
    'penjualan': 'y'
})

df = df[df['ds'] <= '2025-01-01']  

print("CORR")
print(df[['diskon', 'y']].corr())

print("df: ")
print(df)

df.drop_duplicates(inplace=True)
# df['y'].fillna(0, inplace=True)
df['y'] = df['y'].astype(int)  

df.set_index('ds', inplace=True)
df_monthly = df.resample('MS').agg({'y': 'sum', 'diskon': 'mean'})
# df_monthly = df.resample('MS').agg({'y': 'sum'})
df_monthly.reset_index(inplace=True)

scaler = StandardScaler()
# df_monthly['diskon_standardized'] = scaler.fit_transform(df_monthly[['diskon']])
# df_monthly = df_monthly.drop(columns=['diskon'])


# print('diskon')
# print(df_monthly[['ds', 'diskon']])
# plot_one_df_column(df_monthly, 'y')

df_monthly['unique_id'] = "sales_forecast"
# df_monthly.round({"diskon": 2})   

df['diskon_category'] = pd.cut(df['diskon'], bins=[0, 5, 10, 15, 20, np.inf], labels=['Low', 'Medium', 'High', 'Very High', 'Extreme'])

# df_monthly = df_monthly.dropna()  # Drops rows with NaN values
# df_monthly = df_monthly[~df_monthly.isin([float('inf'), float('-inf')]).any(axis=1)] 

# df_monthly['y'] = df_monthly['y'].diff().diff()
# print(df_monthly)

df_monthly = df_monthly.dropna()

print("monthly sales: ")
print(df_monthly)

df_monthly.to_csv('sc_9958_clean.csv', index=True)
exit(0)

check_stationary_timeseries(df_monthly)

# Prepare exogenous variables for prediction
future_horizon = 30

# Generate future dates
future_dates = pd.date_range(start=df_monthly['ds'].max() + pd.Timedelta(days=1), periods=future_horizon, freq='MS')

# Prepare future exogenous DataFrame with 'unique_id' (if only one time series, set to 1)
# future_X = pd.DataFrame({
#     'ds': future_dates,  
#     'diskon_standardized': df_monthly['diskon_standardized'].mean(), 
#     'unique_id': 'sales_forecast'
# })
# print("Future exogenous variables: ")
# print(future_X)

print("Training...")
modelArima = AutoARIMA(
        season_length = 12, 
        seasonal=True,
        stepwise=True,
        trace=True,
        approximation=False
    )

modelETS = AutoETS(
    season_length=12
)

sf = StatsForecast(
    models=[modelArima],
    freq='MS',
)
sf.fit(df_monthly)

forecast_df = sf.predict(h=future_horizon, level=[90])
print(forecast_df.head(20))

# plot_sales_forecast(df_monthly, forecast_df)
sf.plot(df_monthly, forecast_df, level=[90]).show()







