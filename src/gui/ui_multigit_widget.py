# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_multigit_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from src.mg_repo_tree import MgRepoTree
from src.mg_button_history import MgButtonHistory

# import multigit_resources_rc

class Ui_MultigitWidget(object):
    def setupUi(self, MultigitWidget: QWidget) -> None:
        if not MultigitWidget.objectName():
            MultigitWidget.setObjectName(u"MultigitWidget")
        MultigitWidget.resize(649, 639)
        self.verticalLayout_2 = QVBoxLayout(MultigitWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(MultigitWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditBaseDir = QLineEdit(self.layoutWidget)
        self.lineEditBaseDir.setObjectName(u"lineEditBaseDir")
        self.lineEditBaseDir.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEditBaseDir)

        self.buttonHistoryBaseDir = MgButtonHistory(self.layoutWidget)
        self.buttonHistoryBaseDir.setObjectName(u"buttonHistoryBaseDir")
        icon = QIcon()
        icon.addFile(u":/img/icons8-history-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonHistoryBaseDir.setIcon(icon)

        self.horizontalLayout.addWidget(self.buttonHistoryBaseDir)

        self.buttonOpenBaseDir = QPushButton(self.layoutWidget)
        self.buttonOpenBaseDir.setObjectName(u"buttonOpenBaseDir")
        icon1 = QIcon()
        icon1.addFile(u":/img/icons8-open-folder-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonOpenBaseDir.setIcon(icon1)

        self.horizontalLayout.addWidget(self.buttonOpenBaseDir)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.repoTree = MgRepoTree(self.layoutWidget)
        self.repoTree.headerItem().setText(0, "")
        self.repoTree.setObjectName(u"repoTree")
        self.repoTree.setLineWidth(3)
        self.repoTree.setMidLineWidth(4)
        self.repoTree.setAlternatingRowColors(True)
        self.repoTree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.repoTree.setRootIsDecorated(False)
        self.repoTree.setUniformRowHeights(True)
        self.repoTree.setItemsExpandable(False)
        self.repoTree.setSortingEnabled(True)
        self.repoTree.setAllColumnsShowFocus(True)

        self.verticalLayout.addWidget(self.repoTree)

        self.splitter.addWidget(self.layoutWidget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabLastCommit = QWidget()
        self.tabLastCommit.setObjectName(u"tabLastCommit")
        self.horizontalLayout_3 = QHBoxLayout(self.tabLastCommit)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.textEditCommit = QTextEdit(self.tabLastCommit)
        self.textEditCommit.setObjectName(u"textEditCommit")
        self.textEditCommit.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.textEditCommit)

        self.tabWidget.addTab(self.tabLastCommit, "")
        self.tabModifiedFiles = QWidget()
        self.tabModifiedFiles.setObjectName(u"tabModifiedFiles")
        self.horizontalLayout_4 = QHBoxLayout(self.tabModifiedFiles)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.textEditModFiles = QTextEdit(self.tabModifiedFiles)
        self.textEditModFiles.setObjectName(u"textEditModFiles")
        font = QFont()
        font.setFamily(u"Courier New")
        self.textEditModFiles.setFont(font)
        self.textEditModFiles.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.textEditModFiles)

        self.tabWidget.addTab(self.tabModifiedFiles, "")
        self.splitter.addWidget(self.tabWidget)

        self.verticalLayout_2.addWidget(self.splitter)

        QWidget.setTabOrder(self.lineEditBaseDir, self.buttonHistoryBaseDir)
        QWidget.setTabOrder(self.buttonHistoryBaseDir, self.buttonOpenBaseDir)
        QWidget.setTabOrder(self.buttonOpenBaseDir, self.repoTree)
        QWidget.setTabOrder(self.repoTree, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.textEditCommit)
        QWidget.setTabOrder(self.textEditCommit, self.textEditModFiles)

        self.retranslateUi(MultigitWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MultigitWidget)
    # setupUi

    def retranslateUi(self, MultigitWidget: QWidget) -> None:
        MultigitWidget.setWindowTitle(QCoreApplication.translate("MultigitWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("MultigitWidget", u"Base directory :", None))
#if QT_CONFIG(tooltip)
        self.buttonHistoryBaseDir.setToolTip(QCoreApplication.translate("MultigitWidget", u"Open recent base directory", None))
#endif // QT_CONFIG(tooltip)
        self.buttonHistoryBaseDir.setText("")
#if QT_CONFIG(tooltip)
        self.buttonOpenBaseDir.setToolTip(QCoreApplication.translate("MultigitWidget", u"Open base directory", None))
#endif // QT_CONFIG(tooltip)
        self.buttonOpenBaseDir.setText("")
        ___qtreewidgetitem = self.repoTree.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MultigitWidget", u"Last Remote Synchro", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MultigitWidget", u"Status", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MultigitWidget", u"Head", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MultigitWidget", u"Git Repo Path", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLastCommit), QCoreApplication.translate("MultigitWidget", u"Last Commit", None))
        self.textEditModFiles.setHtml(QCoreApplication.translate("MultigitWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Courier New'; font-size:9.75pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; color:#0000ff;\">@@ this is a description @@</span><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt;\"> bla bla bla<br />this line is plain<br /></span><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; color:#aa0000;\">- this line is removed</span><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt;\"><br /></span><span style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; color:#00aa00;\">+ this line is added</span><span style=\" font-family:'MS Shell Dlg 2'; font-size:8"
                        "pt;\"><br /><br /></span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabModifiedFiles), QCoreApplication.translate("MultigitWidget", u"Modified Files", None))
    # retranslateUi

