import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

pd.options.mode.chained_assignment = None 

city_map = {
    'bos':'BOSTON, MA US',
    'jnu':'JUNEAU AIRPORT, AK US',
    'mia':'MIAMI INTERNATIONAL AIRPORT, FL US'
}

def extract_year(date_str):
    # convert yyyy-mm-dd to yyyy
    return int(date_str.split('-')[0])

def compute_avg_days_of_precip(data,city_code):

    # prevent side effects in case 'data' needs to be used elsewhere
    data = data.copy(deep=True)

    # subset dataset based on city
    data = data.loc[data.NAME == city_map[city_code],:]

    # add in year variable and convert snow 'nan' values to 0
    data.loc[:,'year'] = data.loc[:,'DATE'].apply(extract_year)
    data.loc[np.isnan(data.SNOW),'SNOW'] = 0

    # compute total number of days with nonzero precipitation for each year and station
    annual_precip_days = data.groupby(['year']).apply(lambda x: np.sum( (x.PRCP + x.SNOW) > 0),include_groups=False).reset_index()
    annual_precip_days = annual_precip_days.rename(columns={0:'total_rain'})

    # take the average across all years, for each station
    avg_precip_days = np.mean(annual_precip_days.total_rain)
 
    return avg_precip_days


def predict_chance_of_precip(data,city_code,month,day):

    data_sub = data.loc[data.NAME == city_map[city_code],['PRCP','SNOW','DATE']].reset_index(drop=True)
    data_sub.loc[np.isnan(data_sub.SNOW),'SNOW'] = 0

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