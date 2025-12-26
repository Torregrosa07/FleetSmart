# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(408, 300)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, -1, -1, -1)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(20)
        self.lblTema = QLabel(SettingsDialog)
        self.lblTema.setObjectName(u"lblTema")
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(12)
        font.setBold(True)
        self.lblTema.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblTema)

        self.cbTema = QComboBox(SettingsDialog)
        self.cbTema.addItem("")
        self.cbTema.addItem("")
        self.cbTema.setObjectName(u"cbTema")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(12)
        self.cbTema.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.cbTema)

        self.cbIdioma = QComboBox(SettingsDialog)
        self.cbIdioma.addItem("")
        self.cbIdioma.addItem("")
        self.cbIdioma.setObjectName(u"cbIdioma")
        self.cbIdioma.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.cbIdioma)

        self.lblIdioma = QLabel(SettingsDialog)
        self.lblIdioma.setObjectName(u"lblIdioma")
        self.lblIdioma.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblIdioma)

        self.lblDireccion = QLabel(SettingsDialog)
        self.lblDireccion.setObjectName(u"lblDireccion")
        self.lblDireccion.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblDireccion)

        self.leDireccion = QLineEdit(SettingsDialog)
        self.leDireccion.setObjectName(u"leDireccion")
        self.leDireccion.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.leDireccion)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(200, -1, -1, -1)
        self.btnCancelar = QPushButton(SettingsDialog)
        self.btnCancelar.setObjectName(u"btnCancelar")
        self.btnCancelar.setMinimumSize(QSize(0, 30))
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(11)
        font2.setBold(True)
        self.btnCancelar.setFont(font2)

        self.horizontalLayout.addWidget(self.btnCancelar)

        self.btnGuardar = QPushButton(SettingsDialog)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setMinimumSize(QSize(0, 30))
        self.btnGuardar.setFont(font2)

        self.horizontalLayout.addWidget(self.btnGuardar)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(SettingsDialog)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Dialog", None))
        self.lblTema.setText(QCoreApplication.translate("SettingsDialog", u"Tema: ", None))
        self.cbTema.setItemText(0, QCoreApplication.translate("SettingsDialog", u"Claro", None))
        self.cbTema.setItemText(1, QCoreApplication.translate("SettingsDialog", u"Oscuro", None))

        self.cbIdioma.setItemText(0, QCoreApplication.translate("SettingsDialog", u"Espa\u00f1ol", None))
        self.cbIdioma.setItemText(1, QCoreApplication.translate("SettingsDialog", u"Ingl\u00e9s", None))

        self.lblIdioma.setText(QCoreApplication.translate("SettingsDialog", u"Idioma: ", None))
        self.lblDireccion.setText(QCoreApplication.translate("SettingsDialog", u"Direcci\u00f3n Base: ", None))
        self.btnCancelar.setText(QCoreApplication.translate("SettingsDialog", u"Cancelar", None))
        self.btnGuardar.setText(QCoreApplication.translate("SettingsDialog", u"Guardar", None))
    # retranslateUi

