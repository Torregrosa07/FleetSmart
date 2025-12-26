from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from app.views.ConductoresWidget_ui import Ui_ConductoresWidget
from app.repositories.conductor_repository import ConductorRepository
from app.controllers.ConductorDialogController import ConductorDialogController

class ConductoresController(QWidget, Ui_ConductoresWidget):
    def __init__(self, db_connection=None):
        super().__init__()
        self.setupUi(self)
        
        self.repo = None
        if db_connection:
            self.repo = ConductorRepository(db_connection)
            
        self.lista_conductores_actual = []

        self.cargar_tabla()
        self.configurar_tabla()
        
        #Conexiones de botnes
        self.btnNuevoConductor.clicked.connect(self.crear_conductor)
        self.btnBorrar.clicked.connect(self.borrar_seleccionado)
        self.btnEditar.clicked.connect(self.editar_seleccionado)
    
    def configurar_tabla(self):
        self.tablaCondcutores.horizontalHeader().setStretchLastSection(False)
        
        self.tablaCondcutores.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
   
    
    def cargar_tabla(self):
        print("Descargando lista real de Firebase...")
        
        self.lista_conductores_actual = self.repo.obtener_todos()
        
        self.tablaCondcutores.setRowCount(0)
        
        for i, conductor in enumerate(self.lista_conductores_actual):
            self.tablaCondcutores.insertRow(i)
            
            self.tablaCondcutores.setItem(i, 0, QTableWidgetItem(conductor.nombre))
            self.tablaCondcutores.setItem(i, 1, QTableWidgetItem(conductor.dni)) 
            self.tablaCondcutores.setItem(i, 2, QTableWidgetItem(conductor.licencia)) 
            self.tablaCondcutores.setItem(i, 3, QTableWidgetItem(conductor.estado))
            self.tablaCondcutores.setItem(i, 4, QTableWidgetItem(str(conductor.email)))
            self.tablaCondcutores.setItem(i, 5, QTableWidgetItem(str(conductor.telefono))) 
            
    def obtener_conductor_seleccionado(self):
        """Método auxiliar para saber qué conductor ha clicado el usuario"""
        fila_actual = self.tablaCondcutores.currentRow()
        
        if fila_actual == -1:
            QMessageBox.warning(self, "Aviso", "Por favor, selecciona un conductor de la tabla.")
            return None
            
        # Gracias a que guardamos la lista en el mismo orden que la tabla:
        return self.lista_conductores_actual[fila_actual]

    def borrar_seleccionado(self):
        conductor = self.obtener_conductor_seleccionado()
        if not conductor: return

        confirmacion = QMessageBox.question(
            self, "Borrar", 
            f"¿Seguro que quieres borrar el {conductor.nombre} con DNI: {conductor.dni}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmacion == QMessageBox.Yes:
            if self.repo.eliminar_conductor(conductor.id_conductor):
                self.cargar_tabla() # Recargar
            else:
                QMessageBox.critical(self, "Error", "No se pudo borrar.")

    def editar_seleccionado(self):
        conductor = self.obtener_conductor_seleccionado()
        if not conductor: return

        # Abrimos el diálogo pasándole el coche existente
        dialog = ConductorDialogController(self, conductor_a_editar=conductor)
        
        if dialog.exec():
            datos_actualizados = dialog.datos_conductor
            # Llamamos al método de actualizar en vez de guardar nuevo
            if self.repo.actualizar_conductor(datos_actualizados):
                self.cargar_tabla()
            else:
                QMessageBox.critical(self, "Error", "Fallo al actualizar.")

    def crear_conductor(self):
        dialog = ConductorDialogController(self)
        if dialog.exec():
            nuevo = dialog.datos_conductor
            if self.repo.guardar_nuevo_conductor(nuevo):
                self.cargar_tabla()
            else:
                QMessageBox.critical(self, "Error", "Fallo al guardar.")