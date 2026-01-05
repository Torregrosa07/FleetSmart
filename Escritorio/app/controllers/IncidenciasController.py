from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from app.views.IncidenciasWidget_ui import Ui_IncidenciasWidget
from app.repositories.incidencia_repository import IncidenciaRepository
from app.repositories.vehiculo_repository import VehiculoRepository
from app.repositories.conductor_repository import ConductorRepository
from app.controllers.IncidenciaDialogController import IncidenciaDialogController


class IncidenciasController(QWidget, Ui_IncidenciasWidget):

    
    def __init__(self, db_connection, app_state):
        super().__init__()
        self.setupUi(self)
        
        # Estado global
        self.app_state = app_state
        
        # Repositorios
        self.repo_incidencias = IncidenciaRepository(db_connection)
        self.repo_vehiculos = VehiculoRepository(db_connection)
        self.repo_conductores = ConductorRepository(db_connection)
        
        # Lista de incidencias actual
        self.lista_incidencias = []
        
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
        # Obtener todas las incidencias
        self.lista_incidencias = self.repo_incidencias.obtener_todas()
        
        # Aplicar filtro actual
        self.aplicar_filtro()
        
        print(f"{len(self.lista_incidencias)} incidencias cargadas")
    
    def aplicar_filtro(self):
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
            
            self.tablaIncidencias.setItem(i, 0, QTableWidgetItem(inc.fecha))
            self.tablaIncidencias.setItem(i, 1, QTableWidgetItem(inc.hora))
            self.tablaIncidencias.setItem(i, 2, QTableWidgetItem(inc.matricula))
            self.tablaIncidencias.setItem(i, 3, QTableWidgetItem(inc.tipo))
            self.tablaIncidencias.setItem(i, 4, QTableWidgetItem(inc.estado))
            self.tablaIncidencias.setItem(i, 5, QTableWidgetItem(inc.descripcion))
            
            # Conductor (puede ser None)
            conductor = inc.nombre_conductor or "-"
            self.tablaIncidencias.setItem(i, 6, QTableWidgetItem(conductor))
    
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
        dialog = IncidenciaDialogController(self,vehiculos=vehiculos,conductores=conductores)
        
        if dialog.exec():
            incidencia = dialog.datos_incidencia
            
            # Asignar id_gestor del usuario logueado
            incidencia.id_gestor = self.app_state["user"]["uid"]
            
            # Guardar en Firebase
            if self.repo_incidencias.guardar_incidencia(incidencia):
                QMessageBox.information(
                    self,
                    "Incidencia Creada",
                    f"Incidencia registrada correctamente:\n\n"
                    f"Vehículo: {incidencia.matricula}\n"
                    f"Tipo: {incidencia.tipo}\n"
                    f"Estado: {incidencia.estado}"
                )
                self.cargar_tabla()
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
                QMessageBox.information(
                    self,
                    "Actualizado",
                    f"Estado cambiado a: {nuevo_estado}"
                )
                self.cargar_tabla()
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
            if self.repo_incidencias.eliminar_incidencia(incidencia.id_incidencia):
                QMessageBox.information(
                    self,
                    "Eliminado",
                    "Incidencia eliminada correctamente."
                )
                self.cargar_tabla()
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo eliminar la incidencia."
                )