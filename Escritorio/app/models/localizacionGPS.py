from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class LocalizacionGPS:
    """
    Modelo para representar la ubicación GPS de un conductor en tiempo real.
    """
    id_asignacion: str      # Asignación activa (ruta + conductor + vehículo)
    latitud: float          # Coordenada latitud
    longitud: float         # Coordenada longitud
    timestamp: str          
    
    nombre_conductor: str   # Nombre del conductor
    matricula_vehiculo: str # Matrícula del vehículo
    nombre_ruta: str        # Nombre de la ruta
    
    
    id_localizacion: Optional[str] = None  # ID de Firebase

    def to_dict(self):
        """Convierte a diccionario para Firebase"""
        data = asdict(self)
        if 'id_localizacion' in data:
            del data['id_localizacion']
        return data

    @staticmethod
    def from_dict(id_firebase: str, data: dict):
        """Crea objeto desde datos de Firebase"""
        return LocalizacionGPS(
            id_localizacion=id_firebase,
            id_asignacion=data.get("id_asignacion", ""),
            latitud=data.get("latitud", 0.0),
            longitud=data.get("longitud", 0.0),
            timestamp=data.get("timestamp", ""),
            nombre_conductor=data.get("nombre_conductor", ""),
            matricula_vehiculo=data.get("matricula_vehiculo", ""),
            nombre_ruta=data.get("nombre_ruta", "")
        )
