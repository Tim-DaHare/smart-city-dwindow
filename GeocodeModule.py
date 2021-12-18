import requests

API_KEY = '92141569241409777688x89917'


def get_lat_lon(postcode):
    try:
        data = requests.get(f"https://geocode.xyz/{postcode}?json=1&auth={API_KEY}").json()
        return {
            'address': data.get('standard').get('addresst'),
            'region': data.get('standard').get('region'),
            'postal': data.get('standard').get('postal'),
            'lat': data.get('longt'),
            'lon': data.get('latt')
        }
    except:
        return {
            'code': 1337,
            'message': 'Something went wrong while fetching the data from geocode.xyz'
        }
