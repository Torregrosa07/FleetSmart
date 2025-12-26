import io
import folium
from PySide6.QtWidgets import QWidget
# No necesitamos importar QWebEngineView ni QVBoxLayout porque ya están en tu UI
from app.views.CommandCenterPage_ui import Ui_CommandCenterPage

class CommandCenterController(QWidget, Ui_CommandCenterPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Inicializamos el mapa
        self.inicializar_mapa()

    def inicializar_mapa(self, coordenadas_centro=[40.4168, -3.7038]):
  
        m = folium.Map(location=coordenadas_centro, zoom_start=12)
        
        # Añadir marcador
        folium.Marker(
            coordenadas_centro, 
            popup="Sede Central", 
            icon=folium.Icon(color="red", icon="building", prefix="fa")
        ).add_to(m)
        
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webMap.setHtml(data.getvalue().decode())
        
    def actualizar_ubicacion_empresa(self, nuevas_coords):
        """Método público para mover el mapa"""
        if nuevas_coords:
            self.inicializar_mapa(nuevas_coords)