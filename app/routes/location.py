from fastapi import APIRouter
import asyncio

from app.models.schemas import LocationRequest, LocationInfoResponse
from app.services.nearby_places import get_nearby_places
from app.services.place_recommender import filter_and_sort_places, get_recommended_place_types
from app.services.weather import get_weather
from app.services.geocoding import get_location_name

router = APIRouter()

@router.post("/recommend", response_model=LocationInfoResponse)
async def get_location_info(
    request_data: LocationRequest,
) -> LocationInfoResponse:
    """Get weather and location information based on coordinates"""
    
    location_data, weather_data = await asyncio.gather(
        get_location_name(request_data.latitude, request_data.longitude),
        get_weather(request_data.latitude, request_data.longitude)
    )
    
    # Get place types and nearby places in parallel
    place_types, nearby_places = await asyncio.gather(
        get_recommended_place_types(weather_data, location_data),
        get_nearby_places(request_data.latitude, request_data.longitude)
    )
    
    # Filter and sort places
    filtered_places = await filter_and_sort_places(nearby_places, place_types)
    
    return LocationInfoResponse(
        location=location_data,
        weather=weather_data,
        suggestions=filtered_places
    )