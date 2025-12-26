from dataclasses import dataclass, asdict, field
from typing import Optional, List

@dataclass
class Ruta:
    origen: str
    id_conductor: str
    nombre_conductor: str
    id_vehiculo: str
    matricula_vehiculo: str
    # paradas es una lista de diccionarios
    # Ejemplo: [{'direccion': 'Calle A', 'coords': [40.1, -3.2], 'orden': 1}]
    paradas: List[dict] = field(default_factory=list) 
    
    estado: str = "Pendiente"
    fecha_creacion: str = ""
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
            origen=data.get("origen", ""),
            paradas=data.get("paradas", []), 
            id_conductor=data.get("id_conductor", ""),
            nombre_conductor=data.get("nombre_conductor", ""),
            id_vehiculo=data.get("id_vehiculo", ""),
            matricula_vehiculo=data.get("matricula_vehiculo", ""),
            estado=data.get("estado", "Pendiente"),
            fecha_creacion=data.get("fecha_creacion", "")
        )