# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_apply_mgit_file.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

from src.mg_button_history import MgButtonHistory
# import multigit_resources_rc

class Ui_ApplyMgitFile(object):
    def setupUi(self, ApplyMgitFile: QDialog) -> None:
        if not ApplyMgitFile.objectName():
            ApplyMgitFile.setObjectName(u"ApplyMgitFile")
        ApplyMgitFile.resize(1010, 614)
        self.verticalLayout_4 = QVBoxLayout(ApplyMgitFile)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(ApplyMgitFile)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        self.label_2.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.lineEditDestDir = QLineEdit(ApplyMgitFile)
        self.lineEditDestDir.setObjectName(u"lineEditDestDir")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(10)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEditDestDir.sizePolicy().hasHeightForWidth())
        self.lineEditDestDir.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setBold(False)
        self.lineEditDestDir.setFont(font1)
        self.lineEditDestDir.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineEditDestDir)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.groupBox = QGroupBox(ApplyMgitFile)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy2)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)

        self.pushButtonChooseMgitFile = QPushButton(self.groupBox)
        self.pushButtonChooseMgitFile.setObjectName(u"pushButtonChooseMgitFile")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButtonChooseMgitFile.sizePolicy().hasHeightForWidth())
        self.pushButtonChooseMgitFile.setSizePolicy(sizePolicy3)
        self.pushButtonChooseMgitFile.setMinimumSize(QSize(24, 0))
        self.pushButtonChooseMgitFile.setFont(font1)
        icon = QIcon()
        icon.addFile(u":/img/icons8-open-folder-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonChooseMgitFile.setIcon(icon)

        self.gridLayout.addWidget(self.pushButtonChooseMgitFile, 1, 3, 1, 1)

        self.lineEditMgitFile = QLineEdit(self.groupBox)
        self.lineEditMgitFile.setObjectName(u"lineEditMgitFile")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(10)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEditMgitFile.sizePolicy().hasHeightForWidth())
        self.lineEditMgitFile.setSizePolicy(sizePolicy4)
        self.lineEditMgitFile.setFont(font1)

        self.gridLayout.addWidget(self.lineEditMgitFile, 1, 1, 1, 1)

        self.historyButtonMgitFile = MgButtonHistory(self.groupBox)
        self.historyButtonMgitFile.setObjectName(u"historyButtonMgitFile")
        icon1 = QIcon()
        icon1.addFile(u":/img/icons8-history-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.historyButtonMgitFile.setIcon(icon1)

        self.gridLayout.addWidget(self.historyButtonMgitFile, 1, 2, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(ApplyMgitFile)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.checkBoxAutoStash = QCheckBox(self.groupBox_2)
        self.checkBoxAutoStash.setObjectName(u"checkBoxAutoStash")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(3)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.checkBoxAutoStash.sizePolicy().hasHeightForWidth())
        self.checkBoxAutoStash.setSizePolicy(sizePolicy5)
        self.checkBoxAutoStash.setFont(font1)
#if QT_CONFIG(tooltip)
        self.checkBoxAutoStash.setToolTip(u"")
#endif // QT_CONFIG(tooltip)

        self.verticalLayout_5.addWidget(self.checkBoxAutoStash)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(ApplyMgitFile)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFont(font)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.groupBox_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEditUsername = QLineEdit(self.groupBox_4)
        self.lineEditUsername.setObjectName(u"lineEditUsername")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.lineEditUsername.sizePolicy().hasHeightForWidth())
        self.lineEditUsername.setSizePolicy(sizePolicy6)

        self.horizontalLayout_4.addWidget(self.lineEditUsername)

        self.historyButtonUsername = MgButtonHistory(self.groupBox_4)
        self.historyButtonUsername.setObjectName(u"historyButtonUsername")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.historyButtonUsername.sizePolicy().hasHeightForWidth())
        self.historyButtonUsername.setSizePolicy(sizePolicy7)
        self.historyButtonUsername.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.historyButtonUsername)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.tabWidgetProject = QTabWidget(ApplyMgitFile)
        self.tabWidgetProject.setObjectName(u"tabWidgetProject")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(10)
        sizePolicy8.setHeightForWidth(self.tabWidgetProject.sizePolicy().hasHeightForWidth())
        self.tabWidgetProject.setSizePolicy(sizePolicy8)
        self.tabProject = QWidget()
        self.tabProject.setObjectName(u"tabProject")
        self.verticalLayout = QVBoxLayout(self.tabProject)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.labelProjDesc = QLabel(self.tabProject)
        self.labelProjDesc.setObjectName(u"labelProjDesc")
        sizePolicy.setHeightForWidth(self.labelProjDesc.sizePolicy().hasHeightForWidth())
        self.labelProjDesc.setSizePolicy(sizePolicy)
        self.labelProjDesc.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelProjDesc)

        self.textEditProjectDesc = QTextEdit(self.tabProject)
        self.textEditProjectDesc.setObjectName(u"textEditProjectDesc")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(1)
        sizePolicy9.setHeightForWidth(self.textEditProjectDesc.sizePolicy().hasHeightForWidth())
        self.textEditProjectDesc.setSizePolicy(sizePolicy9)
        self.textEditProjectDesc.setMaximumSize(QSize(16777215, 50))
        self.textEditProjectDesc.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.textEditProjectDesc)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.treeWidgetRepoList = QTreeWidget(self.tabProject)
        self.treeWidgetRepoList.setObjectName(u"treeWidgetRepoList")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(20)
        sizePolicy10.setHeightForWidth(self.treeWidgetRepoList.sizePolicy().hasHeightForWidth())
        self.treeWidgetRepoList.setSizePolicy(sizePolicy10)
        self.treeWidgetRepoList.setRootIsDecorated(False)
        self.treeWidgetRepoList.setUniformRowHeights(True)
        self.treeWidgetRepoList.setItemsExpandable(False)
        self.treeWidgetRepoList.setSortingEnabled(True)
        self.treeWidgetRepoList.setColumnCount(3)

        self.verticalLayout.addWidget(self.treeWidgetRepoList)

        self.tabWidgetProject.addTab(self.tabProject, "")
        self.tabConfFile = QWidget()
        self.tabConfFile.setObjectName(u"tabConfFile")
        self.verticalLayout_2 = QVBoxLayout(self.tabConfFile)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textEditProj = QTextEdit(self.tabConfFile)
        self.textEditProj.setObjectName(u"textEditProj")

        self.verticalLayout_2.addWidget(self.textEditProj)

        self.tabWidgetProject.addTab(self.tabConfFile, "")

        self.verticalLayout_4.addWidget(self.tabWidgetProject)

        self.groupBox_3 = QGroupBox(ApplyMgitFile)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(self.groupBox_3)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        QWidget.setTabOrder(self.lineEditDestDir, self.lineEditMgitFile)
        QWidget.setTabOrder(self.lineEditMgitFile, self.historyButtonMgitFile)
        QWidget.setTabOrder(self.historyButtonMgitFile, self.pushButtonChooseMgitFile)
        QWidget.setTabOrder(self.pushButtonChooseMgitFile, self.lineEditUsername)
        QWidget.setTabOrder(self.lineEditUsername, self.historyButtonUsername)
        QWidget.setTabOrder(self.historyButtonUsername, self.tabWidgetProject)
        QWidget.setTabOrder(self.tabWidgetProject, self.textEditProjectDesc)
        QWidget.setTabOrder(self.textEditProjectDesc, self.treeWidgetRepoList)
        QWidget.setTabOrder(self.treeWidgetRepoList, self.textEditProj)

        self.retranslateUi(ApplyMgitFile)
        self.buttonBox.accepted.connect(ApplyMgitFile.accept)
        self.buttonBox.rejected.connect(ApplyMgitFile.reject)

        self.tabWidgetProject.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ApplyMgitFile)
    # setupUi

    def retranslateUi(self, ApplyMgitFile: QDialog) -> None:
        ApplyMgitFile.setWindowTitle(QCoreApplication.translate("ApplyMgitFile", u"Apply Multigit File", None))
        self.label_2.setText(QCoreApplication.translate("ApplyMgitFile", u"Base directory :", None))
        self.groupBox.setTitle(QCoreApplication.translate("ApplyMgitFile", u"Multigit file", None))
        self.label.setText(QCoreApplication.translate("ApplyMgitFile", u"Select a multigit file (extension .mgit)", None))
