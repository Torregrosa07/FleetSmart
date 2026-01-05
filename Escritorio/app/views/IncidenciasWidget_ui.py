# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'IncidenciasWidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHeaderView, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_IncidenciasWidget(object):
    def setupUi(self, IncidenciasWidget):
        if not IncidenciasWidget.objectName():
            IncidenciasWidget.setObjectName(u"IncidenciasWidget")
        IncidenciasWidget.resize(1222, 726)
        self.verticalLayout = QVBoxLayout(IncidenciasWidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 9, -1, -1)
        self.cbFiltroEstado = QComboBox(IncidenciasWidget)
        self.cbFiltroEstado.addItem("")
        self.cbFiltroEstado.addItem("")
        self.cbFiltroEstado.addItem("")
        self.cbFiltroEstado.addItem("")
        self.cbFiltroEstado.setObjectName(u"cbFiltroEstado")
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(12)
        self.cbFiltroEstado.setFont(font)

        self.verticalLayout.addWidget(self.cbFiltroEstado)

        self.tablaIncidencias = QTableWidget(IncidenciasWidget)
        if (self.tablaIncidencias.columnCount() < 7):
            self.tablaIncidencias.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaIncidencias.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaIncidencias.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaIncidencias.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaIncidencias.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaIncidencias.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tablaIncidencias.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tablaIncidencias.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tablaIncidencias.setObjectName(u"tablaIncidencias")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        self.tablaIncidencias.setFont(font1)
        self.tablaIncidencias.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tablaIncidencias.setAlternatingRowColors(True)
        self.tablaIncidencias.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tablaIncidencias.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tablaIncidencias.setColumnCount(7)

        self.verticalLayout.addWidget(self.tablaIncidencias)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btnRecargar = QPushButton(IncidenciasWidget)
        self.btnRecargar.setObjectName(u"btnRecargar")
        self.btnRecargar.setEnabled(True)
        self.btnRecargar.setMaximumSize(QSize(16777215, 60))
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(13)
        font2.setWeight(QFont.Black)
        font2.setStrikeOut(False)
        self.btnRecargar.setFont(font2)
        self.btnRecargar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnRecargar.setCheckable(True)

        self.gridLayout.addWidget(self.btnRecargar, 0, 0, 1, 1)

        self.btnNuevaIncidencia = QPushButton(IncidenciasWidget)
        self.btnNuevaIncidencia.setObjectName(u"btnNuevaIncidencia")
        self.btnNuevaIncidencia.setEnabled(True)
        self.btnNuevaIncidencia.setMaximumSize(QSize(16777215, 60))
        self.btnNuevaIncidencia.setFont(font2)
        self.btnNuevaIncidencia.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnNuevaIncidencia.setCheckable(True)

        self.gridLayout.addWidget(self.btnNuevaIncidencia, 0, 1, 1, 1)

        self.btnCambiarEstado = QPushButton(IncidenciasWidget)
        self.btnCambiarEstado.setObjectName(u"btnCambiarEstado")
        self.btnCambiarEstado.setEnabled(True)
        self.btnCambiarEstado.setMaximumSize(QSize(16777215, 60))
        self.btnCambiarEstado.setFont(font2)
        self.btnCambiarEstado.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnCambiarEstado.setCheckable(True)

        self.gridLayout.addWidget(self.btnCambiarEstado, 1, 0, 1, 1)

        self.btnEliminar = QPushButton(IncidenciasWidget)
        self.btnEliminar.setObjectName(u"btnEliminar")
        self.btnEliminar.setEnabled(True)
        self.btnEliminar.setMaximumSize(QSize(16777215, 60))
        self.btnEliminar.setFont(font2)
        self.btnEliminar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnEliminar.setCheckable(True)

        self.gridLayout.addWidget(self.btnEliminar, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(IncidenciasWidget)

        QMetaObject.connectSlotsByName(IncidenciasWidget)
    # setupUi

    def retranslateUi(self, IncidenciasWidget):
        IncidenciasWidget.setWindowTitle(QCoreApplication.translate("IncidenciasWidget", u"Form", None))
        self.cbFiltroEstado.setItemText(0, QCoreApplication.translate("IncidenciasWidget", u"Todas", None))
        self.cbFiltroEstado.setItemText(1, QCoreApplication.translate("IncidenciasWidget", u"Pendiente", None))
        self.cbFiltroEstado.setItemText(2, QCoreApplication.translate("IncidenciasWidget", u"En Proceso", None))
        self.cbFiltroEstado.setItemText(3, QCoreApplication.translate("IncidenciasWidget", u"Resuelta", None))

        ___qtablewidgetitem = self.tablaIncidencias.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("IncidenciasWidget", u"Fecha", None));
        ___qtablewidgetitem1 = self.tablaIncidencias.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("IncidenciasWidget", u"Hora", None));
        ___qtablewidgetitem2 = self.tablaIncidencias.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("IncidenciasWidget", u"Veh\u00edculo", None));
        ___qtablewidgetitem3 = self.tablaIncidencias.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("IncidenciasWidget", u"Tipo", None));
        ___qtablewidgetitem4 = self.tablaIncidencias.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("IncidenciasWidget", u"Estado", None));
        ___qtablewidgetitem5 = self.tablaIncidencias.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("IncidenciasWidget", u"Descripci\u00f3n", None));
        ___qtablewidgetitem6 = self.tablaIncidencias.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("IncidenciasWidget", u"Conductor", None));
        self.btnRecargar.setText(QCoreApplication.translate("IncidenciasWidget", u"Recargar", None))
        self.btnNuevaIncidencia.setText(QCoreApplication.translate("IncidenciasWidget", u"+ Nueva Incidencia", None))
        self.btnCambiarEstado.setText(QCoreApplication.translate("IncidenciasWidget", u"Cambiar Estado", None))
        self.btnEliminar.setText(QCoreApplication.translate("IncidenciasWidget", u"Eliminar", None))
    # retranslateUi

