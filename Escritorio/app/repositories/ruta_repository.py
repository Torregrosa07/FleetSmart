from app.data.ruta_dao import RutaDAO
from app.models.ruta import Ruta

class RutaRepository:
    def __init__(self, db_connection):
        self.dao = RutaDAO(db_connection)

    def guardar_ruta(self, ruta_obj):
        try:
            datos = ruta_obj.to_dict()
            self.dao.insertar(datos)
            print("Ruta guardada correctamente en Firebase")
            return True
        except Exception as e:
            print(f"Error guardando ruta: {e}")
            return False

    def obtener_todas(self):
        """Devuelve una lista de objetos Ruta"""
        lista = []
        try:
            respuesta = self.dao.leer_todas()
            if respuesta.each():
                for item in respuesta.each():
                    # Aquí usamos el método estático que acabamos de crear
                    ruta = Ruta.from_dict(item.key(), item.val())
                    lista.append(ruta)
        except Exception as e:
            print(f"Aviso al obtener rutas: {e}")
        return lista