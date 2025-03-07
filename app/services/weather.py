from fastapi import HTTPException
import httpx
from core.config import settings
from models.schemas import WeatherResponse

async def get_weather(lat: float, lon: float) -> WeatherResponse:
    """Get weather data from OpenWeather API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": lat,
                "lon": lon,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric"
            }
        )
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Weather service error")
            
        weather_data = response.json()
        return WeatherResponse(
            temperature=weather_data["main"]["temp"],
            condition=weather_data["weather"][0]["main"],
            description=weather_data["weather"][0]["description"],
            humidity=weather_data["main"]["humidity"],
            codes=[str(weather["id"])[0] for weather in weather_data["weather"]],
            wind_speed=weather_data["wind"]["speed"],
            clouds=weather_data["clouds"]["all"]
        )