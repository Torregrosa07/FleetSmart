from PySide6.QtWidgets import QApplication, QMessageBox
from app.controllers.LoginController import LoginController
from app.controllers.MainController import MainWindowController
from app.styles.style_manager import StyleManager
# IMPORTAR EL SERVICIO
from app.services.settings_service import SettingsService

class AppController:
    def __init__(self):
        # 1. INICIALIZAR SERVICIO DE AJUSTES
        self.settings_service = SettingsService()
        
        # Usamos el diccionario del servicio como estado global
        self.app_state = self.settings_service.app_state
        
        # Aplicar el tema cargado inmediatamente
        app = QApplication.instance()
        StyleManager.aplicar_tema(app, self.app_state.get("theme", "Oscuro"))

        # 2. INICIALIZAR LOGIN
        self.login_window = LoginController()
        self.login_window.login_success.connect(self.abrir_menu_principal)
        self.login_window.show()

        self.main_window = None

    def abrir_menu_principal(self, user_data):
        
        if user_data['rol'] != 'gestor':
            QMessageBox.warning(
                self.login_window,
                "Acceso Denegado",
                "Esta aplicación es solo para gestores de flota.\n"
                "Los conductores deben usar la aplicación móvil."
            )
            return
        
        # Guardar usuario en el estado global (memoria)
        self.app_state["user"] = user_data
        
        self.login_window.close()
        
        # Abrir Main Window pasando TAMBIÉN el servicio de ajustes para poder guardar
        self.main_window = MainWindowController(self.app_state, self.settings_service)
        self.main_window.show()