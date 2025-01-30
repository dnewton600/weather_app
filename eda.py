#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#%% 
data = pd.read_csv('data/noaa_historical_weather_10yr.csv')

#%%
print(f'Unique stations: {pd.unique(data.NAME)}')
print(f'Number of NA dates: {np.sum(pd.isna(data.DATE))}')
print(f'Number of NA days of rain: {np.sum(pd.isna(data.PRCP))}')
print(f'Number of NA days of snow: {np.sum(pd.isna(data.SNOW))}')

# %%
def extract_year(date_str):
    # convert yyyy-mm-dd to yyyy
    return int(date_str.split('-')[0])

#%% # double check that there are 365 (or 366) days per year
def compute_days_per_year(data):

    data['year'] = data.DATE.apply(extract_year)
    outdf = data.groupby(['NAME','year']).apply(lambda x: pd.unique(x.DATE).shape[0]).reset_index()

    return outdf


# %%
def compute_avg_days_of_precip(data):

    # add in year variable and convert snow 'nan' values to 0
    data['year'] = data.DATE.apply(extract_year)
    data.loc[np.isnan(data.SNOW),'SNOW'] = 0

    # compute total number of days with nonzero precipitation for each year and station
    annual_precip_days = data.groupby(['NAME','year']).apply(lambda x: np.sum( (x.PRCP + x.SNOW) > 0),include_groups=False).reset_index()
    annual_precip_days = annual_precip_days.rename(columns={0:'total_rain'})

    # take the average across all years, for each station
    avg_precip_days = annual_precip_days.groupby('NAME').apply(lambda x: np.mean(x.total_rain),include_groups=False).reset_index()
    avg_precip_days = avg_precip_days.rename(columns={0:'average_days_rain'})

    return avg_precip_days

#%% 
compute_days_per_year(data)

# %%
compute_avg_days_of_precip(data)
# %%
