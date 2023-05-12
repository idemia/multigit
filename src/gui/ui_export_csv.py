# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_export_csv.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_dialogCsvExport(object):
    def setupUi(self, dialogCsvExport: QDialog) -> None:
        if not dialogCsvExport.objectName():
            dialogCsvExport.setObjectName(u"dialogCsvExport")
        dialogCsvExport.resize(438, 324)
        self.verticalLayout = QVBoxLayout(dialogCsvExport)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(dialogCsvExport)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.checkPath = QCheckBox(dialogCsvExport)
        self.checkPath.setObjectName(u"checkPath")
        self.checkPath.setChecked(True)

        self.gridLayout.addWidget(self.checkPath, 1, 0, 1, 1)

        self.checkCommitSha1 = QCheckBox(dialogCsvExport)
        self.checkCommitSha1.setObjectName(u"checkCommitSha1")

        self.gridLayout.addWidget(self.checkCommitSha1, 1, 1, 1, 1)

        self.checkHead = QCheckBox(dialogCsvExport)
        self.checkHead.setObjectName(u"checkHead")
        self.checkHead.setChecked(True)

        self.gridLayout.addWidget(self.checkHead, 2, 0, 1, 1)

        self.checkCommitDate = QCheckBox(dialogCsvExport)
        self.checkCommitDate.setObjectName(u"checkCommitDate")

        self.gridLayout.addWidget(self.checkCommitDate, 2, 1, 1, 1)

        self.checkCurrentBranch = QCheckBox(dialogCsvExport)
        self.checkCurrentBranch.setObjectName(u"checkCurrentBranch")
        self.checkCurrentBranch.setChecked(True)

        self.gridLayout.addWidget(self.checkCurrentBranch, 3, 0, 1, 1)

        self.checkUrl = QCheckBox(dialogCsvExport)
        self.checkUrl.setObjectName(u"checkUrl")
        self.checkUrl.setChecked(True)

        self.gridLayout.addWidget(self.checkUrl, 3, 1, 1, 1)

        self.checkCurrentTag = QCheckBox(dialogCsvExport)
        self.checkCurrentTag.setObjectName(u"checkCurrentTag")
        self.checkCurrentTag.setChecked(True)

        self.gridLayout.addWidget(self.checkCurrentTag, 4, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 34, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(dialogCsvExport)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.checkPath, self.checkHead)
        QWidget.setTabOrder(self.checkHead, self.checkCurrentBranch)
        QWidget.setTabOrder(self.checkCurrentBranch, self.checkCurrentTag)
        QWidget.setTabOrder(self.checkCurrentTag, self.checkCommitSha1)
        QWidget.setTabOrder(self.checkCommitSha1, self.checkCommitDate)
        QWidget.setTabOrder(self.checkCommitDate, self.checkUrl)

        self.retranslateUi(dialogCsvExport)
        self.buttonBox.accepted.connect(dialogCsvExport.accept)
        self.buttonBox.rejected.connect(dialogCsvExport.reject)

        QMetaObject.connectSlotsByName(dialogCsvExport)
    # setupUi

    def retranslateUi(self, dialogCsvExport: QDialog) -> None:
        dialogCsvExport.setWindowTitle(QCoreApplication.translate("dialogCsvExport", u"Export to CSV", None))
        self.label.setText(QCoreApplication.translate("dialogCsvExport", u"Choose which fields to export :\n"
"", None))
        self.checkPath.setText(QCoreApplication.translate("dialogCsvExport", u"Path", None))
        self.checkCommitSha1.setText(QCoreApplication.translate("dialogCsvExport", u"commit sha1", None))
        self.checkHead.setText(QCoreApplication.translate("dialogCsvExport", u"HEAD", None))
        self.checkCommitDate.setText(QCoreApplication.translate("dialogCsvExport", u"commit date", None))
        self.checkCurrentBranch.setText(QCoreApplication.translate("dialogCsvExport", u"current branch", None))
        self.checkUrl.setText(QCoreApplication.translate("dialogCsvExport", u"url", None))
        self.checkCurrentTag.setText(QCoreApplication.translate("dialogCsvExport", u"current tag", None))
    # retranslateUi

