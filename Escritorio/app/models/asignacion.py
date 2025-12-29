from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Asignacion:
    id_ruta: str
    nombre_ruta: str
    id_conductor: str
    nombre_conductor: str
    id_vehiculo: str
    matricula_vehiculo: str
    fecha_inicio: str  # Formato: "dd/MM/yyyy HH:mm"
    estado: str = "Pendiente" # Pendiente, En Curso, Completada
    
    id_asignacion: Optional[str] = None

    def to_dict(self):
        data = asdict(self)
        if 'id_asignacion' in data:
            del data['id_asignacion']
        return data

    @staticmethod
    def from_dict(id_firebase: str, data: dict):
        return Asignacion(
            id_asignacion=id_firebase,
            id_ruta=data.get("id_ruta", ""),
            nombre_ruta=data.get("nombre_ruta", ""),
            id_conductor=data.get("id_conductor", ""),
            nombre_conductor=data.get("nombre_conductor", ""),
            id_vehiculo=data.get("id_vehiculo", ""),
            matricula_vehiculo=data.get("matricula_vehiculo", ""),
            fecha_inicio=data.get("fecha_inicio", ""),
            estado=data.get("estado", "Pendiente")
        )