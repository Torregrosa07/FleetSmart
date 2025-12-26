# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RutasWidget.ui'
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_RutasWidget(object):
    def setupUi(self, RutasWidget):
        if not RutasWidget.objectName():
            RutasWidget.setObjectName(u"RutasWidget")
        RutasWidget.resize(1220, 789)
        self.horizontalLayout_2 = QHBoxLayout(RutasWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(RutasWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(270, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.lblOrigen = QLabel(self.groupBox)
        self.lblOrigen.setObjectName(u"lblOrigen")
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(16)
        font.setBold(True)
        self.lblOrigen.setFont(font)
        self.lblOrigen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblOrigen)

        self.leOrigen = QLineEdit(self.groupBox)
        self.leOrigen.setObjectName(u"leOrigen")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(12)
        self.leOrigen.setFont(font1)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leOrigen)

        self.lblConductor = QLabel(self.groupBox)
        self.lblConductor.setObjectName(u"lblConductor")
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.lblConductor.setFont(font2)
        self.lblConductor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblConductor)

        self.cbConductor = QComboBox(self.groupBox)
        self.cbConductor.setObjectName(u"cbConductor")
        self.cbConductor.setFont(font1)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cbConductor)

        self.lblVehiculo = QLabel(self.groupBox)
        self.lblVehiculo.setObjectName(u"lblVehiculo")
        font3 = QFont()
        font3.setFamilies([u"Montserrat"])
        font3.setPointSize(14)
        font3.setBold(True)
        self.lblVehiculo.setFont(font3)
        self.lblVehiculo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblVehiculo)

        self.cbVehiculo = QComboBox(self.groupBox)
        self.cbVehiculo.setObjectName(u"cbVehiculo")
        self.cbVehiculo.setFont(font1)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.cbVehiculo)

        self.lblFecha = QLabel(self.groupBox)
        self.lblFecha.setObjectName(u"lblFecha")
        self.lblFecha.setFont(font)
        self.lblFecha.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblFecha)

        self.deFecha = QDateEdit(self.groupBox)
        self.deFecha.setObjectName(u"deFecha")
        self.deFecha.setFont(font1)
        self.deFecha.setCalendarPopup(True)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.deFecha)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblConductor_2 = QLabel(self.groupBox)
        self.lblConductor_2.setObjectName(u"lblConductor_2")
        self.lblConductor_2.setFont(font2)
        self.lblConductor_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblConductor_2)

        self.leNuevaParada = QLineEdit(self.groupBox)
        self.leNuevaParada.setObjectName(u"leNuevaParada")
        self.leNuevaParada.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.leNuevaParada)

        self.btnAgregarParada = QPushButton(self.groupBox)
        self.btnAgregarParada.setObjectName(u"btnAgregarParada")
        self.btnAgregarParada.setEnabled(True)
        self.btnAgregarParada.setMaximumSize(QSize(60, 60))
        font4 = QFont()
        font4.setFamilies([u"Montserrat"])
        font4.setPointSize(13)
        font4.setWeight(QFont.Black)
        font4.setStrikeOut(False)
        self.btnAgregarParada.setFont(font4)
        self.btnAgregarParada.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnAgregarParada.setCheckable(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.btnAgregarParada)


        self.verticalLayout.addLayout(self.formLayout)

        self.listParadas = QListWidget(self.groupBox)
        self.listParadas.setObjectName(u"listParadas")
        self.listParadas.setMinimumSize(QSize(0, 70))

        self.verticalLayout.addWidget(self.listParadas)

        self.btnGuardarRuta = QPushButton(self.groupBox)
        self.btnGuardarRuta.setObjectName(u"btnGuardarRuta")
        self.btnGuardarRuta.setEnabled(True)
        self.btnGuardarRuta.setMaximumSize(QSize(16777215, 60))
        self.btnGuardarRuta.setFont(font4)
        self.btnGuardarRuta.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnGuardarRuta.setCheckable(True)

        self.verticalLayout.addWidget(self.btnGuardarRuta)


        self.horizontalLayout.addWidget(self.groupBox)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.widget = QWidget(RutasWidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.webMapRuta = QWebEngineView(self.widget)
        self.webMapRuta.setObjectName(u"webMapRuta")
        self.webMapRuta.setMinimumSize(QSize(600, 400))
        self.webMapRuta.setMaximumSize(QSize(800, 600))

        self.horizontalLayout_3.addWidget(self.webMapRuta)


        self.horizontalLayout_2.addWidget(self.widget)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.retranslateUi(RutasWidget)

        QMetaObject.connectSlotsByName(RutasWidget)
    # setupUi

    def retranslateUi(self, RutasWidget):
        RutasWidget.setWindowTitle(QCoreApplication.translate("RutasWidget", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("RutasWidget", u"Nueva Ruta", None))
        self.lblOrigen.setText(QCoreApplication.translate("RutasWidget", u"Origen:  ", None))
        self.lblConductor.setText(QCoreApplication.translate("RutasWidget", u"Conductor: ", None))
        self.lblVehiculo.setText(QCoreApplication.translate("RutasWidget", u"Veh\u00edculo: ", None))
        self.lblFecha.setText(QCoreApplication.translate("RutasWidget", u"Fecha: ", None))
        self.lblConductor_2.setText(QCoreApplication.translate("RutasWidget", u"Nueva Parada: ", None))
        self.leNuevaParada.setPlaceholderText(QCoreApplication.translate("RutasWidget", u"Escribe una direcci\u00f3n y pulsa +", None))
        self.btnAgregarParada.setText(QCoreApplication.translate("RutasWidget", u"+", None))
        self.btnGuardarRuta.setText(QCoreApplication.translate("RutasWidget", u"Guardar Ruta", None))
    # retranslateUi

