from django.urls import path
from .views import WeatherView

urlpatterns = [
    path('coords/<str:lat>/<str:long>/', WeatherView.as_view(), name='weather-coords'),
    path('city/<str:city>/', WeatherView.as_view(), name='weather'),
]