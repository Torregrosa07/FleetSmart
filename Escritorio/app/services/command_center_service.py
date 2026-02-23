from PySide6.QtCore import QObject, Signal
from app.repositories.localizacionGPS_repository import LocalizacionGPSRepository


class FirebaseListenerBridge(QObject):
    """
    Bridge para emitir señales Qt desde el listener de Firebase.
    Firebase notifica en un thread separado, esta clase permite
    conectar esa notificación con el thread de la UI.
    """
    ubicacion_actualizada = Signal()


class CommandCenterService:
    """
    Servicio que encapsula la lógica del centro de comandos.
    """
    
    # Coordenadas por defecto (Madrid)
    COORDS_DEFAULT = [40.4168, -3.7038]
    
    def __init__(self):
        self.repo = LocalizacionGPSRepository()
        self.listener_activo = None
        self.bridge = FirebaseListenerBridge()
    
    # =========================================================================
    # LISTENER DE FIREBASE
    # =========================================================================
    
    def iniciar_listener(self, callback):
        """
        Inicia el listener de Firebase para actualizaciones GPS en tiempo real.
        
        
        
        
        Args:
            callback: Función a llamar cuando haya actualización
        """
        try:
            def on_cambio(event):
                self.bridge.ubicacion_actualizada.emit()
            
            # Conectar señal con el callback
            self.bridge.ubicacion_actualizada.connect(callback)
            
            # Crear listener
            self.listener_activo = self.repo.crear_listener(on_cambio)
        
        except Exception as e:
            print(f"Error iniciando listener: {e}")
    
    def detener_listener(self):
        """Detiene el listener activo de Firebase"""
        if self.listener_activo:
            try:
                self.listener_activo.close()
            except Exception as e:
                print(f"Error deteniendo listener: {e}")
            finally:
                self.listener_activo = None
        
        # Desconectar señal del bridge para evitar llamadas fantasma
        try:
            self.bridge.ubicacion_actualizada.disconnect()
        except Exception:
            pass
    
    # =========================================================================
    # CONSULTAS
    # =========================================================================
    
    def obtener_ubicaciones_activas(self):
        """
        Obtiene todas las ubicaciones activas de conductores.
        
        Returns:
            Lista de objetos ubicación con latitud, longitud, matricula, etc.
        """
        return self.repo.obtener_ubicaciones_activas()
    
    def preparar_datos_mapa(self, ubicaciones):
        """
        Convierte ubicaciones del repositorio al formato que necesita MapUtils.
        
        Args:
            ubicaciones: Lista de ubicaciones del repositorio
            
        Returns:
            Lista de dicts con formato para MapUtils.create_fleet_map()
        """
        vehiculos = []
        
        for ubicacion in ubicaciones:
            vehiculos.append({
                'latitud': ubicacion.latitud,
                'longitud': ubicacion.longitud,
                'matricula_vehiculo': ubicacion.matricula_vehiculo,
                'nombre_conductor': ubicacion.nombre_conductor,
                'nombre_ruta': ubicacion.nombre_ruta,
                'timestamp': ubicacion.timestamp
            })
        
        return vehiculos