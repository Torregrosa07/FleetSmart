# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CommandCenterPage.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_CommandCenterPage(object):
    def setupUi(self, CommandCenterPage):
        if not CommandCenterPage.objectName():
            CommandCenterPage.setObjectName(u"CommandCenterPage")
        CommandCenterPage.resize(968, 673)
        self.verticalLayout = QVBoxLayout(CommandCenterPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frameHeader = QFrame(CommandCenterPage)
        self.frameHeader.setObjectName(u"frameHeader")
        self.frameHeader.setMinimumSize(QSize(0, 80))
        self.frameHeader.setMaximumSize(QSize(16777215, 80))
        self.frameHeader.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameHeader.setFrameShadow(QFrame.Shadow.Raised)
        self.lblTitulo = QLabel(self.frameHeader)
        self.lblTitulo.setObjectName(u"lblTitulo")
        self.lblTitulo.setGeometry(QRect(40, 10, 211, 16))
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(15)
        font.setBold(True)
        self.lblTitulo.setFont(font)
        self.lblSubtitulo = QLabel(self.frameHeader)
        self.lblSubtitulo.setObjectName(u"lblSubtitulo")
        self.lblSubtitulo.setGeometry(QRect(40, 50, 501, 16))
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(13)
        self.lblSubtitulo.setFont(font1)

        self.verticalLayout.addWidget(self.frameHeader)

        self.widget = QWidget(CommandCenterPage)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frameLeftPanel = QFrame(self.widget)
        self.frameLeftPanel.setObjectName(u"frameLeftPanel")
        self.frameLeftPanel.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameLeftPanel.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frameLeftPanel)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupConductores = QGroupBox(self.frameLeftPanel)
        self.groupConductores.setObjectName(u"groupConductores")
        self.verticalLayout_2 = QVBoxLayout(self.groupConductores)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listConductores = QListWidget(self.groupConductores)
        self.listConductores.setObjectName(u"listConductores")

        self.verticalLayout_2.addWidget(self.listConductores)


        self.verticalLayout_3.addWidget(self.groupConductores)


        self.horizontalLayout.addWidget(self.frameLeftPanel)

        self.frameMapPanel = QFrame(self.widget)
        self.frameMapPanel.setObjectName(u"frameMapPanel")
        self.frameMapPanel.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameMapPanel.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frameMapPanel)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lblTitulo_2 = QLabel(self.frameMapPanel)
        self.lblTitulo_2.setObjectName(u"lblTitulo_2")
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.lblTitulo_2.setFont(font2)

        self.verticalLayout_5.addWidget(self.lblTitulo_2)

        self.webMap = QWebEngineView(self.frameMapPanel)
        self.webMap.setObjectName(u"webMap")
        self.webMap.setMinimumSize(QSize(600, 400))
        self.webMap.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_5.addWidget(self.webMap)

        self.frameLeyenda = QFrame(self.frameMapPanel)
        self.frameLeyenda.setObjectName(u"frameLeyenda")
        self.frameLeyenda.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameLeyenda.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frameLeyenda)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lblLeyenda1 = QLabel(self.frameLeyenda)
        self.lblLeyenda1.setObjectName(u"lblLeyenda1")
        font3 = QFont()
        font3.setFamilies([u"Montserrat"])
        font3.setPointSize(11)
        font3.setBold(True)
        self.lblLeyenda1.setFont(font3)
        self.lblLeyenda1.setStyleSheet(u"color: rgb(0, 255, 0);")

        self.verticalLayout_4.addWidget(self.lblLeyenda1)

        self.lblLeyenda2 = QLabel(self.frameLeyenda)
        self.lblLeyenda2.setObjectName(u"lblLeyenda2")
        self.lblLeyenda2.setFont(font3)
        self.lblLeyenda2.setStyleSheet(u"color: rgb(255, 219, 73);")

        self.verticalLayout_4.addWidget(self.lblLeyenda2)

        self.lblLeyenda3 = QLabel(self.frameLeyenda)
        self.lblLeyenda3.setObjectName(u"lblLeyenda3")
        self.lblLeyenda3.setFont(font3)
        self.lblLeyenda3.setStyleSheet(u"color: rgb(78, 246, 255);")

        self.verticalLayout_4.addWidget(self.lblLeyenda3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.btnActualizar = QPushButton(self.frameLeyenda)
        self.btnActualizar.setObjectName(u"btnActualizar")
        self.btnActualizar.setEnabled(True)
        self.btnActualizar.setMaximumSize(QSize(16777215, 60))
        font4 = QFont()
        font4.setFamilies([u"Montserrat"])
        font4.setPointSize(13)
        font4.setWeight(QFont.Black)
        font4.setStrikeOut(False)
        self.btnActualizar.setFont(font4)
        self.btnActualizar.setStyleSheet(u"background-color: #3b82f6; color: white;")
        self.btnActualizar.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.btnActualizar)


        self.verticalLayout_5.addWidget(self.frameLeyenda)


        self.horizontalLayout.addWidget(self.frameMapPanel)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)

        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(CommandCenterPage)

        QMetaObject.connectSlotsByName(CommandCenterPage)
    # setupUi

    def retranslateUi(self, CommandCenterPage):
        CommandCenterPage.setWindowTitle(QCoreApplication.translate("CommandCenterPage", u"Form", None))
        self.lblTitulo.setText(QCoreApplication.translate("CommandCenterPage", u"Centro de Mando", None))
        self.lblSubtitulo.setText(QCoreApplication.translate("CommandCenterPage", u"Monitorea la ub\u00edcaci\u00f3n de los condcutores en tiempo real", None))
        self.groupConductores.setTitle(QCoreApplication.translate("CommandCenterPage", u"Conductores Activos", None))
        self.lblTitulo_2.setText(QCoreApplication.translate("CommandCenterPage", u"Mapa en tiempo real", None))
        self.lblLeyenda1.setText(QCoreApplication.translate("CommandCenterPage", u"En Ruta", None))
        self.lblLeyenda2.setText(QCoreApplication.translate("CommandCenterPage", u"Pausado", None))
        self.lblLeyenda3.setText(QCoreApplication.translate("CommandCenterPage", u"Completado", None))
        self.btnActualizar.setText(QCoreApplication.translate("CommandCenterPage", u"Actualizar Mapa", None))
    # retranslateUi

