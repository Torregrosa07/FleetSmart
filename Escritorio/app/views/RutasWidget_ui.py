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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QFormLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QTimeEdit, QVBoxLayout,
    QWidget)

class Ui_RutasWidget(object):
    def setupUi(self, RutasWidget):
        if not RutasWidget.objectName():
            RutasWidget.setObjectName(u"RutasWidget")
        RutasWidget.resize(1220, 785)
        self.horizontalLayout_2 = QHBoxLayout(RutasWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(RutasWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(300, 16777215))
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblNombreRuta = QLabel(self.groupBox)
        self.lblNombreRuta.setObjectName(u"lblNombreRuta")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.lblNombreRuta.setFont(font1)
        self.lblNombreRuta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblNombreRuta)

        self.leNombreRuta = QLineEdit(self.groupBox)
        self.leNombreRuta.setObjectName(u"leNombreRuta")
        self.leNombreRuta.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leNombreRuta)

        self.lblOrigen = QLabel(self.groupBox)
        self.lblOrigen.setObjectName(u"lblOrigen")
        self.lblOrigen.setFont(font1)
        self.lblOrigen.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblOrigen)

        self.leOrigen = QLineEdit(self.groupBox)
        self.leOrigen.setObjectName(u"leOrigen")
        self.leOrigen.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.leOrigen)

        self.lblFecha = QLabel(self.groupBox)
        self.lblFecha.setObjectName(u"lblFecha")
        self.lblFecha.setFont(font1)
        self.lblFecha.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblFecha)

        self.dtFecha = QDateTimeEdit(self.groupBox)
        self.dtFecha.setObjectName(u"dtFecha")
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(11)
        self.dtFecha.setFont(font2)
        self.dtFecha.setCalendarPopup(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.dtFecha)

        self.lblHoraInicio = QLabel(self.groupBox)
        self.lblHoraInicio.setObjectName(u"lblHoraInicio")
        self.lblHoraInicio.setFont(font1)
        self.lblHoraInicio.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblHoraInicio)

        self.teHoraInicio = QTimeEdit(self.groupBox)
        self.teHoraInicio.setObjectName(u"teHoraInicio")
        self.teHoraInicio.setTime(QTime(8, 0, 0))

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.teHoraInicio)

        self.lblHoraFin = QLabel(self.groupBox)
        self.lblHoraFin.setObjectName(u"lblHoraFin")
        self.lblHoraFin.setFont(font1)
        self.lblHoraFin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblHoraFin)

        self.teHoraFin = QTimeEdit(self.groupBox)
        self.teHoraFin.setObjectName(u"teHoraFin")
        self.teHoraFin.setTime(QTime(17, 0, 0))

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.teHoraFin)

        self.lblDestino = QLabel(self.groupBox)
        self.lblDestino.setObjectName(u"lblDestino")
        self.lblDestino.setFont(font1)
        self.lblDestino.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lblDestino)

        self.leDestino = QLineEdit(self.groupBox)
        self.leDestino.setObjectName(u"leDestino")
        self.leDestino.setFont(font)
        self.leDestino.setReadOnly(True)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.leDestino)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lblConductor_2 = QLabel(self.groupBox)
        self.lblConductor_2.setObjectName(u"lblConductor_2")
        self.lblConductor_2.setFont(font1)
        self.lblConductor_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.lblConductor_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btnAgregarParada = QPushButton(self.groupBox)
        self.btnAgregarParada.setObjectName(u"btnAgregarParada")
        self.btnAgregarParada.setEnabled(True)
        self.btnAgregarParada.setMaximumSize(QSize(60, 60))
        font3 = QFont()
        font3.setFamilies([u"Montserrat"])
        font3.setPointSize(13)
        font3.setWeight(QFont.Black)
        font3.setStrikeOut(False)
        self.btnAgregarParada.setFont(font3)
        self.btnAgregarParada.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnAgregarParada.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.btnAgregarParada)

        self.btnEliminarParada = QPushButton(self.groupBox)
        self.btnEliminarParada.setObjectName(u"btnEliminarParada")
        self.btnEliminarParada.setEnabled(True)
        self.btnEliminarParada.setMaximumSize(QSize(60, 60))
        self.btnEliminarParada.setFont(font3)
        self.btnEliminarParada.setStyleSheet(u"background-color: rgb(255, 52, 25); color: white;")
        self.btnEliminarParada.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.btnEliminarParada)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.leNuevaParada = QLineEdit(self.groupBox)
        self.leNuevaParada.setObjectName(u"leNuevaParada")
        font4 = QFont()
        font4.setFamilies([u"Montserrat"])
        font4.setPointSize(10)
        self.leNuevaParada.setFont(font4)

        self.verticalLayout.addWidget(self.leNuevaParada)

        self.listParadas = QListWidget(self.groupBox)
        self.listParadas.setObjectName(u"listParadas")
        self.listParadas.setMinimumSize(QSize(0, 70))

        self.verticalLayout.addWidget(self.listParadas)

        self.btnGuardarRuta = QPushButton(self.groupBox)
        self.btnGuardarRuta.setObjectName(u"btnGuardarRuta")
        self.btnGuardarRuta.setEnabled(True)
        self.btnGuardarRuta.setMaximumSize(QSize(16777215, 60))
        self.btnGuardarRuta.setFont(font3)
        self.btnGuardarRuta.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnGuardarRuta.setCheckable(True)

        self.verticalLayout.addWidget(self.btnGuardarRuta)


        self.horizontalLayout.addWidget(self.groupBox)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.widget = QWidget(RutasWidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableWidget = QTableWidget(self.widget)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.webMapRuta = QWebEngineView(self.widget)
        self.webMapRuta.setObjectName(u"webMapRuta")
        self.webMapRuta.setMinimumSize(QSize(530, 375))
        self.webMapRuta.setMaximumSize(QSize(765, 483))

        self.verticalLayout_2.addWidget(self.webMapRuta)


        self.horizontalLayout_2.addWidget(self.widget)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.retranslateUi(RutasWidget)

        QMetaObject.connectSlotsByName(RutasWidget)
    # setupUi

    def retranslateUi(self, RutasWidget):
        RutasWidget.setWindowTitle(QCoreApplication.translate("RutasWidget", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("RutasWidget", u"Nueva Ruta", None))
        self.lblNombreRuta.setText(QCoreApplication.translate("RutasWidget", u"Nombre:", None))
        self.lblOrigen.setText(QCoreApplication.translate("RutasWidget", u"Origen:  ", None))
        self.lblFecha.setText(QCoreApplication.translate("RutasWidget", u"Fecha: ", None))
        self.dtFecha.setDisplayFormat(QCoreApplication.translate("RutasWidget", u"dd/MM/yyyy", None))
        self.lblHoraInicio.setText(QCoreApplication.translate("RutasWidget", u"Hora Inicio:", None))
        self.teHoraInicio.setDisplayFormat(QCoreApplication.translate("RutasWidget", u"HH:mm", None))
        self.lblHoraFin.setText(QCoreApplication.translate("RutasWidget", u"Hora Fin:", None))
        self.teHoraFin.setDisplayFormat(QCoreApplication.translate("RutasWidget", u"HH:mm", None))
        self.lblDestino.setText(QCoreApplication.translate("RutasWidget", u"Destino: ", None))
        self.leDestino.setPlaceholderText(QCoreApplication.translate("RutasWidget", u"Se autocompleta con la ultima parada", None))
        self.lblConductor_2.setText(QCoreApplication.translate("RutasWidget", u"Nueva Parada: ", None))
        self.btnAgregarParada.setText(QCoreApplication.translate("RutasWidget", u"+", None))
        self.btnEliminarParada.setText(QCoreApplication.translate("RutasWidget", u"-", None))
        self.leNuevaParada.setPlaceholderText(QCoreApplication.translate("RutasWidget", u"Escribe una direcci\u00f3n y pulsa + ", None))
        self.btnGuardarRuta.setText(QCoreApplication.translate("RutasWidget", u"Guardar Ruta", None))
    # retranslateUi

