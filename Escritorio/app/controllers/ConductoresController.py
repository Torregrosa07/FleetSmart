"""
ConductoresController - Versión refactorizada simple

RESPONSABILIDADES:
- Manejo de UI (botones, tabla, diálogos)
- Delegar lógica de negocio al servicio
- Emitir señales para sincronización

Código simple sin lambdas ni funciones complejas.
"""
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView

from app.views.ConductoresWidget_ui import Ui_ConductoresWidget
from app.controllers.ConductorDialogController import ConductorDialogController
from app.services.conductores_service import ConductoresService
from app.utils.language_utils import LanguageService


class ConductoresController(QWidget, Ui_ConductoresWidget):
    """
    Controlador simplificado que delega lógica al servicio.
    """
    
    # ========== SEÑALES ==========
    conductor_creado = Signal(object)
    conductor_actualizado = Signal(str)
    conductor_eliminado = Signal(str)
    conductor_estado_cambiado = Signal(str, str)
    
    def __init__(self, db_connection=None):
        super().__init__()
        self.setupUi(self)
        
        # Servicio de lógica de negocio
        self.service = ConductoresService(db_connection)
        
        # Lista y caché local
        self.lista_conductores = []
        self.cache_conductores = {}
        
        # Configuración inicial
        self.configurar_tabla()
        self.cargar_tabla()
        self.conectar_botones()
    
    # =========================================================================
    # CONFIGURACIÓN INICIAL
    # =========================================================================
    
    def configurar_tabla(self):
        """Configura el estilo de la tabla"""
        self.tablaCondcutores.horizontalHeader().setStretchLastSection(False)
        self.tablaCondcutores.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def conectar_botones(self):
        """Conecta botones con sus métodos"""
        self.btnNuevoConductor.clicked.connect(self.crear_conductor)
        self.btnBorrar.clicked.connect(self.borrar_conductor)
        self.btnEditar.clicked.connect(self.editar_conductor)

    # =========================================================================
    # TRADUCCION DE INTERFAZ
    # =========================================================================

    def actualizar_idioma(self, idioma):
        """Traduce la interfaz de conductores"""
        self.label_4.setText(LanguageService.get_text("drivers", idioma))
        self.btnNuevoConductor.setText("+ " + LanguageService.get_text("new", idioma))
        self.btnEditar.setText(LanguageService.get_text("edit", idioma))
        self.btnBorrar.setText(LanguageService.get_text("delete", idioma))

        claves_columnas = {
            0: "name",
            1: "dni",
            2: "license",
            3: "status",
            4: "email",
            5: "phone"
        }

        for col, clave in claves_columnas.items():
            texto = LanguageService.get_text(clave, idioma)
            item = self.tablaCondcutores.horizontalHeaderItem(col)
            if item:
                item.setText(texto)
    
    # =========================================================================
    # GESTIÓN DE TABLA
    # =========================================================================
    
    def cargar_tabla(self):
        """Carga todos los conductores desde el servicio"""
        # Obtener datos del servicio
        self.lista_conductores = self.service.obtener_todos()
        self.cache_conductores = {c.id_conductor: c for c in self.lista_conductores}
        
        # Limpiar tabla
        self.tablaCondcutores.setRowCount(0)
        
        # Llenar tabla
        for i, conductor in enumerate(self.lista_conductores):
            self.tablaCondcutores.insertRow(i)
            self.llenar_fila(i, conductor)
    
    def llenar_fila(self, fila, conductor):
        """Llena una fila de la tabla con datos de un conductor"""
        self.tablaCondcutores.setItem(fila, 0, QTableWidgetItem(conductor.nombre))
        self.tablaCondcutores.setItem(fila, 1, QTableWidgetItem(conductor.dni))
        self.tablaCondcutores.setItem(fila, 2, QTableWidgetItem(conductor.licencia))
        self.tablaCondcutores.setItem(fila, 3, QTableWidgetItem(conductor.estado))
        self.tablaCondcutores.setItem(fila, 4, QTableWidgetItem(conductor.email))
        self.tablaCondcutores.setItem(fila, 5, QTableWidgetItem(conductor.telefono))
    
    def agregar_a_tabla(self, conductor):
        """Agrega un conductor a la tabla sin recargar todo"""
        self.lista_conductores.append(conductor)
        self.cache_conductores[conductor.id_conductor] = conductor
        
        nueva_fila = self.tablaCondcutores.rowCount()
        self.tablaCondcutores.insertRow(nueva_fila)
        self.llenar_fila(nueva_fila, conductor)
    
    def actualizar_en_tabla(self, fila, conductor):
        """Actualiza una fila específica"""
        self.lista_conductores[fila] = conductor
        self.cache_conductores[conductor.id_conductor] = conductor
        self.llenar_fila(fila, conductor)
    
    def eliminar_de_tabla(self, id_conductor):
        """Elimina un conductor de la tabla"""
        # Buscar fila
        fila = None
        for i, conductor in enumerate(self.lista_conductores):
            if conductor.id_conductor == id_conductor:
                fila = i
                break
        
        if fila is None:
            return
        
        # Eliminar de lista y caché
        del self.lista_conductores[fila]
        if id_conductor in self.cache_conductores:
            del self.cache_conductores[id_conductor]
        
        # Eliminar fila de tabla
        self.tablaCondcutores.removeRow(fila)
    
    # =========================================================================
    # OBTENER SELECCIÓN
    # =========================================================================
    
    def obtener_seleccionado(self):
        """Devuelve el conductor seleccionado o None"""
        fila = self.tablaCondcutores.currentRow()
        
        if fila == -1:
            QMessageBox.warning(self, "Aviso", "Selecciona un conductor de la tabla.")
            return None
        
        return self.lista_conductores[fila]
    
    # =========================================================================
    # CREAR CONDUCTOR
    # =========================================================================
    
    def crear_conductor(self):
        """Crea un nuevo conductor"""
        # 1. Abrir diálogo para capturar datos
        dialog = ConductorDialogController(self)
        if not dialog.exec():
            return
        
        conductor = dialog.datos_conductor
        
        # 2. VALIDAR PRIMERO antes de generar contraseña o confirmar
        valido, mensaje_error = self.service.validar_conductor(conductor)
        if not valido:
            QMessageBox.warning(self, "Datos Inválidos", mensaje_error)
            return
        
        # 3. Generar contraseña
        password = self.service.generar_password()
        
        # 4. Confirmar con el usuario
        respuesta = QMessageBox.question(
            self,
            "Crear Conductor",
            f"Se creará una cuenta para:\n\n"
            f"Nombre: {conductor.nombre}\n"
            f"Email: {conductor.email}\n"
            f"Contraseña: {password}\n\n"
            f"⚠️ Guarda esta contraseña, no se podrá ver después.\n\n"
            f"¿Continuar?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        # 5. Crear usando el servicio (ya no valida porque ya validamos)
        exito, conductor_creado, mensaje = self.service.crear_conductor(conductor, password)
        
        # 6. Manejar resultado
        if exito:
            # Mostrar éxito
            QMessageBox.information(
                self,
                "Conductor Creado",
                f"Conductor creado exitosamente:\n\n"
                f"Nombre: {conductor_creado.nombre}\n"
                f"Email: {conductor_creado.email}\n"
                f"Contraseña: {password}\n\n"
                f"Compártele estos datos de forma segura."
            )
            
            # Agregar a tabla
            self.agregar_a_tabla(conductor_creado)
            
            # Emitir señal
            self.conductor_creado.emit(conductor_creado)
        
        else:
            # Mostrar error (solo errores de Auth o Firebase, no de validación)
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # EDITAR CONDUCTOR
    # =========================================================================
    
    def editar_conductor(self):
        """Edita un conductor existente"""
        # 1. Obtener conductor seleccionado
        conductor = self.obtener_seleccionado()
        if not conductor:
            return
        
        fila_actual = self.tablaCondcutores.currentRow()
        estado_anterior = conductor.estado
        
        # 2. Abrir diálogo
        dialog = ConductorDialogController(self, conductor_a_editar=conductor)
        if not dialog.exec():
            return
        
        conductor_editado = dialog.datos_conductor
        
        # 3. Validar ANTES de actualizar
        valido, mensaje_error = self.service.validar_conductor(conductor_editado)
        if not valido:
            QMessageBox.warning(self, "Datos Inválidos", mensaje_error)
            return
        
        # 4. Actualizar usando el servicio
        exito, mensaje = self.service.actualizar_conductor(conductor_editado)
        
        # 5. Manejar resultado
        if exito:
            # Actualizar tabla
            self.actualizar_en_tabla(fila_actual, conductor_editado)
            
            # Emitir señales
            self.conductor_actualizado.emit(conductor_editado.id_conductor)
            
            # Si cambió el estado, emitir señal
            if estado_anterior != conductor_editado.estado:
                self.conductor_estado_cambiado.emit(
                    conductor_editado.id_conductor,
                    conductor_editado.estado
                )
            
            QMessageBox.information(
                self,
                "Actualizado",
                f"Conductor {conductor.nombre} actualizado correctamente."
            )
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # BORRAR CONDUCTOR
    # =========================================================================
    
    def borrar_conductor(self):
        """Borra un conductor"""
        # 1. Obtener conductor seleccionado
        conductor = self.obtener_seleccionado()
        if not conductor:
            return
        
        # 2. Confirmar
        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Borrar a {conductor.nombre} ({conductor.dni})?\n\n"
            f"Se borrará el perfil del conductor.\n"
            f"La cuenta de Auth permanecerá activa.\n\n"
            f"⚠️ Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        # 3. Eliminar usando el servicio
        exito, mensaje = self.service.eliminar_conductor(conductor.id_conductor)
        
        # 4. Manejar resultado
        if exito:
            # Eliminar de tabla
            self.eliminar_de_tabla(conductor.id_conductor)
            
            # Emitir señal
            self.conductor_eliminado.emit(conductor.id_conductor)
            
            QMessageBox.information(
                self,
                "Eliminado",
                f"Conductor {conductor.nombre} eliminado."
            )
        else:
            QMessageBox.critical(self, "Error", mensaje)
    
    # =========================================================================
    # SINCRONIZACIÓN CON OTRAS VISTAS
    # =========================================================================
    
    def sincronizar_desde_asignacion(self, id_conductor, nuevo_estado):
        """Actualiza el estado cuando cambia desde otra vista"""
        if id_conductor in self.cache_conductores:
            conductor = self.cache_conductores[id_conductor]
            
            if conductor.estado != nuevo_estado:
                conductor.estado = nuevo_estado
                
                # Buscar y actualizar fila
                for i, c in enumerate(self.lista_conductores):
                    if c.id_conductor == id_conductor:
                        self.llenar_fila(i, conductor)
                        break
    
    def recargar_conductor_especifico(self, id_conductor):
        """Recarga un conductor específico desde Firebase"""
        conductor_actualizado = self.service.obtener_por_id(id_conductor)
        if not conductor_actualizado:
            return
        
        # Buscar y actualizar fila
        for i, c in enumerate(self.lista_conductores):
            if c.id_conductor == id_conductor:
                self.actualizar_en_tabla(i, conductor_actualizado)
                break