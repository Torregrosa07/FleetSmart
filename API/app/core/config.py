"""
Configuración de la aplicación
"""
from pydantic_settings import BaseSettings
from typing import List
import os

# Ruta absoluta al directorio de la API (donde está este archivo config.py)
_API_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Settings(BaseSettings):
    """Configuración usando Pydantic"""
    
    PROJECT_NAME: str = "FleetSmart Notificaciones API"
    DESCRIPTION: str = "API de notificaciones push"
    VERSION: str = "1.0.0"
    
    API_HOST: str = "0.0.0.0"
    API_PORT: int = int(os.environ.get("PORT", 8000))  # Render asigna PORT dinámicamente
    DEBUG: bool = False  # En producción siempre False
    
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    FIREBASE_CREDENTIALS_PATH: str = os.path.join(_API_DIR, "config", "serviceAccountKey.json")
    FIREBASE_DATABASE_URL: str = "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()