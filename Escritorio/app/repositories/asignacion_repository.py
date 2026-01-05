from app.data.asignacion_dao import AsignacionDAO
from app.models.asignacion import Asignacion

class AsignacionRepository:
    def __init__(self, db_connection):
        self.dao = AsignacionDAO(db_connection)
        
        
        
    def conductor_tiene_asignacion_activa(self, id_conductor):
        """
        Verifica si un conductor ya tiene una ruta asignada.
        """
        try:
            todas = self.obtener_todas()
            for asig in todas:
                if asig.id_conductor == id_conductor:
                    return True, asig.nombre_ruta
            return False, ""
        except Exception as e:
            print(f"Error verificando conductor: {e}")
            return False, ""
    
    
    
    def vehiculo_tiene_asignacion_activa(self, id_vehiculo):
        """
        Verifica si un vehículo ya tiene una ruta asignada.
        """
        try:
            todas = self.obtener_todas()
            for asig in todas:
                if asig.id_vehiculo == id_vehiculo:
                    return True, asig.nombre_ruta
            return False, ""
        except Exception as e:
            print(f"Error verificando vehículo: {e}")
            return False, ""
    
    
    
    def ruta_tiene_asignacion(self, id_ruta):
        """
        Verifica si una ruta ya está asignada.
        """
        try:
            todas = self.obtener_todas()
            for asig in todas:
                if asig.id_ruta == id_ruta:
                    return True
            return False
        except Exception as e:
            print(f"Error verificando ruta: {e}")
            return False



    def guardar_asignacion(self, asignacion_obj):
        try:
            self.dao.insertar(asignacion_obj.to_dict())
            print("Asignación guardada correctamente")
            return True
        except Exception as e:
            print(f"Error guardando asignación: {e}")
            return False
        
    def obtener_todas(self):
        lista = []
        try:
            respuesta = self.dao.leer_todos()
            if respuesta.each():
                for item in respuesta.each():
                    asignacion = Asignacion.from_dict(item.key(), item.val())
                    lista.append(asignacion)
        except Exception as e:
            print(f"Error obteniendo asignaciones: {e}")
        return lista
    
    
    
    def eliminar_asignacion(self, id_asignacion):
        try:
            self.dao.db.child(self.dao.collection_name).child(id_asignacion).remove()
            print(f"Asignación {id_asignacion} eliminada.")
            return True
        except Exception as e:
            print(f"Error eliminando asignación: {e}")
            return False