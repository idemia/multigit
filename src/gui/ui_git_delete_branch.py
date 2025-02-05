# -*- coding: utf-8 -*-

#    Copyright (c) 2019-2023 IDEMIA
#    Author: IDEMIA (Philippe Fremy, Florent Oulieres)
# 
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
# 
#         http://www.apache.org/licenses/LICENSE-2.0
# 
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#


# Form implementation generated from reading ui file 'ui_git_delete_branch.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
# Patched by patch_ui.py
#
# WARNING! All changes made in this file will be lost!


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_GitDeleteBranch(object):
    def setupUi(self, GitDeleteBranch: QtWidgets.QDialog) -> None:
        GitDeleteBranch.setObjectName("GitDeleteBranch")
        GitDeleteBranch.resize(883, 423)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(GitDeleteBranch)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(GitDeleteBranch)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(554, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.comboBoxBranchName = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxBranchName.sizePolicy().hasHeightForWidth())
        self.comboBoxBranchName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.comboBoxBranchName.setFont(font)
        self.comboBoxBranchName.setEditable(True)
        self.comboBoxBranchName.setObjectName("comboBoxBranchName")
        self.gridLayout.addWidget(self.comboBoxBranchName, 0, 1, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(554, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.checkBoxDeleteLR = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxDeleteLR.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxDeleteLR.setObjectName("checkBoxDeleteLR")
        self.gridLayout.addWidget(self.checkBoxDeleteLR, 1, 1, 1, 2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(GitDeleteBranch)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelRepoSelected = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRepoSelected.sizePolicy().hasHeightForWidth())
        self.labelRepoSelected.setSizePolicy(sizePolicy)
        self.labelRepoSelected.setAlignment(QtCore.Qt.AlignCenter)
        self.labelRepoSelected.setObjectName("labelRepoSelected")
        self.horizontalLayout.addWidget(self.labelRepoSelected)
        self.pushButtonAdjustRepoList = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdjustRepoList.sizePolicy().hasHeightForWidth())
        self.pushButtonAdjustRepoList.setSizePolicy(sizePolicy)
        self.pushButtonAdjustRepoList.setObjectName("pushButtonAdjustRepoList")
        self.horizontalLayout.addWidget(self.pushButtonAdjustRepoList)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeWidgetRepoList = QtWidgets.QTreeWidget(self.groupBox_2)
        self.treeWidgetRepoList.setAlternatingRowColors(True)
        self.treeWidgetRepoList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidgetRepoList.setRootIsDecorated(False)
        self.treeWidgetRepoList.setUniformRowHeights(True)
        self.treeWidgetRepoList.setItemsExpandable(False)
        self.treeWidgetRepoList.setObjectName("treeWidgetRepoList")
        self.verticalLayout.addWidget(self.treeWidgetRepoList)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.buttonBox = QtWidgets.QDialogButtonBox(GitDeleteBranch)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.retranslateUi(GitDeleteBranch)
        self.buttonBox.accepted.connect(GitDeleteBranch.accept)
        self.buttonBox.rejected.connect(GitDeleteBranch.reject)
        QtCore.QMetaObject.connectSlotsByName(GitDeleteBranch)

    def retranslateUi(self, GitDeleteBranch: QtWidgets.QDialog) -> None:
        _translate = QtCore.QCoreApplication.translate
        GitDeleteBranch.setWindowTitle(_translate("GitDeleteBranch", "Delete branch"))
        self.groupBox.setTitle(_translate("GitDeleteBranch", "Delete Branch"))
        self.label.setText(_translate("GitDeleteBranch", "Enter branch name :"))
        self.checkBoxDeleteLR.setText(_translate("GitDeleteBranch", "Delete locally and remotely"))
        self.groupBox_2.setTitle(_translate("GitDeleteBranch", "Targeted repositories"))
        self.labelRepoSelected.setText(_translate("GitDeleteBranch", "3 repositories selected"))
        self.pushButtonAdjustRepoList.setText(_translate("GitDeleteBranch", "Adjust Repository list"))
        self.treeWidgetRepoList.setSortingEnabled(True)
        self.treeWidgetRepoList.headerItem().setText(0, _translate("GitDeleteBranch", "hidden"))
        self.treeWidgetRepoList.headerItem().setText(1, _translate("GitDeleteBranch", "Git Repo Path"))
        self.treeWidgetRepoList.headerItem().setText(2, _translate("GitDeleteBranch", "Head"))
        self.treeWidgetRepoList.headerItem().setText(3, _translate("GitDeleteBranch", "Status"))
        self.treeWidgetRepoList.headerItem().setText(4, _translate("GitDeleteBranch", "Last Remote Syncho"))
