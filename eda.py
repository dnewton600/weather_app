#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.ensemble import RandomForestClassifier

import compute_functions

#%% 
data = pd.read_csv('data/noaa_historical_weather_10yr.csv')

#%%
print(f'Unique stations: {pd.unique(data.NAME)}')
print(f'Number of NA dates: {np.sum(pd.isna(data.DATE))}')
print(f'Number of NA days of rain: {np.sum(pd.isna(data.PRCP))}')
print(f'Number of NA days of snow: {np.sum(pd.isna(data.SNOW))}')

#%% # double check that there are 365 (or 366) days per year
def compute_days_per_year(data):

    data = data.copy(deep=True)
    data.loc[:,'year'] = data.DATE.apply(compute_functions.extract_year)
    outdf = data.groupby(['NAME','year']).apply(lambda x: pd.unique(x.DATE).shape[0]).reset_index()

    return outdf


#%% 
compute_days_per_year(data)

# %%
compute_functions.compute_avg_days_of_precip(data,'bos')
# %%
data.head()


#%%
month_aggs = data_sub.groupby(['month','day']).apply(lambda x: np.mean(x.precip_binary)).reset_index()
month_aggs = month_aggs.rename(columns={0:'avg_rain'})
month_aggs['day_num'] = (month_aggs['month'] - 1)*30 + month_aggs['day']
plt.scatter(month_aggs.day_num,month_aggs.avg_rain,alpha=.5)



#%%
def predict_chance_of_precip(data,city_code,month,day):

    data_sub = data.loc[data.NAME == compute_functions.city_map[city_code],['PRCP','SNOW','DATE']].reset_index(drop=True)

    data_sub['precip_binary'] =  data_sub['PRCP'] + data_sub['SNOW'] > 1e-8
    data_sub['precip_binary'] = data_sub['precip_binary'].astype(np.int64)

    data_sub['month'] = data.DATE.apply(lambda x: x.split('-')[1])
    data_sub['day'] = data.DATE.apply(lambda x: x.split('-')[2])

    data_sub['month'] = data_sub['month'].astype(np.float64)
    data_sub['day'] = data_sub['day'].astype(np.float64)

    data_sub['day_num'] = (data_sub['month'] - 1)*30 + data_sub['day']

    data_sub = data_sub.drop(columns=['PRCP','SNOW','DATE'])

    X = np.array(data_sub['day_num']).reshape((-1,1))
    y = np.array(data_sub['precip_binary'])

    clf = RandomForestClassifier(max_depth=4, random_state=0,n_estimators=500)
    clf.fit(X, y)

    X_pred = (float(month) - 1)*30 + float(day)
    X_pred = np.array(X_pred).reshape(1,1)

    y_pred = clf.predict_proba(X_pred)
    y_pred = np.round(y_pred[0,1],3)

    return y_pred
# %%
predict_chance_of_precip(data,'bos',4,12)
# %%
