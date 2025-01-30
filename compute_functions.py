import numpy as np
import pandas as pd

def extract_year(date_str):
    # convert yyyy-mm-dd to yyyy
    return int(date_str.split('-')[0])

def compute_avg_days_of_precip(data):

    # add in year variable and convert snow 'nan' values to 0
    data['year'] = data.DATE.apply(extract_year)
    data.loc[np.isnan(data.SNOW),'SNOW'] = 0

    # compute total number of days with nonzero precipitation for each year and station
    annual_precip_days = data.groupby(['NAME','year']).apply(lambda x: np.sum( (x.PRCP + x.SNOW) > 0),include_groups=False).reset_index()
    annual_precip_days = annual_precip_days.rename(columns={0:'total_rain'})

    # take the average across all years, for each station
    avg_precip_days = annual_precip_days.groupby('NAME').apply(lambda x: np.mean(x.total_rain),include_groups=False).reset_index()
    avg_precip_days = avg_precip_days.rename(columns={0:'average_annual_days_precip'})

    return avg_precip_days