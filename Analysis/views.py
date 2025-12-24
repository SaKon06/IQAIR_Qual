import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

df = pd.read_json("data.json")
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
df['timestamp'] = df['timestamp'].dt.tz_convert('UTC').dt.tz_localize(None)

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
new_df['timestamp'] = pd.to_datetime(new_df['timestamp'], errors='coerce', utc=True)
new_df['timestamp'] = new_df['timestamp'].dt.tz_convert('UTC').dt.tz_localize(None)
df_updated = pd.concat([df, new_df], ignore_index=True)
#print(df)
df_updated.to_json("data.json", date_format='iso', orient='records')


def air_quality(request):
    return render(request, "analysis/air.html", {"data": data})






def air_plot(request):
# убираем повторы и отсортировать
    df_local = df_updated.drop_duplicates(subset='timestamp', keep='last').sort_values('timestamp')
    df_local = df_local.set_index('timestamp')

    df_local['aqius'] = df_local['pollution'].apply(lambda p: p.get('aqius') if isinstance(p, dict) else None).astype(float)

# возьмём AQI (US) и timestamp из df
    #times = pd.to_datetime(df_local['timestamp'], unit='ms', errors='coerce')
    daily = df_local['aqius'].resample('D').mean().dropna()
    times = daily.index
    aqi = daily.values

    plt.figure(figsize=(8,3), dpi=120)
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