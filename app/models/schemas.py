from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from core.config import settings


class PlaceType(str, Enum):
    MUSEUM = "museum"
    ART_GALLERY = "art_gallery"
    MOVIE_THEATER = "movie_theater"
    SHOPPING_MALL = "shopping_mall"
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    LIBRARY = "library"
    GYM = "gym"
    SPA = "spa"
    PARK = "park"
    TOURIST_ATTRACTION = "tourist_attraction"
    AMUSEMENT_PARK = "amusement_park"
    BEACH = "beach"
    ZOO = "zoo"
    BOTANICAL_GARDEN = "botanical_garden"
    
    # Nouveaux types ajoutés
    AQUARIUM = "aquarium"
    THEATER = "theater"
    CONCERT_HALL = "concert_hall"
    NIGHT_CLUB = "night_club"
    BAR = "bar"
    CASINO = "casino"
    STADIUM = "stadium"
    CHURCH = "church"
    MOSQUE = "mosque"
    TEMPLE = "temple"
    HISTORICAL_LANDMARK = "historical_landmark"
    MARKET = "market"
    BOOKSTORE = "bookstore"
    GALLERY = "gallery"
    VIEWPOINT = "viewpoint"
    
    @classmethod
    def from_google_type(cls, types: List[str]) -> List['PlaceType']:
        type_mapping = {
            'museum': cls.MUSEUM,
            'art_gallery': cls.ART_GALLERY,
            'movie_theater': cls.MOVIE_THEATER,
            'shopping_mall': cls.SHOPPING_MALL,
            'mall': cls.SHOPPING_MALL,
            'restaurant': cls.RESTAURANT,
            'cafe': cls.CAFE,
            'library': cls.LIBRARY,
            'gym': cls.GYM,
            'health': cls.GYM,
            'spa': cls.SPA,
            'park': cls.PARK,
            'tourist_attraction': cls.TOURIST_ATTRACTION,
            'amusement_park': cls.AMUSEMENT_PARK,
            'beach': cls.BEACH,
            'zoo': cls.ZOO,
            'botanical_garden': cls.BOTANICAL_GARDEN,
            
            # Nouveaux mappings
            'aquarium': cls.AQUARIUM,
            'theater': cls.THEATER,
            'performing_arts_theater': cls.THEATER,
            'concert_hall': cls.CONCERT_HALL,
            'night_club': cls.NIGHT_CLUB,
            'bar': cls.BAR,
            'casino': cls.CASINO,
            'stadium': cls.STADIUM,
            'sports_complex': cls.STADIUM,
            'church': cls.CHURCH,
            'mosque': cls.MOSQUE,
            'temple': cls.TEMPLE,
            'place_of_worship': cls.CHURCH,  # Mapping générique
            'historic_site': cls.HISTORICAL_LANDMARK,
            'landmark': cls.HISTORICAL_LANDMARK,
            'market': cls.MARKET,
            'marketplace': cls.MARKET,
            'bookstore': cls.BOOKSTORE,
            'book_store': cls.BOOKSTORE,
            'art_gallery': cls.GALLERY,
            'gallery': cls.GALLERY,
            'viewpoint': cls.VIEWPOINT,
            'scenic_lookout': cls.VIEWPOINT
        }
        r = set()
        for t in types:
            normalized = t.lower().replace(' ', '_')
            if normalized in type_mapping:
                r.add(type_mapping[normalized])
        return list(r)


class LocationRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    device_id: str

class WeatherResponse(BaseModel):
    temperature: float
    condition: str
    description: str
    humidity: int
    wind_speed: float
    clouds: int
    codes: List[str]

class LocationResponse(BaseModel):
    city: str
    country: str
    formatted: str

class OpeningHours(BaseModel):
    open_time: Optional[datetime] = None
    close_time: Optional[datetime] = None

    @classmethod
    def from_periods(cls, periods: List[Dict]) -> 'OpeningHours':
        if not periods:
            return cls()
        period = periods[0]
        open_date = period.get('open', {}).get('date', {})
        close_date = period.get('close', {}).get('date', {})
        
        open_time = datetime(
            year=open_date.get('year', 1900),
            month=open_date.get('month', 1),
            day=open_date.get('day', 1),
            hour=period.get('open', {}).get('hour', 0),
            minute=period.get('open', {}).get('minute', 0)
        )
        
        close_time = datetime(
            year=close_date.get('year', 1900),
            month=close_date.get('month', 1),
            day=close_date.get('day', 1),
            hour=period.get('close', {}).get('hour', 0),
            minute=period.get('close', {}).get('minute', 0)
        )
        
        return cls(open_time=open_time, close_time=close_time)

class Place(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    rating: float
    types: List[PlaceType]
    opening_hours: Optional[OpeningHours] = None
    photos: Optional[List[str]] = None
    editorial_summary: Optional[str] = None
    website_uri: Optional[str] = None
    direction: Optional[str] = None
    national_phone_number: Optional[str] = None
    nb_reviews: Optional[int] = None

    @classmethod
    def from_google_json(cls, json_data: Dict) -> 'Place':
        """Create Place instance from Google Places API JSON response"""
        return cls(
            name=json_data["displayName"]["text"],
            address=json_data.get("shortFormattedAddress", ""),
            latitude=json_data.get("location", {}).get("latitude", 0.0),
            longitude=json_data.get("location", {}).get("longitude", 0.0),
            rating=json_data.get("rating", 0.0),
            types=PlaceType.from_google_type(json_data.get("types", [])),
            opening_hours=OpeningHours.from_periods(json_data.get("currentOpeningHours", {}).get("periods", [])),
            photos=["https://places.googleapis.com/v1/{name}/media?key={key}&maxHeightPx={max_width}".format(name=photo["name"],max_width=500, key=settings.GOOGLE_MAPS_API_KEY) for photo in json_data.get("photos", [])],
            editorial_summary=json_data.get("editorialSummary", {}).get("text", ""),
            nb_reviews=len(json_data.get("reviews", [])),
            website_uri=json_data.get("websiteUri"),
            national_phone_number=json_data.get("nationalPhoneNumber")
        )

    def __hash__(self):
        return hash((self.name, self.address))

class LocationInfoResponse(BaseModel):
    location: LocationResponse
    weather: WeatherResponse
    suggestions: List[Place]

    