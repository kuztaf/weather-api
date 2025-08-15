from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_weather_data
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
import asyncio


class WeatherView(APIView):
    """
    APIView for retrieving weather data based on city name or geographic coordinates.

    Methods:
        get(request: Request, city=None, lat=None, long=None):
            Handles GET requests to fetch weather data.
            - If 'city' is provided, retrieves weather data for the specified city.
            - If 'lat' and 'long' are provided, retrieves weather data for the specified coordinates.
            - If 'lat' and 'long' are present in query parameters, retrieves weather data for those coordinates.
            - Returns a 400 BAD REQUEST if neither city nor coordinates are provided.

    Args:
        request (Request): The HTTP request object.
        city (str, optional): Name of the city to fetch weather data for.
        lat (str or float, optional): Latitude for coordinate-based weather data.
        long (str or float, optional): Longitude for coordinate-based weather data.

    Returns:
        Response: Weather data in JSON format or an error message with appropriate HTTP status code.
    """
    def get(self, request: Request, city=None, lat=None, long=None):
        if city:
            data = asyncio.run(get_weather_data(city))
            return Response(data)
        elif lat and long:
            data = asyncio.run(get_weather_data(None, lat=lat, long=long))
            return Response(data)
        elif request.query_params.get('lat') and request.query_params.get('long'):
            lat = request.query_params.get('lat')
            long = request.query_params.get('long')
            data = asyncio.run(get_weather_data(None, lat=lat, long=long))
            return Response(data)
        return Response({'detail': 'City or coordinates required.'}, status=status.HTTP_400_BAD_REQUEST)