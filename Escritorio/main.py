import sys
from PySide6.QtWidgets import QApplication
from app.controllers.AppController import AppController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setApplicationName("FleetSmart Escritorio")
    controller = AppController()
    
    sys.exit(app.exec())