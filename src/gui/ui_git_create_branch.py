# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_git_create_branch.ui'
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
    QComboBox, QDialog, QDialogButtonBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from src.mg_repo_tree import MgRepoTree

class Ui_GitCreateBranch(object):
    def setupUi(self, GitCreateBranch: QDialog) -> None:
        if not GitCreateBranch.objectName():
            GitCreateBranch.setObjectName(u"GitCreateBranch")
        GitCreateBranch.resize(883, 423)
        self.verticalLayout_2 = QVBoxLayout(GitCreateBranch)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(GitCreateBranch)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_2 = QSpacerItem(554, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.checkBoxSwitchBranch = QCheckBox(self.groupBox)
        self.checkBoxSwitchBranch.setObjectName(u"checkBoxSwitchBranch")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxSwitchBranch.sizePolicy().hasHeightForWidth())
        self.checkBoxSwitchBranch.setSizePolicy(sizePolicy)
        self.checkBoxSwitchBranch.setChecked(True)

        self.gridLayout.addWidget(self.checkBoxSwitchBranch, 1, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.comboBoxBranchName = QComboBox(self.groupBox)
        self.comboBoxBranchName.setObjectName(u"comboBoxBranchName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxBranchName.sizePolicy().hasHeightForWidth())
        self.comboBoxBranchName.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Consolas"])
        self.comboBoxBranchName.setFont(font)
        self.comboBoxBranchName.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxBranchName, 0, 1, 1, 2)

        self.horizontalSpacer_3 = QSpacerItem(554, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 3, 1, 1)

        self.checkBoxPushToRemote = QCheckBox(self.groupBox)
        self.checkBoxPushToRemote.setObjectName(u"checkBoxPushToRemote")
        sizePolicy.setHeightForWidth(self.checkBoxPushToRemote.sizePolicy().hasHeightForWidth())
        self.checkBoxPushToRemote.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.checkBoxPushToRemote, 2, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(GitCreateBranch)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelRepoSelected = QLabel(self.groupBox_2)
        self.labelRepoSelected.setObjectName(u"labelRepoSelected")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelRepoSelected.sizePolicy().hasHeightForWidth())
        self.labelRepoSelected.setSizePolicy(sizePolicy2)
        self.labelRepoSelected.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.labelRepoSelected)

        self.pushButtonAdjustRepoList = QPushButton(self.groupBox_2)
        self.pushButtonAdjustRepoList.setObjectName(u"pushButtonAdjustRepoList")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButtonAdjustRepoList.sizePolicy().hasHeightForWidth())
        self.pushButtonAdjustRepoList.setSizePolicy(sizePolicy3)

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
        self.buttonBox = QDialogButtonBox(GitCreateBranch)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        QWidget.setTabOrder(self.comboBoxBranchName, self.checkBoxSwitchBranch)
        QWidget.setTabOrder(self.checkBoxSwitchBranch, self.checkBoxPushToRemote)
        QWidget.setTabOrder(self.checkBoxPushToRemote, self.pushButtonAdjustRepoList)
        QWidget.setTabOrder(self.pushButtonAdjustRepoList, self.treeWidgetRepoList)

        self.retranslateUi(GitCreateBranch)
        self.buttonBox.accepted.connect(GitCreateBranch.accept)
        self.buttonBox.rejected.connect(GitCreateBranch.reject)

        QMetaObject.connectSlotsByName(GitCreateBranch)
    # setupUi

    def retranslateUi(self, GitCreateBranch: QDialog) -> None:
        GitCreateBranch.setWindowTitle(QCoreApplication.translate("GitCreateBranch", u"Git Create branch", None))
        self.groupBox.setTitle(QCoreApplication.translate("GitCreateBranch", u"Create Branch", None))
        self.checkBoxSwitchBranch.setText(QCoreApplication.translate("GitCreateBranch", u"Switch to branch after creation", None))
        self.label.setText(QCoreApplication.translate("GitCreateBranch", u"Enter branch name :", None))
        self.checkBoxPushToRemote.setText(QCoreApplication.translate("GitCreateBranch", u"Push branch to remote", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("GitCreateBranch", u"Targeted repositories", None))
        self.labelRepoSelected.setText(QCoreApplication.translate("GitCreateBranch", u"3 repositories selected", None))
        self.pushButtonAdjustRepoList.setText(QCoreApplication.translate("GitCreateBranch", u"Adjust Repository list", None))
        ___qtreewidgetitem = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("GitCreateBranch", u"Last Remote Syncho", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("GitCreateBranch", u"Status", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("GitCreateBranch", u"Head", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("GitCreateBranch", u"Git Repo Path", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GitCreateBranch", u"hidden", None));
    # retranslateUi

