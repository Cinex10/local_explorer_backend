from fastapi import HTTPException
import httpx
from core.config import settings
from models.schemas import LocationResponse

async def get_location_name(lat: float, lon: float) -> LocationResponse:
    """Get location name from coordinates using reverse geocoding"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.opencagedata.com/geocode/v1/json",
            params={
                "key": settings.GEOCODING_API_KEY,
                "q": f"{lat},{lon}",
                "language": "en"
            }
        )
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Geocoding service error")
            
        data = response.json()
        if not data["results"]:
            raise HTTPException(status_code=404, detail="Location not found")
            
        components = data["results"][0]["components"]
        return LocationResponse(
            city=components.get("city", ""),
            country=components.get("country", ""),
            formatted=data["results"][0]["formatted"]
        )