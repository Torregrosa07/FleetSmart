from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog, QMessageBox
from app.views.SettingsDialog_ui import Ui_SettingsDialog 
from app.styles.style_manager import StyleManager
from geopy.geocoders import Nominatim

class SettingsController(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None, app_state=None):
        super().__init__(parent)
        self.setupUi(self)
        self.app_state = app_state
        self.nuevos_datos = None

        # Inicializar geolocalizador (necesita un user_agent único)
        self.geolocator = Nominatim(user_agent="fleetsmart_app")

        # Cargar valores actuales
        if self.app_state:
            self.cargar_datos_actuales()

        self.btnGuardar.clicked.connect(self.guardar_cambios)
        self.btnCancelar.clicked.connect(self.reject)

    def cargar_datos_actuales(self):
        # Seleccionar combos según estado
        tema = self.app_state.get("theme", "Claro")
        idx_tema = self.cbTema.findText(tema)
        if idx_tema >= 0: self.cbTema.setCurrentIndex(idx_tema)

        idioma = self.app_state.get("language", "Español")
        idx_idioma = self.cbIdioma.findText(idioma)
        if idx_idioma >= 0: self.cbIdioma.setCurrentIndex(idx_idioma)
        
        # Dirección actual (si existe)
        direccion = self.app_state.get("empresa_direccion", "")
        self.leDireccion.setText(direccion)

    def guardar_cambios(self):
        
        nuevo_tema = self.cbTema.currentText()
        app = QApplication.instance()
        StyleManager.aplicar_tema(app, nuevo_tema)
        
        direccion = self.leDireccion.text().strip()
        
        coords = None
        if direccion:
            try:
                # Intentamos geocodificar
                location = self.geolocator.geocode(direccion)
                if location:
                    coords = [location.latitude, location.longitude]
                else:
                    QMessageBox.warning(self, "Dirección no encontrada", "No pudimos localizar esa dirección en el mapa.")
                    return
            except Exception as e:
                print(f"Error geocoding: {e}")
                # En caso de error de red, podríamos dejar guardar sin coordenadas o avisar
        
        # Guardamos en un diccionario para devolverlo
        self.nuevos_datos = {
            "theme": nuevo_tema,
            "language": self.cbIdioma.currentText(),
            "empresa_direccion": direccion,
            "empresa_coords": coords # Guardamos las coordenadas calculadas
        }
        
        self.accept()