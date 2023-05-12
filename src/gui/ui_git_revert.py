# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_git_revert.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from src.mg_repo_tree import MgRepoTree


class Ui_GitRevert(object):
    def setupUi(self, GitRevert: QDialog) -> None:
        if not GitRevert.objectName():
            GitRevert.setObjectName(u"GitRevert")
        GitRevert.resize(768, 561)
        self.verticalLayout_3 = QVBoxLayout(GitRevert)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(GitRevert)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.textEditRevertContent = QTextEdit(self.groupBox)
        self.textEditRevertContent.setObjectName(u"textEditRevertContent")

        self.verticalLayout_2.addWidget(self.textEditRevertContent)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.widget = QWidget(GitRevert)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 30))

        self.verticalLayout_3.addWidget(self.widget)

        self.groupBox_2 = QGroupBox(GitRevert)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelRepoSelected = QLabel(self.groupBox_2)
        self.labelRepoSelected.setObjectName(u"labelRepoSelected")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRepoSelected.sizePolicy().hasHeightForWidth())
        self.labelRepoSelected.setSizePolicy(sizePolicy)
        self.labelRepoSelected.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.labelRepoSelected)

        self.pushButtonAdjustRepoList = QPushButton(self.groupBox_2)
        self.pushButtonAdjustRepoList.setObjectName(u"pushButtonAdjustRepoList")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonAdjustRepoList.sizePolicy().hasHeightForWidth())
        self.pushButtonAdjustRepoList.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.pushButtonAdjustRepoList)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeWidgetRepoList = MgRepoTree(self.groupBox_2)
        self.treeWidgetRepoList.setObjectName(u"treeWidgetRepoList")
        self.treeWidgetRepoList.setAlternatingRowColors(True)
        self.treeWidgetRepoList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidgetRepoList.setRootIsDecorated(False)
        self.treeWidgetRepoList.setUniformRowHeights(True)
        self.treeWidgetRepoList.setItemsExpandable(False)
        self.treeWidgetRepoList.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.treeWidgetRepoList)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.buttonBox = QDialogButtonBox(GitRevert)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Yes)

        self.horizontalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        QWidget.setTabOrder(self.textEditRevertContent, self.pushButtonAdjustRepoList)
        QWidget.setTabOrder(self.pushButtonAdjustRepoList, self.treeWidgetRepoList)

        self.retranslateUi(GitRevert)
        self.buttonBox.accepted.connect(GitRevert.accept)
        self.buttonBox.rejected.connect(GitRevert.reject)

        QMetaObject.connectSlotsByName(GitRevert)
    # setupUi

    def retranslateUi(self, GitRevert: QDialog) -> None:
        GitRevert.setWindowTitle(QCoreApplication.translate("GitRevert", u"Git Create branch", None))
        self.groupBox.setTitle(QCoreApplication.translate("GitRevert", u"Git Revert", None))
        self.label.setText(QCoreApplication.translate("GitRevert", u"Revert the following changes :", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("GitRevert", u"Targeted repositories", None))
        self.labelRepoSelected.setText(QCoreApplication.translate("GitRevert", u"3 repositories selected", None))
        self.pushButtonAdjustRepoList.setText(QCoreApplication.translate("GitRevert", u"Adjust Repository list", None))
        ___qtreewidgetitem = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("GitRevert", u"Last Remote Syncho", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("GitRevert", u"Status", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("GitRevert", u"Head", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("GitRevert", u"Git Repo Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GitRevert", u"hidden", None));
    # retranslateUi

