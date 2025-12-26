# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConductoresDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ConductoresDialog(object):
    def setupUi(self, ConductoresDialog):
        if not ConductoresDialog.objectName():
            ConductoresDialog.setObjectName(u"ConductoresDialog")
        ConductoresDialog.resize(408, 258)
        self.verticalLayout = QVBoxLayout(ConductoresDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(10)
        self.lblNombre = QLabel(ConductoresDialog)
        self.lblNombre.setObjectName(u"lblNombre")
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(12)
        font.setBold(True)
        self.lblNombre.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblNombre)

        self.leNombre = QLineEdit(ConductoresDialog)
        self.leNombre.setObjectName(u"leNombre")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(12)
        self.leNombre.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leNombre)

        self.lblDNI = QLabel(ConductoresDialog)
        self.lblDNI.setObjectName(u"lblDNI")
        self.lblDNI.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblDNI)

        self.leDNI = QLineEdit(ConductoresDialog)
        self.leDNI.setObjectName(u"leDNI")
        self.leDNI.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.leDNI)

        self.lblModel = QLabel(ConductoresDialog)
        self.lblModel.setObjectName(u"lblModel")
        self.lblModel.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblModel)

        self.leLicencia = QLineEdit(ConductoresDialog)
        self.leLicencia.setObjectName(u"leLicencia")
        self.leLicencia.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.leLicencia)

        self.lblEmail = QLabel(ConductoresDialog)
        self.lblEmail.setObjectName(u"lblEmail")
        self.lblEmail.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblEmail)

        self.leEmail = QLineEdit(ConductoresDialog)
        self.leEmail.setObjectName(u"leEmail")
        self.leEmail.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.leEmail)

        self.leTelefono = QLineEdit(ConductoresDialog)
        self.leTelefono.setObjectName(u"leTelefono")
        self.leTelefono.setFont(font1)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.leTelefono)

        self.lblTelefono = QLabel(ConductoresDialog)
        self.lblTelefono.setObjectName(u"lblTelefono")
        self.lblTelefono.setFont(font)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblTelefono)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(200, -1, -1, -1)
        self.btnCancelar = QPushButton(ConductoresDialog)
        self.btnCancelar.setObjectName(u"btnCancelar")
        self.btnCancelar.setMinimumSize(QSize(0, 30))
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(11)
        font2.setBold(True)
        self.btnCancelar.setFont(font2)

        self.horizontalLayout.addWidget(self.btnCancelar)

        self.btnGuardar = QPushButton(ConductoresDialog)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setMinimumSize(QSize(0, 30))
        self.btnGuardar.setFont(font2)

        self.horizontalLayout.addWidget(self.btnGuardar)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ConductoresDialog)

        QMetaObject.connectSlotsByName(ConductoresDialog)
    # setupUi

    def retranslateUi(self, ConductoresDialog):
        ConductoresDialog.setWindowTitle(QCoreApplication.translate("ConductoresDialog", u"Dialog", None))
        self.lblNombre.setText(QCoreApplication.translate("ConductoresDialog", u"Nombre: ", None))
        self.lblDNI.setText(QCoreApplication.translate("ConductoresDialog", u"DNI/NIE:", None))
        self.lblModel.setText(QCoreApplication.translate("ConductoresDialog", u"Licencia: ", None))
        self.lblEmail.setText(QCoreApplication.translate("ConductoresDialog", u"Email:", None))
        self.lblTelefono.setText(QCoreApplication.translate("ConductoresDialog", u"Tel\u00e9fono:", None))
        self.btnCancelar.setText(QCoreApplication.translate("ConductoresDialog", u"Cancelar", None))
        self.btnGuardar.setText(QCoreApplication.translate("ConductoresDialog", u"Guardar", None))
    # retranslateUi

