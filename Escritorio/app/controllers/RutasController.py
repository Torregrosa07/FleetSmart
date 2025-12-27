import folium
import io
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import QDate
# Importamos la librería para buscar coordenadas (Geocoding)
from geopy.geocoders import Nominatim 

from app.views.RutasWidget_ui import Ui_RutasWidget
from app.models.ruta import Ruta
from app.repositories.ruta_repository import RutaRepository
from app.repositories.conductor_repository import ConductorRepository
from app.repositories.vehiculo_repository import VehiculoRepository

class RutasController(QWidget, Ui_RutasWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.setupUi(self)
        
        # --- 1. INICIALIZAR LA CONEXIÓN DE DATOS ---
        self.repo_rutas = RutaRepository(db_connection)
        self.repo_conductores = ConductorRepository(db_connection)
        self.repo_vehiculos = VehiculoRepository(db_connection)
        
        # Herramienta para convertir direcciones en coordenadas (GPS)
        # "user_agent" es necesario para identificarse ante el servicio de mapas
        self.geolocalizador = Nominatim(user_agent="tfg_flotas_app")
        
        # --- 2. VARIABLES DE MEMORIA ---
        # Aquí guardaremos temporalmente los datos antes de dar a "Guardar"
        self.coordenadas_origen = None  # Guardará [latitud, longitud] del origen
        self.lista_destinos = []        # Lista de diccionarios: [{'direccion': '...', 'coords': [...]}]
        
        # --- 3. CONFIGURACIÓN INICIAL ---
        self.deFecha.setDate(QDate.currentDate()) # Poner fecha de hoy
        self.cargar_conductores_y_vehiculos()     # Rellenar los desplegables
        self.dibujar_mapa_vacio()                 # Mostrar mapa inicial
        
        # --- 4. CONECTAR LOS BOTONES ---
        # Cuando el usuario termina de escribir el Origen (al pulsar Enter o cambiar de casilla)
        self.leOrigen.editingFinished.connect(self.buscar_origen)
        
        # Botón "+" para añadir una parada a la lista
        self.btnAgregarParada.clicked.connect(self.agregar_nueva_parada)
        
        # Botón final "Guardar Ruta"
        self.btnGuardarRuta.clicked.connect(self.guardar_ruta_en_base_datos)

    # =========================================================================
    # LÓGICA DEL MAPA
    # =========================================================================

    def dibujar_mapa_vacio(self):
        """Muestra un mapa de España por defecto al iniciar"""
        mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
        self.mostrar_mapa_en_pantalla(mapa)

    def mostrar_mapa_en_pantalla(self, mapa_creado):
        """Función auxiliar que coge el mapa de Folium y lo pinta en la ventana"""
        datos = io.BytesIO()
        mapa_creado.save(datos, close_file=False)
        self.webMapRuta.setHtml(datos.getvalue().decode())

    def actualizar_mapa_con_ruta(self):
        """
        Esta función es el 'cerebro' visual. 
        Borra el mapa anterior y dibuja uno nuevo con:
        1. El punto de Origen (Verde)
        2. Los puntos de Destino (Rojos)
        3. Una línea azul que los une todos
        """
        # Si no tenemos origen, usamos el centro de España por defecto
        centro = self.coordenadas_origen if self.coordenadas_origen else [40.4168, -3.7038]
        mapa = folium.Map(location=centro, zoom_start=12)
        
        # Lista para guardar todos los puntos y poder dibujar la línea luego
        puntos_para_linea = []

        # 1. DIBUJAR ORIGEN (Si existe)
        if self.coordenadas_origen:
            folium.Marker(
                location=self.coordenadas_origen,
                popup="ORIGEN: " + self.leOrigen.text(),
                icon=folium.Icon(color="green", icon="play", prefix="fa")
            ).add_to(mapa)
            puntos_para_linea.append(self.coordenadas_origen)

        # 2. DIBUJAR PARADAS/DESTINOS
        for i, parada in enumerate(self.lista_destinos):
            coord = parada['coords']
            direccion = parada['direccion']
            
            folium.Marker(
                location=coord,
                popup=f"Parada {i+1}: {direccion}",
                icon=folium.Icon(color="red", icon="stop", prefix="fa")
            ).add_to(mapa)
            puntos_para_linea.append(coord)

        # 3. DIBUJAR LÍNEA AZUL (Si hay al menos 2 puntos)
        if len(puntos_para_linea) > 1:
            folium.PolyLine(
                locations=puntos_para_linea,
                color="blue",
                weight=4,
                opacity=0.7
            ).add_to(mapa)
            
            # Ajustar el zoom para que se vea toda la ruta
            mapa.fit_bounds(puntos_para_linea)

        self.mostrar_mapa_en_pantalla(mapa)

    # =========================================================================
    # LÓGICA DE DIRECCIONES (GEOCODING)
    # =========================================================================

    def buscar_origen(self):
        """Se activa automáticamente al escribir en 'Origen'"""
        texto_origen = self.leOrigen.text().strip()
        
        if not texto_origen:
            return # Si está vacío, no hacemos nada

        try:
            ubicacion = self.geolocalizador.geocode(texto_origen)
            if ubicacion:
                # Guardamos las coordenadas
                self.coordenadas_origen = [ubicacion.latitude, ubicacion.longitude]
                # Actualizamos el mapa para mostrar el marcador verde
                self.actualizar_mapa_con_ruta()
        except Exception:
            # Si falla internet o algo, no molestamos al usuario con popups constantes
            print("No se pudo localizar el origen automáticamente")

    def agregar_nueva_parada(self):
        """Se activa al pulsar el botón '+'"""
        texto_parada = self.leNuevaParada.text().strip()
        
        if not texto_parada:
            QMessageBox.warning(self, "Aviso", "Escribe una dirección para la parada.")
            return

        try:
            # Buscamos coordenadas
            ubicacion = self.geolocalizador.geocode(texto_parada)
            
            if ubicacion:
                # 1. Guardar en nuestra lista interna
                datos_parada = {
                    "direccion": texto_parada,
                    "coords": [ubicacion.latitude, ubicacion.longitude],
                    "orden": len(self.lista_destinos) + 1
                }
                self.lista_destinos.append(datos_parada)
                
                # 2. Mostrar en la lista visual (la caja blanca de la izquierda)
                self.listParadas.addItem(f"{datos_parada['orden']}. {texto_parada}")
                
                # 3. Limpiar la caja de texto para escribir otra
                self.leNuevaParada.clear()
                
                # 4. Actualizar mapa (pintar el nuevo punto rojo y la línea)
                self.actualizar_mapa_con_ruta()
            else:
                QMessageBox.warning(self, "No encontrada", "No se encuentra esa dirección en el mapa.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {e}")

    # =========================================================================
    # LÓGICA DE DATOS
    # =========================================================================

    def cargar_conductores_y_vehiculos(self):
        """Descarga datos de Firebase y rellena los ComboBox"""
        self.cbConductor.clear()
        self.cbVehiculo.clear()
        
        # 1. Conductores
        self.conductores_cargados = self.repo_conductores.obtener_todos()
        for c in self.conductores_cargados:
            self.cbConductor.addItem(f"{c.nombre} ({c.dni})")
            
        # 2. Vehículos (Solo los Disponibles)
        todos_coches = self.repo_vehiculos.obtener_todos()
        self.vehiculos_disponibles = []
        
        for v in todos_coches:
            if v.estado == "Disponible":
                self.vehiculos_disponibles.append(v)
                self.cbVehiculo.addItem(f"{v.marca} {v.modelo} - {v.matricula}")

    def guardar_ruta_en_base_datos(self):
        """Recoge todo y lo envía a Firebase"""
        
        # VALIDACIONES
        if not self.coordenadas_origen:
            QMessageBox.warning(self, "Falta Origen", "Escribe una dirección de Origen válida.")
            return
            
        if len(self.lista_destinos) == 0:
            QMessageBox.warning(self, "Falta Destino", "Añade al menos una parada o destino con el botón '+'.")
            return
            
        idx_conductor = self.cbConductor.currentIndex()
        idx_vehiculo = self.cbVehiculo.currentIndex()
        
        if idx_conductor == -1 or idx_vehiculo == -1:
            QMessageBox.warning(self, "Error", "Selecciona un conductor y un vehículo.")
            return

        # RECUPERAR OBJETOS REALES
        conductor = self.conductores_cargados[idx_conductor]
        vehiculo = self.vehiculos_disponibles[idx_vehiculo]

        # CREAR OBJETO RUTA
        # Nota: Usamos 'origen' como texto y 'paradas' como la lista completa
        nueva_ruta = Ruta(
            origen=self.leOrigen.text(),
            paradas=self.lista_destinos, 
            id_conductor=conductor.id_conductor,
            nombre_conductor=conductor.nombre,
            id_vehiculo=vehiculo.id_vehiculo,
            matricula_vehiculo=vehiculo.matricula,
            fecha_creacion=self.deFecha.date().toString("dd/MM/yyyy"),
            estado="Pendiente"
        )
        
        # GUARDAR
        if self.repo_rutas.guardar_ruta(nueva_ruta):
            QMessageBox.information(self, "Éxito", "Ruta creada y asignada correctamente.")
            
            # Limpiar formulario para la siguiente
            self.leOrigen.clear()
            self.leNuevaParada.clear()
            self.listParadas.clear()
            self.lista_destinos = [] # Vaciar memoria
            self.coordenadas_origen = None
            self.dibujar_mapa_vacio()
            
            # Opcional: Actualizar estado del vehículo a "Ocupado"
            # vehiculo.estado = "En Ruta"
            # self.repo_vehiculos.actualizar_vehiculo(vehiculo)
            # self.cargar_conductores_y_vehiculos() # Recargar listas
            
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar en la base de datos.")