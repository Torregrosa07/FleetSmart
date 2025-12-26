from PySide6.QtWidgets import QDialog, QMessageBox
from app.views.VehiculosDialog_ui import Ui_VehiculosDialog
from app.models.vehiculo import Vehiculo

class VehiculoDialogController(QDialog, Ui_VehiculosDialog):
    def __init__(self, parent=None, vehiculo_a_editar=None):
        super().__init__(parent)
        self.setupUi(self)
        self.datos_vehiculo = None # Aquí guardaremos el resultado si da a Guardar

        self.vehiculo_existente = vehiculo_a_editar
        
        if self.vehiculo_existente:
            self.rellenar_campos()
            self.btnGuardar.setText("Actualizar")
        
        # Conectar botones
        self.btnGuardar.clicked.connect(self.validar_y_guardar)
        self.btnCancelar.clicked.connect(self.reject) # Cierra devolviendo "Cancelado"

    def rellenar_campos(self):
        """Rellena el formulario con los datos del coche a editar"""
        v = self.vehiculo_existente
        self.leMatricula.setText(v.matricula)
        self.leMarca.setText(v.marca)
        self.leModelo.setText(v.modelo)
        self.leAno.setText(str(v.ano))
        self.leITV.setText(v.proxima_itv)
        
        
    def validar_y_guardar(self):
        matricula = self.leMatricula.text().strip().upper()
        marca = self.leMarca.text().strip()
        modelo = self.leModelo.text().strip()
        ano = self.leAno.text().strip() 
        proximaITV = self.leITV.text().strip()

        if not matricula or not marca or not modelo:
            QMessageBox.warning(self, "Faltan datos", "Por favor rellena matrícula, marca y modelo.")
            return
        
        
        self.datos_vehiculo = Vehiculo(
            matricula=matricula,
            marca= marca,
            modelo = modelo,
            estado="Disponible",
            km_actuales=0,
            proxima_itv=proximaITV,
            ano= ano
        )
        
        if self.vehiculo_existente:
            self.datos_vehiculo.id_vehiculo = self.vehiculo_existente.id_vehiculo
            self.datos_vehiculo.estado = self.vehiculo_existente.estado
        
        self.accept()