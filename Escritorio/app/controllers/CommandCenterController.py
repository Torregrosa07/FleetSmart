import folium
import io
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, QObject
from app.views.CommandCenterPage_ui import Ui_CommandCenterPage
from app.repositories.localizacionGPS_repository import LocalizacionGPSRepository


class FirebaseListenerBridge(QObject):
    ubicacion_actualizada = Signal()


class CommandCenterController(QWidget, Ui_CommandCenterPage):
    
    def __init__(self,coords_iniciales = None):
        super().__init__()
        self.setupUi(self)
        
        self.repo = LocalizacionGPSRepository()
        
        # Coordenadas por defecto (Madrid)
        if coords_iniciales:
            self.empresa_coords = coords_iniciales
        else:
            self.empresa_coords = [40.4168, -3.7038] # Madrid por defecto
        
        self.es_primera_carga = True 
        
        self.listener_activo = None
        self.bridge = FirebaseListenerBridge()
        self.bridge.ubicacion_actualizada.connect(self.actualizar_mapa)
        
        if hasattr(self, 'btnActualizar'):
            self.btnActualizar.clicked.connect(self.actualizar_mapa)
        
        # Inicializar
        self.actualizar_mapa()  
        self.iniciar_listener()

    def actualizar_ubicacion_empresa(self, nuevas_coords):
        """
        Recibe [lat, lon] desde SettingsController y actualiza el mapa.
        Al cambiar la sede, permitimos que se re-ajuste el zoom una vez.
        """
        if nuevas_coords:
            print(f"Nueva ubicación de empresa recibida: {nuevas_coords}")
            self.empresa_coords = nuevas_coords
            self.es_primera_carga = True # Permitimos re-centrar una vez
            self.actualizar_mapa()

    def iniciar_listener(self):
        try:
            def on_cambio(event):
                self.bridge.ubicacion_actualizada.emit()
            
            self.listener_activo = self.repo.crear_listener(on_cambio)
            print("Listener GPS iniciado")
        except Exception as e:
            print(f"Error iniciando listener: {e}")
    
    def detener_listener(self):
        if self.listener_activo:
            try:
                self.listener_activo.close()
                print("Listener GPS detenido")
            except Exception as e:
                print(f"Error deteniendo listener: {e}")
            finally:
                self.listener_activo = None
    
    def mostrar_mapa(self, mapa):
        datos = io.BytesIO()
        mapa.save(datos, close_file=False)
        if hasattr(self, 'webMap'):
            self.webMap.setHtml(datos.getvalue().decode())

    def actualizar_mapa(self):
        """
        Dibuja el mapa.
        SOLUCIÓN ZOOM: 'fit_bounds' solo se ejecuta si self.es_primera_carga es True.
        """
        # 1. Obtener conductores
        ubicaciones = self.repo.obtener_ubicaciones_activas()
        
        # 2. Configurar Mapa Base
        # Usamos siempre la empresa como centro estable para actualizaciones suaves
        mapa = folium.Map(location=self.empresa_coords, zoom_start=6)
        
        # 3. DIBUJAR EMPRESA
        folium.Marker(
            location=self.empresa_coords,
            popup="<b>Centro de Operaciones</b><br>FleetSmart HQ",
            icon=folium.Icon(color="blue", icon="building", prefix="fa")
        ).add_to(mapa)

        # 4. DIBUJAR CONDUCTORES
        coordenadas_para_ajuste = [self.empresa_coords]
        
        for ubicacion in ubicaciones:
            coords = [ubicacion.latitud, ubicacion.longitud]
            coordenadas_para_ajuste.append(coords)
            
            popup_text = (
                f"<b>Vehículo:</b> {ubicacion.matricula_vehiculo}<br>"
                f"<b>Conductor:</b> {ubicacion.nombre_conductor}<br>"
                f"<b>Ruta:</b> {ubicacion.nombre_ruta}<br>"
                f"<small>{ubicacion.timestamp}</small>"
            )
            
            folium.Marker(
                location=coords,
                popup=popup_text,
                tooltip=ubicacion.matricula_vehiculo,
                icon=folium.Icon(color="green", icon="truck", prefix="fa")
            ).add_to(mapa)
        
        # 5. AJUSTE DE ZOOM INTELIGENTE
        # Solo ajustamos el encuadre automáticamente la primera vez.
        # Las siguientes veces, mantenemos el zoom por defecto del mapa base
        # para no interrumpir al usuario si está haciendo zoom manual.
        if self.es_primera_carga and len(coordenadas_para_ajuste) > 1:
            mapa.fit_bounds(coordenadas_para_ajuste)
            self.es_primera_carga = False # Desactivar para futuras actualizaciones
        
        self.mostrar_mapa(mapa)
    
    def closeEvent(self, event):
        self.detener_listener()
        event.accept()