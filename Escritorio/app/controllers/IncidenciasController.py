from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Signal

from app.views.IncidenciasWidget_ui import Ui_IncidenciasWidget
from app.services.incidencias_service import IncidenciasService
from app.controllers.IncidenciaDialogController import IncidenciaDialogController
from app.services.notificaciones_api_service import notificaciones_api
from app.utils.language_utils import LanguageService

class IncidenciasController(QWidget, Ui_IncidenciasWidget):
    
    # ========== SEÑALES ==========
    incidencia_creada = Signal(object)
    incidencia_actualizada = Signal(str)
    incidencia_eliminada = Signal(str)
    incidencia_estado_cambiado = Signal(str, str)
    
    def __init__(self, db_connection, app_state):
        super().__init__()
        self.setupUi(self)
        self.app_state = app_state
        
        # Servicio de lógica de negocio
        self.service = IncidenciasService(db_connection)
        
        # Lista y caché
        self.lista_incidencias = []
        self.cache_incidencias = {}
        
        # Configuración inicial
        self.configurar_tabla()
        self.cargar_tabla()
        self.conectar_botones()
    
    # =========================================================================
    # CONFIGURACIÓN INICIAL
    # =========================================================================
    
    def configurar_tabla(self):
        """Configura el estilo de la tabla"""
        self.tablaIncidencias.horizontalHeader().setStretchLastSection(False)
        self.tablaIncidencias.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def conectar_botones(self):
        """Conecta los botones con sus métodos"""
        self.btnNuevaIncidencia.clicked.connect(self.crear_incidencia)
        self.btnRecargar.clicked.connect(self.cargar_tabla)
        self.btnCambiarEstado.clicked.connect(self.cambiar_estado)
        self.btnEliminar.clicked.connect(self.eliminar_incidencia)
        self.cbFiltroEstado.currentTextChanged.connect(self.aplicar_filtro)
    


    # =========================================================================
    # TRADUCCION DE INTERFAZ
    # =========================================================================

    def actualizar_idioma(self, idioma):
        """Traduce la interfaz de incidencias"""
        # Traducir botones
        self.btnNuevaIncidencia.setText("+ " + LanguageService.get_text("new", idioma))
        self.btnRecargar.setText(LanguageService.get_text("refresh", idioma))
        self.btnCambiarEstado.setText(LanguageService.get_text("change_status", idioma))
        self.btnEliminar.setText(LanguageService.get_text("delete", idioma))

        # Traducir cabeceras de la tabla
        claves_columnas = {
            0: "date",
            1: "time",
            2: "license_plate",
            3: "type",
            4: "status",
            5: "description",
            6: "driver"
        }
        for col, clave in claves_columnas.items():
            texto = LanguageService.get_text(clave, idioma)
            item = self.tablaIncidencias.horizontalHeaderItem(col)
            if item:
                item.setText(texto)
    # =========================================================================
    # GESTION DE TABLA
    # =========================================================================
    
    def cargar_tabla(self):
        """Carga todas las incidencias desde el servicio"""
        # Obtener todas las incidencias
        self.lista_incidencias = self.service.obtener_todas()
        
        # Actualizar caché
        self.cache_incidencias = {
            inc.id_incidencia: inc for inc in self.lista_incidencias
        }
        
        # Aplicar filtro actual
        self.aplicar_filtro()
    
    def aplicar_filtro(self):
        """Aplica el filtro de estado seleccionado"""
        filtro = self.cbFiltroEstado.currentText()
        
        # Obtener incidencias filtradas usando el servicio
        incidencias_a_mostrar = self.service.obtener_por_estado(filtro)
        
        # Llenar tabla
        self.llenar_tabla(incidencias_a_mostrar)
    
    def llenar_tabla(self, incidencias):
        """Llena la tabla con una lista de incidencias"""
        # Limpiar tabla
        self.tablaIncidencias.setRowCount(0)
        
        # Llenar filas
        for i, inc in enumerate(incidencias):
            self.tablaIncidencias.insertRow(i)
            self.llenar_fila(i, inc)
    
    def llenar_fila(self, fila, incidencia):
        """Llena una fila de la tabla con datos de una incidencia"""
        self.tablaIncidencias.setItem(fila, 0, QTableWidgetItem(incidencia.fecha))
        self.tablaIncidencias.setItem(fila, 1, QTableWidgetItem(incidencia.hora))
        self.tablaIncidencias.setItem(fila, 2, QTableWidgetItem(incidencia.matricula))
        self.tablaIncidencias.setItem(fila, 3, QTableWidgetItem(incidencia.tipo))
        self.tablaIncidencias.setItem(fila, 4, QTableWidgetItem(incidencia.estado))
        self.tablaIncidencias.setItem(fila, 5, QTableWidgetItem(incidencia.descripcion))
        
        # Conductor (puede ser None)
        conductor = incidencia.nombre_conductor or "-"
        self.tablaIncidencias.setItem(fila, 6, QTableWidgetItem(conductor))
    
    # =========================================================================
    # ACTUALIZACIÓN SELECTIVA DE TABLA
    # =========================================================================
    
    def agregar_a_tabla(self, incidencia):
        """Agrega una incidencia a la tabla sin recargar todo"""
        # Agregar a lista y caché
        self.lista_incidencias.append(incidencia)
        self.cache_incidencias[incidencia.id_incidencia] = incidencia
        
        # Verificar si debe mostrarse según el filtro actual
        filtro = self.cbFiltroEstado.currentText()
        if filtro == "Todas" or incidencia.estado == filtro:
            # Agregar nueva fila
            nueva_fila = self.tablaIncidencias.rowCount()
            self.tablaIncidencias.insertRow(nueva_fila)
            self.llenar_fila(nueva_fila, incidencia)
    
    def actualizar_en_tabla(self, fila, incidencia):
        """Actualiza una fila específica"""
        # Actualizar en lista
        for i, inc in enumerate(self.lista_incidencias):
            if inc.id_incidencia == incidencia.id_incidencia:
                self.lista_incidencias[i] = incidencia
                break
        
        # Actualizar en caché
        self.cache_incidencias[incidencia.id_incidencia] = incidencia
        
        # Actualizar fila en tabla
        self.llenar_fila(fila, incidencia)
    
    def actualizar_incidencia_especifica(self, id_incidencia):
        """Actualiza una incidencia específica desde Firebase"""
        # Buscar fila en tabla actual
        fila = self.encontrar_fila_en_tabla(id_incidencia)
        
        # Obtener datos actualizados
        incidencia_actualizada = self.service.obtener_por_id(id_incidencia)
        if not incidencia_actualizada:
            return
        
        # Actualizar en lista y caché siempre
        for i, inc in enumerate(self.lista_incidencias):
            if inc.id_incidencia == id_incidencia:
                self.lista_incidencias[i] = incidencia_actualizada
                break
        self.cache_incidencias[id_incidencia] = incidencia_actualizada
        
        if fila is None:
            # No está visible (por filtro), solo actualizamos caché
            return
        
        # Verificar si sigue cumpliendo el filtro
        filtro = self.cbFiltroEstado.currentText()
        if filtro != "Todas" and incidencia_actualizada.estado != filtro:
            # Ya no cumple el filtro: eliminar de la tabla
            self.tablaIncidencias.removeRow(fila)
        else:
            # Actualizar fila
            self.actualizar_en_tabla(fila, incidencia_actualizada)
    
    def eliminar_de_tabla(self, id_incidencia):
        """Elimina una incidencia de la tabla"""
        # Buscar fila
        fila = self.encontrar_fila_en_tabla(id_incidencia)
        
        # Eliminar de lista
        for i, inc in enumerate(self.lista_incidencias):
            if inc.id_incidencia == id_incidencia:
                del self.lista_incidencias[i]
                break
        
        # Eliminar de caché
        if id_incidencia in self.cache_incidencias:
            del self.cache_incidencias[id_incidencia]
        
        # Eliminar fila de tabla si está visible
        if fila is not None:
            self.tablaIncidencias.removeRow(fila)
    
    def encontrar_fila_en_tabla(self, id_incidencia):
        """
        Encuentra la fila de una incidencia en la tabla actual.
        
        Returns:
            Número de fila o None si no está visible
        """
        # Obtener incidencias visibles según filtro actual
        filtro = self.cbFiltroEstado.currentText()
        incidencias_visibles = self.service.obtener_por_estado(filtro)
        
        # Buscar en la lista visible
        for i, inc in enumerate(incidencias_visibles):
            if inc.id_incidencia == id_incidencia:
                return i
        
        return None
    
    # =========================================================================
    # OBTENER INCIDENCIA SELECCIONADA
    # =========================================================================
    
    def obtener_seleccionada(self):
        """Devuelve la incidencia seleccionada en la tabla"""
        fila = self.tablaIncidencias.currentRow()
        
        if fila == -1:
            QMessageBox.warning(self, "Aviso", "Selecciona una incidencia de la tabla.")
            return None
        
        # Obtener incidencias visibles actualmente
        filtro = self.cbFiltroEstado.currentText()
        incidencias_visibles = self.service.obtener_por_estado(filtro)
        
        if fila >= len(incidencias_visibles):
            return None
        
        return incidencias_visibles[fila]
    
    # =========================================================================
    # CREAR INCIDENCIA
    # =========================================================================
    
    def crear_incidencia(self):
        """Abre el diálogo para crear una nueva incidencia"""
        # Validar que existan vehículos usando el servicio
        valido, vehiculos, conductores = self.service.validar_creacion_incidencia()
        
        if not valido:
            QMessageBox.warning(
                self,
                "Sin vehículos",
                "No hay vehículos registrados.\n"
                "Debes crear vehículos primero."
            )
            return
        
        # Abrir diálogo
        dialog = IncidenciaDialogController(
            self,
            vehiculos=vehiculos,
            conductores=conductores
        )
        
        if not dialog.exec():
            return
        
        incidencia = dialog.datos_incidencia
        
        # Asignar id_gestor
        incidencia.id_gestor = self.app_state["user"]["uid"]
        
        # Crear usando el servicio
        exito, incidencia_creada, mensaje = self.service.crear_incidencia(incidencia)
        
        if exito:
            # Agregar a tabla
            self.agregar_a_tabla(incidencia_creada)
            
            # Emitir señal
            self.incidencia_creada.emit(incidencia_creada)
            
            QMessageBox.information(
                self,
                "Incidencia Creada",
                f"Incidencia registrada correctamente:\n\n"
                f"Vehículo: {incidencia.matricula}\n"
                f"Tipo: {incidencia.tipo}\n"
                f"Estado: {incidencia.estado}"
            )
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # CAMBIAR ESTADO
    # =========================================================================
    
    def cambiar_estado(self):
        """Cambia el estado de una incidencia al siguiente estado"""
        incidencia = self.obtener_seleccionada()
        if not incidencia:
            return
        
        # Verificar si puede cambiar usando el servicio
        puede, mensaje_error = self.service.puede_cambiar_estado(incidencia.estado)
        
        if not puede:
            QMessageBox.information(self, "Estado final", mensaje_error)
            return
        
        # Obtener siguiente estado
        _, nuevo_estado = self.service.obtener_siguiente_estado(incidencia.estado)
        
        # Confirmar cambio
        respuesta = QMessageBox.question(
            self,
            "Cambiar Estado",
            f"¿Cambiar estado de la incidencia?\n\n"
            f"Estado actual: {incidencia.estado}\n"
            f"Nuevo estado: {nuevo_estado}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        # Cambiar estado usando el servicio
        exito, estado_actualizado, mensaje = self.service.cambiar_estado_incidencia(incidencia)
        
        if exito:
            # Actualizar tabla
            self.actualizar_incidencia_especifica(incidencia.id_incidencia)
            
            # Emitir señales
            self.incidencia_actualizada.emit(incidencia.id_incidencia)
            self.incidencia_estado_cambiado.emit(incidencia.id_incidencia, estado_actualizado)
            
            # Enviar notificacion al conductor
            notificaciones_api.notificar_incidencia_actualizada(incidencia.id_incidencia)
            
            QMessageBox.information(self, "Actualizado", mensaje)
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # ELIMINAR INCIDENCIA
    # =========================================================================
    
    def eliminar_incidencia(self):
        """Elimina una incidencia"""
        incidencia = self.obtener_seleccionada()
        if not incidencia:
            return
        
        # Confirmar
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Eliminar esta incidencia?\n\n"
            f"Vehículo: {incidencia.matricula}\n"
            f"Tipo: {incidencia.tipo}\n"
            f"Fecha: {incidencia.fecha}\n\n"
            f"Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        id_incidencia = incidencia.id_incidencia
        
        # Eliminar usando el servicio
        exito, mensaje = self.service.eliminar_incidencia(id_incidencia)
        
        if exito:
            # Eliminar de tabla
            self.eliminar_de_tabla(id_incidencia)
            
            # Emitir señal
            self.incidencia_eliminada.emit(id_incidencia)
            
            QMessageBox.information(self, "Eliminado", "Incidencia eliminada correctamente.")
        else:
            QMessageBox.critical(self, "Error", mensaje)