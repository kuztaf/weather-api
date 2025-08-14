import os
import redis
import httpx
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

# Configuración de Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("WEATHER_API_URL")

async def get_weather_data(city: str):
    cache_key = f"weather:{city.lower()}"

    # 1. Revisar cache
    cached = redis_client.get(cache_key)
    if cached:
        return {"source": "cache", "data": eval(cached)}

    # 2. Llamar API externa
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params={
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        })
        data = response.json()

    # 3. Guardar en cache por 1 hora
    redis_client.setex(cache_key, 3600, str(data))

    return {"source": "api", "data": data}