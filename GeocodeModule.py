import requests


def get_lat_lon(query):
    try:
        data = requests.get(f"https://nominatim.openstreetmap.org/search/{query}?format=json&addressdetails=1&limit=1&polygon_svg=1").json()
        for x in data:
            return {
                'lat': x.get('lat'),
                'lon': x.get('lon'),
                'display_name': x.get('display_name'),
                'postcode': x.get('address').get('postcode')
            }
    except:
            return {
                'code': 1337,
                'message': 'Something went wrong while fetching the data from nominatim.openstreetmap.org'
            }

