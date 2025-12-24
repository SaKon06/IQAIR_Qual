from django.urls import path

from .views import air_quality, air_plot

urlpatterns = [
    path("", air_quality, name="air"),
    path("plot/aqi.png", air_plot, name="air_plot"),
]