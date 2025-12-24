import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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


def air_plot(request):
# убираем повторы и отсортировать
    df_local = df_updated
    df_local = df_local.drop_duplicates(subset='timestamp', keep='last')
    df_local = df_local.sort_values('timestamp')


# возьмём AQI (US) и timestamp из df
    times = pd.to_datetime(df_local['timestamp'], unit='ms', errors='coerce')
    aqi = df_local['pollution'].apply(lambda p: p.get('aqius') if isinstance(p, dict) else None)


    plt.figure(figsize=(10,3), dpi=120)
    plt.plot(times, aqi, marker='o', linestyle='-', color='#2c7fb8', linewidth=2)
    plt.fill_between(times, aqi, alpha=0.1, color='#2c7fb8')
    plt.title('AQI (US) — история')
    plt.ylabel('AQI (US)', fontsize=10)
    plt.grid(alpha=0.25)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return HttpResponse(buf.getvalue(), content_type='image/png')