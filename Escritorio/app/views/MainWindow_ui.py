# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1280, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frameSidebar = QFrame(self.widget)
        self.frameSidebar.setObjectName(u"frameSidebar")
        self.frameSidebar.setMinimumSize(QSize(250, 0))
        self.frameSidebar.setMaximumSize(QSize(250, 16777215))
        self.frameSidebar.setStyleSheet(u"")
        self.frameSidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameSidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frameSidebar)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.frameSidebar)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 40))
        self.label.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(15)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.menuContainer = QWidget(self.frameSidebar)
        self.menuContainer.setObjectName(u"menuContainer")
        self.verticalLayout_3 = QVBoxLayout(self.menuContainer)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.btnCommandCenter = QPushButton(self.menuContainer)
        self.btnCommandCenter.setObjectName(u"btnCommandCenter")
        self.btnCommandCenter.setEnabled(True)
        self.btnCommandCenter.setMinimumSize(QSize(0, 60))
        self.btnCommandCenter.setMaximumSize(QSize(16777215, 60))
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(13)
        font1.setWeight(QFont.Black)
        font1.setStrikeOut(False)
        self.btnCommandCenter.setFont(font1)
        self.btnCommandCenter.setStyleSheet(u"")
        self.btnCommandCenter.setCheckable(True)
        self.btnCommandCenter.setFlat(False)

        self.verticalLayout_3.addWidget(self.btnCommandCenter)

        self.btnDrivers = QPushButton(self.menuContainer)
        self.btnDrivers.setObjectName(u"btnDrivers")
        self.btnDrivers.setEnabled(True)
        self.btnDrivers.setMinimumSize(QSize(0, 60))
        self.btnDrivers.setMaximumSize(QSize(16777215, 60))
        self.btnDrivers.setFont(font1)
        self.btnDrivers.setStyleSheet(u"")
        self.btnDrivers.setCheckable(True)
        self.btnDrivers.setFlat(False)

        self.verticalLayout_3.addWidget(self.btnDrivers)

        self.btnVehicles = QPushButton(self.menuContainer)
        self.btnVehicles.setObjectName(u"btnVehicles")
        self.btnVehicles.setEnabled(True)
        self.btnVehicles.setMinimumSize(QSize(0, 60))
        self.btnVehicles.setMaximumSize(QSize(16777215, 60))
        self.btnVehicles.setFont(font1)
        self.btnVehicles.setStyleSheet(u"")
        self.btnVehicles.setCheckable(True)
        self.btnVehicles.setFlat(False)

        self.verticalLayout_3.addWidget(self.btnVehicles)

        self.btnRoutes = QPushButton(self.menuContainer)
        self.btnRoutes.setObjectName(u"btnRoutes")
        self.btnRoutes.setEnabled(True)
        self.btnRoutes.setMinimumSize(QSize(0, 60))
        self.btnRoutes.setMaximumSize(QSize(16777215, 60))
        self.btnRoutes.setFont(font1)
        self.btnRoutes.setStyleSheet(u"")
        self.btnRoutes.setCheckable(True)
        self.btnRoutes.setFlat(False)

        self.verticalLayout_3.addWidget(self.btnRoutes)

        self.btnAssign = QPushButton(self.menuContainer)
        self.btnAssign.setObjectName(u"btnAssign")
        self.btnAssign.setEnabled(True)
        self.btnAssign.setMinimumSize(QSize(0, 60))
        self.btnAssign.setMaximumSize(QSize(16777215, 60))
        self.btnAssign.setFont(font1)
        self.btnAssign.setStyleSheet(u"")
        self.btnAssign.setCheckable(True)
        self.btnAssign.setFlat(False)

        self.verticalLayout_3.addWidget(self.btnAssign)

        self.btnIncidents = QPushButton(self.menuContainer)
        self.btnIncidents.setObjectName(u"btnIncidents")
        self.btnIncidents.setEnabled(True)
        self.btnIncidents.setMinimumSize(QSize(0, 60))
        self.btnIncidents.setMaximumSize(QSize(16777215, 60))
        self.btnIncidents.setFont(font1)
        self.btnIncidents.setStyleSheet(u"")
        self.btnIncidents.setCheckable(True)
        self.btnIncidents.setFlat(False)

        self.verticalLayout_3.addWidget(self.btnIncidents)

        self.btnSettings = QPushButton(self.menuContainer)
        self.btnSettings.setObjectName(u"btnSettings")
        self.btnSettings.setMinimumSize(QSize(0, 60))
        self.btnSettings.setMaximumSize(QSize(16777215, 60))
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(13)
        font2.setWeight(QFont.Black)
        self.btnSettings.setFont(font2)

        self.verticalLayout_3.addWidget(self.btnSettings)


        self.verticalLayout_2.addWidget(self.menuContainer)


        self.horizontalLayout.addWidget(self.frameSidebar)

        self.frameMainContent = QFrame(self.widget)
        self.frameMainContent.setObjectName(u"frameMainContent")
        self.frameMainContent.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameMainContent.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frameMainContent)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frameTopBar = QFrame(self.frameMainContent)
        self.frameTopBar.setObjectName(u"frameTopBar")
        self.frameTopBar.setMaximumSize(QSize(16777215, 60))
        self.frameTopBar.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameTopBar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frameTopBar)
        self.horizontalLayout_2.setSpacing(9)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 8, -1)
        self.lblPageTitle = QLabel(self.frameTopBar)
        self.lblPageTitle.setObjectName(u"lblPageTitle")
        font3 = QFont()
        font3.setFamilies([u"Montserrat"])
        font3.setPointSize(14)
        font3.setBold(True)
        self.lblPageTitle.setFont(font3)

        self.horizontalLayout_2.addWidget(self.lblPageTitle)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.lblDate = QLabel(self.frameTopBar)
        self.lblDate.setObjectName(u"lblDate")
        font4 = QFont()
        font4.setFamilies([u"Montserrat"])
        font4.setPointSize(14)
        self.lblDate.setFont(font4)

        self.horizontalLayout_2.addWidget(self.lblDate)


        self.verticalLayout_4.addWidget(self.frameTopBar)

        self.stackContent = QStackedWidget(self.frameMainContent)
        self.stackContent.setObjectName(u"stackContent")
        self.page_dashboard = QWidget()
        self.page_dashboard.setObjectName(u"page_dashboard")
        self.stackContent.addWidget(self.page_dashboard)
        self.page_vehiculos = QWidget()
        self.page_vehiculos.setObjectName(u"page_vehiculos")
        self.stackContent.addWidget(self.page_vehiculos)
        self.page_conductores = QWidget()
        self.page_conductores.setObjectName(u"page_conductores")
        self.stackContent.addWidget(self.page_conductores)

        self.verticalLayout_4.addWidget(self.stackContent)


        self.horizontalLayout.addWidget(self.frameMainContent)


        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackContent.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"FleetSmart", None))
        self.btnCommandCenter.setText(QCoreApplication.translate("MainWindow", u"Centro de Mando", None))
        self.btnDrivers.setText(QCoreApplication.translate("MainWindow", u"Conductores", None))
        self.btnVehicles.setText(QCoreApplication.translate("MainWindow", u"Veh\u00edculos", None))
        self.btnRoutes.setText(QCoreApplication.translate("MainWindow", u"Crear Rutas", None))
        self.btnAssign.setText(QCoreApplication.translate("MainWindow", u"Asignar Rutas", None))
        self.btnIncidents.setText(QCoreApplication.translate("MainWindow", u"Incidencias", None))
        self.btnSettings.setText(QCoreApplication.translate("MainWindow", u"Ajustes", None))
        self.lblPageTitle.setText(QCoreApplication.translate("MainWindow", u"Centro de Mando", None))
        self.lblDate.setText(QCoreApplication.translate("MainWindow", u"Fecha", None))
    # retranslateUi

