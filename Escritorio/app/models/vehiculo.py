from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Vehiculo:
    matricula: str
    marca: str
    modelo: str
    estado: str
    km_actuales: int = 0
    proxima_itv: str = ""
    ano: int =0

    id_vehiculo: Optional[str] = None 

    def to_dict(self):
        """
        Convierte la dataclass a diccionario para enviar a Firebase.
        Excluimos 'id_vehiculo' porque en Firebase el ID es la clave de la rama,
        no suele guardarse repetido dentro de los datos.
        """
        data = asdict(self)
        if 'id_vehiculo' in data:
            del data['id_vehiculo']
        return data

    @staticmethod
    def from_dict(id_firebase: str, data: dict):
  
        return Vehiculo(
            id_vehiculo=id_firebase,
            matricula=data.get("matricula", ""),
            marca= data.get("marca", ""),
            modelo=data.get("modelo", ""),
            estado=data.get("estado", ""),
            km_actuales=data.get("km_actuales", 0),
            proxima_itv=data.get("proxima_itv", ""),
            ano=data.get("ano", 0)
        )