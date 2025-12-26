from PySide6.QtWidgets import QDialog, QMessageBox
from app.views.ConductoresDialog_ui import Ui_ConductoresDialog
from app.models.condcutor import Conductor

class ConductorDialogController(QDialog, Ui_ConductoresDialog):
    def __init__(self, parent=None, conductor_a_editar=None):
        super().__init__(parent)
        self.setupUi(self)
        self.datos_conductor = None # Aquí guardaremos el resultado si da a Guardar

        self.conductor_existente = conductor_a_editar
        
        if self.conductor_existente:
            self.rellenar_campos()
            self.btnGuardar.setText("Actualizar")
        
        # Conectar botones
        self.btnGuardar.clicked.connect(self.validar_y_guardar)
        self.btnCancelar.clicked.connect(self.reject) # Cierra devolviendo "Cancelado"

    def rellenar_campos(self):
        """Rellena el formulario con los datos del conductor a editar"""
        c = self.conductor_existente
        self.leDNI.setText(c.dni)
        self.leNombre.setText(c.nombre)
        self.leLicencia.setText(c.licencia)
        self.leEmail.setText(c.email)
        self.leTelefono.setText(c.telefono)
        
        
    def validar_y_guardar(self):
        dni = self.leDNI.text().strip().upper()
        nombre = self.leNombre.text().strip()
        licencia = self.leLicencia.text().strip().upper()
        email = self.leEmail.text().strip() 
        telefono = self.leTelefono.text().strip()

        if not dni or not nombre or not licencia:
            QMessageBox.warning(self, "Faltan datos", "Por favor rellena DNI, Nombre y Número de licencia.")
            return
        
        
        self.datos_conductor = Conductor(
            dni=dni,
            nombre= nombre,
            licencia= licencia,
            estado="Inactivo",
            telefono=telefono,
            email= email
        )
        
        if self.conductor_existente:
            self.datos_conductor.id_conductor = self.conductor_existente.id_conductor
            self.datos_conductor.estado = self.conductor_existente.estado
        
        self.accept()