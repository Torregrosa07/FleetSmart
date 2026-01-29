import random
import string
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from app.views.ConductoresWidget_ui import Ui_ConductoresWidget
from app.repositories.conductor_repository import ConductorRepository
from app.controllers.ConductorDialogController import ConductorDialogController
from app.services.auth_service import AuthService


class ConductoresController(QWidget, Ui_ConductoresWidget):
    
    # ========== SEÑALES ==========
    # Se emiten para mantener sincronizadas otras vistas (AsignacionController, etc)
    conductor_creado = Signal(object)          # conductor completo
    conductor_actualizado = Signal(str)        # id_conductor
    conductor_eliminado = Signal(str)          # id_conductor
    conductor_estado_cambiado = Signal(str, str)  # id_conductor, nuevo_estado
    
    def __init__(self, db_connection=None):
        super().__init__()
        self.setupUi(self)
        
        # Repositorio
        self.repo = None
        if db_connection:
            self.repo = ConductorRepository(db_connection)
        
        # Servicio de autenticación
        self.auth_service = AuthService()
            
        # Lista de conductores
        self.lista_conductores_actual = []
        
        # Cache para detectar cambios reales y evitar actualizaciones innecesarias
        self.cache_conductores = {}

        # Configuración inicial
        self.cargar_tabla()
        self.configurar_tabla()
        
        # Conectar botones
        self.conectar_senales()
    
    def configurar_tabla(self):
        """Configura el estilo de la tabla"""
        self.tablaCondcutores.horizontalHeader().setStretchLastSection(False)
        self.tablaCondcutores.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def conectar_senales(self):
        """Conecta los botones con sus métodos"""
        self.btnNuevoConductor.clicked.connect(self.crear_conductor)
        self.btnBorrar.clicked.connect(self.borrar_conductor)
        self.btnEditar.clicked.connect(self.editar_conductor)
    
    def cargar_tabla(self):
        """Carga todos los conductores desde Firebase y actualiza el caché"""
        
        # Obtener todos los conductores
        self.lista_conductores_actual = self.repo.obtener_todos()
        
        # Actualizar caché
        self.cache_conductores = {c.id_conductor: c for c in self.lista_conductores_actual}
        
        # Limpiar tabla
        self.tablaCondcutores.setRowCount(0)
        
        # Llenar tabla
        for i, conductor in enumerate(self.lista_conductores_actual):
            self.tablaCondcutores.insertRow(i)
            self._llenar_fila_tabla(i, conductor)
    
    def _llenar_fila_tabla(self, fila, conductor):
        """Método auxiliar para llenar una fila específica de la tabla"""
        self.tablaCondcutores.setItem(fila, 0, QTableWidgetItem(conductor.nombre))
        self.tablaCondcutores.setItem(fila, 1, QTableWidgetItem(conductor.dni)) 
        self.tablaCondcutores.setItem(fila, 2, QTableWidgetItem(conductor.licencia)) 
        self.tablaCondcutores.setItem(fila, 3, QTableWidgetItem(conductor.estado))
        self.tablaCondcutores.setItem(fila, 4, QTableWidgetItem(str(conductor.email)))
        self.tablaCondcutores.setItem(fila, 5, QTableWidgetItem(str(conductor.telefono)))
    
    def actualizar_fila_conductor_con_datos(self, fila, conductor_actualizado):
        """
        Actualiza una fila específica con datos ya proporcionados.
        Más eficiente que obtener desde Firebase.
        """
        # Actualizar en lista y caché
        self.lista_conductores_actual[fila] = conductor_actualizado
        self.cache_conductores[conductor_actualizado.id_conductor] = conductor_actualizado
        
        # Actualizar solo esa fila en la tabla
        self._llenar_fila_tabla(fila, conductor_actualizado)
    
    def actualizar_fila_conductor(self, id_conductor):
        """
        Actualiza selectivamente una fila de la tabla cuando cambia un conductor.
        MUCHO más eficiente que recargar toda la tabla.
        """
        # Buscar la fila del conductor
        fila = None
        for i, conductor in enumerate(self.lista_conductores_actual):
            if conductor.id_conductor == id_conductor:
                fila = i
                break
        
        if fila is None:
            return
        
        # Obtener datos actualizados del repositorio
        conductor_actualizado = self.repo.obtener_por_id(id_conductor)
        if not conductor_actualizado:
            return
        
        # Actualizar usando el método auxiliar
        self.actualizar_fila_conductor_con_datos(fila, conductor_actualizado)
    
    def agregar_conductor_a_tabla(self, conductor):
        """
        Agrega un nuevo conductor a la tabla sin recargar todo.
        Se llama cuando se crea un conductor.
        """
        # Agregar a la lista y caché
        self.lista_conductores_actual.append(conductor)
        self.cache_conductores[conductor.id_conductor] = conductor
        
        # Agregar nueva fila a la tabla
        nueva_fila = self.tablaCondcutores.rowCount()
        self.tablaCondcutores.insertRow(nueva_fila)
        self._llenar_fila_tabla(nueva_fila, conductor)
    
    def eliminar_conductor_de_tabla(self, id_conductor):
        """
        Elimina un conductor de la tabla sin recargar todo.
        Se llama cuando se borra un conductor.
        """
        # Buscar la fila del conductor
        fila = None
        for i, conductor in enumerate(self.lista_conductores_actual):
            if conductor.id_conductor == id_conductor:
                fila = i
                break
        
        if fila is None:
            return
        
        # Eliminar de lista y caché
        del self.lista_conductores_actual[fila]
        if id_conductor in self.cache_conductores:
            del self.cache_conductores[id_conductor]
        
        # Eliminar fila de la tabla
        self.tablaCondcutores.removeRow(fila)
    
    def obtener_conductor_seleccionado(self):
        """Devuelve el conductor seleccionado en la tabla"""
        fila = self.tablaCondcutores.currentRow()
        
        if fila == -1:
            QMessageBox.warning(self, "Aviso", "Selecciona un conductor de la tabla.")
            return None
        
        return self.lista_conductores_actual[fila]

    # =========================================================================
    # CREAR CONDUCTOR
    # =========================================================================
    
    def crear_conductor(self):
        """
        Crea un nuevo conductor con cuenta de Firebase Auth.
        Este es el flujo completo del CU-01.
        """
        # 1. Abrir diálogo
        dialog = ConductorDialogController(self)
        
        if not dialog.exec():
            return  # Usuario canceló
        
        conductor = dialog.datos_conductor
        
        # 2. Validar email
        email = conductor.email.strip()
        if not email or '@' not in email:
            QMessageBox.warning(
                self,
                "Email Inválido",
                "El conductor necesita un email válido para la app móvil."
            )
            return
        
        # 3. Generar contraseña temporal
        password = self.generar_password()
        
        # 4. Confirmar con el usuario
        respuesta = QMessageBox.question(
            self,
            "Crear Conductor",
            f"Se creará una cuenta para:\n\n"
            f"Nombre: {conductor.nombre}\n"
            f"Email: {email}\n"
            f"Contraseña: {password}\n\n"
            f"⚠️ Guarda esta contraseña, no se podrá ver después.\n\n"
            f"¿Continuar?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        # 5. Crear cuenta en Firebase Auth
        try:
            resultado = self.auth_service.crear_conductor(email, password)
            uid = resultado['uid']
            print(f"Cuenta creada: {uid}")
            
        except Exception as e:
            self.mostrar_error_auth(e, email)
            return
        
        # 6. Guardar perfil
        conductor.id_conductor = uid
        
        try:
            print(f"Guardando perfil del conductor...")
            
            if self.repo.guardar_nuevo_conductor(conductor):
                # Todo correcto
                QMessageBox.information(
                    self,
                    "Conductor Creado",
                    f"Conductor creado exitosamente:\n\n"
                    f"Nombre: {conductor.nombre}\n"
                    f"Email: {email}\n"
                    f"Contraseña: {password}\n\n"
                    f"Compártele estos datos de forma segura."
                )
                
                # Actualización selectiva: agregar solo este conductor
                self.agregar_conductor_a_tabla(conductor)
                
                # Emitir señal con el objeto completo para que otras vistas lo tengan
                self.conductor_creado.emit(conductor)
            else:
                QMessageBox.warning(
                    self,
                    "Perfil Incompleto",
                    f"La cuenta de Auth se creó, pero hubo un error\n"
                    f"al guardar el perfil completo.\n\n"
                    f"Email: {email}\n"
                    f"Contraseña: {password}"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al guardar el perfil:\n{str(e)}"
            )

    def generar_password(self):
        numeros = ''.join(random.choices(string.digits, k=4))
        return f"Fleet{numeros}"

    def mostrar_error_auth(self, error, email):
        """Muestra un mensaje de error amigable según el tipo de error de Auth"""
        error_text = str(error)
        
        if "EMAIL_EXISTS" in error_text:
            QMessageBox.critical(
                self,
                "Email Duplicado",
                f"Ya existe una cuenta con el email: {email}\n\n"
                f"Usa otro email o recupera la contraseña existente."
            )
        elif "WEAK_PASSWORD" in error_text:
            QMessageBox.critical(
                self,
                "Contraseña Débil",
                f"La contraseña no cumple los requisitos de Firebase.\n"
                f"Debe tener al menos 6 caracteres."
            )
        else:
            QMessageBox.critical(
                self,
                "Error de Autenticación",
                f"No se pudo crear la cuenta:\n{error_text}"
            )

    # =========================================================================
    # EDITAR CONDUCTOR
    # =========================================================================
    
    def editar_conductor(self):
        """Edita un conductor existente"""
        conductor = self.obtener_conductor_seleccionado()
        if not conductor:
            return
        
        # Guardamos la fila actual antes de abrir el diálogo
        fila_actual = self.tablaCondcutores.currentRow()

        # Abrir diálogo con datos del conductor
        dialog = ConductorDialogController(self, conductor_a_editar=conductor)
        
        if dialog.exec():
            datos_actualizados = dialog.datos_conductor
            id_conductor = datos_actualizados.id_conductor
            
            # Detectar si cambió el estado
            estado_anterior = conductor.estado
            estado_nuevo = datos_actualizados.estado
            cambio_estado = (estado_anterior != estado_nuevo)
            
            # Actualizar en Firebase
            if self.repo.actualizar_conductor(datos_actualizados):
                # Actualización selectiva usando los datos que ya tenemos
                self.actualizar_fila_conductor_con_datos(fila_actual, datos_actualizados)
                
                # Emitir señales
                self.conductor_actualizado.emit(id_conductor)
                
                if cambio_estado:
                    self.conductor_estado_cambiado.emit(id_conductor, estado_nuevo)
                
                QMessageBox.information(
                    self,
                    "Actualizado",
                    f"Conductor {conductor.nombre} actualizado correctamente."
                )
            else:
                QMessageBox.critical(
                    self, 
                    "Error", 
                    "No se pudo actualizar el conductor."
                )

    # =========================================================================
    # BORRAR CONDUCTOR
    # =========================================================================
    
    def borrar_conductor(self):
        """Borra un conductor"""
        conductor = self.obtener_conductor_seleccionado()
        if not conductor:
            return

        respuesta = QMessageBox.question(
            self, 
            "Confirmar", 
            f"¿Borrar a {conductor.nombre} ({conductor.dni})?\n\n"
            f"Se borrará el perfil del conductor.\n"
            f"La cuenta de Auth permanecerá activa.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            id_conductor = conductor.id_conductor
            
            if self.repo.eliminar_conductor(id_conductor):
                # Actualización selectiva: eliminar solo esta fila
                self.eliminar_conductor_de_tabla(id_conductor)
                
                # Emitir señal para notificar a otras vistas
                self.conductor_eliminado.emit(id_conductor)
                
                QMessageBox.information(
                    self,
                    "Eliminado",
                    f"Conductor {conductor.nombre} eliminado."
                )
            else:
                QMessageBox.critical(
                    self, 
                    "Error", 
                    "No se pudo borrar el conductor."
                )
    
    # ========== MÉTODOS PÚBLICOS PARA SINCRONIZACIÓN ==========
    # Estos métodos pueden ser llamados desde otras vistas mediante señales
    
    def sincronizar_desde_asignacion(self, id_conductor, nuevo_estado):
        """
        Método que puede ser llamado cuando AsignacionController cambia el estado
        de un conductor (por ejemplo, de Disponible a En Ruta).
        """
        # Actualizar en caché
        if id_conductor in self.cache_conductores:
            conductor_cache = self.cache_conductores[id_conductor]
            
            # Solo actualizar si realmente cambió
            if conductor_cache.estado != nuevo_estado:
                conductor_cache.estado = nuevo_estado
                self.actualizar_fila_conductor(id_conductor)
    
    def recargar_conductor_especifico(self, id_conductor):
        """
        Recarga un conductor específico desde Firebase.
        Útil cuando otra vista modifica un conductor externamente.
        """
        self.actualizar_fila_conductor(id_conductor)