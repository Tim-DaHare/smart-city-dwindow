from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


from db import getLastReadings, create_connection, getUserConfig, setUserConfig, getAverageValues

def dataReadings(request):
    conn = create_connection(r"sensor_dataset.db")
    # FIXME: check for missing conn and handle error

    readings = getLastReadings(conn, 30)
    eco2Avg, tvocAvg, celsuisAverage = getAverageValues(conn)

    readingsJson = []
    for reading in readings:
        readingsJson.append({
            "temprature": reading[2],
            "eco2": reading[3],
            "tvoc": reading[4],
            "measured_at": reading[1]
        })

    conn.close()

    return JsonResponse({
        "data-readings": readingsJson,
        "averages": {
            "eco2": eco2Avg,
            "temprature": celsuisAverage,
            "tvoc": tvocAvg
        }
    })

def getConfig(request):
    conn = create_connection(r"sensor_dataset.db")
    # FIXME: check for missing conn and handle error

    config = getUserConfig(conn)

    conn.close()

    return JsonResponse({
        "temprature_threshold": config[0],
        "eco2_threshold": config[1],
    })

@csrf_exempt
def setConfig(request):
    if (request.method != "POST"):
        return JsonResponse({
            "message": "ERROR USE A POST CALL",
        })

    conn = create_connection(r"sensor_dataset.db")
    # FIXME: check for missing conn and handle error

    config_obj = json.loads(request.body)
    # print(config_obj)

    setUserConfig(conn, (config_obj['temprature_threshold'], config_obj['eco2_threshold']))

    conn.close()

    return JsonResponse({
        "message": "success",
    })