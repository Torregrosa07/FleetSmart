# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VehiculosWidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_VehiculosWidget(object):
    def setupUi(self, VehiculosWidget):
        if not VehiculosWidget.objectName():
            VehiculosWidget.setObjectName(u"VehiculosWidget")
        VehiculosWidget.resize(1204, 768)
        self.verticalLayout = QVBoxLayout(VehiculosWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameVehiculosTop = QFrame(VehiculosWidget)
        self.frameVehiculosTop.setObjectName(u"frameVehiculosTop")
        self.frameVehiculosTop.setMaximumSize(QSize(16777215, 50))
        self.frameVehiculosTop.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameVehiculosTop.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frameVehiculosTop)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 8, 7, -1)
        self.label_4 = QLabel(self.frameVehiculosTop)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(13)
        font.setBold(True)
        self.label_4.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.horizontalSpacer_2 = QSpacerItem(841, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.btnNuevoVehiculo = QPushButton(self.frameVehiculosTop)
        self.btnNuevoVehiculo.setObjectName(u"btnNuevoVehiculo")
        self.btnNuevoVehiculo.setEnabled(True)
        self.btnNuevoVehiculo.setMaximumSize(QSize(16777215, 60))
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(13)
        font1.setWeight(QFont.Black)
        font1.setStrikeOut(False)
        self.btnNuevoVehiculo.setFont(font1)
        self.btnNuevoVehiculo.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnNuevoVehiculo.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.btnNuevoVehiculo)


        self.verticalLayout.addWidget(self.frameVehiculosTop)

        self.tablaVehiculos = QTableWidget(VehiculosWidget)
        if (self.tablaVehiculos.columnCount() < 6):
            self.tablaVehiculos.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaVehiculos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaVehiculos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaVehiculos.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaVehiculos.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaVehiculos.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tablaVehiculos.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tablaVehiculos.setObjectName(u"tablaVehiculos")
        self.tablaVehiculos.setMaximumSize(QSize(1000, 600))
        self.tablaVehiculos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablaVehiculos.setAlternatingRowColors(True)
        self.tablaVehiculos.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tablaVehiculos.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablaVehiculos.setColumnCount(6)
        self.tablaVehiculos.horizontalHeader().setCascadingSectionResizes(True)
        self.tablaVehiculos.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tablaVehiculos.horizontalHeader().setStretchLastSection(False)
        self.tablaVehiculos.verticalHeader().setVisible(True)
        self.tablaVehiculos.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tablaVehiculos)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnEditar = QPushButton(VehiculosWidget)
        self.btnEditar.setObjectName(u"btnEditar")
        self.btnEditar.setEnabled(True)
        self.btnEditar.setMaximumSize(QSize(200, 40))
        self.btnEditar.setFont(font1)
        self.btnEditar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnEditar.setCheckable(True)

        self.horizontalLayout.addWidget(self.btnEditar)

        self.btnBorrar = QPushButton(VehiculosWidget)
        self.btnBorrar.setObjectName(u"btnBorrar")
        self.btnBorrar.setEnabled(True)
        self.btnBorrar.setMaximumSize(QSize(200, 40))
        self.btnBorrar.setFont(font1)
        self.btnBorrar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnBorrar.setCheckable(True)

        self.horizontalLayout.addWidget(self.btnBorrar)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(VehiculosWidget)

        QMetaObject.connectSlotsByName(VehiculosWidget)
    # setupUi

    def retranslateUi(self, VehiculosWidget):
        VehiculosWidget.setWindowTitle(QCoreApplication.translate("VehiculosWidget", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("VehiculosWidget", u"Gesti\u00f3n de Veh\u00edculos", None))
        self.btnNuevoVehiculo.setText(QCoreApplication.translate("VehiculosWidget", u"+ A\u00f1adir Veh\u00edculo", None))
        ___qtablewidgetitem = self.tablaVehiculos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("VehiculosWidget", u"Matr\u00edcula", None));
        ___qtablewidgetitem1 = self.tablaVehiculos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("VehiculosWidget", u"Marca", None));
        ___qtablewidgetitem2 = self.tablaVehiculos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("VehiculosWidget", u"Modelo", None));
        ___qtablewidgetitem3 = self.tablaVehiculos.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("VehiculosWidget", u"Estado", None));
        ___qtablewidgetitem4 = self.tablaVehiculos.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("VehiculosWidget", u"A\u00f1o", None));
        ___qtablewidgetitem5 = self.tablaVehiculos.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("VehiculosWidget", u"Pr\u00f3xima ITV", None));
        self.btnEditar.setText(QCoreApplication.translate("VehiculosWidget", u"Editar Veh\u00edculo", None))
        self.btnBorrar.setText(QCoreApplication.translate("VehiculosWidget", u"Borrar Veh\u00edculo", None))
    # retranslateUi

