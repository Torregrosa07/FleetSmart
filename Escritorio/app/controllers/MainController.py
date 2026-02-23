from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QDate, QLocale
from app.views.MainWindow_ui import Ui_MainWindow
from app.controllers.CommandCenterController import CommandCenterController
from app.utils.language_utils import LanguageService
from app.controllers.VehiclesController import VehiclesController
from app.controllers.ConductoresController import ConductoresController
from app.controllers.SettingsController import SettingsController
from app.controllers.RutasController import RutasController
from app.controllers.AsignacionController import AsignacionController
from app.controllers.IncidenciasController import IncidenciasController
import pyrebase
from app.config.config import FIREBASE_CONFIG

class MainWindowController(QMainWindow, Ui_MainWindow):
    def __init__(self, app_state, settings_service=None):
        super().__init__()
        self.setupUi(self)
        self.app_state = app_state
        self.settings_service = settings_service
        
        # 1. Inicializar conexión a BD (para pasarla a los hijos)
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.db = self.firebase.database()
        
        coords_guardadas = self.app_state.get("empresa_coords")

        # 2. Inicializar Vistas Hijas
        self.vista_mapa = CommandCenterController(coords_iniciales=self.app_state.get("empresa_coords"))
        self.vista_vehiculos = VehiclesController(self.db, self.app_state)
        self.vista_conductores = ConductoresController(self.db)
        self.vista_rutas = RutasController(self.db, self.app_state)
        self.vista_asignaciones = AsignacionController(self.db)
        self.vista_incidencias = IncidenciasController(self.db, self.app_state)
        
        self.conectar_senales_vistas()

        # 3. Añadirlas al Stacked Widget
        self.idx_mapa = self.stackContent.addWidget(self.vista_mapa)
        self.idx_vehiculos = self.stackContent.addWidget(self.vista_vehiculos)
        self.idx_conductores = self.stackContent.addWidget(self.vista_conductores)
        self.idx_rutas = self.stackContent.addWidget(self.vista_rutas)
        self.idx_asignaciones = self.stackContent.addWidget(self.vista_asignaciones)
        self.idx_incidencias = self.stackContent.addWidget(self.vista_incidencias)

        # 4. Conectar Botones del Menú Lateral
        self.btnCommandCenter.clicked.connect(self.ir_a_mapa)
        self.btnVehicles.clicked.connect(self.ir_a_vehiculos)
        self.btnDrivers.clicked.connect(self.ir_a_conductores)
        self.btnRoutes.clicked.connect(self.ir_a_rutas)
        self.btnSettings.clicked.connect(self.abrir_ajustes)
        self.btnAssign.clicked.connect(self.ir_a_asignaciones)
        self.btnIncidents.clicked.connect(self.ir_a_incidencias)
        
        self.actualizar_fecha()
        self.ir_a_mapa()
        self.actualizar_textos()
        
        
    def actualizar_textos(self):
        """Actualiza los textos de la ventana principal y propaga a las hijas"""
        idioma = self.app_state.get("language", "Español")
        
        # 1. Actualizar textos del Menú Lateral
        self.btnCommandCenter.setText(LanguageService.get_text("command_center", idioma))
        self.btnVehicles.setText(LanguageService.get_text("vehicles", idioma))
        self.btnDrivers.setText(LanguageService.get_text("drivers", idioma))
        self.btnRoutes.setText(LanguageService.get_text("routes", idioma))
        self.btnAssign.setText(LanguageService.get_text("assignments", idioma))
        self.btnIncidents.setText(LanguageService.get_text("incidents", idioma))
        self.btnSettings.setText(LanguageService.get_text("settings", idioma))
        
        # Actualizar titulo de pagina segun vista actual
        idx = self.stackContent.currentIndex()
        if idx == self.idx_mapa:
            self.lblPageTitle.setText(LanguageService.get_text("command_center", idioma))
        elif idx == self.idx_vehiculos:
            self.lblPageTitle.setText(LanguageService.get_text("vehicle_management", idioma))
        elif idx == self.idx_conductores:
            self.lblPageTitle.setText(LanguageService.get_text("driver_management", idioma))
        elif idx == self.idx_rutas:
            self.lblPageTitle.setText(LanguageService.get_text("route_creation", idioma))
        elif idx == self.idx_asignaciones:
            self.lblPageTitle.setText(LanguageService.get_text("assignment_management", idioma))
        elif idx == self.idx_incidencias:
            self.lblPageTitle.setText(LanguageService.get_text("incident_management", idioma))
        
        # 2. Propagar a las vistas hijas
        if hasattr(self.vista_vehiculos, 'actualizar_idioma'):
            self.vista_vehiculos.actualizar_idioma(idioma)
        if hasattr(self.vista_conductores, 'actualizar_idioma'):
            self.vista_conductores.actualizar_idioma(idioma)
        if hasattr(self.vista_rutas, 'actualizar_idioma'):
            self.vista_rutas.actualizar_idioma(idioma)
        if hasattr(self.vista_incidencias, 'actualizar_idioma'):
            self.vista_incidencias.actualizar_idioma(idioma)
        if hasattr(self.vista_asignaciones, 'actualizar_idioma'):
            self.vista_asignaciones.actualizar_idioma(idioma)
        
        
    def actualizar_fecha(self):
        mi_locale = QLocale(QLocale.Spanish, QLocale.Spain)
        fecha = QDate.currentDate()
        texto_fecha = mi_locale.toString(fecha, "dddd, d 'de' MMMM 'de' yyyy")
        self.lblDate.setText(texto_fecha.capitalize())
        
    def conectar_senales_vistas(self):
        """Conecta señales entre las diferentes vistas para sincronización"""
        
        # Rutas → Asignaciones
        self.vista_rutas.ruta_creada.connect(self.vista_asignaciones.agregar_ruta_a_combo)
        self.vista_rutas.ruta_actualizada.connect(self.vista_asignaciones.actualizar_ruta_en_combo)
        self.vista_rutas.ruta_eliminada.connect(self.vista_asignaciones.eliminar_ruta_de_combo)
        self.vista_rutas.ruta_estado_cambiada.connect(self._on_ruta_estado_cambiada)
        
        # Conductores → Asignaciones
        self.vista_conductores.conductor_creado.connect(self.vista_asignaciones.agregar_conductor_a_combo)
        self.vista_conductores.conductor_actualizado.connect(self.vista_asignaciones.actualizar_conductor_en_combo)
        self.vista_conductores.conductor_eliminado.connect(self.vista_asignaciones.eliminar_conductor_de_combo)
        self.vista_conductores.conductor_estado_cambiado.connect(self._on_conductor_estado_cambiado)
        
        # Vehículos → Asignaciones
        self.vista_vehiculos.vehiculo_creado.connect(self.vista_asignaciones.agregar_vehiculo_a_combo)
        self.vista_vehiculos.vehiculo_actualizado.connect(self.vista_asignaciones.actualizar_vehiculo_en_combo)
        self.vista_vehiculos.vehiculo_eliminado.connect(self.vista_asignaciones.eliminar_vehiculo_de_combo)
        self.vista_vehiculos.vehiculo_estado_cambiado.connect(self.vista_asignaciones.manejar_cambio_estado_vehiculo)
    
    def _on_ruta_estado_cambiada(self, id_ruta, nuevo_estado):
        print(f"[MainController] Ruta {id_ruta} → {nuevo_estado}")
    
    def _on_conductor_estado_cambiado(self, id_conductor, nuevo_estado):
        print(f"[MainController] Conductor {id_conductor} cambió a estado: {nuevo_estado}")
    
    def _on_vehiculo_estado_cambiado(self, id_vehiculo, nuevo_estado):
        print(f"[MainController] Vehículo {id_vehiculo} cambió a estado: {nuevo_estado}")

    def ir_a_mapa(self):
        self.stackContent.setCurrentIndex(self.idx_mapa)
        idioma = self.app_state.get("language", "Español")
        self.lblPageTitle.setText(LanguageService.get_text("command_center", idioma))

    def ir_a_vehiculos(self):
        self.stackContent.setCurrentIndex(self.idx_vehiculos)
        idioma = self.app_state.get("language", "Español")
        self.lblPageTitle.setText(LanguageService.get_text("vehicle_management", idioma))
        
    def ir_a_conductores(self):
        self.stackContent.setCurrentIndex(self.idx_conductores)
        idioma = self.app_state.get("language", "Español")
        self.lblPageTitle.setText(LanguageService.get_text("driver_management", idioma))
        
    def ir_a_rutas(self):
        self.stackContent.setCurrentIndex(self.idx_rutas)
        idioma = self.app_state.get("language", "Español")
        self.lblPageTitle.setText(LanguageService.get_text("route_creation", idioma))
        
    def ir_a_asignaciones(self):
        self.stackContent.setCurrentIndex(self.idx_asignaciones)
        idioma = self.app_state.get("language", "Español")
        self.lblPageTitle.setText(LanguageService.get_text("assignment_management", idioma))
        
    def ir_a_incidencias(self):
        self.stackContent.setCurrentIndex(self.idx_incidencias)
        idioma = self.app_state.get("language", "Español")
        self.lblPageTitle.setText(LanguageService.get_text("incident_management", idioma))
        
    def abrir_ajustes(self):
        dialog = SettingsController(self, self.app_state)
        
        if dialog.exec():
            nuevos = dialog.nuevos_datos
            self.app_state.update(nuevos)
            
            if self.settings_service:
                self.settings_service.save()
            
            if nuevos.get("empresa_coords"):
                self.vista_mapa.actualizar_ubicacion_empresa(nuevos["empresa_coords"])
            
            self.actualizar_textos()
                
    def closeEvent(self, event):
        # 1. Detener el listener del Mapa
        if hasattr(self, 'vista_mapa'):
            self.vista_mapa.detener_listener()

        # 2. Detener threads de Rutas (si hubiera alguno corriendo)
        if hasattr(self, 'vista_rutas'):
            if hasattr(self.vista_rutas, 'geocoding_thread') and self.vista_rutas.geocoding_thread:
                if self.vista_rutas.geocoding_thread.isRunning():
                    self.vista_rutas.geocoding_thread.terminate()
                    self.vista_rutas.geocoding_thread.wait()

        # 3. Aceptar el cierre
        event.accept()