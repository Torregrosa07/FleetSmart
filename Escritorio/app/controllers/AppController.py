from PySide6.QtWidgets import QApplication
from app.controllers.LoginController import LoginController
from app.controllers.MainController import MainWindowController
from app.styles.style_manager import StyleManager

class AppController:
    def __init__(self):
        # 1. DEFINIR APPSTATE
        self.app_state = {
            "user": None,
            "theme": "Oscuro",
            "language": "Español"
        }
        
        app = QApplication.instance()
        StyleManager.aplicar_tema(app, self.app_state["theme"])

        # 2. INICIAR LOGIN
        self.login_window = LoginController()
        
        # 3. ESCUCHAR SEÑAL
        # Cuando el login diga "success", ejecutamos self.abrir_menu_principal
        self.login_window.login_success.connect(self.abrir_menu_principal)
        
        # 4. MOSTRAR LOGIN
        self.login_window.show()

        # Placeholder para la ventana principal
        self.main_window = None

    def abrir_menu_principal(self, user_data):
        print("Cambiando a Ventana Principal...")
        
        # Guardar usuario en el estado global
        self.app_state["user"] = user_data
        
        # Cerrar Login
        self.login_window.close()
        
        # Abrir Main Window
        self.main_window = MainWindowController(self.app_state)
        self.main_window.show()