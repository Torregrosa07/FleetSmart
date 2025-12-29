from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from app.views.LoginWindow_ui import Ui_Login
from app.services.auth_service import AuthService

class LoginController(QWidget, Ui_Login):
    # Señal que avisa al AppController: "¡Eh, ya tengo usuario!"
    login_success = Signal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.auth = AuthService()

        # CONEXIONES
        # Ahora sí conectamos tu botón
        self.btnLogin.clicked.connect(self.handle_login)
        self.lePass.returnPressed.connect(self.handle_login)

        # Limpiar mensajes
        self.lblMessage.setText("")

    def handle_login(self):
        email = self.leEmail.text().strip()
        password = self.lePass.text().strip()

        if not email or not password:
            self.lblMessage.setText("Faltan datos")
            self.lblMessage.setStyleSheet("color: orange;")
            return

        self.lblMessage.setText("Conectando...")
        self.lblMessage.setStyleSheet("color: blue;")
        self.btnLogin.setEnabled(False) # Evitar doble click

        try:
            # Llamamos al servicio
            user = self.auth.login(email, password)
            
            # Si no falla, emitimos la señal con los datos
            self.login_success.emit(user)
            
        except Exception as e:
            print(f"Login Error: {e}")
            self.lblMessage.setText("Credenciales incorrectas")
            self.lblMessage.setStyleSheet("color: red;")
            self.btnLogin.setEnabled(True)