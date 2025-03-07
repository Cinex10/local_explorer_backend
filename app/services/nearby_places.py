import json
import httpx
from core.config import settings
from models.schemas import Place

async def get_nearby_places(latitude: float,longitude: float):
    # async with httpx.AsyncClient() as client:
        # response = await client.post(
        #             "https://places.googleapis.com/v1/places:searchNearby",
        #             headers={
        #                 "Content-Type": "application/json",
        #                 "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
        #                 "X-Goog-FieldMask": "places.displayName,places.shortFormattedAddress,places.photos,places.types,places.nationalPhoneNumber,places.rating,places.websiteUri,places.currentOpeningHours,places.id,places.googleMapsLinks,places.editorialSummary,places.reviews",  # 5km radius
        #             },
        #             data=json.dumps({

        #                     "locationRestriction": {
        #                         "circle": {
        #                         "center": {
        #                             "latitude": latitude,
        #                             "longitude": longitude
        #                             },
        #                         "radius": 500.0
        #                         }
        #                     }
        #                     })
        #         )

        
    with open('data.json') as f:
        response = json.load(f)
    
    places_json = response.get("places", [])
    places = [Place.from_google_json(place) for place in places_json]
    return places
                
        # if response.status_code == 200:
        #     places_json = response.json().get("places", [])
        #     places = [Place.from_google_json(place) for place in places_json]
        #     return places
        # return []