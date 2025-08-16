# tests/test_weather_view.py
import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
class TestWeatherView:

    @patch("weather.views.get_weather_data")
    def test_get_weather_by_city(self, mock_get_weather_data):
        mock_get_weather_data.return_value = {"temp": 25, "city": "Madrid"}
        client = APIClient()

        response = client.get("/weather/city/Madrid/")  # ruta según tus urls.py

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"temp": 25, "city": "Madrid"}
        mock_get_weather_data.assert_called_once_with("Madrid")

    @patch("weather.views.get_weather_data")
    def test_get_weather_by_coordinates(self, mock_get_weather_data):
        mock_get_weather_data.return_value = {"temp": 18, "lat": "40.4", "long": "-3.7"}
        client = APIClient()

        response = client.get("/weather/coords/40.4/-3.7/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"temp": 18, "lat": "40.4", "long": "-3.7"}
        mock_get_weather_data.assert_called_once_with(None, lat="40.4", long="-3.7")

    @patch("weather.views.get_weather_data")
    def test_get_weather_missing_params(self, mock_get_weather_data):
        client = APIClient()
        response = client.get("/weather/")

        assert response.status_code == status.HTTP_404_NOT_FOUND  # Porque no existe una ruta /weather/
        mock_get_weather_data.assert_not_called()