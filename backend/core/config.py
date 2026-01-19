from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "EcoCampus Backend"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Database - SQLite for local development
    DATABASE_URL: str = "sqlite:///./ecocampus.db"
    DATABASE_URL_TEST: str = "sqlite:///./ecocampus_test.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys
    OPENWEATHER_API_KEY: Optional[str] = None
    CLIMATIQ_API_KEY: Optional[str] = None
    ELECTRICITYMAP_API_KEY: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MQTT
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str = "campus/iot/#"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()