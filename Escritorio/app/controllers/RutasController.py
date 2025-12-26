import folium
import io
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import QDate
from geopy.geocoders import Nominatim  # <--- IMPORTANTE: Necesitamos esto

from app.views.RutasWidget_ui import Ui_RutasWidget
from app.models.ruta import Ruta
from app.repositories.ruta_repository import RutaRepository
from app.repositories.conductor_repository import ConductorRepository
from app.repositories.vehiculo_repository import VehiculoRepository

class RutasController(QWidget, Ui_RutasWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.setupUi(self)
        
        # Repositorios
        self.repo_rutas = RutaRepository(db_connection)
        self.repo_conductores = ConductorRepository(db_connection)
        self.repo_vehiculos = VehiculoRepository(db_connection)
        
        # Herramientas
        self.geolocator = Nominatim(user_agent="fleetsmart_rutas")
        
        # Datos temporales de la ruta que estamos creando
        self.lista_paradas_data = [] # Aquí guardaremos: {'direccion': '...', 'coords': [x, y]}
        self.origen_coords = None

        # Configuración inicial
        self.deFecha.setDate(QDate.currentDate())
        self.cargar_combos()
        self.inicializar_mapa_vacio()
        
        # Conexiones
        self.btnGuardarRuta.clicked.connect(self.guardar_ruta_final)
        self.btnAgregarParada.clicked.connect(self.agregar_parada)
        
        # Si cambian el origen, intentamos buscarlo en el mapa también
        self.leOrigen.editingFinished.connect(self.actualizar_origen)

    def inicializar_mapa_vacio(self):
        self.actualizar_mapa_visual()

    def actualizar_origen(self):
        """Busca las coordenadas del origen cuando el usuario termina de escribir"""
        direccion = self.leOrigen.text().strip()
        if not direccion: return

        try:
            location = self.geolocator.geocode(direccion)
            if location:
                self.origen_coords = [location.latitude, location.longitude]
                self.actualizar_mapa_visual() # Redibujar mapa con el nuevo origen
        except:
            pass

    def agregar_parada(self):
        """Añade una dirección a la lista y al mapa"""
        direccion = self.leNuevaParada.text().strip()
        if not direccion: return

        try:
            # 1. Buscamos coordenadas
            location = self.geolocator.geocode(direccion)
            
            if location:
                coords = [location.latitude, location.longitude]
                
                # 2. Guardamos en memoria
                parada_info = {
                    "direccion": direccion,
                    "coords": coords,
                    "orden": len(self.lista_paradas_data) + 1
                }
                self.lista_paradas_data.append(parada_info)
                
                # 3. Añadimos a la lista visual (ListWidget)
                self.listParadas.addItem(f"{parada_info['orden']}. {direccion}")
                self.leNuevaParada.clear()
                
                # 4. Actualizamos el mapa
                self.actualizar_mapa_visual()
            else:
                QMessageBox.warning(self, "No encontrada", "No se encontró esa dirección en el mapa.")
                
        except Exception as e:
            print(f"Error geocoding: {e}")
            QMessageBox.warning(self, "Error", "Error de conexión al buscar dirección.")

    def actualizar_mapa_visual(self):
        """Dibuja todos los puntos (origen + paradas) y une con líneas"""
        
        # Centro por defecto (España) o el Origen si existe
        centro = self.origen_coords if self.origen_coords else [40.4168, -3.7038]
        m = folium.Map(location=centro, zoom_start=6 if not self.origen_coords else 13)

        puntos_ruta = []

        # 1. Pintar Origen (Marcador Verde)
        if self.origen_coords:
            folium.Marker(
                self.origen_coords, 
                popup="ORIGEN", 
                icon=folium.Icon(color="green", icon="play", prefix="fa")
            ).add_to(m)
            puntos_ruta.append(self.origen_coords)

        # 2. Pintar Paradas (Marcadores Rojos)
        for p in self.lista_paradas_data:
            coord = p['coords']
            texto = f"{p['orden']}. {p['direccion']}"
            
            folium.Marker(
                coord, 
                popup=texto, 
                icon=folium.Icon(color="red", icon="map-marker", prefix="fa")
            ).add_to(m)
            puntos_ruta.append(coord)

        # 3. Dibujar línea que une los puntos (Polilínea)
        if len(puntos_ruta) > 1:
            folium.PolyLine(
                puntos_ruta,
                color="blue",
                weight=3.5,
                opacity=1
            ).add_to(m)
            
            # Ajustar zoom para que se vea toda la ruta
            m.fit_bounds(puntos_ruta)

        # Renderizar
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webMapRuta.setHtml(data.getvalue().decode())

    def guardar_ruta_final(self):
        # Validaciones
        if not self.origen_coords:
            QMessageBox.warning(self, "Error", "El Origen no es válido o no se ha localizado.")
            return
        if not self.lista_paradas_data:
            QMessageBox.warning(self, "Error", "Debes añadir al menos una parada/destino.")
            return
            
        idx_cond = self.cbConductor.currentIndex()
        idx_veh = self.cbVehiculo.currentIndex()
        
        if idx_cond == -1 or idx_veh == -1: return

        # Crear objeto
        conductor = self.conductores_cargados[idx_cond]
        vehiculo = self.vehiculos_disponibles[idx_veh]

        nueva_ruta = Ruta(
            origen=self.leOrigen.text(),
            # Guardamos toda la lista de paradas
            paradas=self.lista_paradas_data, 
            id_conductor=conductor.id_conductor,
            nombre_conductor=conductor.nombre,
            id_vehiculo=vehiculo.id_vehiculo,
            matricula_vehiculo=vehiculo.matricula,
            fecha_creacion=self.deFecha.date().toString("dd/MM/yyyy"),
            estado="Pendiente"
        )
        
        if self.repo_rutas.guardar_ruta(nueva_ruta):
            QMessageBox.information(self, "Éxito", "Ruta multipunto creada correctamente.")
            # Limpiar todo
            self.leOrigen.clear()
            self.leNuevaParada.clear()
            self.listParadas.clear()
            self.lista_paradas_data = []
            self.origen_coords = None
            self.inicializar_mapa_vacio()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar en Firebase.")
    
    # ... (Mantén tu método cargar_combos igual que antes) ...
    def cargar_combos(self):
        """Descarga conductores y vehículos para llenar las listas"""
        print("🔄 Cargando datos para nueva ruta...")
        
        # A. Cargar Conductores
        self.cbConductor.clear()
        self.conductores_cargados = self.repo_conductores.obtener_todos()
        
        for c in self.conductores_cargados:
            # Mostramos Nombre y DNI en el desplegable
            self.cbConductor.addItem(f"{c.nombre} ({c.dni})")
            
        # B. Cargar Vehículos (Solo los Disponibles)
        
        self.cbVehiculo.clear()
        todos_vehiculos = self.repo_vehiculos.obtener_todos()
        
        # Filtramos en una lista aparte solo los que pueden viajar
        self.vehiculos_disponibles = [v for v in todos_vehiculos if v.estado == "Disponible"]
        
        for v in self.vehiculos_disponibles:
            self.cbVehiculo.addItem(f"{v.marca} {v.modelo} - {v.matricula}")