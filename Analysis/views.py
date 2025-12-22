from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def air_quality(request):
    data = {
        "city": "Almaty",
        "state": "Almaty Oblysy",
        "country": "Kazakhstan",
        "pollution": {
            "aqius": 62,
            "aqicn": 45,
            "mainus": "p2",
            "maincn": "s2",
        },
        "weather": {
            "temperature": 0,
            "humidity": 86,
            "pressure": 1026,
            "wind_speed": 3,
            "wind_direction": 340,
            "icon": "50d",
        }
    }
    return render(request, "analysis/air.html", {"data": data})