"""
GeocodingUtils - Utilidades para geocodificación

Maneja la conversión de direcciones a coordenadas geográficas.
Proporciona geocodificación asíncrona para no bloquear la UI.
"""
from PySide6.QtCore import QThread, Signal
from geopy.geocoders import Nominatim
from geopy.location import Location
from typing import Optional, Tuple


class GeocodingThread(QThread):
    """
    Thread para geocodificar direcciones sin bloquear la UI.
    Se ejecuta en segundo plano y emite señal cuando termina.
    """
    finished = Signal(object, str)  # (ubicacion, tipo)
    
    def __init__(self, direccion: str, tipo: str):
        super().__init__()
        self.direccion = direccion
        self.tipo = tipo
        self.geolocalizador = Nominatim(user_agent="tfg_fleetsmart_v1")
    
    def run(self):
        """Ejecuta la geocodificación en segundo plano"""
        try:
            ubicacion = self.geolocalizador.geocode(self.direccion)
            self.finished.emit(ubicacion, self.tipo)
        except Exception as e:
            print(f"Error geocodificando '{self.direccion}': {e}")
            self.finished.emit(None, self.tipo)


class GeocodingUtils:
    """
    Utilidad para gestionar geocodificación.
    Proporciona métodos síncronos y asíncronos simples.
    """
    
    def __init__(self, user_agent: str = "tfg_fleetsmart_v1"):
        self.geolocalizador = Nominatim(user_agent=user_agent)
        self.active_thread: Optional[GeocodingThread] = None
    
    # =========================================================================
    # GEOCODIFICACIÓN SÍNCRONA (bloquea la UI)
    # =========================================================================
    
    def geocode_sync(self, direccion: str) -> Optional[Location]:
        """
        Geocodifica de forma síncrona (bloqueante).
        Útil para casos simples donde no importa bloquear momentáneamente.
        
        Args:
            direccion: Dirección a geocodificar
            
        Returns:
            Location con latitude/longitude o None si falla
        """
        try:
            return self.geolocalizador.geocode(direccion)
        except Exception as e:
            print(f"Error geocodificando '{direccion}': {e}")
            return None
    
    # =========================================================================
    # GEOCODIFICACIÓN ASÍNCRONA (no bloquea la UI)
    # =========================================================================
    
    def geocode_async(self, direccion: str, tipo: str, callback) -> GeocodingThread:
        """
        Geocodifica de forma asíncrona (no bloqueante).
        Ideal para no congelar la interfaz mientras busca la dirección.
        
        Args:
            direccion: Dirección a geocodificar
            tipo: Tipo para identificar en callback ('origen', 'parada', etc)
            callback: Función a llamar cuando termine (recibe ubicacion, tipo)
            
        Returns:
            El thread en ejecución
        
        Ejemplo:
            def cuando_termine(ubicacion, tipo):
                if ubicacion:
                    print(f"Encontrado: {ubicacion.latitude}, {ubicacion.longitude}")
            
            geocoding = GeocodingUtils()
            geocoding.geocode_async("Madrid, España", "origen", cuando_termine)
        """
        # Cancelar thread anterior si existe
        if self.active_thread and self.active_thread.isRunning():
            self.active_thread.terminate()
            self.active_thread.wait()
        
        # Crear y ejecutar nuevo thread
        self.active_thread = GeocodingThread(direccion, tipo)
        self.active_thread.finished.connect(callback)
        self.active_thread.start()
        
        return self.active_thread
    
    def cancel_active(self):
        """
        Cancela la geocodificación activa.
        Útil cuando el usuario cambia de vista o cierra el formulario.
        """
        if self.active_thread and self.active_thread.isRunning():
            self.active_thread.terminate()
            self.active_thread.wait()
            self.active_thread = None
    
    # =========================================================================
    # MÉTODOS DE CONVERSIÓN
    # =========================================================================
    
    @staticmethod
    def extract_coords(location: Optional[Location]) -> Optional[Tuple[float, float]]:
        """
        Extrae coordenadas como tupla (lat, lon).
        
        Args:
            location: Objeto Location de geopy
            
        Returns:
            Tupla (latitud, longitud) o None
        """
        if location is None:
            return None
        return (location.latitude, location.longitude)
    
    @staticmethod
    def coords_to_list(location: Optional[Location]) -> Optional[list]:
        """
        Convierte coordenadas a lista [lat, lon] para usar con Folium.
        
        Args:
            location: Objeto Location de geopy
            
        Returns:
            Lista [latitud, longitud] o None
        """
        if location is None:
            return None
        return [location.latitude, location.longitude]
    
    @staticmethod
    def format_address(location: Optional[Location]) -> str:
        """
        Obtiene la dirección formateada como string.
        
        Args:
            location: Objeto Location de geopy
            
        Returns:
            Dirección formateada o string vacío
        """
        if location is None:
            return ""
        return location.address if hasattr(location, 'address') else str(location)