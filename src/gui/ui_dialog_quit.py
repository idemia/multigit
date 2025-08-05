# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_dialog_quit.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_quitConfirmDialog(object):
    def setupUi(self, quitConfirmDialog: QDialog) -> None:
        if not quitConfirmDialog.objectName():
            quitConfirmDialog.setObjectName(u"quitConfirmDialog")
        quitConfirmDialog.resize(347, 162)
        quitConfirmDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(quitConfirmDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.label = QLabel(quitConfirmDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.checkBoxConfirmQuit = QCheckBox(quitConfirmDialog)
        self.checkBoxConfirmQuit.setObjectName(u"checkBoxConfirmQuit")
        self.checkBoxConfirmQuit.setChecked(True)

        self.verticalLayout.addWidget(self.checkBoxConfirmQuit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(quitConfirmDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Yes)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(quitConfirmDialog)
        self.buttonBox.accepted.connect(quitConfirmDialog.accept)
        self.buttonBox.rejected.connect(quitConfirmDialog.reject)

        QMetaObject.connectSlotsByName(quitConfirmDialog)
    # setupUi

    def retranslateUi(self, quitConfirmDialog: QDialog) -> None:
        quitConfirmDialog.setWindowTitle(QCoreApplication.translate("quitConfirmDialog", u"Quitting confirmation", None))
        self.label.setText(QCoreApplication.translate("quitConfirmDialog", u"Do you want to quit ?", None))
        self.checkBoxConfirmQuit.setText(QCoreApplication.translate("quitConfirmDialog", u"Always confirm before quitting", None))
    # retranslateUi

