# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_git_switch_branch.ui'
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
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from src.mg_repo_tree import MgRepoTree

class Ui_GitSwitchBranch(object):
    def setupUi(self, GitSwitchBranch: QDialog) -> None:
        if not GitSwitchBranch.objectName():
            GitSwitchBranch.setObjectName(u"GitSwitchBranch")
        GitSwitchBranch.resize(883, 723)
        self.verticalLayout_2 = QVBoxLayout(GitSwitchBranch)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelBranchOrTag = QLabel(GitSwitchBranch)
        self.labelBranchOrTag.setObjectName(u"labelBranchOrTag")

        self.gridLayout.addWidget(self.labelBranchOrTag, 0, 1, 1, 1)

        self.lineEditBranchTagName = QLineEdit(GitSwitchBranch)
        self.lineEditBranchTagName.setObjectName(u"lineEditBranchTagName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditBranchTagName.sizePolicy().hasHeightForWidth())
        self.lineEditBranchTagName.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        self.lineEditBranchTagName.setFont(font)

        self.gridLayout.addWidget(self.lineEditBranchTagName, 0, 2, 1, 1)

        self.widget_2 = QWidget(GitSwitchBranch)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.widget_2, 0, 3, 1, 1)

        self.checkBoxDefaultForNotExist = QCheckBox(GitSwitchBranch)
        self.checkBoxDefaultForNotExist.setObjectName(u"checkBoxDefaultForNotExist")

        self.gridLayout.addWidget(self.checkBoxDefaultForNotExist, 1, 2, 1, 1)

        self.checkBoxDeleteLocalBranch = QCheckBox(GitSwitchBranch)
        self.checkBoxDeleteLocalBranch.setObjectName(u"checkBoxDeleteLocalBranch")
        self.checkBoxDeleteLocalBranch.setChecked(True)

        self.gridLayout.addWidget(self.checkBoxDeleteLocalBranch, 2, 2, 1, 1)

        self.checkBoxDeleteRemoteBranch = QCheckBox(GitSwitchBranch)
        self.checkBoxDeleteRemoteBranch.setObjectName(u"checkBoxDeleteRemoteBranch")
        self.checkBoxDeleteRemoteBranch.setChecked(True)

        self.gridLayout.addWidget(self.checkBoxDeleteRemoteBranch, 3, 2, 1, 1)

        self.widget_4 = QWidget(GitSwitchBranch)
        self.widget_4.setObjectName(u"widget_4")

        self.gridLayout.addWidget(self.widget_4, 4, 0, 1, 3)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.groupBoxBranchOrTagSelection = QGroupBox(GitSwitchBranch)
        self.groupBoxBranchOrTagSelection.setObjectName(u"groupBoxBranchOrTagSelection")
        self.groupBoxBranchOrTagSelection.setFont(font)
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxBranchOrTagSelection)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.groupBoxBranchOrTagSelection)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setPointSize(9)
        self.label_3.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.label = QLabel(self.groupBoxBranchOrTagSelection)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.lineEditBranchFilter = QLineEdit(self.groupBoxBranchOrTagSelection)
        self.lineEditBranchFilter.setObjectName(u"lineEditBranchFilter")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(9)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEditBranchFilter.sizePolicy().hasHeightForWidth())
        self.lineEditBranchFilter.setSizePolicy(sizePolicy2)
        self.lineEditBranchFilter.setFont(font1)

        self.horizontalLayout_2.addWidget(self.lineEditBranchFilter)

        self.widget = QWidget(self.groupBoxBranchOrTagSelection)
        self.widget.setObjectName(u"widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(3)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.widget)

        self.pushButtonGrouping = QPushButton(self.groupBoxBranchOrTagSelection)
        self.pushButtonGrouping.setObjectName(u"pushButtonGrouping")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButtonGrouping.sizePolicy().hasHeightForWidth())
        self.pushButtonGrouping.setSizePolicy(sizePolicy4)
        self.pushButtonGrouping.setFont(font1)

        self.horizontalLayout_2.addWidget(self.pushButtonGrouping)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.treeWidgetBranches = QTreeWidget(self.groupBoxBranchOrTagSelection)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignLeading|Qt.AlignVCenter);
        self.treeWidgetBranches.setHeaderItem(__qtreewidgetitem)
        QTreeWidgetItem(self.treeWidgetBranches)
        QTreeWidgetItem(self.treeWidgetBranches)
        QTreeWidgetItem(self.treeWidgetBranches)
        self.treeWidgetBranches.setObjectName(u"treeWidgetBranches")
        self.treeWidgetBranches.setFont(font1)
        self.treeWidgetBranches.setFrameShape(QFrame.Shape.NoFrame)
        self.treeWidgetBranches.setProperty(u"showDropIndicator", False)
        self.treeWidgetBranches.setAlternatingRowColors(False)
        self.treeWidgetBranches.setSortingEnabled(True)
        self.treeWidgetBranches.header().setVisible(True)

        self.verticalLayout_3.addWidget(self.treeWidgetBranches)


        self.verticalLayout_2.addWidget(self.groupBoxBranchOrTagSelection)

        self.widget_5 = QWidget(GitSwitchBranch)
        self.widget_5.setObjectName(u"widget_5")

        self.verticalLayout_2.addWidget(self.widget_5)

        self.widget_3 = QWidget(GitSwitchBranch)
        self.widget_3.setObjectName(u"widget_3")

        self.verticalLayout_2.addWidget(self.widget_3)

        self.groupBox_2 = QGroupBox(GitSwitchBranch)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(23)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelRepoSelected = QLabel(self.groupBox_2)
        self.labelRepoSelected.setObjectName(u"labelRepoSelected")
        sizePolicy1.setHeightForWidth(self.labelRepoSelected.sizePolicy().hasHeightForWidth())
        self.labelRepoSelected.setSizePolicy(sizePolicy1)
        self.labelRepoSelected.setFont(font1)
        self.labelRepoSelected.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.labelRepoSelected)

        self.pushButtonAdjustRepoList = QPushButton(self.groupBox_2)
        self.pushButtonAdjustRepoList.setObjectName(u"pushButtonAdjustRepoList")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.pushButtonAdjustRepoList.sizePolicy().hasHeightForWidth())
        self.pushButtonAdjustRepoList.setSizePolicy(sizePolicy5)
        self.pushButtonAdjustRepoList.setFont(font1)

        self.horizontalLayout.addWidget(self.pushButtonAdjustRepoList)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.treeWidgetRepoList = MgRepoTree(self.groupBox_2)
        self.treeWidgetRepoList.setObjectName(u"treeWidgetRepoList")
        self.treeWidgetRepoList.setFont(font1)
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
        self.buttonBox = QDialogButtonBox(GitSwitchBranch)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFont(font1)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        QWidget.setTabOrder(self.lineEditBranchTagName, self.checkBoxDefaultForNotExist)
        QWidget.setTabOrder(self.checkBoxDefaultForNotExist, self.checkBoxDeleteLocalBranch)
        QWidget.setTabOrder(self.checkBoxDeleteLocalBranch, self.checkBoxDeleteRemoteBranch)
        QWidget.setTabOrder(self.checkBoxDeleteRemoteBranch, self.lineEditBranchFilter)
        QWidget.setTabOrder(self.lineEditBranchFilter, self.pushButtonGrouping)
        QWidget.setTabOrder(self.pushButtonGrouping, self.treeWidgetBranches)
        QWidget.setTabOrder(self.treeWidgetBranches, self.pushButtonAdjustRepoList)
        QWidget.setTabOrder(self.pushButtonAdjustRepoList, self.treeWidgetRepoList)

        self.retranslateUi(GitSwitchBranch)
        self.buttonBox.accepted.connect(GitSwitchBranch.accept)
        self.buttonBox.rejected.connect(GitSwitchBranch.reject)

        QMetaObject.connectSlotsByName(GitSwitchBranch)
    # setupUi

    def retranslateUi(self, GitSwitchBranch: QDialog) -> None:
        GitSwitchBranch.setWindowTitle(QCoreApplication.translate("GitSwitchBranch", u"Git Switch branch", None))
        self.labelBranchOrTag.setText(QCoreApplication.translate("GitSwitchBranch", u"Choose branch", None))
        self.checkBoxDefaultForNotExist.setText(QCoreApplication.translate("GitSwitchBranch", u"If selected branch does not exist, switch to branch int", None))
        self.checkBoxDeleteLocalBranch.setText(QCoreApplication.translate("GitSwitchBranch", u"Delete local branch", None))
        self.checkBoxDeleteRemoteBranch.setText(QCoreApplication.translate("GitSwitchBranch", u"Delete remote branch", None))
        self.groupBoxBranchOrTagSelection.setTitle(QCoreApplication.translate("GitSwitchBranch", u"Branch selection", None))
        self.label_3.setText(QCoreApplication.translate("GitSwitchBranch", u"Display filter :", None))
        self.label.setText("")
        self.pushButtonGrouping.setText(QCoreApplication.translate("GitSwitchBranch", u"    Group          ", None))
        ___qtreewidgetitem = self.treeWidgetBranches.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("GitSwitchBranch", u"Type of branch", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("GitSwitchBranch", u"Present in repositories", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("GitSwitchBranch", u"Possible names", None));

        __sortingEnabled = self.treeWidgetBranches.isSortingEnabled()
        self.treeWidgetBranches.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidgetBranches.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("GitSwitchBranch", u"sdfk", None));
        ___qtreewidgetitem2 = self.treeWidgetBranches.topLevelItem(1)
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("GitSwitchBranch", u"(in all 15)", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("GitSwitchBranch", u"master", None));
        ___qtreewidgetitem3 = self.treeWidgetBranches.topLevelItem(2)
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("GitSwitchBranch", u"(in 13)", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("GitSwitchBranch", u"feat/toto", None));
        self.treeWidgetBranches.setSortingEnabled(__sortingEnabled)

        self.groupBox_2.setTitle(QCoreApplication.translate("GitSwitchBranch", u"Targeted repositories", None))
        self.labelRepoSelected.setText(QCoreApplication.translate("GitSwitchBranch", u"3 repositories selected", None))
        self.pushButtonAdjustRepoList.setText(QCoreApplication.translate("GitSwitchBranch", u"Adjust Repository list", None))
        ___qtreewidgetitem4 = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem4.setText(4, QCoreApplication.translate("GitSwitchBranch", u"Last Remote Syncho", None));
        ___qtreewidgetitem4.setText(3, QCoreApplication.translate("GitSwitchBranch", u"Status", None));
        ___qtreewidgetitem4.setText(2, QCoreApplication.translate("GitSwitchBranch", u"Head", None));
        ___qtreewidgetitem4.setText(1, QCoreApplication.translate("GitSwitchBranch", u"Git Repo Path", None));
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("GitSwitchBranch", u"hidden", None));
    # retranslateUi

