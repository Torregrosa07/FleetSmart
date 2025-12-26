# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VehiculosDialog.ui'
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

class Ui_VehiculosDialog(object):
    def setupUi(self, VehiculosDialog):
        if not VehiculosDialog.objectName():
            VehiculosDialog.setObjectName(u"VehiculosDialog")
        VehiculosDialog.resize(408, 268)
        self.verticalLayout = QVBoxLayout(VehiculosDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(10)
        self.lblMatricula = QLabel(VehiculosDialog)
        self.lblMatricula.setObjectName(u"lblMatricula")
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(12)
        font.setBold(True)
        self.lblMatricula.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblMatricula)

        self.leMatricula = QLineEdit(VehiculosDialog)
        self.leMatricula.setObjectName(u"leMatricula")
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(12)
        self.leMatricula.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leMatricula)

        self.lblMarca = QLabel(VehiculosDialog)
        self.lblMarca.setObjectName(u"lblMarca")
        self.lblMarca.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblMarca)

        self.leMarca = QLineEdit(VehiculosDialog)
        self.leMarca.setObjectName(u"leMarca")
        self.leMarca.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.leMarca)

        self.lblModelo = QLabel(VehiculosDialog)
        self.lblModelo.setObjectName(u"lblModelo")
        self.lblModelo.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblModelo)

        self.leModelo = QLineEdit(VehiculosDialog)
        self.leModelo.setObjectName(u"leModelo")
        self.leModelo.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.leModelo)

        self.lblAno = QLabel(VehiculosDialog)
        self.lblAno.setObjectName(u"lblAno")
        self.lblAno.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblAno)

        self.leAno = QLineEdit(VehiculosDialog)
        self.leAno.setObjectName(u"leAno")
        self.leAno.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.leAno)

        self.leITV = QLineEdit(VehiculosDialog)
        self.leITV.setObjectName(u"leITV")
        self.leITV.setFont(font1)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.leITV)

        self.lblITV = QLabel(VehiculosDialog)
        self.lblITV.setObjectName(u"lblITV")
        self.lblITV.setFont(font)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblITV)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(30)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(200, -1, -1, -1)
        self.btnCancelar = QPushButton(VehiculosDialog)
        self.btnCancelar.setObjectName(u"btnCancelar")
        self.btnCancelar.setMinimumSize(QSize(0, 30))
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(11)
        font2.setBold(True)
        self.btnCancelar.setFont(font2)

        self.horizontalLayout.addWidget(self.btnCancelar)

        self.btnGuardar = QPushButton(VehiculosDialog)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setMinimumSize(QSize(0, 30))
        self.btnGuardar.setFont(font2)

        self.horizontalLayout.addWidget(self.btnGuardar)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(VehiculosDialog)

        QMetaObject.connectSlotsByName(VehiculosDialog)
    # setupUi

    def retranslateUi(self, VehiculosDialog):
        VehiculosDialog.setWindowTitle(QCoreApplication.translate("VehiculosDialog", u"Dialog", None))
        self.lblMatricula.setText(QCoreApplication.translate("VehiculosDialog", u"Matr\u00edcula: ", None))
        self.lblMarca.setText(QCoreApplication.translate("VehiculosDialog", u"Marca: ", None))
        self.lblModelo.setText(QCoreApplication.translate("VehiculosDialog", u"Modelo: ", None))
        self.lblAno.setText(QCoreApplication.translate("VehiculosDialog", u"A\u00f1o: ", None))
        self.lblITV.setText(QCoreApplication.translate("VehiculosDialog", u"Pr\u00f3xima ITV: ", None))
        self.btnCancelar.setText(QCoreApplication.translate("VehiculosDialog", u"Cancelar", None))
        self.btnGuardar.setText(QCoreApplication.translate("VehiculosDialog", u"Guardar", None))
    # retranslateUi

