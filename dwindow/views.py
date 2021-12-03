from django.http import HttpResponse, JsonResponse

from db import getLastReadings, create_connection

def dataReadings(request):

    conn = create_connection(r"sensor_dataset.db")
    # FIXME: check for missing conn and handle error

    readings = getLastReadings(conn, 20)

    readingsJson = []
    for reading in readings:
        readingsJson.append({
            "temprature": reading[2],
            "eco2": reading[3],
            "tvoc": reading[4],
        })

    return JsonResponse({"data-readings": readingsJson})