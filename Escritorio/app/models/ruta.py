from dataclasses import dataclass, asdict, field
from typing import Optional, List

@dataclass
class Ruta:
    nombre: str          # Ej: "Ruta Nocturna Madrid-Sur"
    origen: str          # Ej: "Calle Gran Vía 1"
    estado: str = "Pendiente"

    # Lista de paradas: [{'direccion': '...', 'coords': [lat, lon], 'orden': 1}]
    paradas: List[dict] = field(default_factory=list) 
    
    
    id_ruta: Optional[str] = None

    def to_dict(self):
        data = asdict(self)
        if 'id_ruta' in data:
            del data['id_ruta']
        return data

    @staticmethod
    def from_dict(id_firebase: str, data: dict):
        return Ruta(
            id_ruta=id_firebase,
            nombre=data.get("nombre", "Ruta sin nombre"),
            origen=data.get("origen", ""),
            estado=data.get("estado", "Pendiente"),
            paradas=data.get("paradas", [])
        )