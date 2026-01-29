"""
Configuración de la aplicación
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configuración usando Pydantic"""
    
    PROJECT_NAME: str = "FleetSmart Notificaciones API"
    DESCRIPTION: str = "API de notificaciones push"
    VERSION: str = "1.0.0"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    FIREBASE_CREDENTIALS_PATH: str = "./config/serviceAccountKey.json"
    FIREBASE_DATABASE_URL: str = "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()