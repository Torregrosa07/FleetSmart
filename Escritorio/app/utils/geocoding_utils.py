"""
GeocodingService - Servicio para geocodificación asíncrona
Maneja la conversión de direcciones a coordenadas geográficas
"""
from PySide6.QtCore import QThread, Signal
from geopy.geocoders import Nominatim
from geopy.location import Location
from typing import Optional, Tuple, Callable


class GeocodingThread(QThread):
    """
    Thread para geocodificar direcciones sin bloquear la UI.
    """
    finished = Signal(object, str, object)  # (ubicacion, tipo, metadata)
    
    def __init__(self, direccion: str, tipo: str, metadata: dict = None):
        super().__init__()
        self.direccion = direccion
        self.tipo = tipo
        self.metadata = metadata or {}
        self.geolocalizador = Nominatim(user_agent="tfg_fleetsmart_v1")
    
    def run(self):
        """Ejecuta la geocodificación en segundo plano"""
        try:
            ubicacion = self.geolocalizador.geocode(self.direccion)
            self.finished.emit(ubicacion, self.tipo, self.metadata)
        except Exception as e:
            print(f"Error geocodificando '{self.direccion}': {e}")
            self.finished.emit(None, self.tipo, self.metadata)


class GeocodingService:
    """
    Servicio de alto nivel para gestionar geocodificación.
    Proporciona métodos síncronos y asíncronos.
    """
    
    def __init__(self, user_agent: str = "tfg_fleetsmart_v1"):
        self.geolocalizador = Nominatim(user_agent=user_agent)
        self.active_thread: Optional[GeocodingThread] = None
    
    def geocode_sync(self, direccion: str) -> Optional[Location]:
        """
        Geocodifica de forma síncrona (bloqueante).
        
        Args:
            direccion: Dirección a geocodificar
            
        Returns:
            Location con latitude/longitude o None
        """
        try:
            return self.geolocalizador.geocode(direccion)
        except Exception as e:
            print(f"Error geocodificando '{direccion}': {e}")
            return None
    
    def geocode_async(
        self,
        direccion: str,
        tipo: str,
        callback: Callable,
        metadata: dict = None
    ) -> GeocodingThread:
        """
        Geocodifica de forma asíncrona (no bloqueante).
        
        Args:
            direccion: Dirección a geocodificar
            tipo: Tipo para identificar en callback
            callback: Función a llamar cuando termine
            metadata: Info adicional para el callback
            
        Returns:
            El thread en ejecución
        """
        # Cancelar thread anterior si existe
        if self.active_thread and self.active_thread.isRunning():
            self.active_thread.terminate()
            self.active_thread.wait()
        
        # Crear y ejecutar nuevo thread
        self.active_thread = GeocodingThread(direccion, tipo, metadata)
        self.active_thread.finished.connect(callback)
        self.active_thread.start()
        
        return self.active_thread
    
    def cancel_active(self):
        """Cancela la geocodificación activa"""
        if self.active_thread and self.active_thread.isRunning():
            self.active_thread.terminate()
            self.active_thread.wait()
            self.active_thread = None
    
    @staticmethod
    def extract_coords(location: Optional[Location]) -> Optional[Tuple[float, float]]:
        """Extrae coordenadas como tupla (lat, lon)"""
        if location is None:
            return None
        return (location.latitude, location.longitude)
    
    @staticmethod
    def coords_to_list(location: Optional[Location]) -> Optional[list]:
        """Convierte a lista [lat, lon] para Folium"""
        if location is None:
            return None
        return [location.latitude, location.longitude]
    
    @staticmethod
    def format_address(location: Optional[Location]) -> str:
        """Obtiene la dirección formateada"""
        if location is None:
            return ""
        return location.address if hasattr(location, 'address') else str(location)


class GeocodingHelper:
    """Funciones de utilidad para geocodificación"""
    
    @staticmethod
    def geocode_simple(direccion: str) -> Optional[Tuple[float, float]]:
        """
        Geocodificación síncrona simple.
        
        Args:
            direccion: Dirección a geocodificar
            
        Returns:
            Tupla (lat, lon) o None
        """
        service = GeocodingService()
        location = service.geocode_sync(direccion)
        return GeocodingService.extract_coords(location)
    
    @staticmethod
    def create_service() -> GeocodingService:
        """Factory function para crear un servicio"""
        return GeocodingService()