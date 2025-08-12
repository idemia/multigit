# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_git_exec_window.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QHeaderView, QLabel, QProgressBar,
    QSizePolicy, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_GitExecDialog(object):
    def setupUi(self, GitExecDialog: QDialog) -> None:
        if not GitExecDialog.objectName():
            GitExecDialog.setObjectName(u"GitExecDialog")
        GitExecDialog.resize(915, 624)
        self.verticalLayout = QVBoxLayout(GitExecDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeGitJobs = QTreeWidget(GitExecDialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"col1");
        self.treeGitJobs.setHeaderItem(__qtreewidgetitem)
        QTreeWidgetItem(self.treeGitJobs)
        self.treeGitJobs.setObjectName(u"treeGitJobs")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.treeGitJobs.sizePolicy().hasHeightForWidth())
        self.treeGitJobs.setSizePolicy(sizePolicy)
        self.treeGitJobs.setHeaderHidden(True)

        self.verticalLayout.addWidget(self.treeGitJobs)

        self.progressBar = QProgressBar(GitExecDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)

        self.verticalLayout.addWidget(self.progressBar)

        self.widget = QWidget(GitExecDialog)
        self.widget.setObjectName(u"widget")

        self.verticalLayout.addWidget(self.widget)

        self.label = QLabel(GitExecDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.textEditSummary = QTextEdit(GitExecDialog)
        self.textEditSummary.setObjectName(u"textEditSummary")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textEditSummary.sizePolicy().hasHeightForWidth())
        self.textEditSummary.setSizePolicy(sizePolicy1)
        self.textEditSummary.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEditSummary)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelTasks = QLabel(GitExecDialog)
        self.labelTasks.setObjectName(u"labelTasks")

        self.horizontalLayout.addWidget(self.labelTasks)

        self.buttonBox = QDialogButtonBox(GitExecDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        font1 = QFont()
        font1.setPointSize(10)
        self.buttonBox.setFont(font1)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Discard|QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(GitExecDialog)
        self.buttonBox.accepted.connect(GitExecDialog.accept)
        self.buttonBox.rejected.connect(GitExecDialog.reject)

        QMetaObject.connectSlotsByName(GitExecDialog)
    # setupUi

    def retranslateUi(self, GitExecDialog: QDialog) -> None:
        GitExecDialog.setWindowTitle(QCoreApplication.translate("GitExecDialog", u"Running Commands", None))
        ___qtreewidgetitem = self.treeGitJobs.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("GitExecDialog", u"col2", None));

        __sortingEnabled = self.treeGitJobs.isSortingEnabled()
        self.treeGitJobs.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeGitJobs.topLevelItem(0)
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("GitExecDialog", u"toto", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("GitExecDialog", u"New Item", None));
        self.treeGitJobs.setSortingEnabled(__sortingEnabled)

        self.progressBar.setFormat(QCoreApplication.translate("GitExecDialog", u"%v of %m done", None))
        self.label.setText(QCoreApplication.translate("GitExecDialog", u"Access right summary :", None))
        self.labelTasks.setText(QCoreApplication.translate("GitExecDialog", u"TextLabel", None))
    # retranslateUi

