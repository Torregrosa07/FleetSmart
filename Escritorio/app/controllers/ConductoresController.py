import random
import string
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from app.views.ConductoresWidget_ui import Ui_ConductoresWidget
from app.repositories.conductor_repository import ConductorRepository
from app.controllers.ConductorDialogController import ConductorDialogController
from app.services.auth_service import AuthService


class ConductoresController(QWidget, Ui_ConductoresWidget):
    
    conductor_creado = Signal()
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
        """Carga todos los conductores desde Firebase"""
        
        # Obtener todos los conductores
        self.lista_conductores_actual = self.repo.obtener_todos()
        
        # Limpiar tabla
        self.tablaCondcutores.setRowCount(0)
        
        # Llenar tabla
        for i, conductor in enumerate(self.lista_conductores_actual):
            self.tablaCondcutores.insertRow(i)
            
            self.tablaCondcutores.setItem(i, 0, QTableWidgetItem(conductor.nombre))
            self.tablaCondcutores.setItem(i, 1, QTableWidgetItem(conductor.dni)) 
            self.tablaCondcutores.setItem(i, 2, QTableWidgetItem(conductor.licencia)) 
            self.tablaCondcutores.setItem(i, 3, QTableWidgetItem(conductor.estado))
            self.tablaCondcutores.setItem(i, 4, QTableWidgetItem(str(conductor.email)))
            self.tablaCondcutores.setItem(i, 5, QTableWidgetItem(str(conductor.telefono)))
        
    
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
            f" Guarda esta contraseña, no se podrá ver después.\n\n"
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
                self.conductor_creado.emit()
                self.cargar_tabla()
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

        # Abrir diálogo con datos del conductor
        dialog = ConductorDialogController(self, conductor_a_editar=conductor)
        
        if dialog.exec():
            datos_actualizados = dialog.datos_conductor
            
            # Actualizar en Firebase
            if self.repo.actualizar_conductor(datos_actualizados):
                QMessageBox.information(
                    self,
                    "Actualizado",
                    f"Conductor {conductor.nombre} actualizado correctamente."
                )
                self.cargar_tabla()
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
            if self.repo.eliminar_conductor(conductor.id_conductor):
                QMessageBox.information(
                    self,
                    "Eliminado",
                    f"Conductor {conductor.nombre} eliminado."
                )
                self.cargar_tabla()
            else:
                QMessageBox.critical(
                    self, 
                    "Error", 
                    "No se pudo borrar el conductor."
                ) 