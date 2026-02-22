
from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide6.QtCore import QDateTime, Signal

from app.views.AsignacionWidget_ui import Ui_AsignacionWidget
from app.models.asignacion import Asignacion
from app.services.asignaciones_service import AsignacionesService
from app.services.notificaciones_api_service import notificaciones_api
from app.utils.language_utils import LanguageService


class AsignacionController(QWidget, Ui_AsignacionWidget):

    # ========== SEÑALES ==========
    asignacion_creada = Signal(object)
    asignacion_eliminada = Signal(str)
    
    def __init__(self, db_connection, parent=None, app_state=None):
        super().__init__(parent)
        self.setupUi(self)
        self.app_state = app_state
        
        # Servicio de lógica de negocio
        self.service = AsignacionesService(db_connection)
        
        # Variables de estado
        self.rutas_en_tabla = []
        self.dic_asignaciones = {}
        
        # Configuración inicial
        self.configurar_tabla()
        self.dtInicio.setDateTime(QDateTime.currentDateTime())
        
        # Conectar botones
        self.btnConfirmar.clicked.connect(self.registrar_asignacion)
        self.btnEliminarAsignacion.clicked.connect(self.borrar_asignacion)
        self.tableWidget.cellClicked.connect(self.seleccionar_ruta_de_tabla)
        
        # Cargar datos iniciales
        self.cargar_datos()
    
    # =========================================================================
    # CONFIGURACIÓN INICIAL
    # =========================================================================
    
    def configurar_tabla(self):
        """Configura el estilo de la tabla"""
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setVisible(False)
    
    def cargar_datos(self):
        """Carga todos los datos iniciales"""
        self.cargar_combos()
        self.cargar_tabla()
    
    # =========================================================================
    # GESTIÓN DE COMBOS
    # =========================================================================
    
    def cargar_combos(self):
        """Carga todos los combos desde el servicio"""
        self.cbRuta.clear()
        self.cbConductor.clear()
        self.cbVehiculo.clear()
        
        # Rutas
        todas_rutas = self.service.obtener_todas_rutas()
        for r in todas_rutas:
            self.cbRuta.addItem(r.nombre, r.id_ruta)
        
        # Conductores
        todos_conductores = self.service.obtener_todos_conductores()
        for c in todos_conductores:
            self.cbConductor.addItem(f"{c.nombre} ({c.dni})", c.id_conductor)
        
        # Vehículos (solo disponibles)
        vehiculos_disponibles = self.service.obtener_vehiculos_disponibles()
        for v in vehiculos_disponibles:
            self.cbVehiculo.addItem(
                f"{v.marca} {v.modelo} - {v.matricula}", 
                v.id_vehiculo
            )
    
    # =========================================================================
    # SINCRONIZACIÓN DE COMBOS - RUTAS
    # =========================================================================
    
    def agregar_ruta_a_combo(self, ruta):
        """Añade una nueva ruta al combo (llamado por señal)"""
        self.cbRuta.addItem(ruta.nombre, ruta.id_ruta)
    
    def actualizar_ruta_en_combo(self, id_ruta):
        """Actualiza una ruta en el combo (llamado por señal)"""
        index = self.cbRuta.findData(id_ruta)
        if index >= 0:
            ruta_actualizada = self.service.obtener_ruta_por_id(id_ruta)
            if ruta_actualizada:
                self.cbRuta.setItemText(index, ruta_actualizada.nombre)
    
    def eliminar_ruta_de_combo(self, id_ruta):
        """Elimina una ruta del combo (llamado por señal)"""
        index = self.cbRuta.findData(id_ruta)
        if index >= 0:
            self.cbRuta.removeItem(index)
    
    # =========================================================================
    # SINCRONIZACIÓN DE COMBOS - CONDUCTORES
    # =========================================================================
    
    def agregar_conductor_a_combo(self, conductor):
        """Añade un conductor al combo (llamado por señal)"""
        self.cbConductor.addItem(
            f"{conductor.nombre} ({conductor.dni})",
            conductor.id_conductor
        )
    
    def actualizar_conductor_en_combo(self, id_conductor):
        """Actualiza un conductor en el combo (llamado por señal)"""
        index = self.cbConductor.findData(id_conductor)
        if index >= 0:
            conductor_actualizado = self.service.obtener_conductor_por_id(id_conductor)
            if conductor_actualizado:
                self.cbConductor.setItemText(
                    index,
                    f"{conductor_actualizado.nombre} ({conductor_actualizado.dni})"
                )
    
    def eliminar_conductor_de_combo(self, id_conductor):
        """Elimina un conductor del combo (llamado por señal)"""
        index = self.cbConductor.findData(id_conductor)
        if index >= 0:
            self.cbConductor.removeItem(index)
    
    # =========================================================================
    # SINCRONIZACIÓN DE COMBOS - VEHÍCULOS
    # =========================================================================
    
    def agregar_vehiculo_a_combo(self, vehiculo):
        """
        Añade un vehículo al combo (llamado por señal).
        Solo si está disponible.
        """
        if getattr(vehiculo, 'estado', 'Disponible') == "Disponible":
            self.cbVehiculo.addItem(
                f"{vehiculo.marca} {vehiculo.modelo} - {vehiculo.matricula}",
                vehiculo.id_vehiculo
            )
    
    def actualizar_vehiculo_en_combo(self, id_vehiculo):
        """
        Actualiza un vehículo en el combo (llamado por señal).
        Si cambió a no disponible, lo elimina.
        """
        index = self.cbVehiculo.findData(id_vehiculo)
        vehiculo_actualizado = self.service.obtener_vehiculo_por_id(id_vehiculo)
        
        if vehiculo_actualizado:
            estado = getattr(vehiculo_actualizado, 'estado', 'Disponible')
            
            if estado == "Disponible":
                # Actualizar o agregar
                if index >= 0:
                    self.cbVehiculo.setItemText(
                        index,
                        f"{vehiculo_actualizado.marca} {vehiculo_actualizado.modelo} - {vehiculo_actualizado.matricula}"
                    )
                else:
                    self.agregar_vehiculo_a_combo(vehiculo_actualizado)
            else:
                # Eliminar si está en el combo
                if index >= 0:
                    self.cbVehiculo.removeItem(index)
    
    def eliminar_vehiculo_de_combo(self, id_vehiculo):
        """Elimina un vehículo del combo (llamado por señal)"""
        index = self.cbVehiculo.findData(id_vehiculo)
        if index >= 0:
            self.cbVehiculo.removeItem(index)
    
    def manejar_cambio_estado_vehiculo(self, id_vehiculo, nuevo_estado):
        """
        Maneja cambios de estado de vehículos.
        Si cambia a Disponible, lo añade.
        Si cambia a otro estado, lo elimina.
        """
        index = self.cbVehiculo.findData(id_vehiculo)
        
        if nuevo_estado == "Disponible":
            if index < 0:
                vehiculo = self.service.obtener_vehiculo_por_id(id_vehiculo)
                if vehiculo:
                    self.agregar_vehiculo_a_combo(vehiculo)
        else:
            if index >= 0:
                self.cbVehiculo.removeItem(index)
    
    # =========================================================================
    # GESTIÓN DE TABLA
    # =========================================================================
    
    def cargar_tabla(self):
        """Muestra las rutas y sus asignaciones"""
        self.tableWidget.setRowCount(0)
        
        # Obtener datos del servicio
        self.rutas_en_tabla = self.service.obtener_todas_rutas()
        lista_asignaciones = self.service.obtener_todas()
        
        # Diccionario para saber qué rutas tienen asignación
        self.dic_asignaciones = {a.id_ruta: a for a in lista_asignaciones}
        
        for i, ruta in enumerate(self.rutas_en_tabla):
            self.tableWidget.insertRow(i)
            
            # Nombre de la Ruta
            self.tableWidget.setItem(i, 0, QTableWidgetItem(ruta.nombre))
            
            if ruta.id_ruta in self.dic_asignaciones:
                # Ruta asignada
                asignacion = self.dic_asignaciones[ruta.id_ruta]
                
                self.tableWidget.setItem(i, 1, QTableWidgetItem(asignacion.nombre_conductor))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(asignacion.matricula_vehiculo))
                self.tableWidget.setItem(i, 3, QTableWidgetItem("Asignada"))
            else:
                # Ruta disponible
                self.tableWidget.setItem(i, 1, QTableWidgetItem("-"))
                self.tableWidget.setItem(i, 2, QTableWidgetItem("-"))
                self.tableWidget.setItem(i, 3, QTableWidgetItem("Disponible"))
    
    def seleccionar_ruta_de_tabla(self, fila, columna):
        """Al hacer clic en la tabla, selecciona esa ruta en el combo"""
        if fila < len(self.rutas_en_tabla):
            ruta_seleccionada = self.rutas_en_tabla[fila]
            
            index = self.cbRuta.findData(ruta_seleccionada.id_ruta)
            if index >= 0:
                self.cbRuta.setCurrentIndex(index)
    
    # =========================================================================
    # CREAR ASIGNACIÓN
    # =========================================================================
    
    def registrar_asignacion(self):
        """Crea una nueva asignación"""
        # 1. Obtener datos de los combos
        id_ruta = self.cbRuta.currentData()
        nombre_ruta = self.cbRuta.currentText()
        
        id_conductor = self.cbConductor.currentData()
        nombre_conductor = self.cbConductor.currentText().split("(")[0].strip()
        
        id_vehiculo = self.cbVehiculo.currentData()
        texto_vehiculo = self.cbVehiculo.currentText()
        matricula = texto_vehiculo.split("-")[-1].strip() if "-" in texto_vehiculo else texto_vehiculo
        
        # 2. Validación básica usando el servicio
        valido, mensaje = self.service.validar_asignacion_basica(
            id_ruta, id_conductor, id_vehiculo
        )
        
        if not valido:
            QMessageBox.warning(self, "Faltan datos", mensaje)
            return
        
        # 3. Validar que la ruta esté disponible
        valido, mensaje = self.service.validar_ruta_disponible(id_ruta, nombre_ruta)
        
        if not valido:
            QMessageBox.warning(self, "Ruta Ya Asignada", mensaje)
            return
        
        # 4. Validar conductor (puede reasignarse)
        valido, mensaje, ruta_anterior = self.service.validar_conductor(
            id_conductor, nombre_conductor
        )
        
        if mensaje:  # Hay un mensaje de confirmación
            respuesta = QMessageBox.question(
                self,
                "Conductor Ya Asignado",
                mensaje,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if respuesta != QMessageBox.Yes:
                return
        
        # 5. Validar vehículo (NO puede reasignarse)
        valido, mensaje = self.service.validar_vehiculo(id_vehiculo, matricula)
        
        if not valido:
            QMessageBox.warning(self, "Vehículo Ya Asignado", mensaje)
            return
        
        # 6. Crear objeto Asignacion
        nueva_asignacion = Asignacion(
            id_ruta=id_ruta,
            nombre_ruta=nombre_ruta,
            id_conductor=id_conductor,
            nombre_conductor=nombre_conductor,
            id_vehiculo=id_vehiculo,
            matricula_vehiculo=matricula,
            fecha_inicio=self.dtInicio.dateTime().toString("dd/MM/yyyy HH:mm"),
            estado="Asignada"
        )
        
        # 7. Guardar usando el servicio
        exito, asignacion_creada, mensaje = self.service.crear_asignacion(nueva_asignacion)
        
        if exito:
            # Emitir señal
            self.asignacion_creada.emit(asignacion_creada)

            # Enviar notificacion push al conductor
            notif_ok, notif_msg = notificaciones_api.notificar_ruta_asignada(
                id_conductor, id_ruta
            )
            if notif_ok:
                QMessageBox.information(self, "Exito", "Ruta asignada correctamente. \nNotificacion enviada al conductor.")
            else:
                QMessageBox.information(self, "Exito", f"Ruta asignada correctamente. \n(Notificacion: {notif_msg})")

            # Actualizar tabla
            self.cargar_tabla()
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # ELIMINAR ASIGNACIÓN
    # =========================================================================
    
    def borrar_asignacion(self):
        """Elimina la asignación de la ruta seleccionada"""
        fila = self.tableWidget.currentRow()
        
        if fila < 0:
            QMessageBox.warning(
                self,
                "Aviso",
                "Selecciona una fila de la tabla para eliminar su asignación."
            )
            return
        
        # Verificar que la fila esté en rango
        if fila >= len(self.rutas_en_tabla):
            return
        
        ruta_seleccionada = self.rutas_en_tabla[fila]
        
        # Verificar si esa ruta tiene asignación
        if ruta_seleccionada.id_ruta not in self.dic_asignaciones:
            QMessageBox.information(
                self,
                "Info",
                "Esta ruta está libre (Disponible), no hay asignación que borrar."
            )
            return
        
        # Obtener la asignación
        asignacion_a_borrar = self.dic_asignaciones[ruta_seleccionada.id_ruta]
        
        # Confirmar
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Seguro que quieres quitar la asignación de '{ruta_seleccionada.nombre}'?\n"
            f"El conductor dejará de tener esta ruta.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        # Eliminar usando el servicio
        exito, mensaje = self.service.eliminar_asignacion(asignacion_a_borrar.id_asignacion)
        
        if exito:
            # Emitir señal
            self.asignacion_eliminada.emit(asignacion_a_borrar.id_ruta)
            
            QMessageBox.information(
                self,
                "Hecho",
                "Asignación eliminada. La ruta vuelve a estar disponible."
            )
            
            # Actualizar tabla
            self.cargar_tabla()
        else:
            QMessageBox.critical(self, "Error", mensaje)