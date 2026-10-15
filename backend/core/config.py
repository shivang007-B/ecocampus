from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import tempfile
from pathlib import Path


def default_database_url() -> str:
    """Use Vercel's writable temporary directory for the self-contained demo."""
    if os.getenv("VERCEL"):
        db_file = Path(tempfile.gettempdir()) / "ecocampus-demo.db"
        return f"sqlite:///{db_file.as_posix()}"
    return "sqlite:///./ecocampus.db"


class Settings(BaseSettings):
    # App
    APP_NAME: str = "EcoCampus Backend"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Database - SQLite for local development
    DATABASE_URL: str = default_database_url()
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

# Values in a checked-in local .env must never make a Vercel function attempt
# to write beside the deployed source bundle.
if os.getenv("VERCEL"):
    settings.DATABASE_URL = default_database_url()
