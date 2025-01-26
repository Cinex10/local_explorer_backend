import functools
import json
import httpx
from app.core.config import settings
from app.models.schemas import Place

@functools.lru_cache(maxsize=128)
async def get_nearby_places(latitude: float,longitude: float):
    async with httpx.AsyncClient() as client:
        response = await client.post(
                    "https://places.googleapis.com/v1/places:searchNearby",
                    headers={
                        "Content-Type": "application/json",
                        "Content-Type": settings.GOOGLE_MAPS_API_KEY,
                        "X-Goog-FieldMask": "places.displayName,places.shortFormattedAddress,places.photos,places.types,places.nationalPhoneNumber,places.rating,places.websiteUri,places.currentOpeningHours,places.id,places.googleMapsLinks,places.editorialSummary,places.reviews",  # 5km radius
                    },
                    data={
                        "locationRestriction": {
                            "circle": {
                            "center": {
                                "latitude": latitude,
                                "longitude": longitude
                                },
                            "radius": 5000.0
                            }
                        }
                        }
                )
        
        # with open('data.json') as f:
        #     response = json.load(f)
        
        # places_json = response.get("places", [])
        # # pdb.set_trace()
        # places = [Place.from_google_json(place) for place in places_json]
        # return places
                
        if response.status_code == 200:
            places_json = response.json().get("results", [])
            places = [Place.from_google_json(place) for place in places_json]
            return places
        return []