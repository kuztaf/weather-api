import os
import redis
import httpx
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

# Initialize Redis client
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Load environment variables
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("WEATHER_API_URL")

"""
Asynchronously retrieves weather data for a given city or coordinates.

This function first checks if the weather data for the specified city is available in the Redis cache.
If cached data is found, it returns the cached data. Otherwise, it fetches the weather data from an
external API, stores the result in the cache for 1 hour, and then returns the data.

Args:
    city (str, optional): The name of the city for which to retrieve weather data.
    lat (str, optional): Latitude coordinate.
    long (str, optional): Longitude coordinate.

Returns:
    dict: A dictionary containing the data source ("cache" or "api") and the weather data.

Raises:
    httpx.HTTPError: If the external API request fails.
"""
async def get_weather_data(city: str = None, lat: str = None, long: str = None):

    if city:
        cache_key = f"weather:{city.lower()}"
        query_param = city
    elif lat and long:
        cache_key = f"weather:{lat},{long}"
        query_param = f"{lat},{long}"
    else:
        raise ValueError("Either city or coordinates (lat, long) must be provided")

    # 1. Check cache
    cached = redis_client.get(cache_key)

    if cached:
        return {"source": "cache", "data": eval(cached)}

    # 2. Call external API
    async with httpx.AsyncClient() as client:
        headers = {
            "key": WEATHER_API_KEY,
        }
        response = await client.get(
            BASE_URL,
            params={"q": query_param,
                    "lang": "es"},
            headers=headers
        )
        data = response.json()

    # 3. Save the API response in cache for 1 hour
    redis_client.setex(cache_key, 3600, str(data))

    return {"source": "api", "data": data}