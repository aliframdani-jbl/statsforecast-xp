import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from ml.trainer import train_with_statsforecast
from ml.cleaner import basic_data_cleaning
from helper.helper import check_stationary_timeseries, reverse_differencing, output_csv
from helper.dataset import retrieve_from_raw_sales_cube_data, split_train_test, remove_noise_data_sc_1161
from ml.predictor import predict
from ml.plotter import plot_sales_forecast, statsforecast_plot

# dataset_path = '../../merge_csv/9985/merged_sales_cube_9985.csv'
# dataset_path = '../../merge_csv/merged_sales_cube_1161.csv'

# dataset_path = "./weekly_1161_clean.csv"
dataset_path = "./weekly_1161_all.csv"
is_raw_dateset = False # if False it means dataset has been cleaned by basic_data_cleaning()

# df = df[df['ds'] <= '2025-01-01']  

if is_raw_dateset:
    df = retrieve_from_raw_sales_cube_data(dataset_path)
else:
    df = pd.read_csv(dataset_path, index_col=0)
    
df["ds"] = pd.to_datetime(df["ds"])
df['y'] = df['y'].astype(int)  

print("df: ")
print(df)

print("CORR")
print(df[['margin', 'y']].corr())

if is_raw_dateset:
    clean_df = basic_data_cleaning(df)
else:
    clean_df = df

if 'unique_id' not in clean_df.columns:
    clean_df['unique_id'] = "sales_forecast"
    
clean_df = remove_noise_data_sc_1161(clean_df)

# train_df = clean_df
train_df, test_df = split_train_test(clean_df, 0.2)

# statsforecast_plot(train_df)
# exit(0)

print("\nAfter Split: ")
print("train_df sales: ")
print(train_df.shape[0])
print(train_df)

print("test_df sales: ")
print(test_df.shape[0])
print(test_df)

# import statsmodels.api as sm

# X = train_df[['margin']]
# X = sm.add_constant(X)  # Menambahkan konstanta untuk intercept
# y = train_df['y']

# model = sm.OLS(y, X).fit()
# print("Linear regression: ")
# print(model.summary())

check_stationary_timeseries(train_df)

model = train_with_statsforecast(train_df)

forecast_df = predict(train_df, model)

# train_df, forecast_df = reverse_differencing(train_df, 'y'), reverse_differencing(forecast_df, 'SeasonalNaive')

# statsforecast_plot(train_df, forecast_df)
plot_sales_forecast(train_df, forecast_df, test_df, [
    'SeasonalNaive', 
    # 'AutoARIMA', 
    # 'AutoETS', 
    # 'HistoricAverage', 
    # 'DynamicOptimizedTheta',
    'HoltWinters'
])





