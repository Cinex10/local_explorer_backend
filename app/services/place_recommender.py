import json
from typing import List, Dict
import httpx
from app.core.config import settings
from app.models.schemas import WeatherResponse, LocationResponse, PlaceType, Place
from groq import AsyncGroq


async def get_groq_suggestion(prompt: str) -> List[str]:
    client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    
    try:
        response = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=settings.MODEL,
            max_tokens=100,
            temperature=0.7
        )
        if not response.choices:
            return []
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return []

async def get_recommended_place_types(weather: WeatherResponse, location: LocationResponse) -> List[PlaceType]:
    prompt = f"""Based on:
Location: {location.city}
Temperature: {weather.temperature}°C
Condition: {weather.condition}
Description: {weather.description}

Suggest exactly 5 most appropriate place types from this list for the current weather:
museum, art_gallery, movie_theater, shopping_mall, restaurant, cafe, library, gym, spa, park, tourist_attraction, amusement_park, beach, zoo, botanical_garden

Return only a JSON array of 10 place types without any extra text. Example:
["museum", "art_gallery", "cafe", "library", "restaurant", "gym", "park", "tourist_attraction", "amusement_park", "shopping_mall"]"""

    response = await get_groq_suggestion(prompt)
    print(response)
    try:
        place_types = json.loads(response)
        return [PlaceType(pt) for pt in place_types]
    except json.JSONDecodeError:
        print(f"Error decoding Groq response: {response}")
        return []
    
        

async def filter_and_sort_places(places: List[Place], place_types: List[PlaceType]) -> List[Place]:
    max_results = 15
    filtered_places = set()
    
    for place in places:
        if any(pt.value in place.types for pt in place_types):
            filtered_places.add(place)
        if len(filtered_places) >= max_results:
            break
        
    sorted_places = sorted(filtered_places, key=lambda x: x.rating, reverse=True)
    return sorted_places