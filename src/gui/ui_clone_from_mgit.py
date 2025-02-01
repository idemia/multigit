# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_clone_from_mgit.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from src.mg_button_history import MgButtonHistory

# import multigit_resources_rc

class Ui_CloneFromMgitFile(object):
    def setupUi(self, CloneFromMgitFile: QDialog) -> None:
        if not CloneFromMgitFile.objectName():
            CloneFromMgitFile.setObjectName(u"CloneFromMgitFile")
        CloneFromMgitFile.resize(935, 692)
        self.gridLayout_3 = QGridLayout(CloneFromMgitFile)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox = QGroupBox(CloneFromMgitFile)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setBold(False)
        font1.setWeight(50)
        self.label.setFont(font1)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)

        self.pushButtonChooseMgitFile = QPushButton(self.groupBox)
        self.pushButtonChooseMgitFile.setObjectName(u"pushButtonChooseMgitFile")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonChooseMgitFile.sizePolicy().hasHeightForWidth())
        self.pushButtonChooseMgitFile.setSizePolicy(sizePolicy1)
        self.pushButtonChooseMgitFile.setMinimumSize(QSize(24, 0))
        self.pushButtonChooseMgitFile.setFont(font1)
        icon = QIcon()
        icon.addFile(u":/img/icons8-open-folder-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButtonChooseMgitFile.setIcon(icon)

        self.gridLayout.addWidget(self.pushButtonChooseMgitFile, 1, 3, 1, 1)

        self.lineEditMgitFile = QLineEdit(self.groupBox)
        self.lineEditMgitFile.setObjectName(u"lineEditMgitFile")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(10)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEditMgitFile.sizePolicy().hasHeightForWidth())
        self.lineEditMgitFile.setSizePolicy(sizePolicy2)
        self.lineEditMgitFile.setFont(font1)

        self.gridLayout.addWidget(self.lineEditMgitFile, 1, 1, 1, 1)

        self.historyButtonMgitFile = MgButtonHistory(self.groupBox)
        self.historyButtonMgitFile.setObjectName(u"historyButtonMgitFile")
        icon1 = QIcon()
        icon1.addFile(u":/img/icons8-history-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.historyButtonMgitFile.setIcon(icon1)

        self.gridLayout.addWidget(self.historyButtonMgitFile, 1, 2, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 2)

        self.groupBox_2 = QGroupBox(CloneFromMgitFile)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButtonChooseDestDir = QPushButton(self.groupBox_2)
        self.pushButtonChooseDestDir.setObjectName(u"pushButtonChooseDestDir")
        sizePolicy1.setHeightForWidth(self.pushButtonChooseDestDir.sizePolicy().hasHeightForWidth())
        self.pushButtonChooseDestDir.setSizePolicy(sizePolicy1)
        self.pushButtonChooseDestDir.setMinimumSize(QSize(24, 0))
        self.pushButtonChooseDestDir.setFont(font1)
        self.pushButtonChooseDestDir.setIcon(icon)

        self.gridLayout_2.addWidget(self.pushButtonChooseDestDir, 1, 3, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 4)

        self.lineEditDestDir = QLineEdit(self.groupBox_2)
        self.lineEditDestDir.setObjectName(u"lineEditDestDir")
        sizePolicy2.setHeightForWidth(self.lineEditDestDir.sizePolicy().hasHeightForWidth())
        self.lineEditDestDir.setSizePolicy(sizePolicy2)
        self.lineEditDestDir.setFont(font1)

        self.gridLayout_2.addWidget(self.lineEditDestDir, 1, 1, 1, 1)

        self.historyButtonDestDir = MgButtonHistory(self.groupBox_2)
        self.historyButtonDestDir.setObjectName(u"historyButtonDestDir")
        self.historyButtonDestDir.setIcon(icon1)

        self.gridLayout_2.addWidget(self.historyButtonDestDir, 1, 2, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 2)

        self.groupBox_4 = QGroupBox(CloneFromMgitFile)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioDoNotAlterUrl = QRadioButton(self.groupBox_4)
        self.radioDoNotAlterUrl.setObjectName(u"radioDoNotAlterUrl")
        self.radioDoNotAlterUrl.setFont(font1)
        self.radioDoNotAlterUrl.setChecked(True)

        self.verticalLayout.addWidget(self.radioDoNotAlterUrl)

        self.radioStripUsername = QRadioButton(self.groupBox_4)
        self.radioStripUsername.setObjectName(u"radioStripUsername")
        self.radioStripUsername.setFont(font1)

        self.verticalLayout.addWidget(self.radioStripUsername)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioForceUsername = QRadioButton(self.groupBox_4)
        self.radioForceUsername.setObjectName(u"radioForceUsername")
        self.radioForceUsername.setFont(font1)

        self.horizontalLayout_2.addWidget(self.radioForceUsername)

        self.lineEditUsername = QLineEdit(self.groupBox_4)
        self.lineEditUsername.setObjectName(u"lineEditUsername")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(10)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lineEditUsername.sizePolicy().hasHeightForWidth())
        self.lineEditUsername.setSizePolicy(sizePolicy3)
        self.lineEditUsername.setFont(font1)

        self.horizontalLayout_2.addWidget(self.lineEditUsername)

        self.historyButtonUsername = MgButtonHistory(self.groupBox_4)
        self.historyButtonUsername.setObjectName(u"historyButtonUsername")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.historyButtonUsername.sizePolicy().hasHeightForWidth())
        self.historyButtonUsername.setSizePolicy(sizePolicy4)
        self.historyButtonUsername.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.historyButtonUsername)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_3.addWidget(self.groupBox_4, 2, 0, 1, 1)

        self.groupBox_5 = QGroupBox(CloneFromMgitFile)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_4 = QLabel(self.groupBox_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.verticalLayout_5.addWidget(self.label_4)

        self.radioButtonDirExistsGitFail = QRadioButton(self.groupBox_5)
        self.radioButtonDirExistsGitFail.setObjectName(u"radioButtonDirExistsGitFail")
        self.radioButtonDirExistsGitFail.setFont(font1)
        self.radioButtonDirExistsGitFail.setChecked(True)

        self.verticalLayout_5.addWidget(self.radioButtonDirExistsGitFail)

        self.radioButtonDirExistsSkipDir = QRadioButton(self.groupBox_5)
        self.radioButtonDirExistsSkipDir.setObjectName(u"radioButtonDirExistsSkipDir")
        self.radioButtonDirExistsSkipDir.setFont(font1)

        self.verticalLayout_5.addWidget(self.radioButtonDirExistsSkipDir)

        self.radioButtonDirExistsDelDir = QRadioButton(self.groupBox_5)
        self.radioButtonDirExistsDelDir.setObjectName(u"radioButtonDirExistsDelDir")
        self.radioButtonDirExistsDelDir.setFont(font1)

        self.verticalLayout_5.addWidget(self.radioButtonDirExistsDelDir)


        self.gridLayout_3.addWidget(self.groupBox_5, 2, 1, 1, 1)

        self.tabWidgetProject = QTabWidget(CloneFromMgitFile)
        self.tabWidgetProject.setObjectName(u"tabWidgetProject")
        self.tabProject = QWidget()
        self.tabProject.setObjectName(u"tabProject")
        self.verticalLayout_3 = QVBoxLayout(self.tabProject)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelProjDesc = QLabel(self.tabProject)
        self.labelProjDesc.setObjectName(u"labelProjDesc")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.labelProjDesc.sizePolicy().hasHeightForWidth())
        self.labelProjDesc.setSizePolicy(sizePolicy5)
        self.labelProjDesc.setFont(font)

        self.horizontalLayout_3.addWidget(self.labelProjDesc)

        self.textEditProjectDesc = QTextEdit(self.tabProject)
        self.textEditProjectDesc.setObjectName(u"textEditProjectDesc")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(1)
        sizePolicy6.setHeightForWidth(self.textEditProjectDesc.sizePolicy().hasHeightForWidth())
        self.textEditProjectDesc.setSizePolicy(sizePolicy6)
        self.textEditProjectDesc.setMaximumSize(QSize(16777215, 50))
        self.textEditProjectDesc.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.textEditProjectDesc)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.treeWidgetRepoList = QTreeWidget(self.tabProject)
        self.treeWidgetRepoList.setObjectName(u"treeWidgetRepoList")
        self.treeWidgetRepoList.setRootIsDecorated(False)
        self.treeWidgetRepoList.setUniformRowHeights(True)
        self.treeWidgetRepoList.setItemsExpandable(False)
        self.treeWidgetRepoList.setSortingEnabled(True)
        self.treeWidgetRepoList.setColumnCount(4)

        self.verticalLayout_3.addWidget(self.treeWidgetRepoList)

        self.tabWidgetProject.addTab(self.tabProject, "")
        self.tabConfFile = QWidget()
        self.tabConfFile.setObjectName(u"tabConfFile")
        self.verticalLayout_2 = QVBoxLayout(self.tabConfFile)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textEditProj = QTextEdit(self.tabConfFile)
        self.textEditProj.setObjectName(u"textEditProj")

        self.verticalLayout_2.addWidget(self.textEditProj)

        self.tabWidgetProject.addTab(self.tabConfFile, "")

        self.gridLayout_3.addWidget(self.tabWidgetProject, 3, 0, 1, 2)

        self.groupBox_3 = QGroupBox(CloneFromMgitFile)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(self.groupBox_3)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.gridLayout_3.addWidget(self.groupBox_3, 4, 0, 1, 2)

        QWidget.setTabOrder(self.lineEditMgitFile, self.historyButtonMgitFile)
        QWidget.setTabOrder(self.historyButtonMgitFile, self.pushButtonChooseMgitFile)
        QWidget.setTabOrder(self.pushButtonChooseMgitFile, self.lineEditDestDir)
        QWidget.setTabOrder(self.lineEditDestDir, self.historyButtonDestDir)
        QWidget.setTabOrder(self.historyButtonDestDir, self.pushButtonChooseDestDir)
        QWidget.setTabOrder(self.pushButtonChooseDestDir, self.lineEditUsername)
        QWidget.setTabOrder(self.lineEditUsername, self.historyButtonUsername)
        QWidget.setTabOrder(self.historyButtonUsername, self.radioButtonDirExistsGitFail)
        QWidget.setTabOrder(self.radioButtonDirExistsGitFail, self.radioButtonDirExistsSkipDir)
        QWidget.setTabOrder(self.radioButtonDirExistsSkipDir, self.radioButtonDirExistsDelDir)
        QWidget.setTabOrder(self.radioButtonDirExistsDelDir, self.tabWidgetProject)
        QWidget.setTabOrder(self.tabWidgetProject, self.textEditProjectDesc)
        QWidget.setTabOrder(self.textEditProjectDesc, self.treeWidgetRepoList)
        QWidget.setTabOrder(self.treeWidgetRepoList, self.textEditProj)

        self.retranslateUi(CloneFromMgitFile)
        self.buttonBox.accepted.connect(CloneFromMgitFile.accept)
        self.buttonBox.rejected.connect(CloneFromMgitFile.reject)
        self.radioForceUsername.toggled.connect(self.lineEditUsername.setEnabled)
        self.radioForceUsername.toggled.connect(self.historyButtonUsername.setEnabled)

        self.tabWidgetProject.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CloneFromMgitFile)
    # setupUi

    def retranslateUi(self, CloneFromMgitFile: QDialog) -> None:
        CloneFromMgitFile.setWindowTitle(QCoreApplication.translate("CloneFromMgitFile", u"Clone from Multigit file", None))
        self.groupBox.setTitle(QCoreApplication.translate("CloneFromMgitFile", u"Multigit File", None))
        self.label.setText(QCoreApplication.translate("CloneFromMgitFile", u"Select a multigit file (extension .mgit)", None))
