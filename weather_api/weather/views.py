from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_weather_data
import asyncio

class WeatherView(APIView):
    async def get(self, request, city):
        data = await get_weather_data(city)
        return Response(data)