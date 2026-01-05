from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Gestor:
    """
    Modelo para representar a un gestor de flota.
    """
    nombre: str
    apellidos: str
    email: str
    telefono: str
    estado: str  # "Activo" o "Inactivo"
    
    id_gestor: Optional[str] = None  # UID de Firebase Auth

    def to_dict(self):
        """
        Convierte la dataclass a diccionario para enviar a Firebase.
        """
        data = asdict(self)
        if 'id_gestor' in data:
            del data['id_gestor']
        return data

    @staticmethod
    def from_dict(id_firebase: str, data: dict):
        """
        Crea un objeto Gestor desde los datos de Firebase.
        """
        return Gestor(
            id_gestor=id_firebase,
            nombre=data.get("nombre", ""),
            apellidos=data.get("apellidos", ""),
            email=data.get("email", ""),
            telefono=data.get("telefono", ""),
            estado=data.get("estado", "Activo")
        )