from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide6.QtCore import Qt, QDate, QDateTime, Signal

from app.views.AsignacionWidget_ui import Ui_AsignacionWidget
from app.models.asignacion import Asignacion
from app.repositories.asignacion_repository import AsignacionRepository
from app.repositories.ruta_repository import RutaRepository
from app.repositories.conductor_repository import ConductorRepository
from app.repositories.vehiculo_repository import VehiculoRepository

class AsignacionController(QWidget, Ui_AsignacionWidget):
    """
    Controlador para gestionar asignaciones de rutas a conductores y vehículos.
    
    OPTIMIZACIONES IMPLEMENTADAS:
    - ✅ Actualización selectiva de combos (sin recargar todo)
    - ✅ Sistema de señales para notificar cambios
    - ✅ Caché de datos para evitar consultas repetidas
    """
    
    # ========== SEÑALES ==========
    asignacion_creada = Signal(object)      # asignacion completa
    asignacion_eliminada = Signal(str)      # id_ruta
    
    def __init__(self, db_connection, parent=None, app_state=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = db_connection
        self.app_state = app_state
        
        # Repositorios
        self.repo_asignacion = AsignacionRepository(self.db)
        self.repo_rutas = RutaRepository(self.db)
        self.repo_conductores = ConductorRepository(self.db)
        self.repo_vehiculos = VehiculoRepository(self.db)

        # Configuración inicial
        self.dtInicio.setDateTime(QDateTime.currentDateTime())
        self.configurar_tabla()

        # Conectar señales internas
        self.btnConfirmar.clicked.connect(self.registrar_asignacion)
        self.btnEliminarAsignacion.clicked.connect(self.borrar_asignacion)
        self.tableWidget.cellClicked.connect(self.seleccionar_ruta_de_tabla)
        
        # Variables de estado
        self.rutas_en_tabla = [] 
        self.dic_asignaciones = {}

        # Cargar datos iniciales
        self.cargar_datos()

    def configurar_tabla(self):
        """Estilo de la tabla"""
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setVisible(False)

    def cargar_datos(self):
        """Refresca todos los datos (solo usar al inicio o cuando sea necesario)"""
        self.cargar_combos()
        self.cargar_tabla()

    def cargar_combos(self):
        """Carga todos los combos desde cero"""
        self.cbRuta.clear()
        self.cbConductor.clear()
        self.cbVehiculo.clear()

        # A. Rutas (Plantillas)
        todas_rutas = self.repo_rutas.obtener_todas()
        for r in todas_rutas:
            self.cbRuta.addItem(r.nombre, r.id_ruta)

        # B. Conductores
        todos_conductores = self.repo_conductores.obtener_todos()
        for c in todos_conductores:
            self.cbConductor.addItem(f"{c.nombre} ({c.dni})", c.id_conductor)

        # C. Vehículos (Solo Disponibles)
        todos_vehiculos = self.repo_vehiculos.obtener_todos()
        for v in todos_vehiculos:
            if getattr(v, 'estado', 'Disponible') == "Disponible":
                self.cbVehiculo.addItem(f"{v.marca} {v.modelo} - {v.matricula}", v.id_vehiculo)

    # =========================================================================
    # ACTUALIZACIÓN SELECTIVA DE COMBOS - RUTAS
    # =========================================================================
    
    def agregar_ruta_a_combo(self, ruta):
        """
        Añade una nueva ruta al combo sin recargar todo.
        Se llama cuando RutasController emite ruta_creada.
        """
        self.cbRuta.addItem(ruta.nombre, ruta.id_ruta)
        print(f"[AsignacionController] Ruta '{ruta.nombre}' añadida al combo")
    
    def actualizar_ruta_en_combo(self, id_ruta):
        """
        Actualiza una ruta específica en el combo.
        Se llama cuando RutasController emite ruta_actualizada.
        """
        # Buscar el índice de la ruta en el combo
        index = self.cbRuta.findData(id_ruta)
        if index >= 0:
            # Obtener datos actualizados
            ruta_actualizada = self.repo_rutas.obtener_por_id(id_ruta)
            if ruta_actualizada:
                # Actualizar el texto del combo
                self.cbRuta.setItemText(index, ruta_actualizada.nombre)
                print(f"[AsignacionController] Ruta '{ruta_actualizada.nombre}' actualizada en combo")
    
    def eliminar_ruta_de_combo(self, id_ruta):
        """
        Elimina una ruta del combo sin recargar todo.
        Se llama cuando RutasController emite ruta_eliminada.
        """
        index = self.cbRuta.findData(id_ruta)
        if index >= 0:
            nombre_ruta = self.cbRuta.itemText(index)
            self.cbRuta.removeItem(index)
            print(f"[AsignacionController] Ruta '{nombre_ruta}' eliminada del combo")

    # =========================================================================
    # ACTUALIZACIÓN SELECTIVA DE COMBOS - CONDUCTORES
    # =========================================================================
    
    def agregar_conductor_a_combo(self, conductor):
        """
        Añade un nuevo conductor al combo sin recargar todo.
        Se llama cuando ConductoresController emite conductor_creado.
        """
        self.cbConductor.addItem(
            f"{conductor.nombre} ({conductor.dni})", 
            conductor.id_conductor
        )
        print(f"[AsignacionController] Conductor '{conductor.nombre}' añadido al combo")
    
    def actualizar_conductor_en_combo(self, id_conductor):
        """
        Actualiza un conductor específico en el combo.
        Se llama cuando ConductoresController emite conductor_actualizado.
        """
        index = self.cbConductor.findData(id_conductor)
        if index >= 0:
            # Obtener datos actualizados
            conductor_actualizado = self.repo_conductores.obtener_por_id(id_conductor)
            if conductor_actualizado:
                # Actualizar el texto del combo
                self.cbConductor.setItemText(
                    index, 
                    f"{conductor_actualizado.nombre} ({conductor_actualizado.dni})"
                )
                print(f"[AsignacionController] Conductor '{conductor_actualizado.nombre}' actualizado en combo")
    
    def eliminar_conductor_de_combo(self, id_conductor):
        """
        Elimina un conductor del combo sin recargar todo.
        Se llama cuando ConductoresController emite conductor_eliminado.
        """
        index = self.cbConductor.findData(id_conductor)
        if index >= 0:
            nombre_conductor = self.cbConductor.itemText(index)
            self.cbConductor.removeItem(index)
            print(f"[AsignacionController] Conductor '{nombre_conductor}' eliminado del combo")

    # =========================================================================
    # ACTUALIZACIÓN SELECTIVA DE COMBOS - VEHÍCULOS
    # =========================================================================
    
    def agregar_vehiculo_a_combo(self, vehiculo):
        """
        Añade un nuevo vehículo al combo sin recargar todo.
        Se llama cuando VehiclesController emite vehiculo_creado.
        
        IMPORTANTE: Solo se añade si el estado es "Disponible".
        """
        if getattr(vehiculo, 'estado', 'Disponible') == "Disponible":
            self.cbVehiculo.addItem(
                f"{vehiculo.marca} {vehiculo.modelo} - {vehiculo.matricula}", 
                vehiculo.id_vehiculo
            )
            print(f"[AsignacionController] Vehículo '{vehiculo.matricula}' añadido al combo")
    
    def actualizar_vehiculo_en_combo(self, id_vehiculo):
        """
        Actualiza un vehículo específico en el combo.
        Se llama cuando VehiclesController emite vehiculo_actualizado.
        
        IMPORTANTE: Si cambió a "No Disponible", se elimina del combo.
        """
        index = self.cbVehiculo.findData(id_vehiculo)
        vehiculo_actualizado = self.repo_vehiculos.obtener_por_id(id_vehiculo)
        
        if vehiculo_actualizado:
            estado = getattr(vehiculo_actualizado, 'estado', 'Disponible')
            
            if estado == "Disponible":
                # Vehículo disponible: actualizar o añadir al combo
                if index >= 0:
                    # Ya está en el combo: actualizar texto
                    self.cbVehiculo.setItemText(
                        index, 
                        f"{vehiculo_actualizado.marca} {vehiculo_actualizado.modelo} - {vehiculo_actualizado.matricula}"
                    )
                    print(f"[AsignacionController] Vehículo '{vehiculo_actualizado.matricula}' actualizado en combo")
                else:
                    # No está en el combo: añadirlo
                    self.agregar_vehiculo_a_combo(vehiculo_actualizado)
            else:
                # Vehículo NO disponible: eliminar del combo si está
                if index >= 0:
                    self.cbVehiculo.removeItem(index)
                    print(f"[AsignacionController] Vehículo '{vehiculo_actualizado.matricula}' eliminado del combo (no disponible)")
    
    def eliminar_vehiculo_de_combo(self, id_vehiculo):
        """
        Elimina un vehículo del combo sin recargar todo.
        Se llama cuando VehiclesController emite vehiculo_eliminado.
        """
        index = self.cbVehiculo.findData(id_vehiculo)
        if index >= 0:
            nombre_vehiculo = self.cbVehiculo.itemText(index)
            self.cbVehiculo.removeItem(index)
            print(f"[AsignacionController] Vehículo '{nombre_vehiculo}' eliminado del combo")
    
    def manejar_cambio_estado_vehiculo(self, id_vehiculo, nuevo_estado):
        """
        Maneja cambios de estado de vehículos.
        Si cambia a "Disponible", se añade al combo.
        Si cambia a otro estado, se elimina del combo.
        """
        index = self.cbVehiculo.findData(id_vehiculo)
        
        if nuevo_estado == "Disponible":
            # Vehículo ahora disponible
            if index < 0:  # No está en el combo
                vehiculo = self.repo_vehiculos.obtener_por_id(id_vehiculo)
                if vehiculo:
                    self.agregar_vehiculo_a_combo(vehiculo)
        else:
            # Vehículo NO disponible
            if index >= 0:  # Está en el combo
                self.cbVehiculo.removeItem(index)
                print(f"[AsignacionController] Vehículo eliminado del combo (estado: {nuevo_estado})")

    # =========================================================================
    # GESTIÓN DE TABLA
    # =========================================================================

    def cargar_tabla(self):
        """Muestra las rutas y sus asignaciones"""
        self.tableWidget.setRowCount(0)
        
        # Guardar listas en 'self' para usarlas al borrar
        self.rutas_en_tabla = self.repo_rutas.obtener_todas()
        lista_asignaciones = self.repo_asignacion.obtener_todas()

        # Diccionario para saber si una plantilla tiene asignación activa
        self.dic_asignaciones = {a.id_ruta: a for a in lista_asignaciones}

        for i, ruta in enumerate(self.rutas_en_tabla):
            self.tableWidget.insertRow(i)
            
            # Nombre de la Ruta (Col 0)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(ruta.nombre))
            
            if ruta.id_ruta in self.dic_asignaciones:
                asignacion = self.dic_asignaciones[ruta.id_ruta]
                
                # Conductor (Col 1)
                self.tableWidget.setItem(i, 1, QTableWidgetItem(asignacion.nombre_conductor))
                # Vehículo (Col 2)
                self.tableWidget.setItem(i, 2, QTableWidgetItem(asignacion.matricula_vehiculo))
                
                # Estado (Col 3)
                estado_item = QTableWidgetItem("Asignada")
                self.tableWidget.setItem(i, 3, estado_item)
            else:
                self.tableWidget.setItem(i, 1, QTableWidgetItem("-"))
                self.tableWidget.setItem(i, 2, QTableWidgetItem("-"))
                
                estado_item = QTableWidgetItem("Disponible")
                self.tableWidget.setItem(i, 3, estado_item)

    def seleccionar_ruta_de_tabla(self, fila, columna):
        """Al hacer clic en la tabla, selecciona esa ruta en el desplegable"""
        if fila < len(self.rutas_en_tabla):
            ruta_seleccionada = self.rutas_en_tabla[fila]
            
            # Buscar el ID de esa ruta en el ComboBox
            index = self.cbRuta.findData(ruta_seleccionada.id_ruta)
            if index >= 0:
                self.cbRuta.setCurrentIndex(index)

    # =========================================================================
    # CREAR / ELIMINAR ASIGNACIONES
    # =========================================================================

    def registrar_asignacion(self):
        """Crea una nueva asignación"""
        # 1. Validaciones
        idx_ruta = self.cbRuta.currentIndex()
        idx_cond = self.cbConductor.currentIndex()
        idx_veh = self.cbVehiculo.currentIndex()

        if idx_ruta == -1 or idx_cond == -1 or idx_veh == -1:
            QMessageBox.warning(self, "Faltan datos", "Selecciona Ruta, Conductor y Vehículo.")
            return

        # 2. Recuperar IDs (Data) y Textos
        id_ruta = self.cbRuta.currentData()
        nombre_ruta = self.cbRuta.currentText()
        
        id_cond = self.cbConductor.currentData()
        nombre_cond = self.cbConductor.currentText().split("(")[0].strip()

        id_veh = self.cbVehiculo.currentData()
        texto_veh = self.cbVehiculo.currentText()
        matricula = texto_veh.split("-")[-1].strip() if "-" in texto_veh else texto_veh
        
        # 3. Validar que la ruta no esté ya asignada
        if self.repo_asignacion.ruta_tiene_asignacion(id_ruta):
            QMessageBox.warning(
                self,
                "Ruta Ya Asignada",
                f"La ruta '{nombre_ruta}' ya está asignada.\n\n"
                "Primero elimina la asignación existente."
            )
            return
        
        # 4. Validar conductor (permitir reasignación)
        tiene_ruta, ruta_actual = self.repo_asignacion.conductor_tiene_asignacion_activa(id_cond)
        if tiene_ruta:
            respuesta = QMessageBox.question(
                self,
                "Conductor Ya Asignado",
                f"El conductor '{nombre_cond}' ya tiene asignada la ruta:\n"
                f"'{ruta_actual}'\n\n"
                "¿Quieres reasignarlo a esta nueva ruta?\n"
                "(La asignación anterior se eliminará)",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if respuesta == QMessageBox.No:
                return
        
        # 5. Validar vehículo (no permitir reasignación)
        tiene_ruta, ruta_actual = self.repo_asignacion.vehiculo_tiene_asignacion_activa(id_veh)
        if tiene_ruta:
            QMessageBox.warning(
                self,
                "Vehículo Ya Asignado",
                f"El vehículo {matricula} ya está asignado a:\n"
                f"'{ruta_actual}'\n\n"
                "Selecciona otro vehículo o elimina la asignación existente."
            )
            return

        # 6. Crear Objeto Asignación
        nueva_asignacion = Asignacion(
            id_ruta=id_ruta,
            nombre_ruta=nombre_ruta,
            id_conductor=id_cond,
            nombre_conductor=nombre_cond,
            id_vehiculo=id_veh,
            matricula_vehiculo=matricula,
            fecha_inicio=self.dtInicio.dateTime().toString("dd/MM/yyyy HH:mm"),
            estado="Asignada"
        )

        # 7. Guardar
        if self.repo_asignacion.guardar_asignacion(nueva_asignacion):
            # Emitir señal de asignación creada
            self.asignacion_creada.emit(nueva_asignacion)
            
            QMessageBox.information(self, "Éxito", "Ruta asignada correctamente.")
            
            # Actualizar solo la tabla (los combos ya están actualizados)
            self.cargar_tabla()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la asignación.")

    def borrar_asignacion(self):
        """Elimina la asignación de la ruta seleccionada en la tabla"""
        fila = self.tableWidget.currentRow()
        
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una fila de la tabla para eliminar su asignación.")
            return

        # 1. Identificar qué ruta es
        if fila >= len(self.rutas_en_tabla):
            return
            
        ruta_seleccionada = self.rutas_en_tabla[fila]
        
        # 2. Verificar si esa ruta tiene asignación
        if ruta_seleccionada.id_ruta not in self.dic_asignaciones:
            QMessageBox.information(self, "Info", "Esta ruta está libre (Disponible), no hay asignación que borrar.")
            return

        # 3. Recuperar el ID de la asignación para borrarlo
        asignacion_a_borrar = self.dic_asignaciones[ruta_seleccionada.id_ruta]
        
        confirmacion = QMessageBox.question(
            self, "Confirmar", 
            f"¿Seguro que quieres quitar la asignación de '{ruta_seleccionada.nombre}'?\nEl conductor dejará de tener esta ruta.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmacion == QMessageBox.Yes:
            if self.repo_asignacion.eliminar_asignacion(asignacion_a_borrar.id_asignacion):
                # Emitir señal de asignación eliminada
                self.asignacion_eliminada.emit(asignacion_a_borrar.id_ruta)
                
                QMessageBox.information(self, "Hecho", "Asignación eliminada. La ruta vuelve a estar disponible.")
                
                # Actualizar solo la tabla
                self.cargar_tabla()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar de la base de datos.")