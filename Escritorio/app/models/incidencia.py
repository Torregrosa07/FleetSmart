from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Incidencia:
    """
    Modelo para representar una incidencia de vehículo.
    """
    id_vehiculo: str        # ID del vehículo afectado
    matricula: str          # Matrícula del vehículo (desnormalizado para mostrar)
    tipo: str               # "Avería", "Accidente", "Mantenimiento", "Otro"
    descripcion: str        # Descripción detallada de la incidencia
    fecha: str              # Fecha de la incidencia (formato: "dd/MM/yyyy")
    hora: str               # Hora de la incidencia (formato: "HH:mm")
    estado: str             # "Pendiente", "En Proceso", "Resuelta"
    id_gestor: str          # Gestor que registró la incidencia
    
    # Opcionales
    id_conductor: Optional[str] = None  # Conductor involucrado (si aplica)
    nombre_conductor: Optional[str] = None  # Nombre del conductor (desnormalizado)
    
    id_incidencia: Optional[str] = None  # ID de Firebase

    def to_dict(self):
        """Convierte la incidencia a diccionario para Firebase"""
        data = asdict(self)
        if 'id_incidencia' in data:
            del data['id_incidencia']
        return data

    @staticmethod
    def from_dict(id_firebase: str, data: dict):
        """Crea un objeto Incidencia desde los datos de Firebase"""
        return Incidencia(
            id_incidencia=id_firebase,
            id_vehiculo=data.get("id_vehiculo", ""),
            matricula=data.get("matricula", ""),
            tipo=data.get("tipo", "Otro"),
            descripcion=data.get("descripcion", ""),
            fecha=data.get("fecha", ""),
            hora=data.get("hora", ""),
            estado=data.get("estado", "Pendiente"),
            id_gestor=data.get("id_gestor", ""),
            id_conductor=data.get("id_conductor"),
            nombre_conductor=data.get("nombre_conductor")
        )