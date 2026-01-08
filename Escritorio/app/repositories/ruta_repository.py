from app.data.ruta_dao import RutaDAO
from app.models.ruta import Ruta

class RutaRepository:
    def __init__(self, db_connection):
        self.dao = RutaDAO(db_connection)

    def guardar_ruta(self, ruta_obj):
        """Guarda una nueva ruta en Firebase"""
        try:
            self.dao.insertar(ruta_obj.to_dict())
            print("Ruta guardada correctamente")
            return True
        except Exception as e:
            print(f"Error guardando ruta: {e}")
            return False

    def obtener_todas(self):
        """Devuelve una lista con todas las rutas"""
        lista_rutas = []
        try:
            rutas_firebase = self.dao.leer_todas()
            if rutas_firebase.each():
                for item in rutas_firebase.each():
                    # Convertimos el diccionario de Firebase a objeto Ruta
                    ruta = Ruta.from_dict(item.key(), item.val())
                    lista_rutas.append(ruta)
        except Exception as e:
            print(f"Error obteniendo rutas: {e}")
        return lista_rutas


    def obtener_por_id(self, id_ruta):
        """Busca una ruta específica por su ID único"""
        try:
            # Accedemos directamente al nodo de esa ruta usando su ID
            snapshot = self.dao.db.child(self.dao.collection_name).child(id_ruta).get()
            
            if snapshot.val():
                return Ruta.from_dict(snapshot.key(), snapshot.val())
            else:
                print(f"Ruta {id_ruta} no encontrada.")
                return None
        except Exception as e:
            print(f"Error buscando ruta por ID: {e}")
            return None

    def actualizar_estado(self, id_ruta, nuevo_estado):
        """Actualiza solo el campo 'estado' de la ruta"""
        try:
            self.dao.db.child(self.dao.collection_name).child(id_ruta).update({
                "estado": nuevo_estado
            })
            print(f"Estado de ruta {id_ruta} actualizado a '{nuevo_estado}'")
            return True
        except Exception as e:
            print(f"Error actualizando estado: {e}")
            return False
            
    def actualizar(self, ruta_obj):
        """Actualiza una ruta completa (por si acaso usas esta versión)"""
        try:
            if not ruta_obj.id_ruta:
                return False
            self.dao.db.child(self.dao.collection_name).child(ruta_obj.id_ruta).update(ruta_obj.to_dict())
            return True
        except Exception as e:
            return False