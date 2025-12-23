import requests
import pandas as pd
import matplotlib as plt
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse

df = pd.read_json("data.json")


API = "543f4eee-9541-4cc5-a5b7-19500e4e851a"
url = f"http://api.airvisual.com/v2/city?city=Almaty&state=Almaty Oblysy&country=Kazakhstan&key={API}"
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
#print(response.text, '\n\n')

# извлекаем данные
data = response.json()
pollution = data.get('data', {}).get('current', {}).get('pollution', {})
weather = data.get('data', {}).get('current', {}).get('weather', {})

data = {
        "city": "Almaty",
        "state": "Almaty Oblysy",
        "country": "Kazakhstan",
        "timestamp": pollution.get('ts', 'N/A'),
        "pollution": {
            "aqius": pollution.get('aqius', 'N/A'),
            "aqicn": pollution.get('aqicn', 'N/A'),
            "mainus": pollution.get('mainus', 'N/A'),
            "maincn": pollution.get('maincn', 'N/A'),
        },
        "weather": {
            "temperature": weather.get('tp', 'N/A'),
            "humidity": weather.get('hu', 'N/A'),
            "pressure": weather.get('pr', 'N/A'),
            "wind_speed": weather.get('ws', 'N/A'),
            "wind_direction": weather.get('wd', 'N/A'),
            "icon": "50d",
        }
    }

new_df = pd.DataFrame([data])
new_df['timestamp'] = pd.to_datetime(df['timestamp'])
df_updated = pd.concat([df, new_df], ignore_index=True)
#print(df)
df_updated.to_json("data.json")


def air_quality(request):
    return render(request, "analysis/air.html", {"data": data})



