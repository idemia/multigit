# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_git_tag.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from src.mg_repo_tree import MgRepoTree


class Ui_GitAddTag(object):
    def setupUi(self, GitAddTag: QDialog) -> None:
        if not GitAddTag.objectName():
            GitAddTag.setObjectName(u"GitAddTag")
        GitAddTag.resize(883, 617)
        self.verticalLayout_2 = QVBoxLayout(GitAddTag)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(GitAddTag)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textAnnotated = QTextEdit(self.widget)
        self.textAnnotated.setObjectName(u"textAnnotated")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.textAnnotated.sizePolicy().hasHeightForWidth())
        self.textAnnotated.setSizePolicy(sizePolicy1)
        self.textAnnotated.setTabChangesFocus(True)
        self.textAnnotated.setAcceptRichText(False)

        self.gridLayout.addWidget(self.textAnnotated, 1, 1, 1, 1)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(3)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.widget_2, 0, 2, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.checkBoxSwitchToTag = QCheckBox(self.widget)
        self.checkBoxSwitchToTag.setObjectName(u"checkBoxSwitchToTag")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(3)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.checkBoxSwitchToTag.sizePolicy().hasHeightForWidth())
        self.checkBoxSwitchToTag.setSizePolicy(sizePolicy3)
        self.checkBoxSwitchToTag.setChecked(False)

        self.gridLayout.addWidget(self.checkBoxSwitchToTag, 3, 1, 1, 1)

        self.comboBoxTagName = QComboBox(self.widget)
        self.comboBoxTagName.setObjectName(u"comboBoxTagName")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(6)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBoxTagName.sizePolicy().hasHeightForWidth())
        self.comboBoxTagName.setSizePolicy(sizePolicy4)
        font1 = QFont()
        font1.setFamily(u"Consolas")
        font1.setPointSize(8)
        self.comboBoxTagName.setFont(font1)
        self.comboBoxTagName.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxTagName, 0, 1, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(2)
        sizePolicy5.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy5)

        self.gridLayout.addWidget(self.widget_3, 5, 1, 1, 1)

        self.checkBoxPushToRemote = QCheckBox(self.widget)
        self.checkBoxPushToRemote.setObjectName(u"checkBoxPushToRemote")
        sizePolicy3.setHeightForWidth(self.checkBoxPushToRemote.sizePolicy().hasHeightForWidth())
        self.checkBoxPushToRemote.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.checkBoxPushToRemote, 2, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.widget)

        self.groupBox_2 = QGroupBox(GitAddTag)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(10)
        sizePolicy6.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy6)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelRepoSelected = QLabel(self.groupBox_2)
        self.labelRepoSelected.setObjectName(u"labelRepoSelected")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.labelRepoSelected.sizePolicy().hasHeightForWidth())
        self.labelRepoSelected.setSizePolicy(sizePolicy7)
        self.labelRepoSelected.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.labelRepoSelected)

        self.pushButtonAdjustRepoList = QPushButton(self.groupBox_2)
        self.pushButtonAdjustRepoList.setObjectName(u"pushButtonAdjustRepoList")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(1)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.pushButtonAdjustRepoList.sizePolicy().hasHeightForWidth())
        self.pushButtonAdjustRepoList.setSizePolicy(sizePolicy8)

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
        self.buttonBox = QDialogButtonBox(GitAddTag)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.comboBoxTagName)
        self.label_2.setBuddy(self.textAnnotated)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.comboBoxTagName, self.textAnnotated)
        QWidget.setTabOrder(self.textAnnotated, self.checkBoxPushToRemote)
        QWidget.setTabOrder(self.checkBoxPushToRemote, self.checkBoxSwitchToTag)
        QWidget.setTabOrder(self.checkBoxSwitchToTag, self.pushButtonAdjustRepoList)
        QWidget.setTabOrder(self.pushButtonAdjustRepoList, self.treeWidgetRepoList)

        self.retranslateUi(GitAddTag)
        self.buttonBox.accepted.connect(GitAddTag.accept)
        self.buttonBox.rejected.connect(GitAddTag.reject)

        QMetaObject.connectSlotsByName(GitAddTag)
    # setupUi

    def retranslateUi(self, GitAddTag: QDialog) -> None:
        GitAddTag.setWindowTitle(QCoreApplication.translate("GitAddTag", u"Git Add tag", None))
#if QT_CONFIG(tooltip)
        self.textAnnotated.setToolTip(QCoreApplication.translate("GitAddTag", u"Add text to create an annotated tag", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("GitAddTag", u"Create tag :", None))
        self.checkBoxSwitchToTag.setText(QCoreApplication.translate("GitAddTag", u"Switch to tag after creation", None))
        self.label_2.setText(QCoreApplication.translate("GitAddTag", u"Annotation :", None))
        self.checkBoxPushToRemote.setText(QCoreApplication.translate("GitAddTag", u"Push tag  to remote", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("GitAddTag", u"Targeted repositories", None))
        self.labelRepoSelected.setText(QCoreApplication.translate("GitAddTag", u"3 repositories selected", None))
        self.pushButtonAdjustRepoList.setText(QCoreApplication.translate("GitAddTag", u"Adjust Repository list", None))
        ___qtreewidgetitem = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("GitAddTag", u"Last Remote Syncho", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("GitAddTag", u"Status", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("GitAddTag", u"Head", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("GitAddTag", u"Git Repo Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GitAddTag", u"hidden", None));
    # retranslateUi

