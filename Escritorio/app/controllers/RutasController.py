import folium
import io
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import QThread, Signal, QDate, QTime
from geopy.geocoders import Nominatim 

from app.views.RutasWidget_ui import Ui_RutasWidget
from app.models.ruta import Ruta
from app.repositories.ruta_repository import RutaRepository


class GeocodingThread(QThread):
    """
    Thread para geocodificar direcciones sin bloquear la interfaz.
    Esto hace que la app no se congele mientras busca direcciones en internet.
    """
    # Señal que emite el resultado cuando termina
    finished = Signal(object, str)  # (ubicacion, tipo)
    
    
    def __init__(self, direccion, tipo):
        """
        Args:
            direccion: Texto a buscar (ej: "Madrid, Gran Vía")
            tipo: "origen" o "parada" (para saber qué hacer cuando termine)
        """
        super().__init__()
        self.direccion = direccion
        self.tipo = tipo
        self.geolocalizador = Nominatim(user_agent="tfg_fleetsmart_v1")
    
    def run(self):
        """Se ejecuta en segundo plano"""
        try:
            ubicacion = self.geolocalizador.geocode(self.direccion)
            self.finished.emit(ubicacion, self.tipo)
        except Exception as e:
            print(f"Error geocodificando: {e}")
            self.finished.emit(None, self.tipo)


