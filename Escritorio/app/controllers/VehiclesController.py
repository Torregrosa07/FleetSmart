
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Signal

from app.views.VehiculosWidget_ui import Ui_VehiculosWidget
from app.controllers.VehiculoDialogController import VehiculoDialogController
from app.services.vehiculos_service import VehiculosService
from app.utils.language_utils import LanguageService
class VehiclesController(QWidget, Ui_VehiculosWidget):
    
    # ========== SEÑALES ==========
    vehiculo_creado = Signal(object)
    vehiculo_actualizado = Signal(str)
    vehiculo_eliminado = Signal(str)
    vehiculo_estado_cambiado = Signal(str, str)
    
    def __init__(self, db_connection=None, app_state=None):
        super().__init__()
        self.setupUi(self)
        self.app_state = app_state
        
        # Servicio de lógica de negocio
        self.service = VehiculosService(db_connection)
        
        # Lista y caché local
        self.lista_vehiculos = []
        self.cache_vehiculos = {}
        
        # Configuración inicial
        self.configurar_tabla()
        self.cargar_tabla()
        self.conectar_botones()
    
    # =========================================================================
    # CONFIGURACIÓN INICIAL
    # =========================================================================
    
    def configurar_tabla(self):
        """Configura el estilo de la tabla"""
        self.tablaVehiculos.horizontalHeader().setStretchLastSection(False)
        self.tablaVehiculos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def conectar_botones(self):
        """Conecta botones con sus métodos"""
        self.btnNuevoVehiculo.clicked.connect(self.crear_vehiculo)
        self.btnBorrar.clicked.connect(self.borrar_vehiculo)
        self.btnEditar.clicked.connect(self.editar_vehiculo)
    
    # =========================================================================
    # TRADUCCIÓN DE INTERFAZ
    # =========================================================================
    
    def actualizar_idioma(self, idioma):
        """Traduce la interfaz de vehículos"""
        # Traducir etiquetas y botones
        self.label_4.setText(LanguageService.get_text("vehicles", idioma))
        self.btnNuevoVehiculo.setText("+ " + LanguageService.get_text("new", idioma))
        self.btnEditar.setText(LanguageService.get_text("edit", idioma))
        self.btnBorrar.setText(LanguageService.get_text("delete", idioma))
        
        # Traducir cabeceras de la tabla
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
    
    # =========================================================================
    # GESTIÓN DE TABLA
    # =========================================================================
    
    def cargar_tabla(self):
        """Carga todos los vehículos desde el servicio"""
        # Obtener datos del servicio
        self.lista_vehiculos = self.service.obtener_todos()
        self.cache_vehiculos = {v.id_vehiculo: v for v in self.lista_vehiculos}
        
        # Limpiar tabla
        self.tablaVehiculos.setRowCount(0)
        
        # Llenar tabla
        for i, vehiculo in enumerate(self.lista_vehiculos):
            self.tablaVehiculos.insertRow(i)
            self.llenar_fila(i, vehiculo)
    
    def llenar_fila(self, fila, vehiculo):
        """Llena una fila de la tabla con datos de un vehículo"""
        self.tablaVehiculos.setItem(fila, 0, QTableWidgetItem(vehiculo.matricula))
        self.tablaVehiculos.setItem(fila, 1, QTableWidgetItem(vehiculo.marca))
        self.tablaVehiculos.setItem(fila, 2, QTableWidgetItem(vehiculo.modelo))
        self.tablaVehiculos.setItem(fila, 3, QTableWidgetItem(vehiculo.estado))
        self.tablaVehiculos.setItem(fila, 4, QTableWidgetItem(str(vehiculo.ano)))
        self.tablaVehiculos.setItem(fila, 5, QTableWidgetItem(str(vehiculo.proxima_itv)))
    
    def agregar_a_tabla(self, vehiculo):
        """Agrega un vehículo a la tabla sin recargar todo"""
        self.lista_vehiculos.append(vehiculo)
        self.cache_vehiculos[vehiculo.id_vehiculo] = vehiculo
        
        nueva_fila = self.tablaVehiculos.rowCount()
        self.tablaVehiculos.insertRow(nueva_fila)
        self.llenar_fila(nueva_fila, vehiculo)
    
    def actualizar_en_tabla(self, fila, vehiculo):
        """Actualiza una fila específica"""
        self.lista_vehiculos[fila] = vehiculo
        self.cache_vehiculos[vehiculo.id_vehiculo] = vehiculo
        self.llenar_fila(fila, vehiculo)
    
    def eliminar_de_tabla(self, id_vehiculo):
        """Elimina un vehículo de la tabla"""
        # Buscar fila
        fila = None
        for i, vehiculo in enumerate(self.lista_vehiculos):
            if vehiculo.id_vehiculo == id_vehiculo:
                fila = i
                break
        
        if fila is None:
            return
        
        # Eliminar de lista y caché
        del self.lista_vehiculos[fila]
        if id_vehiculo in self.cache_vehiculos:
            del self.cache_vehiculos[id_vehiculo]
        
        # Eliminar fila de tabla
        self.tablaVehiculos.removeRow(fila)
    
    # =========================================================================
    # OBTENER SELECCIÓN
    # =========================================================================
    
    def obtener_seleccionado(self):
        """Devuelve el vehículo seleccionado o None"""
        fila = self.tablaVehiculos.currentRow()
        
        if fila == -1:
            QMessageBox.warning(self, "Aviso", "Selecciona un vehículo de la tabla.")
            return None
        
        return self.lista_vehiculos[fila]
    
    # =========================================================================
    # CREAR VEHÍCULO
    # =========================================================================
    
    def crear_vehiculo(self):
        """Crea un nuevo vehículo"""
        # 1. Abrir diálogo para capturar datos
        dialog = VehiculoDialogController(self)
        if not dialog.exec():
            return
        
        vehiculo = dialog.datos_vehiculo
        
        # 2. Validar ANTES de guardar
        valido, mensaje_error = self.service.validar_vehiculo(vehiculo)
        if not valido:
            QMessageBox.warning(self, "Datos Inválidos", mensaje_error)
            return
        
        # 3. Crear usando el servicio
        exito, vehiculo_creado, mensaje = self.service.crear_vehiculo(vehiculo)
        
        # 4. Manejar resultado
        if exito:
            # Agregar a tabla
            self.agregar_a_tabla(vehiculo_creado)
            
            # Emitir señal
            self.vehiculo_creado.emit(vehiculo_creado)
            
            QMessageBox.information(self, "Éxito", "Vehículo creado correctamente.")
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # EDITAR VEHÍCULO
    # =========================================================================
    
    def editar_vehiculo(self):
        """Edita un vehículo existente"""
        # 1. Obtener vehículo seleccionado
        vehiculo = self.obtener_seleccionado()
        if not vehiculo:
            return
        
        fila_actual = self.tablaVehiculos.currentRow()
        estado_anterior = vehiculo.estado
        
        # 2. Abrir diálogo
        dialog = VehiculoDialogController(self, vehiculo_a_editar=vehiculo)
        if not dialog.exec():
            return
        
        vehiculo_editado = dialog.datos_vehiculo
        
        # 3. Validar ANTES de actualizar
        valido, mensaje_error = self.service.validar_vehiculo(vehiculo_editado)
        if not valido:
            QMessageBox.warning(self, "Datos Inválidos", mensaje_error)
            return
        
        # 4. Actualizar usando el servicio
        exito, mensaje = self.service.actualizar_vehiculo(vehiculo_editado)
        
        # 5. Manejar resultado
        if exito:
            # Actualizar tabla
            self.actualizar_en_tabla(fila_actual, vehiculo_editado)
            
            # Emitir señales
            self.vehiculo_actualizado.emit(vehiculo_editado.id_vehiculo)
            
            # Si cambió el estado, emitir señal
            if estado_anterior != vehiculo_editado.estado:
                self.vehiculo_estado_cambiado.emit(
                    vehiculo_editado.id_vehiculo,
                    vehiculo_editado.estado
                )
            
            QMessageBox.information(self, "Éxito", "Vehículo actualizado correctamente.")
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # BORRAR VEHÍCULO
    # =========================================================================
    
    def borrar_vehiculo(self):
        """Borra un vehículo"""
        # 1. Obtener vehículo seleccionado
        vehiculo = self.obtener_seleccionado()
        if not vehiculo:
            return
        
        # 2. Confirmar
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Seguro que quieres borrar el {vehiculo.marca} {vehiculo.modelo}?\n\n"
            f"Matrícula: {vehiculo.matricula}\n\n"
            f"⚠️ Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        # 3. Eliminar usando el servicio
        exito, mensaje = self.service.eliminar_vehiculo(vehiculo.id_vehiculo)
        
        # 4. Manejar resultado
        if exito:
            # Eliminar de tabla
            self.eliminar_de_tabla(vehiculo.id_vehiculo)
            
            # Emitir señal
            self.vehiculo_eliminado.emit(vehiculo.id_vehiculo)
            
            QMessageBox.information(self, "Éxito", "Vehículo eliminado correctamente.")
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # SINCRONIZACIÓN CON OTRAS VISTAS
    # =========================================================================
    
    def sincronizar_desde_asignacion(self, id_vehiculo, nuevo_estado):
        """Actualiza el estado cuando cambia desde otra vista"""
        if id_vehiculo in self.cache_vehiculos:
            vehiculo = self.cache_vehiculos[id_vehiculo]
            
            if vehiculo.estado != nuevo_estado:
                vehiculo.estado = nuevo_estado
                
                # Buscar y actualizar fila
                for i, v in enumerate(self.lista_vehiculos):
                    if v.id_vehiculo == id_vehiculo:
                        self.llenar_fila(i, vehiculo)
                        break
    
    def recargar_vehiculo_especifico(self, id_vehiculo):
        """Recarga un vehículo específico desde Firebase"""
        vehiculo_actualizado = self.service.obtener_por_id(id_vehiculo)
        if not vehiculo_actualizado:
            return
        
        # Buscar y actualizar fila
        for i, v in enumerate(self.lista_vehiculos):
            if v.id_vehiculo == id_vehiculo:
                self.actualizar_en_tabla(i, vehiculo_actualizado)
                break