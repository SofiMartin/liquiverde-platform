from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    OPENFOODFACTS_API_URL: str = "https://world.openfoodfacts.org/api/v2"
    USDA_API_KEY: Optional[str] = None
    USDA_API_URL: str = "https://api.nal.usda.gov/fdc/v1"
    CARBON_API_KEY: Optional[str] = None
    NOMINATIM_API_URL: str = "https://nominatim.openstreetmap.org"
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "liquiverde"
    
    # Redis (optional)
    REDIS_URL: Optional[str] = None
    
    # Application
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
