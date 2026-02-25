from PySide6.QtWidgets import QDialog, QMessageBox
from app.views.VehiculosDialog_ui import Ui_VehiculosDialog
from app.models.vehiculo import Vehiculo
from app.utils.language_utils import LanguageService

class VehiculoDialogController(QDialog, Ui_VehiculosDialog):
    def __init__(self, parent=None, vehiculo_a_editar=None, app_state=None):
        super().__init__(parent)
        self.setupUi(self)
        self.datos_vehiculo = None
        self.app_state = app_state

        self.vehiculo_existente = vehiculo_a_editar
        
        idioma = "Español"
        if parent and hasattr(parent, 'app_state') and parent.app_state:
             idioma = parent.app_state.get("language", "Español")
        
        
        self.lblMarca.setText(LanguageService.get_text("brand", idioma))
        self.lblMatricula.setText(LanguageService.get_text("license_plate", idioma))
        self.lblAno.setText(LanguageService.get_text("year", idioma))
        self.lblModelo.setText(LanguageService.get_text("model", idioma))
        self.lblITV.setText(LanguageService.get_text("ITV", idioma))
        
        self.btnGuardar.setText(LanguageService.get_text("save", idioma))
        self.btnCancelar.setText(LanguageService.get_text("cancel", idioma))
        
        
        
        if self.vehiculo_existente:
            self.rellenar_campos()
            self.btnGuardar.setText("Actualizar")
        
        # Conectar botones
        self.btnGuardar.clicked.connect(self.validar_y_guardar)
        self.btnCancelar.clicked.connect(self.reject) 

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
        ano_texto = self.leAno.text().strip() 
        proximaITV = self.leITV.text().strip()

        if not matricula or not marca or not modelo:
            QMessageBox.warning(self, "Faltan datos", "Por favor rellena matrícula, marca y modelo.")
            return
        
        # --- CORRECCIÓN AQUÍ ---
        # Convertir el año a entero, si falla mostramos un aviso y detenemos el guardado
        try:
            ano = int(ano_texto) if ano_texto else 0
        except ValueError:
            QMessageBox.warning(self, "Dato Inválido", "El año debe ser un número entero válido.")
            return
        # -----------------------
        
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