import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

channel_mapping = {
    'TIKTOK': 1,
    'AKULAKU': 2,
    'INTERNAL': 3,
    'LAZADA': 4,
    'BLIBLI': 5,
    'BUKALAPAK': 6,
    'SHOPEE': 7,
    'TOKOPEDIA': 8
}

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
    
def retrieve_from_raw_sales_cube_data(dataset_path):
    df = pd.read_csv(dataset_path, parse_dates=['transaction_date'], low_memory=False)
    print(df.columns)
    df['diskon'] = np.where(df['diskon'] == 0, 0, (df['penjualan'] - df['diskon']) / df['penjualan'] * 100)
    df['channel_name_numeric'] = df['channel_name'].map(channel_mapping)

    print("CORR")
    print(df[['margin', 'penjualan']].corr())
    print(df[['qty', 'penjualan']].corr())
    print(df[['diskon', 'penjualan']].corr())
    print(df[['channel_name_numeric', 'penjualan']].corr())

    df = df[['transaction_date', 'penjualan', 
            'margin'
            ]].rename(columns={
        'transaction_date': 'ds',
        'penjualan': 'y'
    })

    return df