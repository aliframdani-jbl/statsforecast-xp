import pandas as pd
import numpy as np

def basic_data_cleaning(df):
    # df.drop_duplicates(inplace=True)
    df['y'] = df['y'].astype(int)  

    full_range = pd.date_range(start=df['ds'].min(), end=df['ds'].max(), freq='MS')
    
    df.set_index('ds', inplace=True)
  
    df_monthly = df.resample('W').agg({'y': 'sum', 'margin': 'sum'})
    # df_monthly = df.resample('MS').agg({'y': 'sum'})

    # df_monthly = df_monthly.reindex(full_range, fill_value=0)
    # print("REINDEX: ")
    # print(df_monthly)

    df_monthly.reset_index(inplace=True)
    # df_monthly.rename(columns={'index': 'ds'}, inplace=True)
    
    df_monthly['unique_id'] = "sales_forecast"
    # print("---")
    # print(df_monthly.shape[0])
    # print("Debug shit mf:")
    # print(df.shape[0])
    # print(df.tail)
    # statsforecast_plot(df_monthly)
    # exit(0)

    df_monthly['margin'].fillna(0, inplace=True)


    # scaler = StandardScaler()
    # df_monthly['diskon_standardized'] = scaler.fit_transform(df_monthly[['diskon']])
    # df_monthly = df_monthly.drop(columns=['diskon'])


    # print('diskon')
    # print(df_monthly[['ds', 'diskon']])
    # plot_one_df_column(df_monthly, 'y')

    # df_monthly.round({"diskon": 2})   

    # ['Low', 'Medium', 'High', 'Very High', 'Extreme']
    # [1, 2, 3, 4, 5]
    # df_monthly['diskon_category'] = pd.cut(df_monthly['diskon'], bins=[-0.001, 5, 10, 15, 20, np.inf], labels=[1, 2, 3, 4, 5])

    # df_monthly = df_monthly.dropna()  # Drops rows with NaN values
    # df_monthly = df_monthly[~df_monthly.isin([float('inf'), float('-inf')]).any(axis=1)] 

    df_monthly['y'] = df_monthly['y'].diff()
    # df_monthly['y'] = np.log(df_monthly['y'])
    df_monthly = df_monthly.dropna()
    # print(df_monthly)

    # df_monthly.drop(columns=['diskon'], inplace=True)
    
    # all_dates = pd.date_range(start=df_monthly["ds"].min(), end=df_monthly["ds"].max(), freq="MS")
    # df_filled = pd.DataFrame({"ds": all_dates}).merge(df_monthly, on="ds", how="left").fillna({"y": 0, "unique_id": "sales_forecast", "diskon_category": 1})
    
    return df_monthly