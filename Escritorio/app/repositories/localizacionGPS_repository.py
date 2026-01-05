from app.data.localizacionGPS_dao import LocalizacionGPSDAO
from app.models.localizacionGPS import LocalizacionGPS

class LocalizacionGPSRepository:
    """
    Repositorio para gestionar localizaciones GPS.
    Contiene la lógica de negocio y convierte entre objetos y dicts.
    """
    
    def __init__(self):
        self.dao = LocalizacionGPSDAO()

    def actualizar_ubicacion(self, localizacion_obj, guardar_historial=True):
        """
        Actualiza la ubicación actual de un conductor.
        
        Args:
            localizacion_obj: Objeto LocalizacionGPS
            guardar_historial: Si True, también guarda en historial
        
        Returns:
            True si se guardó correctamente
        """
        try:
            datos = localizacion_obj.to_dict()
            
            # Guardar/actualizar ubicación actual
            success = self.dao.guardar_ubicacion_actual(
                localizacion_obj.id_asignacion,
                datos
            )
            
            if not success:
                return False
            
            # Opcionalmente guardar en historial
            if guardar_historial:
                self.dao.guardar_en_historial(
                    localizacion_obj.id_asignacion,
                    datos
                )
            
            return True
            
        except Exception as e:
            print(f"Error al actualizar ubicación: {e}")
            return False
    
    def obtener_ubicaciones_activas(self):
        """
        Obtiene todas las ubicaciones actuales de conductores activos.
        Usado por CommandCenter para mostrar todos en el mapa.
        
        Returns:
            Lista de objetos LocalizacionGPS
        """
        lista = []
        try:
            snapshot = self.dao.leer_todas_ubicaciones_actuales()
            
            if snapshot:
                for id_asignacion, datos in snapshot.items():
                    localizacion = LocalizacionGPS.from_dict(id_asignacion, datos)
                    lista.append(localizacion)
                    
        except Exception as e:
            print(f"Error al obtener ubicaciones activas: {e}")
            
        return lista
    
    def obtener_ubicacion_asignacion(self, id_asignacion):
        """
        Obtiene la última ubicación de una asignación específica.
        
        Returns:
            Objeto LocalizacionGPS o None
        """
        try:
            datos = self.dao.leer_ubicacion_actual(id_asignacion)
            
            if datos:
                return LocalizacionGPS.from_dict(id_asignacion, datos)
            else:
                return None
                
        except Exception as e:
            print(f"Error al obtener ubicación: {e}")
            return None
    
    def obtener_historial_asignacion(self, id_asignacion):
        """
        Obtiene el historial completo de ubicaciones de una asignación.
        Útil para ver la ruta recorrida.
        
        Returns:
            Lista de objetos LocalizacionGPS ordenados por timestamp
        """
        lista = []
        try:
            snapshot = self.dao.leer_historial(id_asignacion)
            
            if snapshot:
                for id_loc, datos in snapshot.items():
                    localizacion = LocalizacionGPS.from_dict(id_loc, datos)
                    lista.append(localizacion)
            
            # Ordenar por timestamp
            lista.sort(key=lambda x: x.timestamp)
                    
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            
        return lista
    
    def limpiar_ubicacion(self, id_asignacion):
        """
        Elimina la ubicación actual cuando una asignación termina.
        El historial se mantiene para análisis.
        """
        try:
            return self.dao.eliminar_ubicacion_actual(id_asignacion)
        except Exception as e:
            print(f"Error al limpiar ubicación: {e}")
            return False
    
    def crear_listener(self, callback_function):
        """
        Crea un listener para recibir actualizaciones en tiempo real.
        
        Args:
            callback_function: Función que se ejecutará cuando haya cambios.
                              Recibe un parámetro 'event' con información del cambio.
        
        Returns:
            Listener stream o None si falla
        """
        try:
            return self.dao.crear_listener(callback_function)
        except Exception as e:
            print(f"Error al crear listener: {e}")
            return None