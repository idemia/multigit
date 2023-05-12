# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_git_run_command.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from src.mg_repo_tree import MgRepoTree
from src.mg_button_history import MgButtonHistory

# import multigit_resources_rc

class Ui_GitRunCommand(object):
    def setupUi(self, GitRunCommand: QDialog) -> None:
        if not GitRunCommand.objectName():
            GitRunCommand.setObjectName(u"GitRunCommand")
        GitRunCommand.resize(869, 384)
        self.verticalLayout_2 = QVBoxLayout(GitRunCommand)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEditGitText = QLineEdit(GitRunCommand)
        self.lineEditGitText.setObjectName(u"lineEditGitText")
        self.lineEditGitText.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditGitText.sizePolicy().hasHeightForWidth())
        self.lineEditGitText.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Consolas")
        self.lineEditGitText.setFont(font)
        self.lineEditGitText.setAlignment(Qt.AlignCenter)
        self.lineEditGitText.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditGitText, 0, 1, 1, 1)

        self.lineEditGitCmd = QLineEdit(GitRunCommand)
        self.lineEditGitCmd.setObjectName(u"lineEditGitCmd")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(11)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEditGitCmd.sizePolicy().hasHeightForWidth())
        self.lineEditGitCmd.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.lineEditGitCmd, 0, 2, 1, 1)

        self.label = QLabel(GitRunCommand)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.historyButton = MgButtonHistory(GitRunCommand)
        self.historyButton.setObjectName(u"historyButton")
        icon = QIcon()
        icon.addFile(u":/img/icons8-history-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.historyButton.setIcon(icon)

        self.gridLayout.addWidget(self.historyButton, 0, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.widget = QWidget(GitRunCommand)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 30))

        self.verticalLayout_2.addWidget(self.widget)

        self.groupBox_2 = QGroupBox(GitRunCommand)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelRepoSelected = QLabel(self.groupBox_2)
        self.labelRepoSelected.setObjectName(u"labelRepoSelected")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelRepoSelected.sizePolicy().hasHeightForWidth())
        self.labelRepoSelected.setSizePolicy(sizePolicy2)
        self.labelRepoSelected.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.labelRepoSelected)

        self.pushButtonAdjustRepoList = QPushButton(self.groupBox_2)
        self.pushButtonAdjustRepoList.setObjectName(u"pushButtonAdjustRepoList")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButtonAdjustRepoList.sizePolicy().hasHeightForWidth())
        self.pushButtonAdjustRepoList.setSizePolicy(sizePolicy3)

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

        self.label_3 = QLabel(GitRunCommand)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.buttonBox = QDialogButtonBox(GitRunCommand)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lineEditGitText, self.lineEditGitCmd)
        QWidget.setTabOrder(self.lineEditGitCmd, self.historyButton)
        QWidget.setTabOrder(self.historyButton, self.pushButtonAdjustRepoList)
        QWidget.setTabOrder(self.pushButtonAdjustRepoList, self.treeWidgetRepoList)

        self.retranslateUi(GitRunCommand)
        self.buttonBox.accepted.connect(GitRunCommand.accept)
        self.buttonBox.rejected.connect(GitRunCommand.reject)

        QMetaObject.connectSlotsByName(GitRunCommand)
    # setupUi

    def retranslateUi(self, GitRunCommand: QDialog) -> None:
        GitRunCommand.setWindowTitle(QCoreApplication.translate("GitRunCommand", u"Run git command", None))
        self.lineEditGitText.setText(QCoreApplication.translate("GitRunCommand", u"git", None))
        self.label.setText(QCoreApplication.translate("GitRunCommand", u"Git command to run :", None))
#if QT_CONFIG(tooltip)
        self.historyButton.setToolTip(QCoreApplication.translate("GitRunCommand", u"Choose recent multigit file", None))
#endif // QT_CONFIG(tooltip)
        self.historyButton.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("GitRunCommand", u"Targeted repositories", None))
        self.labelRepoSelected.setText(QCoreApplication.translate("GitRunCommand", u"3 repositories selected", None))
        self.pushButtonAdjustRepoList.setText(QCoreApplication.translate("GitRunCommand", u"Adjust Repository list", None))
        ___qtreewidgetitem = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("GitRunCommand", u"Last Remote Syncho", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("GitRunCommand", u"Status", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("GitRunCommand", u"Head", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("GitRunCommand", u"Git Repo Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GitRunCommand", u"hidden", None));
        self.label_3.setText("")
    # retranslateUi

