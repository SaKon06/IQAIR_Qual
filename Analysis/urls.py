from django.urls import path

from .views import air_quality, air_plot, temp_plot

urlpatterns = [
    path("", air_quality, name="air"),
    path("plot/aqi.png", air_plot, name="air_plot"),
    path("plot/temp.png", temp_plot, name="temp_plot"),
]