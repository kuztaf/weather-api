from django.urls import path
from .views import WeatherView

"""
URL configuration for the weather API.

Defines URL patterns for accessing weather information:
- 'coords/<str:lat>/<str:long>/': Retrieves weather data based on latitude and longitude coordinates.
- 'city/<str:city>/': Retrieves weather data for a specified city.

Both endpoints are handled by the WeatherView class-based view.
"""
urlpatterns = [
    path('coords/<str:lat>/<str:long>/', WeatherView.as_view(), name='weather-coords'),
    path('city/<str:city>/', WeatherView.as_view(), name='weather'),
]