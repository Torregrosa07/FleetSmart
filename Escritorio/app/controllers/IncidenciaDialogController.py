from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import QDate, QTime
from app.views.IncidenciaDialog_ui import Ui_IncidenciaDialog
from app.models.incidencia import Incidencia

class IncidenciaDialogController(QDialog, Ui_IncidenciaDialog):
    """
    Diálogo para crear o editar una incidencia.
    Código simple, sin lambdas, fácil de entender.
    """
    
    def __init__(self, parent=None, vehiculos=None, conductores=None, incidencia_a_editar=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Datos recibidos
        self.vehiculos = vehiculos or []
        self.conductores = conductores or []
        self.incidencia_a_editar = incidencia_a_editar
        
        # Datos a devolver
        self.datos_incidencia = None
        
        # Configuración inicial
        self.configurar_fecha_hora()
        self.llenar_combos()
        self.conectar_senales()
        
        # Si es edición, cargar datos
        if self.incidencia_a_editar:
            self.cargar_datos_edicion()
        
        # Título del diálogo
        if incidencia_a_editar:
            self.setWindowTitle("Editar Incidencia")
        else:
            self.setWindowTitle("Nueva Incidencia")
    
    def configurar_fecha_hora(self):
        """Configura fecha y hora actuales por defecto"""
        self.dtFecha.setDate(QDate.currentDate())
        self.teHora.setTime(QTime.currentTime())
    
    def llenar_combos(self):
        """Llena los ComboBox con datos"""
        # Llenar vehículos
        self.cbVehiculo.clear()
        for vehiculo in self.vehiculos:
            # Mostrar: "ABC-1234 - Ford Transit"
            texto = f"{vehiculo.matricula} - {vehiculo.marca} {vehiculo.modelo}"
            self.cbVehiculo.addItem(texto, vehiculo.id_vehiculo)
        
        # Llenar conductores (opcional)
        self.cbConductor.clear()
        self.cbConductor.addItem("(Ninguno)", None)  # Opción por defecto
        for conductor in self.conductores:
            texto = f"{conductor.nombre} - {conductor.dni}"
            self.cbConductor.addItem(texto, conductor.id_conductor)
    
    def conectar_senales(self):
        """Conecta las señales de los botones"""
        self.btnGuardarIncidencia.clicked.connect(self.validar_y_aceptar)
        self.btnCancelar.clicked.connect(self.reject)
    
    def cargar_datos_edicion(self):
        """Carga los datos de una incidencia existente para editar"""
        inc = self.incidencia_a_editar
        
        # Buscar y seleccionar vehículo
        for i in range(self.cbVehiculo.count()):
            if self.cbVehiculo.itemData(i) == inc.id_vehiculo:
                self.cbVehiculo.setCurrentIndex(i)
                break
        
        # Seleccionar tipo
        index = self.cbTipo.findText(inc.tipo)
        if index >= 0:
            self.cbTipo.setCurrentIndex(index)
        
        # Fecha y hora
        # Convertir string "dd/MM/yyyy" a QDate
        partes_fecha = inc.fecha.split('/')
        if len(partes_fecha) == 3:
            dia = int(partes_fecha[0])
            mes = int(partes_fecha[1])
            anio = int(partes_fecha[2])
            self.dtFecha.setDate(QDate(anio, mes, dia))
        
        # Convertir string "HH:mm" a QTime
        partes_hora = inc.hora.split(':')
        if len(partes_hora) == 2:
            hora = int(partes_hora[0])
            minuto = int(partes_hora[1])
            self.teHora.setTime(QTime(hora, minuto))
        
        # Estado
        index = self.cbEstado.findText(inc.estado)
        if index >= 0:
            self.cbEstado.setCurrentIndex(index)
        
        # Conductor (opcional)
        if inc.id_conductor:
            for i in range(self.cbConductor.count()):
                if self.cbConductor.itemData(i) == inc.id_conductor:
                    self.cbConductor.setCurrentIndex(i)
                    break
        
        # Descripción
        self.txtDescripcion.setPlainText(inc.descripcion)
    
    def validar_y_aceptar(self):
        """Valida los datos antes de aceptar el diálogo"""
        # Validar que hay un vehículo seleccionado
        if self.cbVehiculo.currentIndex() < 0:
            QMessageBox.warning(
                self,
                "Vehículo requerido",
                "Debes seleccionar un vehículo."
            )
            return
        
        # Validar descripción
        descripcion = self.txtDescripcion.toPlainText().strip()
        if not descripcion:
            QMessageBox.warning(
                self,
                "Descripción requerida",
                "Debes escribir una descripción de la incidencia."
            )
            return
        
        # Si todo es válido, crear el objeto Incidencia
        self.crear_objeto_incidencia()
        self.accept()
    
    def crear_objeto_incidencia(self):
        """Crea el objeto Incidencia con los datos del formulario"""
        # Obtener datos del vehículo seleccionado
        id_vehiculo = self.cbVehiculo.currentData()
        matricula = self.cbVehiculo.currentText().split(' - ')[0]  # Extraer matrícula
        
        # Obtener datos del conductor (opcional)
        id_conductor = self.cbConductor.currentData()
        nombre_conductor = None
        if id_conductor:
            nombre_conductor = self.cbConductor.currentText().split(' - ')[0]
        
        # Crear objeto
        self.datos_incidencia = Incidencia(
            id_vehiculo=id_vehiculo,
            matricula=matricula,
            tipo=self.cbTipo.currentText(),
            descripcion=self.txtDescripcion.toPlainText().strip(),
            fecha=self.dtFecha.date().toString("dd/MM/yyyy"),
            hora=self.teHora.time().toString("HH:mm"),
            estado=self.cbEstado.currentText(),
            id_gestor="",  # Se asignará en el controlador principal
            id_conductor=id_conductor,
            nombre_conductor=nombre_conductor
        )
        
        # Si es edición, mantener el ID
        if self.incidencia_a_editar:
            self.datos_incidencia.id_incidencia = self.incidencia_a_editar.id_incidencia