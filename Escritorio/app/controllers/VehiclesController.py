from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Signal
from app.views.VehiculosWidget_ui import Ui_VehiculosWidget
from app.repositories.vehiculo_repository import VehiculoRepository
from app.services.language_service import LanguageService
from app.controllers.VehiculoDialogController import VehiculoDialogController

class VehiclesController(QWidget, Ui_VehiculosWidget):
    
    # ========== SEÑALES ==========
    # Se emiten para mantener sincronizadas otras vistas (AsignacionController, IncidenciasController, etc)
    vehiculo_creado = Signal(object)           # vehiculo completo
    vehiculo_actualizado = Signal(str)         # id_vehiculo
    vehiculo_eliminado = Signal(str)           # id_vehiculo
    vehiculo_estado_cambiado = Signal(str, str)  # id_vehiculo, nuevo_estado
    
    def __init__(self, db_connection=None, app_state=None):
        super().__init__()
        self.setupUi(self)
        self.app_state = app_state
        
        self.repo = None
        if db_connection:
            self.repo = VehiculoRepository(db_connection)
            
        self.lista_vehiculos_actual = []
        
        # Cache para detectar cambios reales y evitar actualizaciones innecesarias
        self.cache_vehiculos = {}

        self.cargar_tabla()
        self.configurar_tabla()
        
        # Conexiones de botones
        self.btnNuevoVehiculo.clicked.connect(self.crear_vehiculo)
        self.btnBorrar.clicked.connect(self.borrar_seleccionado)
        self.btnEditar.clicked.connect(self.editar_seleccionado)
        
        
    def actualizar_idioma(self, idioma):
        """Traduce la interfaz de vehículos"""
        
        # 1. Traducir etiquetas y botones
        self.label_4.setText(LanguageService.get_text("vehicles", idioma))
        self.btnNuevoVehiculo.setText("+ " + LanguageService.get_text("new", idioma))
        self.btnEditar.setText(LanguageService.get_text("edit", idioma))
        self.btnBorrar.setText(LanguageService.get_text("delete", idioma))
        
        # 2. Traducir Cabeceras de la Tabla
        claves_columnas = {
            0: "license_plate",
            1: "brand",
            2: "model",
            3: "status",
            4: "year",
            5: "ITV"
        }

        for col, clave in claves_columnas.items():
            texto = LanguageService.get_text(clave, idioma)
            item = self.tablaVehiculos.horizontalHeaderItem(col)
            if item:
                item.setText(texto)
        
        
        
    def configurar_tabla(self):
        self.tablaVehiculos.horizontalHeader().setStretchLastSection(False)
        self.tablaVehiculos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
   
    
    def cargar_tabla(self):
        """Carga todos los vehículos y actualiza el caché"""
        
        self.lista_vehiculos_actual = self.repo.obtener_todos()
        
        # Actualizar caché
        self.cache_vehiculos = {v.id_vehiculo: v for v in self.lista_vehiculos_actual}
        
        self.tablaVehiculos.setRowCount(0)
        
        for i, coche in enumerate(self.lista_vehiculos_actual):
            self.tablaVehiculos.insertRow(i)
            self._llenar_fila_tabla(i, coche)
    
    def _llenar_fila_tabla(self, fila, vehiculo):
        """Método auxiliar para llenar una fila específica de la tabla"""
        self.tablaVehiculos.setItem(fila, 0, QTableWidgetItem(vehiculo.matricula))
        self.tablaVehiculos.setItem(fila, 1, QTableWidgetItem(vehiculo.marca)) 
        self.tablaVehiculos.setItem(fila, 2, QTableWidgetItem(vehiculo.modelo)) 
        self.tablaVehiculos.setItem(fila, 3, QTableWidgetItem(vehiculo.estado))
        self.tablaVehiculos.setItem(fila, 4, QTableWidgetItem(str(vehiculo.ano)))
        self.tablaVehiculos.setItem(fila, 5, QTableWidgetItem(str(vehiculo.proxima_itv)))
    
    def actualizar_fila_vehiculo_con_datos(self, fila, vehiculo_actualizado):
        """
        Actualiza una fila específica con datos ya proporcionados.
        Más eficiente que obtener desde Firebase.
        """
        # Actualizar en lista y caché
        self.lista_vehiculos_actual[fila] = vehiculo_actualizado
        self.cache_vehiculos[vehiculo_actualizado.id_vehiculo] = vehiculo_actualizado
        
        # Actualizar solo esa fila en la tabla
        self._llenar_fila_tabla(fila, vehiculo_actualizado)
    
    def actualizar_fila_vehiculo(self, id_vehiculo):
        """
        Actualiza selectivamente una fila de la tabla cuando cambia un vehículo.
        MUCHO más eficiente que recargar toda la tabla.
        """
        # Buscar la fila del vehículo
        fila = None
        for i, vehiculo in enumerate(self.lista_vehiculos_actual):
            if vehiculo.id_vehiculo == id_vehiculo:
                fila = i
                break
        
        if fila is None:
            return
        
        # Obtener datos actualizados del repositorio
        vehiculo_actualizado = self.repo.obtener_por_id(id_vehiculo)
        if not vehiculo_actualizado:
            return
        
        # Actualizar usando el método auxiliar
        self.actualizar_fila_vehiculo_con_datos(fila, vehiculo_actualizado)
    
    def agregar_vehiculo_a_tabla(self, vehiculo):
        """
        Agrega un nuevo vehículo a la tabla sin recargar todo.
        Se llama cuando se crea un vehículo.
        """
        # Agregar a la lista y caché
        self.lista_vehiculos_actual.append(vehiculo)
        self.cache_vehiculos[vehiculo.id_vehiculo] = vehiculo
        
        # Agregar nueva fila a la tabla
        nueva_fila = self.tablaVehiculos.rowCount()
        self.tablaVehiculos.insertRow(nueva_fila)
        self._llenar_fila_tabla(nueva_fila, vehiculo)
    
    def eliminar_vehiculo_de_tabla(self, id_vehiculo):
        """
        Elimina un vehículo de la tabla sin recargar todo.
        Se llama cuando se borra un vehículo.
        """
        # Buscar la fila del vehículo
        fila = None
        for i, vehiculo in enumerate(self.lista_vehiculos_actual):
            if vehiculo.id_vehiculo == id_vehiculo:
                fila = i
                break
        
        if fila is None:
            return
        
        # Eliminar de lista y caché
        del self.lista_vehiculos_actual[fila]
        if id_vehiculo in self.cache_vehiculos:
            del self.cache_vehiculos[id_vehiculo]
        
        # Eliminar fila de la tabla
        self.tablaVehiculos.removeRow(fila)
            
    def obtener_vehiculo_seleccionado(self):
        """Método auxiliar para saber qué coche ha clicado el usuario"""
        fila_actual = self.tablaVehiculos.currentRow()
        
        if fila_actual == -1:
            QMessageBox.warning(self, "Aviso", "Por favor, selecciona un vehículo de la tabla.")
            return None
            
        return self.lista_vehiculos_actual[fila_actual]

    def borrar_seleccionado(self):
        vehiculo = self.obtener_vehiculo_seleccionado()
        if not vehiculo: 
            return

        confirmacion = QMessageBox.question(
            self, "Borrar", 
            f"¿Seguro que quieres borrar el {vehiculo.marca} {vehiculo.modelo}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmacion == QMessageBox.Yes:
            id_vehiculo = vehiculo.id_vehiculo
            
            if self.repo.eliminar_vehiculo(id_vehiculo):
                # Actualización selectiva: eliminar solo esta fila
                self.eliminar_vehiculo_de_tabla(id_vehiculo)
                
                # Emitir señal para notificar a otras vistas
                self.vehiculo_eliminado.emit(id_vehiculo)
                
                QMessageBox.information(self, "Éxito", "Vehículo eliminado correctamente.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo borrar.")

    def editar_seleccionado(self):
        vehiculo = self.obtener_vehiculo_seleccionado()
        if not vehiculo: 
            return
        
        # Guardamos la fila actual antes de abrir el diálogo
        fila_actual = self.tablaVehiculos.currentRow()

        # Abrimos el diálogo pasándole el coche existente
        dialog = VehiculoDialogController(self, vehiculo_a_editar=vehiculo)
        
        if dialog.exec():
            datos_actualizados = dialog.datos_vehiculo
            id_vehiculo = datos_actualizados.id_vehiculo
            
            # Detectar si cambió el estado
            estado_anterior = vehiculo.estado
            estado_nuevo = datos_actualizados.estado
            cambio_estado = (estado_anterior != estado_nuevo)
            
            # Llamamos al método de actualizar en vez de guardar nuevo
            if self.repo.actualizar_vehiculo(datos_actualizados):
                # Actualización selectiva usando los datos que ya tenemos
                # Es más eficiente que volver a consultar Firebase
                self.actualizar_fila_vehiculo_con_datos(fila_actual, datos_actualizados)
                
                # Emitir señales
                self.vehiculo_actualizado.emit(id_vehiculo)
                
                if cambio_estado:
                    self.vehiculo_estado_cambiado.emit(id_vehiculo, estado_nuevo)
                
                QMessageBox.information(self, "Éxito", "Vehículo actualizado correctamente.")
            else:
                QMessageBox.critical(self, "Error", "Fallo al actualizar.")

    def crear_vehiculo(self):
        dialog = VehiculoDialogController(self)
        if dialog.exec():
            nuevo = dialog.datos_vehiculo
            if self.repo.guardar_nuevo_vehiculo(nuevo):
                # Actualización selectiva: agregar solo este vehículo
                self.agregar_vehiculo_a_tabla(nuevo)
                
                # Emitir señal con el objeto completo para que otras vistas lo tengan
                self.vehiculo_creado.emit(nuevo)
                
                QMessageBox.information(self, "Éxito", "Vehículo creado correctamente.")
            else:
                QMessageBox.critical(self, "Error", "Fallo al guardar.")
    
    # ========== MÉTODOS PÚBLICOS PARA SINCRONIZACIÓN ==========
    # Estos métodos pueden ser llamados desde otras vistas mediante señales
    
    def sincronizar_desde_asignacion(self, id_vehiculo, nuevo_estado):
        """
        Método que puede ser llamado cuando AsignacionController cambia el estado
        de un vehículo (por ejemplo, de Disponible a En Uso).
        """
        # Actualizar en caché
        if id_vehiculo in self.cache_vehiculos:
            vehiculo_cache = self.cache_vehiculos[id_vehiculo]
            
            # Solo actualizar si realmente cambió
            if vehiculo_cache.estado != nuevo_estado:
                vehiculo_cache.estado = nuevo_estado
                self.actualizar_fila_vehiculo(id_vehiculo)
    
    def recargar_vehiculo_especifico(self, id_vehiculo):
        """
        Recarga un vehículo específico desde Firebase.
        Útil cuando otra vista modifica un vehículo externamente.
        """
        self.actualizar_fila_vehiculo(id_vehiculo)