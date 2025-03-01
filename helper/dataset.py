import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

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

def split_train_test(df, test_size=0.2):
    train_size = 1 - test_size
    train_df = df[:int(train_size * len(df))]
    test_df = df[int(train_size * len(df)):]
    return train_df, test_df

def split_train_test_sklearn(df, test_size=0.2, target_column='y'):
    y = df[target_column] 
    X = df.drop(columns=[target_column])   
                    
    
    print("X: ")
    print(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    print("train_df: ")
    print(train_df)
    print("test_df: ")
    print(test_df)
    
    return train_df, test_df

def remove_noise_data_sc_1161(df):
    df = df[(df['ds'] >= '2021-04-26') & (df['ds'] <= '2024-04-01')]
    return df
