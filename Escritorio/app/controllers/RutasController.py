from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtCore import Signal, QDate, QTime

from app.views.RutasWidget_ui import Ui_RutasWidget
from app.models.ruta import Ruta
from app.services.rutas_service import RutasService
from app.utils.geocoding_utils import GeocodingUtils
from app.utils.map_utils import MapUtils
from app.utils.language_utils import LanguageService


class RutasController(QWidget, Ui_RutasWidget):

    # ========== SEÑALES ==========
    ruta_creada = Signal(object)
    ruta_actualizada = Signal(str)
    ruta_eliminada = Signal(str)
    ruta_estado_cambiada = Signal(str, str)
    
    def __init__(self, db_connection, app_state):
        super().__init__()
        self.setupUi(self)
        
        # Estado global
        self.app_state = app_state
        
        # Servicio de lógica de negocio
        self.service = RutasService(db_connection)
        
        # Utilidad de geocodificación
        self.geocoding = GeocodingUtils()
        
        # Lista y caché
        self.lista_rutas = []
        self.cache_rutas = {}
        
        # Variables para el mapa
        self.coordenadas_origen = None
        self.lista_paradas = []
        
        # Variable temporal para geocoding de paradas
        self.texto_parada_temporal = ""
        
        # Control de modo edición
        self.modo_edicion = False
        self.ruta_en_edicion = None
        
        # Configuración inicial
        self.configurar_fecha_hora()
        self.configurar_tabla()
        self.cargar_tabla()
        self.dibujar_mapa_vacio()
        self.conectar_botones()
    
    # =========================================================================
    # CONFIGURACIÓN INICIAL
    # =========================================================================
    
    def configurar_tabla(self):
        """Configura el estilo de la tabla de rutas"""
        if hasattr(self, 'tablaRutas'):
            self.tablaRutas.setColumnCount(6)
            self.tablaRutas.setHorizontalHeaderLabels([
                "Nombre", "Origen", "Destino", "Fecha", "Estado", "Nº Paradas"
            ])
            
            self.tablaRutas.horizontalHeader().setStretchLastSection(False)
            self.tablaRutas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tablaRutas.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tablaRutas.setSelectionBehavior(QAbstractItemView.SelectRows)
    
    def configurar_fecha_hora(self):
        """Configura los valores por defecto de fecha y hora"""
        self.dtFecha.setDate(QDate.currentDate())
        self.teHoraInicio.setTime(QTime(8, 0))
        self.teHoraFin.setTime(QTime(17, 0))
    
    def conectar_botones(self):
        """Conecta todos los botones y eventos"""
        # Geocodificación
        self.leOrigen.editingFinished.connect(self.buscar_origen)
        
        # Botones de formulario
        self.btnAgregarParada.clicked.connect(self.agregar_parada)
        self.btnEliminarParada.clicked.connect(self.borrar_parada)
        self.btnGuardarRuta.clicked.connect(self.guardar_o_actualizar_ruta)
        
        # Botones de gestión de rutas
        if hasattr(self, 'btnEditarRuta'):
            self.btnEditarRuta.clicked.connect(self.editar_ruta_seleccionada)
        if hasattr(self, 'btnEliminarRuta'):
            self.btnEliminarRuta.clicked.connect(self.eliminar_ruta_seleccionada)
        if hasattr(self, 'btnNuevaRuta'):
            self.btnNuevaRuta.clicked.connect(self.modo_crear_nueva)
        if hasattr(self, 'btnCancelar'):
            self.btnCancelar.clicked.connect(self.cancelar_edicion)
    


    # =========================================================================
    # TRADUCCION DE INTERFAZ
    # =========================================================================

    def actualizar_idioma(self, idioma):
        """Traduce la interfaz de rutas"""
        # Traducir botones
        self.btnGuardarRuta.setText(LanguageService.get_text("save_route", idioma))
        self.btnAgregarParada.setText(LanguageService.get_text("add_stop", idioma))
        self.btnEliminarParada.setText(LanguageService.get_text("delete_stop", idioma))
        
        if hasattr(self, 'btnEditarRuta'):
            self.btnEditarRuta.setText(LanguageService.get_text("edit", idioma))
        if hasattr(self, 'btnEliminarRuta'):
            self.btnEliminarRuta.setText(LanguageService.get_text("delete", idioma))
        if hasattr(self, 'btnNuevaRuta'):
            self.btnNuevaRuta.setText(LanguageService.get_text("new_route", idioma))
        if hasattr(self, 'btnCancelar'):
            self.btnCancelar.setText(LanguageService.get_text("cancel", idioma))

        # Traducir cabeceras de la tabla
        if hasattr(self, 'tablaRutas'):
            claves_columnas = {
                0: "name",
                1: "origin",
                2: "destination",
                3: "date",
                4: "status",
                5: "num_stops"
            }
            for col, clave in claves_columnas.items():
                texto = LanguageService.get_text(clave, idioma)
                item = self.tablaRutas.horizontalHeaderItem(col)
                if item:
                    item.setText(texto)
    # =========================================================================
    # GESTION DE TABLA
    # =========================================================================
    
    def cargar_tabla(self):
        """Carga todas las rutas desde el servicio"""
        if not hasattr(self, 'tablaRutas'):
            return
        
        self.lista_rutas = self.service.obtener_todas()
        self.cache_rutas = {r.id_ruta: r for r in self.lista_rutas}
        
        self.tablaRutas.setRowCount(0)
        
        for i, ruta in enumerate(self.lista_rutas):
            self.tablaRutas.insertRow(i)
            self.llenar_fila(i, ruta)
    
    def llenar_fila(self, fila, ruta):
        """Llena una fila de la tabla con datos de una ruta"""
        if not hasattr(self, 'tablaRutas'):
            return
        
        self.tablaRutas.setItem(fila, 0, QTableWidgetItem(ruta.nombre))
        self.tablaRutas.setItem(fila, 1, QTableWidgetItem(ruta.origen))
        self.tablaRutas.setItem(fila, 2, QTableWidgetItem(ruta.destino))
        self.tablaRutas.setItem(fila, 3, QTableWidgetItem(ruta.fecha))
        self.tablaRutas.setItem(fila, 4, QTableWidgetItem(ruta.estado))
        self.tablaRutas.setItem(fila, 5, QTableWidgetItem(str(len(ruta.paradas))))
    
    def agregar_a_tabla(self, ruta):
        """Agrega una ruta a la tabla sin recargar todo"""
        if not hasattr(self, 'tablaRutas'):
            return
        
        self.lista_rutas.append(ruta)
        self.cache_rutas[ruta.id_ruta] = ruta
        
        nueva_fila = self.tablaRutas.rowCount()
        self.tablaRutas.insertRow(nueva_fila)
        self.llenar_fila(nueva_fila, ruta)
    
    def actualizar_en_tabla(self, fila, ruta):
        """Actualiza una fila específica"""
        if not hasattr(self, 'tablaRutas'):
            return
        
        self.lista_rutas[fila] = ruta
        self.cache_rutas[ruta.id_ruta] = ruta
        self.llenar_fila(fila, ruta)
    
    def eliminar_de_tabla(self, id_ruta):
        """Elimina una ruta de la tabla"""
        if not hasattr(self, 'tablaRutas'):
            return
        
        # Buscar fila
        fila = None
        for i, ruta in enumerate(self.lista_rutas):
            if ruta.id_ruta == id_ruta:
                fila = i
                break
        
        if fila is None:
            return
        
        # Eliminar de lista y caché
        del self.lista_rutas[fila]
        if id_ruta in self.cache_rutas:
            del self.cache_rutas[id_ruta]
        
        # Eliminar fila de tabla
        self.tablaRutas.removeRow(fila)
    
    # =========================================================================
    # GESTIÓN DE MAPA
    # =========================================================================
    
    def dibujar_mapa_vacio(self):
        """Dibuja un mapa vacío centrado en España"""
        mapa = MapUtils.create_base_map()
        self.mostrar_mapa(mapa)
    
    def mostrar_mapa(self, mapa):
        """Renderiza el mapa en el QWebEngineView"""
        html = MapUtils.render_to_html(mapa)
        self.webMapRuta.setHtml(html)
    
    def actualizar_mapa(self):
        """Actualiza el mapa con origen y paradas usando MapUtils"""
        if not self.coordenadas_origen and not self.lista_paradas:
            self.dibujar_mapa_vacio()
            return
        
        origen_label = self.leOrigen.text() if self.leOrigen.text() else "Origen"
        
        mapa = MapUtils.create_route_map(
            origin_coords=self.coordenadas_origen,
            origin_label=origen_label,
            waypoints=self.lista_paradas
        )
        
        self.mostrar_mapa(mapa)
    
    # =========================================================================
    # GEOCODIFICACIÓN
    # =========================================================================
    
    def buscar_origen(self):
        """Geocodifica el origen usando GeocodingUtils"""
        texto = self.leOrigen.text().strip()
        if not texto:
            return
        
        # Usar geocoding asíncrono
        self.geocoding.geocode_async(texto, "origen", self.cuando_termine_geocoding)
    
    def agregar_parada(self):
        """Geocodifica y añade una parada"""
        texto = self.leNuevaParada.text().strip()
        if not texto:
            QMessageBox.warning(self, "Aviso", "Escribe una dirección para la parada.")
            return
        
        # Guardar texto temporal
        self.texto_parada_temporal = texto
        
        self.geocoding.geocode_async(texto, "parada", self.cuando_termine_geocoding)
    
    def cuando_termine_geocoding(self, ubicacion, tipo):
        """Callback cuando termina la geocodificación"""
        if not ubicacion:
            QMessageBox.warning(self, "Error", "No se encontró la dirección.")
            return
        
        if tipo == "origen":
            self.coordenadas_origen = GeocodingUtils.coords_to_list(ubicacion)
            self.actualizar_mapa()
        
        elif tipo == "parada":
            parada = {
                "direccion": self.texto_parada_temporal,
                "coords": GeocodingUtils.coords_to_list(ubicacion),
                "orden": len(self.lista_paradas) + 1
            }
            
            self.lista_paradas.append(parada)
            
            self.listParadas.addItem(f"{parada['orden']}. {parada['direccion']}")
            
            self.leDestino.setText(self.texto_parada_temporal)
            
            self.leNuevaParada.clear()
            self.texto_parada_temporal = ""
            
            self.actualizar_mapa()
    
    def borrar_parada(self):
        """Borra la parada seleccionada"""
        fila = self.listParadas.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una parada para borrar.")
            return
        
        # Eliminar de lista
        del self.lista_paradas[fila]
        
        # Reordenar paradas
        for i, parada in enumerate(self.lista_paradas):
            parada['orden'] = i + 1
        
        # Actualizar lista visual
        self.listParadas.clear()
        for parada in self.lista_paradas:
            self.listParadas.addItem(f"{parada['orden']}. {parada['direccion']}")
        
        # Actualizar destino
        if self.lista_paradas:
            self.leDestino.setText(self.lista_paradas[-1]['direccion'])
        else:
            self.leDestino.clear()
        
        # Actualizar mapa
        self.actualizar_mapa()
    
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
        
        # Cargar fecha
        fecha_partes = ruta.fecha.split("/")
        if len(fecha_partes) == 3:
            self.dtFecha.setDate(QDate(
                int(fecha_partes[2]),
                int(fecha_partes[1]),
                int(fecha_partes[0])
            ))
        
        # Cargar horas
        hora_inicio_partes = ruta.hora_inicio_prevista.split(":")
        if len(hora_inicio_partes) == 2:
            self.teHoraInicio.setTime(QTime(
                int(hora_inicio_partes[0]),
                int(hora_inicio_partes[1])
            ))
        
        hora_fin_partes = ruta.hora_fin_prevista.split(":")
        if len(hora_fin_partes) == 2:
            self.teHoraFin.setTime(QTime(
                int(hora_fin_partes[0]),
                int(hora_fin_partes[1])
            ))
        
        # Cargar paradas
        self.lista_paradas = ruta.paradas if ruta.paradas else []
        self.listParadas.clear()
        for parada in self.lista_paradas:
            self.listParadas.addItem(f"{parada['orden']}. {parada['direccion']}")
        
        # Geocodificar origen para mostrar en mapa
        if ruta.origen:
            self.buscar_origen()
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.leNombreRuta.clear()
        self.leOrigen.clear()
        self.leNuevaParada.clear()
        self.leDestino.clear()
        self.listParadas.clear()
        self.coordenadas_origen = None
        self.lista_paradas = []
        self.dtFecha.setDate(QDate.currentDate())
        self.teHoraInicio.setTime(QTime(8, 0))
        self.teHoraFin.setTime(QTime(17, 0))
        self.dibujar_mapa_vacio()
    
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
        """Guarda una nueva ruta"""
        # Obtener datos del formulario
        nombre = self.leNombreRuta.text().strip()
        origen = self.leOrigen.text().strip()
        fecha = self.dtFecha.date().toString("dd/MM/yyyy")
        hora_inicio = self.teHoraInicio.time().toString("HH:mm")
        hora_fin = self.teHoraFin.time().toString("HH:mm")
        
        # VALIDAR PRIMERO
        valido, mensaje_error = self.service.validar_ruta(
            nombre, origen, self.lista_paradas, fecha, hora_inicio, hora_fin
        )
        
        if not valido:
            QMessageBox.warning(self, "Datos Inválidos", mensaje_error)
            return
        
        # Crear objeto Ruta
        id_gestor = self.app_state["user"]["uid"]
        destino = self.lista_paradas[-1]['direccion']
        
        nueva_ruta = Ruta(
            nombre=nombre,
            origen=origen,
            destino=destino,
            fecha=fecha,
            hora_inicio_prevista=hora_inicio,
            hora_fin_prevista=hora_fin,
            id_gestor=id_gestor,
            estado="Pendiente",
            paradas=self.lista_paradas
        )
        
        # Guardar usando el servicio
        exito, ruta_creada, mensaje = self.service.crear_ruta(nueva_ruta)
        
        if exito:
            QMessageBox.information(
                self,
                "Guardado",
                f"Ruta '{nombre}' creada correctamente."
            )
            
            # Agregar a tabla
            self.agregar_a_tabla(ruta_creada)
            
            # Emitir señal
            self.ruta_creada.emit(ruta_creada)
            
            # Limpiar formulario
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    def actualizar_ruta(self):
        """Actualiza una ruta existente"""
        if not self.ruta_en_edicion:
            return
        
        # Obtener datos del formulario
        nombre = self.leNombreRuta.text().strip()
        origen = self.leOrigen.text().strip()
        fecha = self.dtFecha.date().toString("dd/MM/yyyy")
        hora_inicio = self.teHoraInicio.time().toString("HH:mm")
        hora_fin = self.teHoraFin.time().toString("HH:mm")
        
        # VALIDAR PRIMERO
        valido, mensaje_error = self.service.validar_ruta(
            nombre, origen, self.lista_paradas, fecha, hora_inicio, hora_fin
        )
        
        if not valido:
            QMessageBox.warning(self, "Datos Inválidos", mensaje_error)
            return
        
        # Mantener datos originales
        id_ruta = self.ruta_en_edicion.id_ruta
        id_gestor = self.ruta_en_edicion.id_gestor
        estado = self.ruta_en_edicion.estado
        destino = self.lista_paradas[-1]['direccion']
        
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
            estado=estado,
            paradas=self.lista_paradas
        )
        
        # Actualizar usando el servicio
        exito, mensaje = self.service.actualizar_ruta(ruta_actualizada)
        
        if exito:
            QMessageBox.information(
                self,
                "Actualizado",
                f"Ruta '{nombre}' actualizada correctamente."
            )
            
            # Actualizar tabla
            fila = self.lista_rutas.index(self.ruta_en_edicion)
            self.actualizar_en_tabla(fila, ruta_actualizada)
            
            # Emitir señal
            self.ruta_actualizada.emit(id_ruta)
            
            # Volver a modo creación
            self.modo_crear_nueva()
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
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
        
        ruta = self.lista_rutas[fila]
        self.modo_editar(ruta)
    
    def eliminar_ruta_seleccionada(self):
        """Elimina la ruta seleccionada"""
        if not hasattr(self, 'tablaRutas'):
            return
        
        fila = self.tablaRutas.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una ruta de la tabla.")
            return
        
        ruta = self.lista_rutas[fila]
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Eliminar la ruta '{ruta.nombre}'?\n\n"
            f"⚠️ Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        # Eliminar usando el servicio
        exito, mensaje = self.service.eliminar_ruta(ruta.id_ruta)
        
        if exito:
            # Eliminar de tabla
            self.eliminar_de_tabla(ruta.id_ruta)
            
            # Emitir señal
            self.ruta_eliminada.emit(ruta.id_ruta)
            
            QMessageBox.information(self, "Eliminado", "Ruta eliminada correctamente.")
            
            # Si estábamos editando esta ruta, limpiar formulario
            if self.modo_edicion and self.ruta_en_edicion.id_ruta == ruta.id_ruta:
                self.modo_crear_nueva()
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # LIMPIEZA AL CERRAR
    # =========================================================================
    
    def closeEvent(self, event):
        """Cancelar geocoding activo al cerrar"""
        self.geocoding.cancel_active()
        event.accept()