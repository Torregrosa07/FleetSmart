from app.data.ruta_dao import RutaDAO
from app.models.ruta import Ruta

class RutaRepository:
    def __init__(self, db_connection):
        self.dao = RutaDAO(db_connection)

    def guardar_ruta(self, ruta_obj):
        """Guarda una nueva ruta en Firebase"""
        try:
            resultado = self.dao.insertar(ruta_obj.to_dict())
            # Asignar el ID generado al objeto
            ruta_obj.id_ruta = resultado['name']
            print(f"Ruta guardada correctamente con ID: {resultado['name']}")
            return True
        except Exception as e:
            print(f"Error guardando ruta: {e}")
            return False

    def obtener_todas(self):
        """Devuelve una lista con todas las rutas"""
        lista_rutas = []
        try:
            rutas_firebase = self.dao.leer_todas()
            # CORREGIDO: Solo verificar que no sea None
            if rutas_firebase:
                for item in rutas_firebase.each():
                    ruta = Ruta.from_dict(item.key(), item.val())
                    lista_rutas.append(ruta)
            
            print(f"✅ Se cargaron {len(lista_rutas)} rutas desde Firebase")
        except Exception as e:
            print(f"❌ Error obteniendo rutas: {e}")
        return lista_rutas

    def obtener_por_id(self, id_ruta):
        """Busca una ruta específica por su ID único"""
        try:
            datos = self.dao.leer_una(id_ruta)
            if datos:
                return Ruta.from_dict(id_ruta, datos)
            else:
                print(f"Ruta {id_ruta} no encontrada.")
                return None
        except Exception as e:
            print(f"Error buscando ruta por ID: {e}")
            return None

    def actualizar_ruta(self, ruta_obj):
        """Actualiza una ruta completa"""
        try:
            if not ruta_obj.id_ruta:
                return False
            self.dao.actualizar(ruta_obj.id_ruta, ruta_obj.to_dict())
            print(f"Ruta {ruta_obj.id_ruta} actualizada correctamente")
            return True
        except Exception as e:
            print(f"Error actualizando ruta: {e}")
            return False
    
    def eliminar_ruta(self, id_ruta):
        """Elimina una ruta de Firebase"""
        try:
            self.dao.eliminar(id_ruta)
            print(f"Ruta {id_ruta} eliminada correctamente")
            return True
        except Exception as e:
            print(f"Error eliminando ruta: {e}")
            return False
    
    def actualizar_estado(self, id_ruta, nuevo_estado):
        """Actualiza solo el campo 'estado' de la ruta"""
        try:
            self.dao.actualizar(id_ruta, {"estado": nuevo_estado})
            print(f"Estado de ruta {id_ruta} actualizado a '{nuevo_estado}'")
            return True
        except Exception as e:
            print(f"Error actualizando estado: {e}")
            return False