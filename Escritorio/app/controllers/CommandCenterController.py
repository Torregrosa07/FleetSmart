"""
CommandCenterController - Versión refactorizada

RESPONSABILIDADES:
- Manejo de UI (mapa en tiempo real)
- Usar MapUtils para crear el mapa
- Usar CommandCenterService para datos y listener
- Lógica de zoom inteligente

Código simple y claro.
"""
from PySide6.QtWidgets import QWidget

from app.views.CommandCenterPage_ui import Ui_CommandCenterPage
from app.services.command_center_service import CommandCenterService
from app.utils.map_utils import MapUtils


class CommandCenterController(QWidget, Ui_CommandCenterPage):
    """
    Centro de Comandos: muestra vehículos en tiempo real en un mapa.
    
    Características:
    - Listener de Firebase para actualizaciones GPS
    - Zoom inteligente (solo ajusta la primera vez)
    - Usa MapUtils para crear mapas
    - Usa CommandCenterService para datos
    """
    
    def __init__(self, coords_iniciales=None):
        super().__init__()
        self.setupUi(self)
        
        # Servicio de lógica de negocio
        self.service = CommandCenterService()
        
        # Coordenadas de la empresa
        if coords_iniciales:
            self.empresa_coords = coords_iniciales
        else:
            self.empresa_coords = CommandCenterService.COORDS_DEFAULT
        
        # Control de zoom inteligente
        self.es_primera_carga = True
        
        # Conectar botones
        if hasattr(self, 'btnActualizar'):
            self.btnActualizar.clicked.connect(self.actualizar_mapa)
        
        # Inicializar
        self.actualizar_mapa()
        self.service.iniciar_listener(self.actualizar_mapa)
    
    # =========================================================================
    # ACTUALIZACIÓN DE EMPRESA
    # =========================================================================
    
    def actualizar_ubicacion_empresa(self, nuevas_coords):
        """
        Recibe [lat, lon] desde SettingsController y actualiza el mapa.
        Al cambiar la sede, permite que se re-ajuste el zoom una vez.
        """
        if nuevas_coords:
            self.empresa_coords = nuevas_coords
            self.es_primera_carga = True
            self.actualizar_mapa()
    
    # =========================================================================
    # MAPA
    # =========================================================================
    
    def actualizar_mapa(self):
        """
        Dibuja el mapa con empresa y vehículos activos.
        
        ZOOM INTELIGENTE:
        - Primera carga: fit_bounds para mostrar todos los puntos
        - Siguientes actualizaciones: mantiene el zoom actual
          para no interrumpir si el usuario está haciendo zoom manual
        """
        # 1. Obtener ubicaciones del servicio
        ubicaciones = self.service.obtener_ubicaciones_activas()
        
        # 2. Convertir al formato que necesita MapUtils
        vehiculos = self.service.preparar_datos_mapa(ubicaciones)
        
        # 3. Crear mapa usando MapUtils
        # Pasamos fit_to_bounds solo en primera carga
        mapa = MapUtils.create_fleet_map(
            company_coords=self.empresa_coords,
            company_name="FleetSmart HQ",
            vehicles=vehiculos,
            fit_to_bounds=self.es_primera_carga
        )
        
        # 4. Desactivar fit_bounds para futuras actualizaciones
        if self.es_primera_carga:
            self.es_primera_carga = False
        
        # 5. Renderizar mapa
        html = MapUtils.render_to_html(mapa)
        if hasattr(self, 'webMap'):
            self.webMap.setHtml(html)
    
    # =========================================================================
    # LIMPIEZA AL CERRAR
    # =========================================================================
    
    def detener_listener(self):
        """Detiene el listener de Firebase (llamado desde MainController)"""
        self.service.detener_listener()

    def closeEvent(self, event):
        """Detener listener al cerrar"""
        self.service.detener_listener()
        event.accept()
        
        
    def detener_listener(self):
        """Permite que MainController detenga el listener externamente"""
        self.service.detener_listener()