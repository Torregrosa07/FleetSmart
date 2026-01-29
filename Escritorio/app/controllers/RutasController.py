import folium
import io
from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QHeaderView, QAbstractItemView
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
    finished = Signal(object, str)  # (ubicacion, tipo)
    
    def __init__(self, direccion, tipo):
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
    Controlador para gestionar plantillas de rutas (CRUD completo).
    Las rutas se asignan a conductores/vehículos desde AsignacionController.
    """
    # ========== SEÑALES ==========
    ruta_creada = Signal(object)          # ruta completa
    ruta_actualizada = Signal(str)        # id_ruta
    ruta_eliminada = Signal(str)          # id_ruta
    ruta_estado_cambiada = Signal(str, str)  # id_ruta, nuevo_estado
    
    def __init__(self, db_connection, app_state):
        super().__init__()
        self.setupUi(self)
        
        # Estado global
        self.app_state = app_state
        
        # Repositorio
        self.repo_rutas = RutaRepository(db_connection)
        
        # Lista y caché de rutas
        self.lista_rutas_actual = []
        self.cache_rutas = {}
        
        # Variables para el mapa
        self.coordenadas_origen = None 
        self.lista_destinos = []
        
        # Variables para geocodificación
        self.geocoding_thread = None
        self.texto_parada_temporal = ""
        
        # Control de modo edición
        self.modo_edicion = False
        self.ruta_en_edicion = None
        
        # Configuración inicial
        self.configurar_fecha_hora()
        self.configurar_tabla()
        self.cargar_tabla_rutas()
        self.dibujar_mapa_vacio()
        
        # Conectar señales
        self.conectar_senales()
    
    def configurar_tabla(self):
        """Configura el estilo de la tabla de rutas"""
        if hasattr(self, 'tablaRutas'):
            # AGREGAR: Configurar columnas
            self.tablaRutas.setColumnCount(6)
            self.tablaRutas.setHorizontalHeaderLabels([
                "Nombre", "Origen", "Destino", "Fecha", "Estado", "Nº Paradas"
            ])
            
            # Configurar estilo
            self.tablaRutas.horizontalHeader().setStretchLastSection(False)
            self.tablaRutas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tablaRutas.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tablaRutas.setSelectionBehavior(QAbstractItemView.SelectRows)
    
    def cargar_tabla_rutas(self):
        """Carga todas las rutas en la tabla"""
        if not hasattr(self, 'tablaRutas'):
            # Si no hay tabla en el UI, simplemente no hacer nada
            return
            
        self.lista_rutas_actual = self.repo_rutas.obtener_todas()
        self.cache_rutas = {r.id_ruta: r for r in self.lista_rutas_actual}
        
        self.tablaRutas.setRowCount(0)
        
        for i, ruta in enumerate(self.lista_rutas_actual):
            self.tablaRutas.insertRow(i)
            self._llenar_fila_tabla(i, ruta)
    
    def _llenar_fila_tabla(self, fila, ruta):
        """Método auxiliar para llenar una fila de la tabla"""
        if not hasattr(self, 'tablaRutas'):
            return
            
        self.tablaRutas.setItem(fila, 0, QTableWidgetItem(ruta.nombre))
        self.tablaRutas.setItem(fila, 1, QTableWidgetItem(ruta.origen))
        self.tablaRutas.setItem(fila, 2, QTableWidgetItem(ruta.destino))
        self.tablaRutas.setItem(fila, 3, QTableWidgetItem(ruta.fecha))
        self.tablaRutas.setItem(fila, 4, QTableWidgetItem(ruta.estado))
        self.tablaRutas.setItem(fila, 5, QTableWidgetItem(str(len(ruta.paradas))))

    def configurar_fecha_hora(self):
        """Configura los valores por defecto de fecha y hora"""
        self.dtFecha.setDate(QDate.currentDate())
        self.teHoraInicio.setTime(QTime(8, 0))
        self.teHoraFin.setTime(QTime(17, 0))

    def conectar_senales(self):
        """Conecta todos los botones y eventos con sus métodos"""
        # Geocodificación
        self.leOrigen.editingFinished.connect(self.buscar_origen)
        
        # Botones de formulario
        self.btnAgregarParada.clicked.connect(self.agregar_parada)
        self.btnEliminarParada.clicked.connect(self.borrar_parada)
        self.btnGuardarRuta.clicked.connect(self.guardar_o_actualizar_ruta)
        
        # Nuevos botones para gestión de rutas
        if hasattr(self, 'btnEditarRuta'):
            self.btnEditarRuta.clicked.connect(self.editar_ruta_seleccionada)
        if hasattr(self, 'btnEliminarRuta'):
            self.btnEliminarRuta.clicked.connect(self.eliminar_ruta_seleccionada)
        if hasattr(self, 'btnNuevaRuta'):
            self.btnNuevaRuta.clicked.connect(self.modo_crear_nueva)
        if hasattr(self, 'btnCancelar'):
            self.btnCancelar.clicked.connect(self.cancelar_edicion)

    # =========================================================================
    # GESTIÓN DE MODOS (CREAR vs EDITAR)
    # =========================================================================
    
    def modo_crear_nueva(self):
        """Cambia al modo de creación de nueva ruta"""
        self.modo_edicion = False
        self.ruta_en_edicion = None
        self.limpiar_formulario()
        self.btnGuardarRuta.setText("Guardar Ruta")
        if hasattr(self, 'btnCancelar'):
            self.btnCancelar.setVisible(False)
    
    def modo_editar(self, ruta):
        """Cambia al modo de edición de ruta existente"""
        self.modo_edicion = True
        self.ruta_en_edicion = ruta
        self.cargar_ruta_en_formulario(ruta)
        self.btnGuardarRuta.setText("Actualizar Ruta")
        if hasattr(self, 'btnCancelar'):
            self.btnCancelar.setVisible(True)
    
    def cancelar_edicion(self):
        """Cancela la edición y vuelve al modo creación"""
        self.modo_crear_nueva()
    
    def cargar_ruta_en_formulario(self, ruta):
        """Carga los datos de una ruta en el formulario para editar"""
        # Cargar datos básicos
        self.leNombreRuta.setText(ruta.nombre)
        self.leOrigen.setText(ruta.origen)
        self.leDestino.setText(ruta.destino)
        
        # Cargar fecha y horas
        fecha_partes = ruta.fecha.split("/")
        if len(fecha_partes) == 3:
            self.dtFecha.setDate(QDate(int(fecha_partes[2]), int(fecha_partes[1]), int(fecha_partes[0])))
        
        hora_inicio_partes = ruta.hora_inicio_prevista.split(":")
        if len(hora_inicio_partes) == 2:
            self.teHoraInicio.setTime(QTime(int(hora_inicio_partes[0]), int(hora_inicio_partes[1])))
        
        hora_fin_partes = ruta.hora_fin_prevista.split(":")
        if len(hora_fin_partes) == 2:
            self.teHoraFin.setTime(QTime(int(hora_fin_partes[0]), int(hora_fin_partes[1])))
        
        # Cargar paradas
        self.lista_destinos = ruta.paradas if ruta.paradas else []
        self.listParadas.clear()
        for parada in self.lista_destinos:
            self.listParadas.addItem(f"{parada['orden']}. {parada['direccion']}")
        
        # Intentar geocodificar el origen para mostrar en el mapa
        if ruta.origen:
            self.buscar_origen()

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
        
        self.geocoding_thread = GeocodingThread(texto, "origen")
        self.geocoding_thread.finished.connect(self.cuando_termine_geocoding)
        self.geocoding_thread.start()

    def agregar_parada(self):
        """Geocodifica y añade una parada en segundo plano"""
        texto = self.leNuevaParada.text().strip()
        if not texto:
            return
        
        self.texto_parada_temporal = texto
        
        self.geocoding_thread = GeocodingThread(texto, "parada")
        self.geocoding_thread.finished.connect(self.cuando_termine_geocoding)
        self.geocoding_thread.start()

    def cuando_termine_geocoding(self, ubicacion, tipo):
        """Callback que se ejecuta cuando termina la geocodificación"""
        if not ubicacion:
            QMessageBox.warning(self, "Error", "No se encontró la dirección.")
            return
        
        if tipo == "origen":
            self.coordenadas_origen = [ubicacion.latitude, ubicacion.longitude]
            self.actualizar_mapa()
            
        elif tipo == "parada":
            parada = {
                "direccion": self.texto_parada_temporal,
                "coords": [ubicacion.latitude, ubicacion.longitude],
                "orden": len(self.lista_destinos) + 1
            }
            
            self.lista_destinos.append(parada)
            self.listParadas.addItem(f"{parada['orden']}. {parada['direccion']}")
            self.leDestino.setText(self.texto_parada_temporal)
            self.leNuevaParada.clear()
            self.texto_parada_temporal = ""
            self.actualizar_mapa()

    def borrar_parada(self):
        """Borra la parada seleccionada"""
        fila = self.listParadas.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una parada.")
            return

        del self.lista_destinos[fila]
        
        for i, parada in enumerate(self.lista_destinos):
            parada['orden'] = i + 1
        
        self.listParadas.clear()
        for parada in self.lista_destinos:
            self.listParadas.addItem(f"{parada['orden']}. {parada['direccion']}")
        
        if self.lista_destinos:
            self.leDestino.setText(self.lista_destinos[-1]['direccion'])
        else:
            self.leDestino.clear()
        
        self.actualizar_mapa()

    # =========================================================================
    # GUARDAR / ACTUALIZAR RUTA
    # =========================================================================
    
    def guardar_o_actualizar_ruta(self):
        """Guarda una nueva ruta o actualiza una existente según el modo"""
        if self.modo_edicion:
            self.actualizar_ruta()
        else:
            self.guardar_ruta_nueva()
    
    def guardar_ruta_nueva(self):
        """Guarda una nueva plantilla de ruta en Firebase"""
        
        # Validaciones
        nombre = self.leNombreRuta.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "La ruta necesita un nombre.")
            return

        if not self.coordenadas_origen:
            QMessageBox.warning(self, "Error", "Define un punto de origen.")
            return
        
        if not self.lista_destinos:
            QMessageBox.warning(self, "Error", "Añade al menos una parada.")
            return

        # Obtener datos
        id_gestor = self.app_state["user"]["uid"]
        origen = self.leOrigen.text()
        destino = self.lista_destinos[-1]['direccion']
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
                f"Ruta '{nombre}' creada correctamente."
            )
            
            # Actualización selectiva si hay tabla
            if hasattr(self, 'tablaRutas'):
                self.agregar_ruta_a_tabla(nueva_ruta)
            
            # Emitir señal
            self.ruta_creada.emit(nueva_ruta)
            
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", "Error al guardar la ruta.")
    
    def actualizar_ruta(self):
        """Actualiza una ruta existente"""
        if not self.ruta_en_edicion:
            return
        
        # Validaciones
        nombre = self.leNombreRuta.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "La ruta necesita un nombre.")
            return

        if not self.coordenadas_origen:
            QMessageBox.warning(self, "Error", "Define un punto de origen.")
            return
        
        if not self.lista_destinos:
            QMessageBox.warning(self, "Error", "Añade al menos una parada.")
            return

        # Mantener el mismo ID y gestor
        id_ruta = self.ruta_en_edicion.id_ruta
        id_gestor = self.ruta_en_edicion.id_gestor
        estado_anterior = self.ruta_en_edicion.estado
        
        # Obtener datos actualizados
        origen = self.leOrigen.text()
        destino = self.lista_destinos[-1]['direccion']
        fecha = self.dtFecha.date().toString("dd/MM/yyyy")
        hora_inicio = self.teHoraInicio.time().toString("HH:mm")
        hora_fin = self.teHoraFin.time().toString("HH:mm")

        # Crear objeto Ruta actualizado
        ruta_actualizada = Ruta(
            id_ruta=id_ruta,
            nombre=nombre,
            origen=origen,
            destino=destino,
            fecha=fecha,
            hora_inicio_prevista=hora_inicio,
            hora_fin_prevista=hora_fin,
            id_gestor=id_gestor,
            estado=estado_anterior,  # Mantener el estado actual
            paradas=self.lista_destinos
        )
        
        # Actualizar en Firebase
        if self.repo_rutas.actualizar_ruta(ruta_actualizada):
            QMessageBox.information(
                self,
                "Actualizado",
                f"Ruta '{nombre}' actualizada correctamente."
            )
            
            # Actualización selectiva si hay tabla
            if hasattr(self, 'tablaRutas'):
                self.actualizar_fila_ruta_con_datos(
                    self.lista_rutas_actual.index(self.ruta_en_edicion),
                    ruta_actualizada
                )
            
            # Emitir señal
            self.ruta_actualizada.emit(id_ruta)
            
            self.modo_crear_nueva()
        else:
            QMessageBox.critical(self, "Error", "Error al actualizar la ruta.")

    # =========================================================================
    # EDITAR / ELIMINAR RUTA
    # =========================================================================
    
    def editar_ruta_seleccionada(self):
        """Carga la ruta seleccionada en el formulario para editarla"""
        if not hasattr(self, 'tablaRutas'):
            return
            
        fila = self.tablaRutas.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una ruta de la tabla.")
            return
        
        ruta = self.lista_rutas_actual[fila]
        self.modo_editar(ruta)
    
    def eliminar_ruta_seleccionada(self):
        """Elimina la ruta seleccionada"""
        if not hasattr(self, 'tablaRutas'):
            return
            
        fila = self.tablaRutas.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una ruta de la tabla.")
            return
        
        ruta = self.lista_rutas_actual[fila]
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar la ruta '{ruta.nombre}'?\n\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            id_ruta = ruta.id_ruta
            
            if self.repo_rutas.eliminar_ruta(id_ruta):
                # Actualización selectiva
                self.eliminar_ruta_de_tabla(id_ruta)
                
                # Emitir señal
                self.ruta_eliminada.emit(id_ruta)
                
                QMessageBox.information(self, "Eliminado", "Ruta eliminada correctamente.")
                
                # Si estábamos editando esta ruta, limpiar formulario
                if self.modo_edicion and self.ruta_en_edicion.id_ruta == id_ruta:
                    self.modo_crear_nueva()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la ruta.")

    # =========================================================================
    # ACTUALIZACIÓN SELECTIVA DE TABLA
    # =========================================================================
    
    def agregar_ruta_a_tabla(self, ruta):
        """Agrega una nueva ruta a la tabla sin recargar todo"""
        if not hasattr(self, 'tablaRutas'):
            return
            
        self.lista_rutas_actual.append(ruta)
        self.cache_rutas[ruta.id_ruta] = ruta
        
        nueva_fila = self.tablaRutas.rowCount()
        self.tablaRutas.insertRow(nueva_fila)
        self._llenar_fila_tabla(nueva_fila, ruta)
    
    def actualizar_fila_ruta_con_datos(self, fila, ruta_actualizada):
        """Actualiza una fila específica con datos ya proporcionados"""
        if not hasattr(self, 'tablaRutas'):
            return
            
        self.lista_rutas_actual[fila] = ruta_actualizada
        self.cache_rutas[ruta_actualizada.id_ruta] = ruta_actualizada
        self._llenar_fila_tabla(fila, ruta_actualizada)
    
    def eliminar_ruta_de_tabla(self, id_ruta):
        """Elimina una ruta de la tabla sin recargar todo"""
        if not hasattr(self, 'tablaRutas'):
            return
            
        fila = None
        for i, ruta in enumerate(self.lista_rutas_actual):
            if ruta.id_ruta == id_ruta:
                fila = i
                break
        
        if fila is None:
            return
        
        del self.lista_rutas_actual[fila]
        if id_ruta in self.cache_rutas:
            del self.cache_rutas[id_ruta]
        
        self.tablaRutas.removeRow(fila)

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