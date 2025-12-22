from django.urls import path

from .views import air_quality

urlpatterns = [
    path("", air_quality, name="air"),
]