#if QT_CONFIG(tooltip)
        self.pushButtonChooseMgitFile.setToolTip(QCoreApplication.translate("ApplyMgitFile", u"Choose multigit file", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonChooseMgitFile.setText("")
#if QT_CONFIG(tooltip)
        self.historyButtonMgitFile.setToolTip(QCoreApplication.translate("ApplyMgitFile", u"Select recent multigit file", None))
#endif // QT_CONFIG(tooltip)
        self.historyButtonMgitFile.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("ApplyMgitFile", u"Apply behavior", None))
        self.checkBoxAutoStash.setText(QCoreApplication.translate("ApplyMgitFile", u"Auto-stash : stash local changes before switching branch, unstash after switching", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ApplyMgitFile", u" User Name", None))
        self.label_3.setText(QCoreApplication.translate("ApplyMgitFile", u"User name in the git URL when cloning", None))
#if QT_CONFIG(tooltip)
        self.historyButtonUsername.setToolTip(QCoreApplication.translate("ApplyMgitFile", u"Select recent username", None))
#endif // QT_CONFIG(tooltip)
        self.historyButtonUsername.setText("")
        self.labelProjDesc.setText(QCoreApplication.translate("ApplyMgitFile", u"Project description :", None))
        self.textEditProjectDesc.setHtml(QCoreApplication.translate("ApplyMgitFile", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:8.25pt;\"><br /></p></body></html>", None))
        ___qtreewidgetitem = self.treeWidgetRepoList.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("ApplyMgitFile", u"Path", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("ApplyMgitFile", u"HEAD target", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("ApplyMgitFile", u"Repository", None));
        self.tabWidgetProject.setTabText(self.tabWidgetProject.indexOf(self.tabProject), QCoreApplication.translate("ApplyMgitFile", u"Repositories", None))
        self.tabWidgetProject.setTabText(self.tabWidgetProject.indexOf(self.tabConfFile), QCoreApplication.translate("ApplyMgitFile", u"Multigit file content", None))
        self.groupBox_3.setTitle("")
    # retranslateUi

