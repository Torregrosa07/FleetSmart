import sys
from PySide6.QtWidgets import QApplication
from app.controllers.AppController import AppController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Arrancamos el controlador principal
    controller = AppController()
    
    sys.exit(app.exec())