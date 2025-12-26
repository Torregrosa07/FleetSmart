from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QDate, QLocale
from app.views.MainWindow_ui import Ui_MainWindow
from app.controllers.CommandCenterController import CommandCenterController
from app.controllers.VehiclesController import VehiclesController
from app.controllers.ConductoresController import ConductoresController
from app.controllers.SettingsController import SettingsController
from app.controllers.RutasController import RutasController
import pyrebase
from app.config import FIREBASE_CONFIG

class MainWindowController(QMainWindow, Ui_MainWindow):
    def __init__(self, app_state):
        super().__init__()
        self.setupUi(self)
        self.app_state = app_state
        
        # 1. Inicializar conexión a BD (para pasarla a los hijos)
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.db = self.firebase.database()

        # 2. Inicializar Vistas Hijas
        self.vista_mapa = CommandCenterController()
        self.vista_vehiculos = VehiclesController(self.db)
        self.vista_conductores = ConductoresController(self.db)
        self.vista_rutas = RutasController(self.db)

        # 3. Añadirlas al Stacked Widget (el contenedor cambiante)
        # OJO: Guardamos el índice que nos devuelve addWidget para usarlo luego
        self.idx_mapa = self.stackContent.addWidget(self.vista_mapa)
        self.idx_vehiculos = self.stackContent.addWidget(self.vista_vehiculos)
        self.idx_conductores = self.stackContent.addWidget(self.vista_conductores)
        self.idx_rutas = self.stackContent.addWidget(self.vista_rutas)

        # 4. Conectar Botones del Menú Lateral
        self.btnCommandCenter.clicked.connect(self.ir_a_mapa)
        self.btnVehicles.clicked.connect(self.ir_a_vehiculos)
        self.btnDrivers.clicked.connect(self.ir_a_conductores)
        self.btnRoutes.clicked.connect(self.ir_a_rutas)
        self.btnSettings.clicked.connect(self.abrir_ajustes)
        
        self.actualizar_fecha()
        
        # Cargar página inicial
        self.ir_a_mapa()
        
        
    def actualizar_fecha(self):
        mi_locale = QLocale(QLocale.Spanish, QLocale.Spain)
        fecha = QDate.currentDate()
        texto_fecha = mi_locale.toString(fecha, "dddd, d 'de' MMMM 'de' yyyy")
        self.lblDate.setText(texto_fecha.capitalize())
        
    def abrir_ajustes(self):
        # Abrimos diálogo pasando el estado actual
        dialog = SettingsController(self, self.app_state)
        
        if dialog.exec():
            # Si guardó cambios, recuperamos los nuevos datos
            nuevos = dialog.nuevos_datos
            
            # 1. Actualizamos el estado global
            self.app_state.update(nuevos)
            print("Configuración actualizada:")
            
            # 2. Aplicamos cambios en el MAPA (si hay coordenadas nuevas)
            if nuevos.get("empresa_coords"):
                self.vista_mapa.actualizar_ubicacion_empresa(nuevos["empresa_coords"])
                
            # 3. Aquí aplicarías cambios de Tema/Idioma si quisieras implementarlos visualmente
            # self.aplicar_tema(nuevos["theme"])
        
        

    def ir_a_mapa(self):
        # Cambiar el stack a la vista del mapa
        self.stackContent.setCurrentIndex(self.idx_mapa)
        
        # Actualizar título y fecha (si quieres)
        self.lblPageTitle.setText("Centro de Mando")
        
        # Gestión visual de botones (Checkable=True en Designer ayuda)
        self.btnCommandCenter.setChecked(True)
        self.btnVehicles.setChecked(False)

    def ir_a_vehiculos(self):
        # Cambiar el stack a la vista de vehículos
        self.stackContent.setCurrentIndex(self.idx_vehiculos)
        
        self.lblPageTitle.setText("Gestión de Vehículos")
        
        self.btnCommandCenter.setChecked(False)
        self.btnVehicles.setChecked(True)
        
    def ir_a_conductores(self):
        # Cambiar el stack a la vista de vehículos
        self.stackContent.setCurrentIndex(self.idx_conductores)
        
        self.lblPageTitle.setText("Gestión de Conductores")
        
        self.btnCommandCenter.setChecked(False)
        self.btnDrivers.setChecked(True)
        
    def ir_a_rutas(self):
        self.stackContent.setCurrentIndex(self.idx_rutas)
        self.lblPageTitle.setText("Creación de Rutas")
        # Actualizar estado visual de los botones
        self.btnCommandCenter.setChecked(False)
        self.btnVehicles.setChecked(False)
        self.btnDrivers.setChecked(False)
        self.btnRoutes.setChecked(True)