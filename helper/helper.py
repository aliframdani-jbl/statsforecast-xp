import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def check_stationary_timeseries(df):
    from statsmodels.tsa.stattools import adfuller
    result = adfuller(df['y'])
    print(f'ADF Statistic: {result[0]}')
    print(f'p-value: {result[1]}')

def reverse_differencing(df, column_name):
    print(df.columns)
    if column_name == '':
        column_name = df.columns[2]
    
    last_actual = df[column_name].iloc[-1] 
    df[column_name] = df[column_name].cumsum() + last_actual  # Reverse differencing
    
    return df

def output_csv(df, output_filename):
    df.to_csv(output_filename, index=True)
  