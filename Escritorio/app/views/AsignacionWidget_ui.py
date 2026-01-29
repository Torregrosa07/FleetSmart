# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AsignacionWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateTimeEdit, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_AsignacionWidget(object):
    def setupUi(self, AsignacionWidget):
        if not AsignacionWidget.objectName():
            AsignacionWidget.setObjectName(u"AsignacionWidget")
        AsignacionWidget.resize(1217, 765)
        self.horizontalLayout_2 = QHBoxLayout(AsignacionWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(AsignacionWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 250))
        self.groupBox.setMaximumSize(QSize(250, 16777215))
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 55)
        self.lblSeleccionar = QLabel(self.groupBox)
        self.lblSeleccionar.setObjectName(u"lblSeleccionar")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(13)
        font1.setBold(True)
        self.lblSeleccionar.setFont(font1)
        self.lblSeleccionar.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.lblSeleccionar)

        self.cbRuta = QComboBox(self.groupBox)
        self.cbRuta.setObjectName(u"cbRuta")
        self.cbRuta.setFont(font)

        self.verticalLayout_3.addWidget(self.cbRuta)

        self.lblConductor = QLabel(self.groupBox)
        self.lblConductor.setObjectName(u"lblConductor")
        self.lblConductor.setFont(font1)
        self.lblConductor.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.lblConductor)

        self.cbConductor = QComboBox(self.groupBox)
        self.cbConductor.setObjectName(u"cbConductor")
        self.cbConductor.setFont(font)

        self.verticalLayout_3.addWidget(self.cbConductor)

        self.lblVehiculo = QLabel(self.groupBox)
        self.lblVehiculo.setObjectName(u"lblVehiculo")
        self.lblVehiculo.setFont(font1)
        self.lblVehiculo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.lblVehiculo)

        self.cbVehiculo = QComboBox(self.groupBox)
        self.cbVehiculo.setObjectName(u"cbVehiculo")
        self.cbVehiculo.setFont(font)

        self.verticalLayout_3.addWidget(self.cbVehiculo)

        self.lblFechaHora = QLabel(self.groupBox)
        self.lblFechaHora.setObjectName(u"lblFechaHora")
        self.lblFechaHora.setFont(font1)
        self.lblFechaHora.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.lblFechaHora)

        self.dtInicio = QDateTimeEdit(self.groupBox)
        self.dtInicio.setObjectName(u"dtInicio")
        self.dtInicio.setCalendarPopup(True)

        self.verticalLayout_3.addWidget(self.dtInicio)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.btnConfirmar = QPushButton(self.groupBox)
        self.btnConfirmar.setObjectName(u"btnConfirmar")
        self.btnConfirmar.setEnabled(True)
        self.btnConfirmar.setMinimumSize(QSize(0, 60))
        self.btnConfirmar.setMaximumSize(QSize(16777215, 60))
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(13)
        font2.setWeight(QFont.Black)
        font2.setStrikeOut(False)
        self.btnConfirmar.setFont(font2)
        self.btnConfirmar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnConfirmar.setCheckable(True)

        self.verticalLayout_4.addWidget(self.btnConfirmar)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.groupBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_2 = QGroupBox(AsignacionWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableWidget = QTableWidget(self.groupBox_2)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.btnEliminarAsignacion = QPushButton(self.groupBox_2)
        self.btnEliminarAsignacion.setObjectName(u"btnEliminarAsignacion")
        self.btnEliminarAsignacion.setEnabled(True)
        self.btnEliminarAsignacion.setMinimumSize(QSize(0, 60))
        self.btnEliminarAsignacion.setMaximumSize(QSize(300, 40))
        self.btnEliminarAsignacion.setFont(font2)
        self.btnEliminarAsignacion.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnEliminarAsignacion.setCheckable(True)

        self.verticalLayout_2.addWidget(self.btnEliminarAsignacion)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 3)

        self.retranslateUi(AsignacionWidget)

        QMetaObject.connectSlotsByName(AsignacionWidget)
    # setupUi

    def retranslateUi(self, AsignacionWidget):
        AsignacionWidget.setWindowTitle(QCoreApplication.translate("AsignacionWidget", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("AsignacionWidget", u"Nueva Asignaci\u00f3n", None))
        self.lblSeleccionar.setText(QCoreApplication.translate("AsignacionWidget", u"Seleccionar Ruta: ", None))
        self.lblConductor.setText(QCoreApplication.translate("AsignacionWidget", u"Conductor: ", None))
        self.lblVehiculo.setText(QCoreApplication.translate("AsignacionWidget", u"Veh\u00edculo: ", None))
        self.lblFechaHora.setText(QCoreApplication.translate("AsignacionWidget", u"Fecha y hora de inicio: ", None))
        self.btnConfirmar.setText(QCoreApplication.translate("AsignacionWidget", u"Confirmar asignaci\u00f3n", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("AsignacionWidget", u"Rutas Disponibles y Asignadas", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("AsignacionWidget", u"Ruta", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("AsignacionWidget", u"Conductor", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("AsignacionWidget", u"Veh\u00edculo", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("AsignacionWidget", u"Estado", None));
        self.btnEliminarAsignacion.setText(QCoreApplication.translate("AsignacionWidget", u"Eliminar Asignaci\u00f3n", None))
    # retranslateUi

