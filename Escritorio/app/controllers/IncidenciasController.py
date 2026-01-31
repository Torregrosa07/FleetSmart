from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Signal
from app.views.IncidenciasWidget_ui import Ui_IncidenciasWidget
from app.repositories.incidencia_repository import IncidenciaRepository
from app.repositories.vehiculo_repository import VehiculoRepository
from app.repositories.conductor_repository import ConductorRepository
from app.controllers.IncidenciaDialogController import IncidenciaDialogController


class IncidenciasController(QWidget, Ui_IncidenciasWidget):
    """
    Controlador para gestionar incidencias de vehículos.
    
    OPTIMIZACIONES IMPLEMENTADAS:
    - ✅ Sistema de señales para notificar cambios
    - ✅ Actualización selectiva de tabla (sin recargar todo)
    - ✅ Caché de incidencias para mejor rendimiento
    - ✅ Métodos granulares de actualización
    """
    
    # ========== SEÑALES ==========
    incidencia_creada = Signal(object)          # incidencia completa
    incidencia_actualizada = Signal(str)        # id_incidencia
    incidencia_eliminada = Signal(str)          # id_incidencia
    incidencia_estado_cambiado = Signal(str, str)  # id_incidencia, nuevo_estado
    
    def __init__(self, db_connection, app_state):
        super().__init__()
        self.setupUi(self)
        
        # Estado global
        self.app_state = app_state
        
        # Repositorios
        self.repo_incidencias = IncidenciaRepository(db_connection)
        self.repo_vehiculos = VehiculoRepository(db_connection)
        self.repo_conductores = ConductorRepository(db_connection)
        
        # Lista de incidencias y caché
        self.lista_incidencias = []
        self.cache_incidencias = {}  # {id_incidencia: incidencia}
        
        # Configuración inicial
        self.configurar_tabla()
        self.cargar_tabla()
        self.conectar_senales()
    
    def configurar_tabla(self):
        """Configura el estilo y comportamiento de la tabla"""
        self.tablaIncidencias.horizontalHeader().setStretchLastSection(False)
        self.tablaIncidencias.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def conectar_senales(self):
        """Conecta los botones con sus métodos"""
        self.btnNuevaIncidencia.clicked.connect(self.crear_incidencia)
        self.btnRecargar.clicked.connect(self.cargar_tabla)
        self.btnCambiarEstado.clicked.connect(self.cambiar_estado)
        self.btnEliminar.clicked.connect(self.eliminar_incidencia)
        self.cbFiltroEstado.currentTextChanged.connect(self.aplicar_filtro)
    
    def cargar_tabla(self):
        """Carga todas las incidencias desde Firebase"""
        # Obtener todas las incidencias
        self.lista_incidencias = self.repo_incidencias.obtener_todas()
        
        # Actualizar caché
        self.cache_incidencias = {
            inc.id_incidencia: inc for inc in self.lista_incidencias
        }
        
        # Aplicar filtro actual
        self.aplicar_filtro()
    
    def aplicar_filtro(self):
        """Aplica el filtro de estado seleccionado"""
        filtro = self.cbFiltroEstado.currentText()
        
        # Obtener incidencias filtradas
        if filtro == "Todas":
            incidencias_a_mostrar = self.lista_incidencias
        else:
            incidencias_a_mostrar = [
                inc for inc in self.lista_incidencias 
                if inc.estado == filtro
            ]
        
        # Llenar tabla
        self.llenar_tabla(incidencias_a_mostrar)
    
    def llenar_tabla(self, incidencias):
        """Llena la tabla con una lista de incidencias"""
        # Limpiar tabla
        self.tablaIncidencias.setRowCount(0)
        
        # Llenar filas
        for i, inc in enumerate(incidencias):
            self.tablaIncidencias.insertRow(i)
            self._llenar_fila_tabla(i, inc)
    
    def _llenar_fila_tabla(self, fila, incidencia):
        """Método auxiliar para llenar una fila de la tabla"""
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
    
    def agregar_incidencia_a_tabla(self, incidencia):
        """
        Agrega una nueva incidencia a la tabla sin recargar todo.
        Se llama cuando se crea una incidencia.
        """
        # Agregar a la lista y caché
        self.lista_incidencias.append(incidencia)
        self.cache_incidencias[incidencia.id_incidencia] = incidencia
        
        # Verificar si debe mostrarse según el filtro actual
        filtro = self.cbFiltroEstado.currentText()
        if filtro == "Todas" or incidencia.estado == filtro:
            # Agregar nueva fila a la tabla
            nueva_fila = self.tablaIncidencias.rowCount()
            self.tablaIncidencias.insertRow(nueva_fila)
            self._llenar_fila_tabla(nueva_fila, incidencia)
            
            print(f"[IncidenciasController] Incidencia añadida a la tabla: {incidencia.tipo}")
    
    def actualizar_fila_incidencia_con_datos(self, fila, incidencia_actualizada):
        """
        Actualiza una fila específica con datos ya proporcionados.
        Más eficiente que obtener desde Firebase.
        """
        # Actualizar en lista y caché
        # Buscar el índice en lista_incidencias
        for i, inc in enumerate(self.lista_incidencias):
            if inc.id_incidencia == incidencia_actualizada.id_incidencia:
                self.lista_incidencias[i] = incidencia_actualizada
                break
        
        self.cache_incidencias[incidencia_actualizada.id_incidencia] = incidencia_actualizada
        
        # Actualizar solo esa fila en la tabla
        self._llenar_fila_tabla(fila, incidencia_actualizada)
        
        print(f"[IncidenciasController] Incidencia actualizada en tabla: {incidencia_actualizada.tipo}")
    
    def actualizar_fila_incidencia(self, id_incidencia):
        """
        Actualiza selectivamente una fila de la tabla cuando cambia una incidencia.
        MUCHO más eficiente que recargar toda la tabla.
        """
        # Buscar la fila de la incidencia en la tabla actual
        fila = self._encontrar_fila_en_tabla(id_incidencia)
        
        if fila is None:
            # La incidencia no está visible actualmente (por filtro)
            # Actualizar en lista y caché solamente
            incidencia_actualizada = self.repo_incidencias.obtener_por_id(id_incidencia)
            if incidencia_actualizada:
                for i, inc in enumerate(self.lista_incidencias):
                    if inc.id_incidencia == id_incidencia:
                        self.lista_incidencias[i] = incidencia_actualizada
                        break
                self.cache_incidencias[id_incidencia] = incidencia_actualizada
            return
        
        # Obtener datos actualizados del repositorio
        incidencia_actualizada = self.repo_incidencias.obtener_por_id(id_incidencia)
        if not incidencia_actualizada:
            return
        
        # Verificar si sigue cumpliendo el filtro
        filtro = self.cbFiltroEstado.currentText()
        if filtro != "Todas" and incidencia_actualizada.estado != filtro:
            # Ya no cumple el filtro: eliminar de la tabla
            self.tablaIncidencias.removeRow(fila)
        else:
            # Actualizar usando el método auxiliar
            self.actualizar_fila_incidencia_con_datos(fila, incidencia_actualizada)
    
    def eliminar_incidencia_de_tabla(self, id_incidencia):
        """
        Elimina una incidencia de la tabla sin recargar todo.
        Se llama cuando se borra una incidencia.
        """
        # Buscar la fila de la incidencia
        fila = self._encontrar_fila_en_tabla(id_incidencia)
        
        # Eliminar de lista y caché
        self.lista_incidencias = [
            inc for inc in self.lista_incidencias 
            if inc.id_incidencia != id_incidencia
        ]
        if id_incidencia in self.cache_incidencias:
            del self.cache_incidencias[id_incidencia]
        
        # Eliminar fila de la tabla si está visible
        if fila is not None:
            self.tablaIncidencias.removeRow(fila)
            print(f"[IncidenciasController] Incidencia eliminada de tabla")
    
    def _encontrar_fila_en_tabla(self, id_incidencia):
        """
        Encuentra la fila en la tabla que corresponde a una incidencia.
        Retorna None si no está visible actualmente.
        """
        # Obtener incidencias visibles según filtro
        filtro = self.cbFiltroEstado.currentText()
        if filtro == "Todas":
            incidencias_visibles = self.lista_incidencias
        else:
            incidencias_visibles = [
                inc for inc in self.lista_incidencias 
                if inc.estado == filtro
            ]
        
        # Buscar el índice
        for i, inc in enumerate(incidencias_visibles):
            if inc.id_incidencia == id_incidencia:
                return i
        
        return None
    
    # =========================================================================
    # OBTENER INCIDENCIA SELECCIONADA
    # =========================================================================
    
    def obtener_incidencia_seleccionada(self):
        """Devuelve la incidencia seleccionada en la tabla"""
        fila = self.tablaIncidencias.currentRow()
        
        if fila == -1:
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecciona una incidencia de la tabla."
            )
            return None
        
        # Obtener incidencias visibles actualmente
        filtro = self.cbFiltroEstado.currentText()
        if filtro == "Todas":
            incidencias_visibles = self.lista_incidencias
        else:
            incidencias_visibles = [
                inc for inc in self.lista_incidencias 
                if inc.estado == filtro
            ]
        
        return incidencias_visibles[fila]
    
    # =========================================================================
    # CREAR INCIDENCIA
    # =========================================================================
    
    def crear_incidencia(self):
        """Abre el diálogo para crear una nueva incidencia"""
        # Obtener vehículos y conductores para el diálogo
        vehiculos = self.repo_vehiculos.obtener_todos()
        conductores = self.repo_conductores.obtener_todos()
        
        if not vehiculos:
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
        
        if dialog.exec():
            incidencia = dialog.datos_incidencia
            
            # Asignar id_gestor del usuario logueado
            incidencia.id_gestor = self.app_state["user"]["uid"]
            
            # Guardar en Firebase
            if self.repo_incidencias.guardar_incidencia(incidencia):
                # Actualización selectiva: agregar solo esta incidencia
                self.agregar_incidencia_a_tabla(incidencia)
                
                # Emitir señal de incidencia creada
                self.incidencia_creada.emit(incidencia)
                
                QMessageBox.information(
                    self,
                    "Incidencia Creada",
                    f"Incidencia registrada correctamente:\n\n"
                    f"Vehículo: {incidencia.matricula}\n"
                    f"Tipo: {incidencia.tipo}\n"
                    f"Estado: {incidencia.estado}"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo guardar la incidencia."
                )
    
    # =========================================================================
    # CAMBIAR ESTADO
    # =========================================================================
    
    def cambiar_estado(self):
        """Cambia el estado de una incidencia (Pendiente → En Proceso → Resuelta)"""
        incidencia = self.obtener_incidencia_seleccionada()
        if not incidencia:
            return
        
        # Determinar siguiente estado
        estados = ["Pendiente", "En Proceso", "Resuelta"]
        indice_actual = estados.index(incidencia.estado)
        
        if indice_actual == len(estados) - 1:
            QMessageBox.information(
                self,
                "Estado final",
                "Esta incidencia ya está en estado 'Resuelta'."
            )
            return
        
        nuevo_estado = estados[indice_actual + 1]
        estado_anterior = incidencia.estado
        
        # Confirmar cambio
        respuesta = QMessageBox.question(
            self,
            "Cambiar Estado",
            f"¿Cambiar estado de la incidencia?\n\n"
            f"Estado actual: {incidencia.estado}\n"
            f"Nuevo estado: {nuevo_estado}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            # Actualizar estado
            incidencia.estado = nuevo_estado
            
            if self.repo_incidencias.actualizar_incidencia(incidencia):
                # Detectar si cambió el estado
                cambio_estado = (estado_anterior != nuevo_estado)
                
                # Actualización selectiva: actualizar solo esta fila
                self.actualizar_fila_incidencia(incidencia.id_incidencia)
                
                # Emitir señales
                self.incidencia_actualizada.emit(incidencia.id_incidencia)
                if cambio_estado:
                    self.incidencia_estado_cambiado.emit(
                        incidencia.id_incidencia, 
                        nuevo_estado
                    )
                
                QMessageBox.information(
                    self,
                    "Actualizado",
                    f"Estado cambiado a: {nuevo_estado}"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo actualizar el estado."
                )
    
    # =========================================================================
    # ELIMINAR INCIDENCIA
    # =========================================================================
    
    def eliminar_incidencia(self):
        """Elimina una incidencia"""
        incidencia = self.obtener_incidencia_seleccionada()
        if not incidencia:
            return
        
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
        
        if respuesta == QMessageBox.Yes:
            id_incidencia = incidencia.id_incidencia
            
            if self.repo_incidencias.eliminar_incidencia(id_incidencia):
                # Actualización selectiva: eliminar solo esta fila
                self.eliminar_incidencia_de_tabla(id_incidencia)
                
                # Emitir señal de incidencia eliminada
                self.incidencia_eliminada.emit(id_incidencia)
                
                QMessageBox.information(
                    self,
                    "Eliminado",
                    "Incidencia eliminada correctamente."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo eliminar la incidencia."
                )