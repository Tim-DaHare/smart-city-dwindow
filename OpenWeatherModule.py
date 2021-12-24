# pip3 install requests
import requests
from requests.api import get
# pip3 install geocoder
# import geocoder

import GeocodeModule as gcm

from datetime import datetime
import time

# Get current location
# LOCATION = geocoder.ip('me')
# API Key
# APP_ID = '12aa733d76825d884a0caf790e3bb128' OLD KEY
APP_ID = 'd7e4c920bf451acf69831342e79fe06f'
LOC_QUERY = 'Hospitaaldreef'
# Get LAT and LON
LAT = str(gcm.get_lat_lon(LOC_QUERY).get('lat'))
LON = str(gcm.get_lat_lon(LOC_QUERY).get('lon'))
# URL to the weather API
DATA_URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&units=metric&exclude=daily,minutely&appid={APP_ID}'
# Weather data parsed to json
GLOBAL_PARSED_DATA = requests.get(DATA_URL).json()

def get_weather_prediction():
    response = requests.get(DATA_URL).json()

    # now = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    # temp = datetime.utcfromtimestamp(response.get('hourly')[1].get('dt')).strftime('%Y-%m-%d %H:%M:%S')

    # get precipitation chance in the next hour
    return int(response.get('hourly')[1].get('pop') * 100)



# Returns your current location with latitude and longitude
# def get_location():
#     try:
#         lat = str(gcm.get_lat_lon(LOC_QUERY).get('lat'))
#         # Get longitude
#         lon = str(gcm.get_lat_lon(LOC_QUERY).get('lon'))
#         return {
#             'location': str(gcm.get_lat_lon(LOC_QUERY).get('address')),
#             'lat': lat,
#             'lon': lon
#         }
#     except:
#         return {
#             'message': 'Failed to return location',
#             'code': 1337
#         }


# # Returns the current temperature and feels like temperature
# def get_current_temp():
#     try:
#         data_current_temp = GLOBAL_PARSED_DATA.get('current').get('temp')
#         data_feels_like = GLOBAL_PARSED_DATA.get('current').get('feels_like')
#         return {
#             "current_temp": data_current_temp,
#             "feels_like_temp": data_feels_like
#         }
#     except:
#         return {
#             'message': 'Failed to return current temperature',
#             'code': 1337
#         }


# # Returns array for the upcoming predictions
# # Example code:
# #             for data in yourModuleName.get_upcoming_temp():
# #                 data  - Returns all the data
# #                 data['lorem'] - Returns specific data
# def get_upcoming_temp():
#     try:
#         upcoming_data = []
#         for data in GLOBAL_PARSED_DATA.get('hourly'):
#             # Get date and time in UNIX format
#             unix_datetime = data.get('dt')
#             # Convert Unix format to UTC
#             utc_datetime = datetime.utcfromtimestamp(unix_datetime).strftime('%Y-%m-%d %H:%M:%S')
#             upcoming_data.append({
#                 'dt': utc_datetime,
#                 'id': data.get('weather')[0].get('id'),
#                 'main': data.get('weather')[0].get('main'),
#                 'description': data.get('weather')[0].get('description'),
#                 'temp': data.get('temp'),
#                 'pop': data.get('pop') * 100,
#                 'rain_mm': data.get('rain').get('1h') if data.get('rain') else 0
#             })
#         return upcoming_data
#     except:
#         return {
#             'message': 'Failed to return upcoming data',
#             'code': 1337
#         }

# def open_close_window_prediction():
#     ts = time.time()
#     utc_ts = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

#     for x in range(len(get_upcoming_temp())):
#         if get_upcoming_temp()[x]['dt'] < utc_ts or x > 2 or x == 1: 
#             continue
#         # If probability of precipitation >= x set windowOpen to FALSE
#         if get_upcoming_temp()[x]['pop'] >= 0:
#             # return windowOpen = false
#             pass
#         # If probability of precipitation <= x and sensor_data > x set windowOpen to TRUE
#         if get_upcoming_temp()[x]['pop'] <= 0 and sensor_data > 0:
#             # return windowOpen = true
#             pass

