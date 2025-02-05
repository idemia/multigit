# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_git_push_tag.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from src.mg_repo_tree import MgRepoTree


class Ui_GitPushTag(object):
    def setupUi(self, GitPushTag: QDialog) -> None:
        if not GitPushTag.objectName():
            GitPushTag.setObjectName(u"GitPushTag")
        GitPushTag.resize(965, 492)
        self.verticalLayout_2 = QVBoxLayout(GitPushTag)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(GitPushTag)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.comboBoxTagName = QComboBox(self.groupBox)
        self.comboBoxTagName.setObjectName(u"comboBoxTagName")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxTagName.sizePolicy().hasHeightForWidth())
        self.comboBoxTagName.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(8)
        self.comboBoxTagName.setFont(font1)
        self.comboBoxTagName.setEditable(True)

        self.horizontalLayout_2.addWidget(self.comboBoxTagName)

        self.widget_2 = QWidget(self.groupBox)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.widget_2)

        self.widget_4 = QWidget(self.groupBox)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(5)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.widget_4)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.widget_3 = QWidget(GitPushTag)
        self.widget_3.setObjectName(u"widget_3")

        self.verticalLayout_2.addWidget(self.widget_3)

        self.groupBox_2 = QGroupBox(GitPushTag)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelRepoSelected = QLabel(self.groupBox_2)
        self.labelRepoSelected.setObjectName(u"labelRepoSelected")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.labelRepoSelected.sizePolicy().hasHeightForWidth())
        self.labelRepoSelected.setSizePolicy(sizePolicy3)
        self.labelRepoSelected.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.labelRepoSelected)

        self.pushButtonAdjustRepoList = QPushButton(self.groupBox_2)
        self.pushButtonAdjustRepoList.setObjectName(u"pushButtonAdjustRepoList")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButtonAdjustRepoList.sizePolicy().hasHeightForWidth())
        self.pushButtonAdjustRepoList.setSizePolicy(sizePolicy4)

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


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.buttonBox = QDialogButtonBox(GitPushTag)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.comboBoxTagName)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.comboBoxTagName, self.pushButtonAdjustRepoList)
        QWidget.setTabOrder(self.pushButtonAdjustRepoList, self.treeWidgetRepoList)

        self.retranslateUi(GitPushTag)
        self.buttonBox.accepted.connect(GitPushTag.accept)
        self.buttonBox.rejected.connect(GitPushTag.reject)

        QMetaObject.connectSlotsByName(GitPushTag)
    # setupUi

    def retranslateUi(self, GitPushTag: QDialog) -> None:
        GitPushTag.setWindowTitle(QCoreApplication.translate("GitPushTag", u"Git push tag", None))
        self.groupBox.setTitle(QCoreApplication.translate("GitPushTag", u"Git push tag", None))
        self.label.setText(QCoreApplication.translate("GitPushTag", u"Choose tag to push :", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("GitPushTag", u"Targeted repositories", None))
        self.labelRepoSelected.setText(QCoreApplication.translate("GitPushTag", u"3 repositories selected", None))
        self.pushButtonAdjustRepoList.setText(QCoreApplication.translate("GitPushTag", u"Adjust Repository list", None))
        ___qtreewidgetitem = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("GitPushTag", u"Last Remote Syncho", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("GitPushTag", u"Status", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("GitPushTag", u"Head", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("GitPushTag", u"Git Repo Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GitPushTag", u"hidden", None));
    # retranslateUi

