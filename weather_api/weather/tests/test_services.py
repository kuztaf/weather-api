# tests/test_services.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from weather.services import get_weather_data


@pytest.mark.asyncio
@patch("weather.services.redis_client")
async def test_get_weather_data_from_cache(mock_redis_client):
    # Simular que Redis devuelve datos
    mock_redis_client.get.return_value = "{'temp': 25, 'city': 'Madrid'}"

    result = await get_weather_data("Madrid")

    assert result["source"] == "cache"
    assert result["data"] == {'temp': 25, 'city': 'Madrid'}
    mock_redis_client.get.assert_called_once_with("weather:madrid")
    mock_redis_client.setex.assert_not_called()


@pytest.mark.asyncio
@patch("weather.services.redis_client")
@patch("weather.services.httpx.AsyncClient")
async def test_get_weather_data_from_api(mock_httpx_client, mock_redis_client):
    # Simular que Redis no tiene datos
    mock_redis_client.get.return_value = None

    # Simular respuesta de la API
    mock_response = MagicMock()
    mock_response.json.return_value = {"temp": 30, "city": "Madrid"}

    mock_httpx_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

    result = await get_weather_data("Madrid")

    assert result["source"] == "api"
    assert result["data"] == {"temp": 30, "city": "Madrid"}
    mock_redis_client.setex.assert_called_once_with(
        "weather:madrid", 3600, str({"temp": 30, "city": "Madrid"})
    )


@pytest.mark.asyncio
@patch("weather.services.redis_client")
@patch("weather.services.httpx.AsyncClient")
async def test_get_weather_data_api_failure(mock_httpx_client, mock_redis_client):
    # Simular que Redis no tiene datos
    mock_redis_client.get.return_value = None

    # Simular error HTTP
    mock_httpx_client.return_value.__aenter__.return_value.get = AsyncMock(
        side_effect=httpx.HTTPError("API down")
    )

    with pytest.raises(httpx.HTTPError):
        await get_weather_data("Madrid")