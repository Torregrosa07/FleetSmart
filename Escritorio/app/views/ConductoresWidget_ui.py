# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConductoresWidget.ui'
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

class Ui_ConductoresWidget(object):
    def setupUi(self, ConductoresWidget):
        if not ConductoresWidget.objectName():
            ConductoresWidget.setObjectName(u"ConductoresWidget")
        ConductoresWidget.resize(1204, 768)
        self.verticalLayout = QVBoxLayout(ConductoresWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameConductoresTop = QFrame(ConductoresWidget)
        self.frameConductoresTop.setObjectName(u"frameConductoresTop")
        self.frameConductoresTop.setMaximumSize(QSize(16777215, 50))
        self.frameConductoresTop.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameConductoresTop.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frameConductoresTop)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 8, 7, -1)
        self.label_4 = QLabel(self.frameConductoresTop)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(13)
        font.setBold(True)
        self.label_4.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.horizontalSpacer_2 = QSpacerItem(841, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.btnNuevoConductor = QPushButton(self.frameConductoresTop)
        self.btnNuevoConductor.setObjectName(u"btnNuevoConductor")
        self.btnNuevoConductor.setEnabled(True)
        self.btnNuevoConductor.setMaximumSize(QSize(16777215, 60))
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(13)
        font1.setWeight(QFont.Black)
        font1.setStrikeOut(False)
        self.btnNuevoConductor.setFont(font1)
        self.btnNuevoConductor.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnNuevoConductor.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.btnNuevoConductor)


        self.verticalLayout.addWidget(self.frameConductoresTop)

        self.tablaCondcutores = QTableWidget(ConductoresWidget)
        if (self.tablaCondcutores.columnCount() < 6):
            self.tablaCondcutores.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaCondcutores.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaCondcutores.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaCondcutores.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaCondcutores.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaCondcutores.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tablaCondcutores.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tablaCondcutores.setObjectName(u"tablaCondcutores")
        self.tablaCondcutores.setMaximumSize(QSize(1000, 600))
        self.tablaCondcutores.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablaCondcutores.setAlternatingRowColors(True)
        self.tablaCondcutores.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tablaCondcutores.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablaCondcutores.setColumnCount(6)
        self.tablaCondcutores.horizontalHeader().setCascadingSectionResizes(True)
        self.tablaCondcutores.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tablaCondcutores.horizontalHeader().setStretchLastSection(False)
        self.tablaCondcutores.verticalHeader().setVisible(True)
        self.tablaCondcutores.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tablaCondcutores)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnEditar = QPushButton(ConductoresWidget)
        self.btnEditar.setObjectName(u"btnEditar")
        self.btnEditar.setEnabled(True)
        self.btnEditar.setMaximumSize(QSize(200, 40))
        self.btnEditar.setFont(font1)
        self.btnEditar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnEditar.setCheckable(True)

        self.horizontalLayout.addWidget(self.btnEditar)

        self.btnBorrar = QPushButton(ConductoresWidget)
        self.btnBorrar.setObjectName(u"btnBorrar")
        self.btnBorrar.setEnabled(True)
        self.btnBorrar.setMaximumSize(QSize(200, 40))
        self.btnBorrar.setFont(font1)
        self.btnBorrar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnBorrar.setCheckable(True)

        self.horizontalLayout.addWidget(self.btnBorrar)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ConductoresWidget)

        QMetaObject.connectSlotsByName(ConductoresWidget)
    # setupUi

    def retranslateUi(self, ConductoresWidget):
        ConductoresWidget.setWindowTitle(QCoreApplication.translate("ConductoresWidget", u"Form", None))
        self.label_4.setText(QCoreApplication.translate("ConductoresWidget", u"Gesti\u00f3n de Conductores", None))
        self.btnNuevoConductor.setText(QCoreApplication.translate("ConductoresWidget", u"+ A\u00f1adir Conductor", None))
        ___qtablewidgetitem = self.tablaCondcutores.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ConductoresWidget", u"Nombre", None));
        ___qtablewidgetitem1 = self.tablaCondcutores.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ConductoresWidget", u"DNI", None));
        ___qtablewidgetitem2 = self.tablaCondcutores.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ConductoresWidget", u"Licencia", None));
        ___qtablewidgetitem3 = self.tablaCondcutores.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ConductoresWidget", u"Estado", None));
        ___qtablewidgetitem4 = self.tablaCondcutores.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ConductoresWidget", u"Email", None));
        ___qtablewidgetitem5 = self.tablaCondcutores.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ConductoresWidget", u"Tel\u00e9fono", None));
        self.btnEditar.setText(QCoreApplication.translate("ConductoresWidget", u"Editar Conductor", None))
        self.btnBorrar.setText(QCoreApplication.translate("ConductoresWidget", u"Borrar Conductor", None))
    # retranslateUi