class RutasController(QWidget, Ui_RutasWidget):
    """
    Controlador para crear plantillas de rutas.
    Las rutas se asignan a conductores/vehículos desde AsignacionController.
    """
    ruta_creada = Signal()  # Se emite cuando se guarda una ruta
    
    def __init__(self, db_connection, app_state):
        super().__init__()
        self.setupUi(self)
        
        # Estado global (para obtener id_gestor del usuario logueado)
        self.app_state = app_state
        
        # Repositorio
        self.repo_rutas = RutaRepository(db_connection)
        
        # Variables para el mapa
        self.coordenadas_origen = None 
        self.lista_destinos = []
        
        # Variables para geocodificación
        self.geocoding_thread = None
        self.texto_parada_temporal = ""  # Guardamos el texto mientras geocodifica
        
        # Configuración inicial
        self.configurar_fecha_hora()
        self.dibujar_mapa_vacio()
        
        # Conectar señales de los botones
        self.conectar_senales()

    def configurar_fecha_hora(self):
        """Configura los valores por defecto de fecha y hora"""
        # Fecha actual
        self.dtFecha.setDate(QDate.currentDate())
        
        # Horas por defecto (ya están en el .ui, pero por si acaso)
        self.teHoraInicio.setTime(QTime(8, 0))
        self.teHoraFin.setTime(QTime(17, 0))

    def conectar_senales(self):
        """Conecta todos los botones y eventos con sus métodos"""
        # Cuando el usuario termine de escribir el origen
        self.leOrigen.editingFinished.connect(self.buscar_origen)
        
        # Botones
        self.btnAgregarParada.clicked.connect(self.agregar_parada)
        self.btnEliminarParada.clicked.connect(self.borrar_parada)
        self.btnGuardarRuta.clicked.connect(self.guardar_ruta)

    # =========================================================================
    # MAPA
    # =========================================================================
    
    def dibujar_mapa_vacio(self):
        """Dibuja un mapa vacío centrado en España"""
        mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
        self.mostrar_mapa(mapa)

    def mostrar_mapa(self, mapa):
        """Renderiza el mapa en el QWebEngineView"""
        datos = io.BytesIO()
        mapa.save(datos, close_file=False)
        self.webMapRuta.setHtml(datos.getvalue().decode())

    def actualizar_mapa(self):
        """Actualiza el mapa con origen y paradas"""
        # Centro del mapa
        if self.coordenadas_origen:
            centro = self.coordenadas_origen
        else:
            centro = [40.4168, -3.7038]
        
        mapa = folium.Map(location=centro, zoom_start=12)
        puntos = []

        # Pintar origen
        if self.coordenadas_origen:
            folium.Marker(
                location=self.coordenadas_origen,
                popup="INICIO: " + self.leOrigen.text(),
                icon=folium.Icon(color="green", icon="play", prefix="fa")
            ).add_to(mapa)
            puntos.append(self.coordenadas_origen)

        # Pintar paradas
        for i, parada in enumerate(self.lista_destinos):
            # La última parada es el destino (icono diferente)
            es_ultima = (i == len(self.lista_destinos) - 1)
            
            folium.Marker(
                location=parada['coords'],
                popup=f"Parada {i+1}: {parada['direccion']}",
                icon=folium.Icon(
                    color="blue" if es_ultima else "red", 
                    icon="stop" if es_ultima else "flag", 
                    prefix="fa"
                )
            ).add_to(mapa)
            puntos.append(parada['coords'])

        # Línea conectando todos los puntos
        if len(puntos) > 1:
            folium.PolyLine(
                locations=puntos, 
                color="blue", 
                weight=4, 
                opacity=0.7
            ).add_to(mapa)
            mapa.fit_bounds(puntos)

        self.mostrar_mapa(mapa)

    # =========================================================================
    # GEOCODIFICACIÓN
    # =========================================================================
    
    def buscar_origen(self):
        """Geocodifica el origen en segundo plano"""
        texto = self.leOrigen.text().strip()
        if not texto:
            return
        
        # Lanzar thread
        self.geocoding_thread = GeocodingThread(texto, "origen")
        self.geocoding_thread.finished.connect(self.cuando_termine_geocoding)
        self.geocoding_thread.start()

    def agregar_parada(self):
        """Geocodifica y añade una parada en segundo plano"""
        texto = self.leNuevaParada.text().strip()
        if not texto:
            return
        
        # Guardar el texto temporalmente
        self.texto_parada_temporal = texto
        
        # Lanzar thread
        self.geocoding_thread = GeocodingThread(texto, "parada")
        self.geocoding_thread.finished.connect(self.cuando_termine_geocoding)
        self.geocoding_thread.start()

    def cuando_termine_geocoding(self, ubicacion, tipo):
        """
        Callback que se ejecuta cuando termina la geocodificación.
        
        Args:
            ubicacion: Resultado de geocode() o None si no encontró
            tipo: "origen" o "parada"
        """
        if not ubicacion:
            QMessageBox.warning(self, "Error", "No se encontró la dirección.")
            return
        
        if tipo == "origen":
            self.coordenadas_origen = [ubicacion.latitude, ubicacion.longitude]
            self.actualizar_mapa()
            
        elif tipo == "parada":
            # Crear parada
            parada = {
                "direccion": self.texto_parada_temporal,
                "coords": [ubicacion.latitude, ubicacion.longitude],
                "orden": len(self.lista_destinos) + 1
            }
            
            # Añadir a la lista
            self.lista_destinos.append(parada)
            
            # Mostrar en QListWidget
            self.listParadas.addItem(f"{parada['orden']}. {parada['direccion']}")
            
            # Actualizar campo de destino (última parada)
            self.leDestino.setText(self.texto_parada_temporal)
            
            # Limpiar campo de nueva parada
            self.leNuevaParada.clear()
            self.texto_parada_temporal = ""
            
            # Actualizar mapa
            self.actualizar_mapa()

    def borrar_parada(self):
        """Borra la parada seleccionada"""
        fila = self.listParadas.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una parada.")
            return

        # Borrar de la lista de datos
        del self.lista_destinos[fila]
        
        # Actualizar orden
        for i, parada in enumerate(self.lista_destinos):
            parada['orden'] = i + 1
        
        # Reconstruir lista visual
        self.listParadas.clear()
        for parada in self.lista_destinos:
            self.listParadas.addItem(f"{parada['orden']}. {parada['direccion']}")
        
        # Actualizar destino
        if self.lista_destinos:
            self.leDestino.setText(self.lista_destinos[-1]['direccion'])
        else:
            self.leDestino.clear()
        
        # Actualizar mapa
        self.actualizar_mapa()

    # =========================================================================
    # GUARDAR RUTA
    # =========================================================================
    
    def guardar_ruta(self):
        """Guarda la plantilla de ruta en Firebase"""
        
        # Validar nombre
        nombre = self.leNombreRuta.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "La ruta necesita un nombre.")
            return

        # Validar origen
        if not self.coordenadas_origen:
            QMessageBox.warning(self, "Error", "Define un punto de origen.")
            return
        
        # Validar paradas
        if not self.lista_destinos:
            QMessageBox.warning(self, "Error", "Añade al menos una parada.")
            return

        # Obtener datos del usuario logueado
        id_gestor = self.app_state["user"]["uid"]
        
        # Obtener datos del formulario
        origen = self.leOrigen.text()
        destino = self.lista_destinos[-1]['direccion']  # Última parada
        fecha = self.dtFecha.date().toString("dd/MM/yyyy")
        hora_inicio = self.teHoraInicio.time().toString("HH:mm")
        hora_fin = self.teHoraFin.time().toString("HH:mm")

        # Crear objeto Ruta
        nueva_ruta = Ruta(
            nombre=nombre,
            origen=origen,
            destino=destino,
            fecha=fecha,
            hora_inicio_prevista=hora_inicio,
            hora_fin_prevista=hora_fin,
            id_gestor=id_gestor,
            estado="Pendiente",
            paradas=self.lista_destinos
        )
        
        # Guardar en Firebase
        if self.repo_rutas.guardar_ruta(nueva_ruta):
            QMessageBox.information(
                self, 
                "Guardado", 
                f"Ruta '{nombre}' creada correctamente.\n\n"
                f"Origen: {origen}\n"
                f"Destino: {destino}\n"
                f"Fecha: {fecha}\n"
                f"Paradas: {len(self.lista_destinos)}"
            )
            self.limpiar_formulario()
            self.ruta_creada.emit()
        else:
            QMessageBox.critical(self, "Error", "Error al guardar la ruta.")

    def limpiar_formulario(self):
        """Limpia todos los campos"""
        self.leNombreRuta.clear()
        self.leOrigen.clear()
        self.leNuevaParada.clear()
        self.leDestino.clear()
        self.listParadas.clear()
        self.coordenadas_origen = None
        self.lista_destinos = []
        self.dtFecha.setDate(QDate.currentDate())
        self.teHoraInicio.setTime(QTime(8, 0))
        self.teHoraFin.setTime(QTime(17, 0))
        self.dibujar_mapa_vacio()