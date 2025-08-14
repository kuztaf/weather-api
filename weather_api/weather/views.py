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