#if QT_CONFIG(tooltip)
        self.pushButtonChooseMgitFile.setToolTip(QCoreApplication.translate("CloneFromMgitFile", u"Choose multigit file", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonChooseMgitFile.setText("")
#if QT_CONFIG(tooltip)
        self.historyButtonMgitFile.setToolTip(QCoreApplication.translate("CloneFromMgitFile", u"Select recent multigit file", None))
#endif // QT_CONFIG(tooltip)
        self.historyButtonMgitFile.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("CloneFromMgitFile", u"Project Destination Directory", None))
#if QT_CONFIG(tooltip)
        self.pushButtonChooseDestDir.setToolTip(QCoreApplication.translate("CloneFromMgitFile", u"Choose directory", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonChooseDestDir.setText("")
        self.label_2.setText(QCoreApplication.translate("CloneFromMgitFile", u"Choose target directory for the clone:", None))
#if QT_CONFIG(tooltip)
        self.historyButtonDestDir.setToolTip(QCoreApplication.translate("CloneFromMgitFile", u"Select recent directory", None))
#endif // QT_CONFIG(tooltip)
        self.historyButtonDestDir.setText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("CloneFromMgitFile", u"User Name in url", None))
        self.radioDoNotAlterUrl.setText(QCoreApplication.translate("CloneFromMgitFile", u"Do not alter url", None))
        self.radioStripUsername.setText(QCoreApplication.translate("CloneFromMgitFile", u"Remove login from url if present", None))
        self.radioForceUsername.setText(QCoreApplication.translate("CloneFromMgitFile", u"Force login username to :", None))
#if QT_CONFIG(tooltip)
        self.historyButtonUsername.setToolTip(QCoreApplication.translate("CloneFromMgitFile", u"Select recent user name", None))
#endif // QT_CONFIG(tooltip)
        self.historyButtonUsername.setText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("CloneFromMgitFile", u"Existing directory behavior", None))
        self.label_4.setText(QCoreApplication.translate("CloneFromMgitFile", u"If clone directory already exists :", None))
        self.radioButtonDirExistsGitFail.setText(QCoreApplication.translate("CloneFromMgitFile", u"Git fails to clone", None))
        self.radioButtonDirExistsSkipDir.setText(QCoreApplication.translate("CloneFromMgitFile", u"Skip directory", None))
        self.radioButtonDirExistsDelDir.setText(QCoreApplication.translate("CloneFromMgitFile", u"Delete directory", None))
        self.labelProjDesc.setText(QCoreApplication.translate("CloneFromMgitFile", u"Project description :", None))
        self.textEditProjectDesc.setHtml(QCoreApplication.translate("CloneFromMgitFile", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8.25pt;\"><br /></p></body></html>", None))
        ___qtreewidgetitem = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("CloneFromMgitFile", u"URL", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("CloneFromMgitFile", u"Path", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("CloneFromMgitFile", u"HEAD target", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("CloneFromMgitFile", u"Repository", None));
        self.tabWidgetProject.setTabText(self.tabWidgetProject.indexOf(self.tabProject), QCoreApplication.translate("CloneFromMgitFile", u"Repositories", None))
        self.tabWidgetProject.setTabText(self.tabWidgetProject.indexOf(self.tabConfFile), QCoreApplication.translate("CloneFromMgitFile", u"Multigit file content", None))
        self.groupBox_3.setTitle("")
    # retranslateUi

