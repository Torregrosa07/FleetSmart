from dataclasses import dataclass, asdict, field
from typing import Optional, List

@dataclass
class Ruta:
    """
    Modelo para representar una ruta de transporte.
    Según la memoria del proyecto, una ruta es una plantilla que puede
    ser asignada a múltiples conductores y vehículos.
    """
    nombre: str          # Ej: "Ruta Nocturna Madrid-Sur"
    origen: str          # Ej: "Calle Gran Vía 1, Madrid"
    destino: str         # Destino final de la ruta
    fecha: str           # Fecha planificada (formato: "dd/MM/yyyy")
    hora_inicio_prevista: str  # Ej: "08:00"
    hora_fin_prevista: str     # Ej: "17:00"
    id_gestor: str       # ID del gestor que creó esta ruta
    estado: str = "Pendiente"  # Pendiente, En Curso, Completada

    # Lista de paradas intermedias: [{'direccion': '...', 'coords': [lat, lon], 'orden': 1}]
    paradas: List[dict] = field(default_factory=list) 
    
    id_ruta: Optional[str] = None

    def to_dict(self):
        """
        Convierte la ruta a diccionario para Firebase.
        Excluye id_ruta porque es la clave en Firebase.
        """
        data = asdict(self)
        if 'id_ruta' in data:
            del data['id_ruta']
        return data

    @staticmethod
    def from_dict(id_firebase: str, data: dict):
        """
        Crea un objeto Ruta desde los datos de Firebase.
        """
        return Ruta(
            id_ruta=id_firebase,
            nombre=data.get("nombre", "Ruta sin nombre"),
            origen=data.get("origen", ""),
            destino=data.get("destino", ""),
            fecha=data.get("fecha", ""),
            hora_inicio_prevista=data.get("hora_inicio_prevista", "00:00"),
            hora_fin_prevista=data.get("hora_fin_prevista", "00:00"),
            id_gestor=data.get("id_gestor", ""),
            estado=data.get("estado", "Pendiente"),
            paradas=data.get("paradas", [])
        )