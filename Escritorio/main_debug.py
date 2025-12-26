import sys
from PySide6.QtWidgets import QApplication
from app.controllers.MainController import MainWindowController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. Creamos un "Usuario Falso" (Mock)
    # Así la ventana principal pensará que venimos del login
    app_state_falso = {
        "user": {
            "email": "admin@debug.com",
            "uid": "debug_12345"
        },
        "theme": "Oscuro",
        "language": "Español"
    }
    
    print("MODO DEBUG: Saltando Login...")

    # 2. Arrancamos directamente la ventana principal
    # Le pasamos el estado falso para que no de error
    ventana = MainWindowController(app_state_falso)
    ventana.show()
    
    sys.exit(app.exec())