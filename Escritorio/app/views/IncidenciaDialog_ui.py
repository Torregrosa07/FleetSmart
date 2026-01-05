# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'IncidenciaDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QDateTimeEdit,
    QDialog, QFormLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_IncidenciaDialog(object):
    def setupUi(self, IncidenciaDialog):
        if not IncidenciaDialog.objectName():
            IncidenciaDialog.setObjectName(u"IncidenciaDialog")
        IncidenciaDialog.resize(436, 404)
        self.verticalLayout = QVBoxLayout(IncidenciaDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblVehiculo = QLabel(IncidenciaDialog)
        self.lblVehiculo.setObjectName(u"lblVehiculo")
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(12)
        font.setBold(True)
        self.lblVehiculo.setFont(font)
        self.lblVehiculo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblVehiculo)

        self.cbVehiculo = QComboBox(IncidenciaDialog)
        self.cbVehiculo.setObjectName(u"cbVehiculo")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(12)
        self.cbVehiculo.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbVehiculo)

        self.lblTipo = QLabel(IncidenciaDialog)
        self.lblTipo.setObjectName(u"lblTipo")
        self.lblTipo.setFont(font)
        self.lblTipo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblTipo)

        self.cbTipo = QComboBox(IncidenciaDialog)
        self.cbTipo.addItem("")
        self.cbTipo.addItem("")
        self.cbTipo.addItem("")
        self.cbTipo.addItem("")
        self.cbTipo.setObjectName(u"cbTipo")
        self.cbTipo.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cbTipo)

        self.lblFecha = QLabel(IncidenciaDialog)
        self.lblFecha.setObjectName(u"lblFecha")
        self.lblFecha.setFont(font)
        self.lblFecha.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblFecha)

        self.dtFecha = QDateEdit(IncidenciaDialog)
        self.dtFecha.setObjectName(u"dtFecha")
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(10)
        self.dtFecha.setFont(font2)
        self.dtFecha.setCalendarPopup(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dtFecha)

        self.lblHora = QLabel(IncidenciaDialog)
        self.lblHora.setObjectName(u"lblHora")
        self.lblHora.setFont(font)
        self.lblHora.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblHora)

        self.teHora = QDateTimeEdit(IncidenciaDialog)
        self.teHora.setObjectName(u"teHora")
        self.teHora.setFont(font2)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.teHora)

        self.lblEstado = QLabel(IncidenciaDialog)
        self.lblEstado.setObjectName(u"lblEstado")
        self.lblEstado.setFont(font)
        self.lblEstado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblEstado)

        self.cbEstado = QComboBox(IncidenciaDialog)
        self.cbEstado.addItem("")
        self.cbEstado.addItem("")
        self.cbEstado.addItem("")
        self.cbEstado.setObjectName(u"cbEstado")
        self.cbEstado.setFont(font1)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.cbEstado)

        self.lblConductor = QLabel(IncidenciaDialog)
        self.lblConductor.setObjectName(u"lblConductor")
        self.lblConductor.setFont(font)
        self.lblConductor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lblConductor)

        self.cbConductor = QComboBox(IncidenciaDialog)
        self.cbConductor.setObjectName(u"cbConductor")
        self.cbConductor.setFont(font1)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.cbConductor)


        self.verticalLayout.addLayout(self.formLayout)

        self.txtDescripcion = QTextEdit(IncidenciaDialog)
        self.txtDescripcion.setObjectName(u"txtDescripcion")
        self.txtDescripcion.setMinimumSize(QSize(0, 100))
        font3 = QFont()
        font3.setFamilies([u"Montserrat"])
        font3.setPointSize(11)
        self.txtDescripcion.setFont(font3)

        self.verticalLayout.addWidget(self.txtDescripcion)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnGuardarIncidencia = QPushButton(IncidenciaDialog)
        self.btnGuardarIncidencia.setObjectName(u"btnGuardarIncidencia")
        self.btnGuardarIncidencia.setEnabled(True)
        self.btnGuardarIncidencia.setMaximumSize(QSize(16777215, 60))
        font4 = QFont()
        font4.setFamilies([u"Montserrat"])
        font4.setPointSize(13)
        font4.setWeight(QFont.Black)
        font4.setStrikeOut(False)
        self.btnGuardarIncidencia.setFont(font4)
        self.btnGuardarIncidencia.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnGuardarIncidencia.setCheckable(True)

        self.horizontalLayout.addWidget(self.btnGuardarIncidencia)

        self.btnCancelar = QPushButton(IncidenciaDialog)
        self.btnCancelar.setObjectName(u"btnCancelar")
        self.btnCancelar.setEnabled(True)
        self.btnCancelar.setMaximumSize(QSize(16777215, 60))
        self.btnCancelar.setFont(font4)
        self.btnCancelar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnCancelar.setCheckable(True)

        self.horizontalLayout.addWidget(self.btnCancelar)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(IncidenciaDialog)

        QMetaObject.connectSlotsByName(IncidenciaDialog)
    # setupUi

    def retranslateUi(self, IncidenciaDialog):
        IncidenciaDialog.setWindowTitle(QCoreApplication.translate("IncidenciaDialog", u"Dialog", None))
        self.lblVehiculo.setText(QCoreApplication.translate("IncidenciaDialog", u"Veh\u00edculo: ", None))
        self.lblTipo.setText(QCoreApplication.translate("IncidenciaDialog", u"Tipo:", None))
        self.cbTipo.setItemText(0, QCoreApplication.translate("IncidenciaDialog", u"Aver\u00eda", None))
        self.cbTipo.setItemText(1, QCoreApplication.translate("IncidenciaDialog", u"Accidente", None))
        self.cbTipo.setItemText(2, QCoreApplication.translate("IncidenciaDialog", u"Mantenimiento", None))
        self.cbTipo.setItemText(3, QCoreApplication.translate("IncidenciaDialog", u"Otro", None))

        self.lblFecha.setText(QCoreApplication.translate("IncidenciaDialog", u"Fecha: ", None))
        self.dtFecha.setDisplayFormat(QCoreApplication.translate("IncidenciaDialog", u"dd/MM/yyyy", None))
        self.lblHora.setText(QCoreApplication.translate("IncidenciaDialog", u"Hora: ", None))
        self.teHora.setDisplayFormat(QCoreApplication.translate("IncidenciaDialog", u"HH:mm", None))
        self.lblEstado.setText(QCoreApplication.translate("IncidenciaDialog", u"Estado: ", None))
        self.cbEstado.setItemText(0, QCoreApplication.translate("IncidenciaDialog", u"Pendiente", None))
        self.cbEstado.setItemText(1, QCoreApplication.translate("IncidenciaDialog", u"En Proceso", None))
        self.cbEstado.setItemText(2, QCoreApplication.translate("IncidenciaDialog", u"Resuelta", None))

        self.lblConductor.setText(QCoreApplication.translate("IncidenciaDialog", u"Conductor:", None))
        self.txtDescripcion.setPlaceholderText(QCoreApplication.translate("IncidenciaDialog", u"Escribe aqu\u00ed una descripci\u00f3n de la aver\u00eda", None))
        self.btnGuardarIncidencia.setText(QCoreApplication.translate("IncidenciaDialog", u"Guardar Incidencia", None))
        self.btnCancelar.setText(QCoreApplication.translate("IncidenciaDialog", u"Cancelar", None))
    # retranslateUi

