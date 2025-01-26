from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_MAPS_API_KEY: str
    OPENWEATHER_API_KEY: str
    GEOCODING_API_KEY: str
    GROQ_API_KEY: str
    MODEL: str
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()