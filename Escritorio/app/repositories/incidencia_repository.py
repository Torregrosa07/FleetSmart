from app.data.incidencia_dao import IncidenciaDAO
from app.models.incidencia import Incidencia

class IncidenciaRepository:
    
    def __init__(self, db_connection):
        self.dao = IncidenciaDAO(db_connection)

    def guardar_incidencia(self, incidencia_obj):
        """
        Guarda una nueva incidencia en Firebase.
        """
        try:
            datos = incidencia_obj.to_dict()
            self.dao.insertar(datos)
            print(f"Incidencia guardada: {incidencia_obj.tipo}")
            return True
        except Exception as e:
            print(f"Error al guardar incidencia: {e}")
            return False
            
    def obtener_todas(self):
        """
        Obtiene todas las incidencias de Firebase.
        """
        lista = []
        try:
            respuesta = self.dao.leer_todos()
            
            if respuesta.each():
                for item in respuesta.each():
                    id_firebase = item.key()
                    datos = item.val()
                    
                    incidencia = Incidencia.from_dict(id_firebase, datos)
                    lista.append(incidencia)
            
            # Ordenar por fecha/hora (más recientes primero)
            # Nota: esto es simple, para producción usar timestamp
            lista.reverse()
                    
        except Exception as e:
            print(f"Error al obtener incidencias: {e}")
            
        return lista
    
    def obtener_por_vehiculo(self, id_vehiculo):
        """
        Obtiene todas las incidencias de un vehículo específico.
        """
        todas = self.obtener_todas()
        return [inc for inc in todas if inc.id_vehiculo == id_vehiculo]
    
    def obtener_por_estado(self, estado):
        """
        Obtiene incidencias filtradas por estado.
        """
        todas = self.obtener_todas()
        return [inc for inc in todas if inc.estado == estado]
    
    def obtener_por_id(self, id_incidencia):
        """
        Obtiene una incidencia específica.
        """
        try:
            respuesta = self.dao.leer_por_id(id_incidencia)
            
            if respuesta.val():
                return Incidencia.from_dict(id_incidencia, respuesta.val())
            else:
                return None
                
        except Exception as e:
            print(f"Error al obtener incidencia: {e}")
            return None
    
    def eliminar_incidencia(self, id_incidencia):
        """Elimina una incidencia"""
        try:
            self.dao.eliminar(id_incidencia)
            return True
        except Exception as e:
            print(f"Error al eliminar incidencia: {e}")
            return False

    def actualizar_incidencia(self, incidencia_obj):
        """
        Actualiza una incidencia existente.
        Útil para cambiar el estado de "Pendiente" a "Resuelta".
        """
        try:
            if not incidencia_obj.id_incidencia:
                print("Error: La incidencia debe tener un ID")
                return False
            
            datos = incidencia_obj.to_dict()
            self.dao.actualizar(incidencia_obj.id_incidencia, datos)
            return True
        except Exception as e:
            print(f"Error al actualizar incidencia: {e}")
            return False