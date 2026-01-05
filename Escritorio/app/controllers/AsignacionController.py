from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide6.QtCore import Qt, QDate, QDateTime

from app.views.AsignacionWidget_ui import Ui_AsignacionWidget
from app.models.asignacion import Asignacion
from app.repositories.asignacion_repository import AsignacionRepository
from app.repositories.ruta_repository import RutaRepository
from app.repositories.conductor_repository import ConductorRepository
from app.repositories.vehiculo_repository import VehiculoRepository

class AsignacionController(QWidget, Ui_AsignacionWidget):
    def __init__(self, db_connection, parent=None, app_state=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = db_connection
        self.app_state = app_state
        
        
        # 1. Inicializar Repositorios
        self.repo_asignacion = AsignacionRepository(self.db)
        self.repo_rutas = RutaRepository(self.db)
        self.repo_conductores = ConductorRepository(self.db)
        self.repo_vehiculos = VehiculoRepository(self.db)

        # 2. Configuración UI
        self.dtInicio.setDateTime(QDateTime.currentDateTime())
        self.configurar_tabla()

        # 3. Conexiones
        self.btnConfirmar.clicked.connect(self.registrar_asignacion)
        
        # AQUI ESTÁ EL CAMBIO IMPORTANTE: Conectamos el botón con su nombre real
        self.btnEliminarAsignacion.clicked.connect(self.borrar_asignacion)
        
        # Magia: Al clicar en la tabla, se selecciona en el combo
        self.tableWidget.cellClicked.connect(self.seleccionar_ruta_de_tabla)
        
        # 4. Variables de memoria (Vitales para saber qué borrar)
        self.rutas_en_tabla = [] 
        self.dic_asignaciones = {}

        # 5. Carga inicial
        self.cargar_datos()
        


    def configurar_tabla(self):
        """Estilo de la tabla"""
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.verticalHeader().setVisible(False)

    def cargar_datos(self):
        """Refresca todos los datos"""
        self.cargar_combos()
        self.cargar_tabla()

    def cargar_combos(self):
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

    def cargar_tabla(self):
        """Muestra las rutas y sus asignaciones"""
        self.tableWidget.setRowCount(0)
        
        # CAMBIO VITAL: Guardamos las listas en 'self' para usarlas al borrar
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
        # Usamos la lista guardada en memoria para estar seguros del índice
        if fila < len(self.rutas_en_tabla):
            ruta_seleccionada = self.rutas_en_tabla[fila]
            
            # Buscamos el ID de esa ruta en el ComboBox
            index = self.cbRuta.findData(ruta_seleccionada.id_ruta)
            if index >= 0:
                self.cbRuta.setCurrentIndex(index)

    def registrar_asignacion(self):
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
        
        
        
        if self.repo_asignacion.ruta_tiene_asignacion(id_ruta):
            QMessageBox.warning(
                self,
                "Ruta Ya Asignada",
                f"La ruta '{nombre_ruta}' ya está asignada.\n\n"
                "Primero elimina la asignación existente."
            )
            return
        
        
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

            
        # 3. Crear Objeto Asignación
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

        # 4. Guardar
        if self.repo_asignacion.guardar_asignacion(nueva_asignacion):
            QMessageBox.information(self, "Éxito", "Ruta asignada correctamente.")
            self.cargar_datos() 
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la asignación.")
            
            
            

    def borrar_asignacion(self):
        """Elimina la asignación de la ruta seleccionada en la tabla"""
        fila = self.tableWidget.currentRow()
        
        if fila < 0:
            QMessageBox.warning(self, "Aviso", "Selecciona una fila de la tabla para eliminar su asignación.")
            return

        # 1. Identificar qué ruta es (usando la lista guardada en self)
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
                QMessageBox.information(self, "Hecho", "Asignación eliminada. La ruta vuelve a estar disponible.")
                self.cargar_datos() 
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar de la base de datos.")