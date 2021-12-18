# pip3 install requests
import requests
# pip3 install geocoder
import geocoder

import GeocodeModule as gcm

from datetime import datetime

# Get current location
LOCATION = geocoder.ip('me')
# API Key
APP_ID = '12aa733d76825d884a0caf790e3bb128'
# Get LAT and LON
LAT = str(gcm.get_lat_lon('1315RC').get('lat'))
LON = str(gcm.get_lat_lon('1315RC').get('lon'))
POSTAL = '1315RC'
# URL to the weather API
DATA_URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={LON}&lon={LAT}&units=metric&exclude=minutely,daily&appid={APP_ID}'
# Weather data parsed to json
GLOBAL_PARSED_DATA = requests.get(DATA_URL).json()


# Returns your current location with latitude and longitude
def get_location():
    try:
        lat = str(gcm.get_lat_lon(POSTAL).get('lat'))
        # Get longitude
        lon = str(gcm.get_lat_lon(POSTAL).get('lon'))
        return {
            'location': str(gcm.get_lat_lon('1315RC').get('address')),
            'lat': lat,
            'lon': lon
        }
    except:
        return {
            'message': 'Failed to return location',
            'code': 1337
        }


# Returns the current temperature and feels like temperature
def get_current_temp():
    try:
        data_current_temp = GLOBAL_PARSED_DATA.get('current').get('temp')
        data_feels_like = GLOBAL_PARSED_DATA.get('current').get('feels_like')
        return {
            "current_temp": data_current_temp,
            "feels_like_temp": data_feels_like
        }
    except:
        return {
            'message': 'Failed to return current temperature',
            'code': 1337
        }


# Returns array for the upcoming predictions
# Example code:
#             for data in yourModuleName.get_upcoming_temp():
#                 data  - Returns all the data
#                 data['lorem'] - Returns specific data
def get_upcoming_temp():
    try:
        upcoming_data = []
        for data in GLOBAL_PARSED_DATA.get('hourly'):
            # Get date and time in UNIX format
            unix_datetime = data.get('dt')
            # Convert Unix format to UTC
            utc_datetime = datetime.utcfromtimestamp(unix_datetime).strftime('%Y-%m-%d %H:%M:%S')
            upcoming_data.append({
                'dt': utc_datetime,
                'id': data.get('weather')[0].get('id'),
                'main': data.get('weather')[0].get('main'),
                'description': data.get('weather')[0].get('description'),
                'temp': data.get('temp'),
                'pop': data.get('pop') * 100,
                'rain_mm': data.get('rain').get('1h') if data.get('rain') else 0
            })
        return upcoming_data
    except:
        return {
            'message': 'Failed to return upcoming data',
            'code': 1337
        }


# print(gcm.get_lat_lon(POSTAL))
print(LOCATION.lat, LOCATION.lng)
print(gcm.get_lat_lon(POSTAL))
