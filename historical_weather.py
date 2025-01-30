import compute_functions
import sys
import pandas as pd

data = pd.read_csv('data/noaa_historical_weather_10yr.csv')

if len(sys.argv) == 1:

    print("No arguments submitted.")
    print("Please include either 'days-of-precip' or 'chance-of-precip' as an argument.")
    print("E.g., $python historical_weather days-of-precip")
    sys.exit()

if sys.argv[1] == 'days-of-precip':

    if sys.argv[2] not in list(compute_functions.city_map.keys()):
        print("Invalid city code.")
        sys.exit()

    else:
        res = compute_functions.compute_avg_days_of_precip(data,sys.argv[2])
        print(res)
        sys.exit()

elif sys.argv[1] == 'chance-of-precip':

    if sys.argv[2] not in list(compute_functions.city_map.keys()):
        print("Invalid city code.")
        sys.exit()

    city_code = sys.argv[2]
    month = sys.argv[3]
    day = sys.argv[4]

    res = compute_functions.predict_chance_of_precip(data,city_code,month,day)
    print(res)
    sys.exit()
    
else:
    print("Invalid function name.")

