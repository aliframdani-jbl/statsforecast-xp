import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from ml.trainer import train_with_statsforecast
from ml.cleaner import basic_data_cleaning
from helper.helper import check_stationary_timeseries, retrieve_from_raw_sales_cube_data, reverse_differencing
from ml.predictor import predict
from ml.plotter import plot_sales_forecast

# dataset_path = '../../merge_csv/9985/merged_sales_cube_9985.csv'
# dataset_path = '../../merge_csv/merged_sales_cube_1161.csv'

dataset_path = "./weekly_1161_clean.csv"
is_raw_dateset = False # if False it means dataset has been cleaned by basic_data_cleaning()

# df = df[df['ds'] <= '2025-01-01']  

if is_raw_dateset:
    df = retrieve_from_raw_sales_cube_data(dataset_path)
else:
    df = pd.read_csv(dataset_path, index_col=0)
    
df["ds"] = pd.to_datetime(df["ds"])

print("df: ")
print(df)


print("negative val: ")
print(df[df['y'] < 0])

if is_raw_dateset:
    df_monthly = basic_data_cleaning(df)
else:
    df_monthly = df
    
print("monthly sales: ")
print(df_monthly)
print(df_monthly.shape[0])

import statsmodels.api as sm

X = df_monthly[['margin']]
X = sm.add_constant(X)  # Menambahkan konstanta untuk intercept
y = df_monthly['y']

model = sm.OLS(y, X).fit()
print("Linear regression: ")
print(model.summary())

check_stationary_timeseries(df_monthly)

model = train_with_statsforecast(df_monthly)

forecast_df = predict(df_monthly, model)

df_monthly, forecast_df = reverse_differencing(df_monthly, 'y'), reverse_differencing(forecast_df, 'SeasonalNaive')

plot_sales_forecast(df_monthly, forecast_df, [
    'SeasonalNaive', 
    'AutoARIMA', 
    # 'AutoETS', 
    # 'HistoricAverage', 
    # 'DynamicOptimizedTheta'
])





