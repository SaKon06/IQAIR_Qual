import requests
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse


API = "543f4eee-9541-4cc5-a5b7-19500e4e851a"
url = f"http://api.airvisual.com/v2/city?city=Almaty&state=Almaty Oblysy&country=Kazakhstan&key={API}"
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
#print(response.text, '\n\n')

# извлекаем данные
data = response.json()
pollution_data = data.get('data', {}).get('current', {}).get('pollution', {})
weather = data.get('data', {}).get('current', {}).get('weather', {})

city_info = {
        #Загрязнение
        'AQI (US)': pollution_data.get('aqius', 'N/A'), # Индекс качества воздуха (US)
        'AQI (CN)': pollution_data.get('aqicn', 'N/A'), # Индекс качества воздуха (CN)
        'Timestamp': pollution_data.get('ts', 'N/A'),
        'Основной загрязнитель': pollution_data.get('maincn', 'N/A'),

        #Погода
        'Температура': weather.get('tp', 'N/A'),
        'Влажность': weather.get('hu', 'N/A'),
        'Давление': weather.get('pr', 'N/A'),
        'Скорость ветра': weather.get('ws', 'N/A'),
        'Направление ветра': weather.get('wd', 'N/A'),
}

df = pd.DataFrame([city_info])

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
#print(df)

def air_quality(request):
    data = {
        "city": "Almaty",
        "state": "Almaty Oblysy",
        "country": "Kazakhstan",
        "pollution": {
            "aqius": df.iloc[0, 0],
            "aqicn": df.iloc[0, 1],
            #"mainus": df[""],
            "maincn": df.iloc[0, 3],
        },
        "weather": {
            "temperature": df.iloc[0, 4],
            "humidity": df.iloc[0, 5],
            "pressure": df.iloc[0, 6],
            "wind_speed": df.iloc[0, 7],
            "wind_direction": df.iloc[0, 8],
            "icon": "50d",
        }
    }
    return render(request, "analysis/air.html", {"data": data})