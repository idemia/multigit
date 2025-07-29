# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_git_commit.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QCheckBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QTreeWidgetItem, QVBoxLayout,
    QWidget)

from src.mg_button_history import MgButtonHistory
from src.mg_repo_tree import MgRepoTree

class Ui_GitCommit(object):
    def setupUi(self, GitCommit: QDialog) -> None:
        if not GitCommit.objectName():
            GitCommit.setObjectName(u"GitCommit")
        GitCommit.resize(863, 423)
        self.verticalLayout_2 = QVBoxLayout(GitCommit)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(GitCommit)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textEditCommitMessage = QTextEdit(self.groupBox)
        self.textEditCommitMessage.setObjectName(u"textEditCommitMessage")

        self.gridLayout.addWidget(self.textEditCommitMessage, 0, 0, 1, 1)

        self.buttonHistoryCommit = MgButtonHistory(self.groupBox)
        self.buttonHistoryCommit.setObjectName(u"buttonHistoryCommit")

        self.gridLayout.addWidget(self.buttonHistoryCommit, 0, 1, 1, 1)

        self.checkBoxPushToRemote = QCheckBox(self.groupBox)
        self.checkBoxPushToRemote.setObjectName(u"checkBoxPushToRemote")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxPushToRemote.sizePolicy().hasHeightForWidth())
        self.checkBoxPushToRemote.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.checkBoxPushToRemote, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(GitCommit)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelRepoSelected = QLabel(self.groupBox_2)
        self.labelRepoSelected.setObjectName(u"labelRepoSelected")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelRepoSelected.sizePolicy().hasHeightForWidth())
        self.labelRepoSelected.setSizePolicy(sizePolicy1)
        self.labelRepoSelected.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.labelRepoSelected)

        self.pushButtonAdjustRepoList = QPushButton(self.groupBox_2)
        self.pushButtonAdjustRepoList.setObjectName(u"pushButtonAdjustRepoList")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonAdjustRepoList.sizePolicy().hasHeightForWidth())
        self.pushButtonAdjustRepoList.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.pushButtonAdjustRepoList)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeWidgetRepoList = MgRepoTree(self.groupBox_2)
        self.treeWidgetRepoList.setObjectName(u"treeWidgetRepoList")
        self.treeWidgetRepoList.setAlternatingRowColors(True)
        self.treeWidgetRepoList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.treeWidgetRepoList.setRootIsDecorated(False)
        self.treeWidgetRepoList.setUniformRowHeights(True)
        self.treeWidgetRepoList.setItemsExpandable(False)
        self.treeWidgetRepoList.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.treeWidgetRepoList)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.buttonBox = QDialogButtonBox(GitCommit)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        QWidget.setTabOrder(self.textEditCommitMessage, self.buttonHistoryCommit)
        QWidget.setTabOrder(self.buttonHistoryCommit, self.checkBoxPushToRemote)
        QWidget.setTabOrder(self.checkBoxPushToRemote, self.pushButtonAdjustRepoList)
        QWidget.setTabOrder(self.pushButtonAdjustRepoList, self.treeWidgetRepoList)

        self.retranslateUi(GitCommit)
        self.buttonBox.accepted.connect(GitCommit.accept)
        self.buttonBox.rejected.connect(GitCommit.reject)

        QMetaObject.connectSlotsByName(GitCommit)
    # setupUi

    def retranslateUi(self, GitCommit: QDialog) -> None:
        GitCommit.setWindowTitle(QCoreApplication.translate("GitCommit", u"Git Commit", None))
        self.groupBox.setTitle(QCoreApplication.translate("GitCommit", u"Message", None))
        self.buttonHistoryCommit.setText("")
        self.checkBoxPushToRemote.setText(QCoreApplication.translate("GitCommit", u"Push to remote", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("GitCommit", u"Targeted repositories", None))
        self.labelRepoSelected.setText(QCoreApplication.translate("GitCommit", u"3 repositories selected", None))
        self.pushButtonAdjustRepoList.setText(QCoreApplication.translate("GitCommit", u"Adjust Repository list", None))
        ___qtreewidgetitem = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("GitCommit", u"Last Remote Syncho", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("GitCommit", u"Status", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("GitCommit", u"Head", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("GitCommit", u"Git Repo Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GitCommit", u"hidden", None));
    # retranslateUi

