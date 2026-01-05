from app.config.config import get_admin_db

class LocalizacionGPSDAO:
    """
    Data Access Object para localizaciones GPS.
    Usa Firebase Admin SDK exclusivamente para listeners en tiempo real.
    
    Estructura en Firebase:
    /localizaciones_actuales/{id_asignacion}  <- Última ubicación de cada conductor
    /historial_localizaciones/{id_asignacion}/{timestamp_id}  <- Historial completo
    """
    
    def __init__(self):
        self.db = get_admin_db()
        self.ref_actual = self.db.child('localizaciones_actuales')
        self.ref_historial = self.db.child('historial_localizaciones')

    def guardar_ubicacion_actual(self, id_asignacion, localizacion_dict):
        """
        Guarda/actualiza la última ubicación de una asignación.
        Sobrescribe la ubicación anterior (solo mantiene la más reciente).
        """
        try:
            self.ref_actual.child(id_asignacion).set(localizacion_dict)
            return True
        except Exception as e:
            print(f"Error guardando ubicación: {e}")
            return False
    
    def guardar_en_historial(self, id_asignacion, localizacion_dict):
        """
        Guarda la ubicación en el historial.
        Firebase genera un ID único automáticamente.
        """
        try:
            self.ref_historial.child(id_asignacion).push(localizacion_dict)
            return True
        except Exception as e:
            print(f"Error guardando historial: {e}")
            return False
    
    def leer_ubicacion_actual(self, id_asignacion):
        """Obtiene la última ubicación de una asignación específica"""
        try:
            return self.ref_actual.child(id_asignacion).get()
        except Exception as e:
            print(f"Error leyendo ubicación: {e}")
            return None
    
    def leer_todas_ubicaciones_actuales(self):
        """
        Obtiene todas las ubicaciones actuales.
        Usado por CommandCenter para mostrar todos los conductores en el mapa.
        """
        try:
            return self.ref_actual.get()
        except Exception as e:
            print(f"Error leyendo ubicaciones: {e}")
            return None
    
    def leer_historial(self, id_asignacion):
        """Obtiene el historial completo de ubicaciones de una asignación"""
        try:
            return self.ref_historial.child(id_asignacion).get()
        except Exception as e:
            print(f"Error leyendo historial: {e}")
            return None
    
    def eliminar_ubicacion_actual(self, id_asignacion):
        """
        Elimina la ubicación actual de una asignación.
        Se usa cuando la asignación termina.
        """
        try:
            self.ref_actual.child(id_asignacion).delete()
            return True
        except Exception as e:
            print(f"Error eliminando ubicación: {e}")
            return False
    
    def crear_listener(self, callback):
        """
        Crea un listener para escuchar cambios en tiempo real.
        Cuando hay un cambio en /localizaciones_actuales, se ejecuta el callback.
        
        Args:
            callback: Función que se ejecuta cuando hay cambios
        
        Returns:
            Listener stream (para poder cerrarlo después)
        """
        return self.ref_actual.listen(callback)