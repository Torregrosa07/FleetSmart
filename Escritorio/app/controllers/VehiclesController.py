from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from app.views.VehiculosWidget_ui import Ui_VehiculosWidget
from app.repositories.vehiculo_repository import VehiculoRepository
from app.controllers.VehiculoDialogController import VehiculoDialogController

class VehiclesController(QWidget, Ui_VehiculosWidget):
    def __init__(self, db_connection=None):
        super().__init__()
        self.setupUi(self)
        
        self.repo = None
        if db_connection:
            self.repo = VehiculoRepository(db_connection)
            
        self.lista_vehiculos_actual = []

        self.cargar_tabla()
        self.configurar_tabla()
        
        #Conexiones de botnes
        self.btnNuevoVehiculo.clicked.connect(self.crear_vehiculo)
        self.btnBorrar.clicked.connect(self.borrar_seleccionado)
        self.btnEditar.clicked.connect(self.editar_seleccionado)
    
    def configurar_tabla(self):
        self.tablaVehiculos.horizontalHeader().setStretchLastSection(False)
        
        self.tablaVehiculos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
   
    
    def cargar_tabla(self):
        print("Descargando lista real de Firebase...")
        
        self.lista_vehiculos_actual = self.repo.obtener_todos()
        
        self.tablaVehiculos.setRowCount(0)
        
        for i, coche in enumerate(self.lista_vehiculos_actual):
            self.tablaVehiculos.insertRow(i)
            
            self.tablaVehiculos.setItem(i, 0, QTableWidgetItem(coche.matricula))
            self.tablaVehiculos.setItem(i, 1, QTableWidgetItem(coche.marca)) 
            self.tablaVehiculos.setItem(i, 2, QTableWidgetItem(coche.modelo)) 
            self.tablaVehiculos.setItem(i, 3, QTableWidgetItem(coche.estado))
            self.tablaVehiculos.setItem(i, 4, QTableWidgetItem(str(coche.ano)))
            self.tablaVehiculos.setItem(i, 5, QTableWidgetItem(str(coche.proxima_itv))) 
            
    def obtener_vehiculo_seleccionado(self):
        """Método auxiliar para saber qué coche ha clicado el usuario"""
        fila_actual = self.tablaVehiculos.currentRow()
        
        if fila_actual == -1:
            QMessageBox.warning(self, "Aviso", "Por favor, selecciona un vehículo de la tabla.")
            return None
            
        # Gracias a que guardamos la lista en el mismo orden que la tabla:
        return self.lista_vehiculos_actual[fila_actual]

    def borrar_seleccionado(self):
        vehiculo = self.obtener_vehiculo_seleccionado()
        if not vehiculo: return

        confirmacion = QMessageBox.question(
            self, "Borrar", 
            f"¿Seguro que quieres borrar el {vehiculo.marca} {vehiculo.modelo}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmacion == QMessageBox.Yes:
            if self.repo.eliminar_vehiculo(vehiculo.id_vehiculo):
                self.cargar_tabla() # Recargar
            else:
                QMessageBox.critical(self, "Error", "No se pudo borrar.")

    def editar_seleccionado(self):
        vehiculo = self.obtener_vehiculo_seleccionado()
        if not vehiculo: return

        # Abrimos el diálogo pasándole el coche existente
        dialog = VehiculoDialogController(self, vehiculo_a_editar=vehiculo)
        
        if dialog.exec():
            datos_actualizados = dialog.datos_vehiculo
            # Llamamos al método de actualizar en vez de guardar nuevo
            if self.repo.actualizar_vehiculo(datos_actualizados):
                self.cargar_tabla()
            else:
                QMessageBox.critical(self, "Error", "Fallo al actualizar.")

    def crear_vehiculo(self):
        dialog = VehiculoDialogController(self)
        if dialog.exec():
            nuevo = dialog.datos_vehiculo
            if self.repo.guardar_nuevo_vehiculo(nuevo):
                self.cargar_tabla()
            else:
                QMessageBox.critical(self, "Error", "Fallo al guardar.")