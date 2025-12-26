# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(600, 500)
        Login.setMaximumSize(QSize(600, 500))
        self.lblLogin = QLabel(Login)
        self.lblLogin.setObjectName(u"lblLogin")
        self.lblLogin.setGeometry(QRect(190, 90, 201, 71))
        font = QFont()
        font.setFamilies([u"Montserrat"])
        font.setPointSize(16)
        font.setBold(True)
        self.lblLogin.setFont(font)
        self.lblLogin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblMessage = QLabel(Login)
        self.lblMessage.setObjectName(u"lblMessage")
        self.lblMessage.setGeometry(QRect(100, 400, 391, 71))
        font1 = QFont()
        font1.setFamilies([u"Montserrat"])
        font1.setPointSize(13)
        font1.setBold(True)
        self.lblMessage.setFont(font1)
        self.lblMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btnLogin = QPushButton(Login)
        self.btnLogin.setObjectName(u"btnLogin")
        self.btnLogin.setGeometry(QRect(230, 300, 121, 41))
        font2 = QFont()
        font2.setFamilies([u"Montserrat"])
        font2.setPointSize(15)
        font2.setBold(True)
        self.btnLogin.setFont(font2)
        self.layoutWidget = QWidget(Login)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(110, 180, 391, 89))
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.lblEmail = QLabel(self.layoutWidget)
        self.lblEmail.setObjectName(u"lblEmail")
        self.lblEmail.setFont(font)
        self.lblEmail.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblEmail)

        self.leEmail = QLineEdit(self.layoutWidget)
        self.leEmail.setObjectName(u"leEmail")
        font3 = QFont()
        font3.setFamilies([u"Montserrat"])
        font3.setPointSize(12)
        font3.setBold(True)
        self.leEmail.setFont(font3)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leEmail)

        self.lblPass = QLabel(self.layoutWidget)
        self.lblPass.setObjectName(u"lblPass")
        self.lblPass.setFont(font)
        self.lblPass.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblPass)

        self.lePass = QLineEdit(self.layoutWidget)
        self.lePass.setObjectName(u"lePass")
        self.lePass.setFont(font3)
        self.lePass.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lePass)


        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Form", None))
        self.lblLogin.setText(QCoreApplication.translate("Login", u"Inicia Sesi\u00f3n", None))
        self.lblMessage.setText("")
        self.btnLogin.setText(QCoreApplication.translate("Login", u"Ingresar", None))
        self.lblEmail.setText(QCoreApplication.translate("Login", u"Email: ", None))
        self.leEmail.setPlaceholderText(QCoreApplication.translate("Login", u"Email", None))
        self.lblPass.setText(QCoreApplication.translate("Login", u"Contrase\u00f1a: ", None))
        self.lePass.setPlaceholderText(QCoreApplication.translate("Login", u"Contrase\u00f1a", None))
    # retranslateUi

