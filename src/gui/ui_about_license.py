# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_about_license.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_FullLicenseInfoDialog(object):
    def setupUi(self, FullLicenseInfoDialog: QDialog) -> None:
        if not FullLicenseInfoDialog.objectName():
            FullLicenseInfoDialog.setObjectName(u"FullLicenseInfoDialog")
        FullLicenseInfoDialog.resize(765, 586)
        self.verticalLayout = QVBoxLayout(FullLicenseInfoDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser = QTextBrowser(FullLicenseInfoDialog)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.buttonBox = QDialogButtonBox(FullLicenseInfoDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(FullLicenseInfoDialog)
        self.buttonBox.accepted.connect(FullLicenseInfoDialog.accept)
        self.buttonBox.rejected.connect(FullLicenseInfoDialog.reject)

        QMetaObject.connectSlotsByName(FullLicenseInfoDialog)
    # setupUi

    def retranslateUi(self, FullLicenseInfoDialog: QDialog) -> None:
        FullLicenseInfoDialog.setWindowTitle(QCoreApplication.translate("FullLicenseInfoDialog", u"Full Licensing Information", None))
    # retranslateUi

