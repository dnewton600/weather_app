import compute_functions
import sys
import pandas as pd

data = pd.read_csv('data/noaa_historical_weather_10yr.csv')

if len(sys.argv) == 1 :
    print("No arguments submitted.")
    print("Please include either 'days-of-precip' or 'chance-of-precip' as an argument.")
    print("E.g., $python historical_weather days-of-precip")

elif len(sys.argv) == 2:

    if sys.argv[1] == 'days-of-precip':

        res = compute_functions.compute_avg_days_of_precip(data)
        print(res)

    elif sys.argv[1] == 'chance-of-precip':

        print("not implemented yet!")
    
    else:
        print("Invalid function name.")

elif len(sys.argv > 2):
    print('Too many command line arguments submitted.')