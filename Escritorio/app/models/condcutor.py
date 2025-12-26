from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Conductor:
    dni: str
    nombre: str
    licencia: str
    estado: str
    telefono: str
    email: str 
    

    id_conductor: Optional[str] = None 

    def to_dict(self):
        """
        Convierte la dataclass a diccionario para enviar a Firebase.
        Excluimos 'id_vehiculo' porque en Firebase el ID es la clave de la rama,
        no suele guardarse repetido dentro de los datos.
        """
        data = asdict(self)
        if 'id_conductor' in data:
            del data['id_conductor']
        return data

    @staticmethod
    def from_dict(id_firebase: str, data: dict):
  
        return Conductor(
            id_conductor=id_firebase,
            dni=data.get("dni", ""),
            nombre= data.get("nombre", ""),
            licencia=data.get("licencia", ""),
            estado=data.get("estado", ""),
            telefono=data.get("telefono", ""),
            email=data.get("email", ""),
            
        )