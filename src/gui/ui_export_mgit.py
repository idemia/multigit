# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_export_mgit.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from src.mg_button_history import MgButtonHistory
# import multigit_resources_rc

class Ui_ExportMgit(object):
    def setupUi(self, ExportMgit: QDialog) -> None:
        if not ExportMgit.objectName():
            ExportMgit.setObjectName(u"ExportMgit")
        ExportMgit.resize(646, 196)
        self.verticalLayout = QVBoxLayout(ExportMgit)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ExportMgit)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(False)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditMgitFile = QLineEdit(ExportMgit)
        self.lineEditMgitFile.setObjectName(u"lineEditMgitFile")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditMgitFile.sizePolicy().hasHeightForWidth())
        self.lineEditMgitFile.setSizePolicy(sizePolicy)
        self.lineEditMgitFile.setFont(font)

        self.horizontalLayout_2.addWidget(self.lineEditMgitFile)

        self.historyButtonMgitFile = MgButtonHistory(ExportMgit)
        self.historyButtonMgitFile.setObjectName(u"historyButtonMgitFile")
        icon = QIcon()
        icon.addFile(u":/img/icons8-history-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.historyButtonMgitFile.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.historyButtonMgitFile)

        self.pushButtonChooseMgitFile = QPushButton(ExportMgit)
        self.pushButtonChooseMgitFile.setObjectName(u"pushButtonChooseMgitFile")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonChooseMgitFile.sizePolicy().hasHeightForWidth())
        self.pushButtonChooseMgitFile.setSizePolicy(sizePolicy1)
        self.pushButtonChooseMgitFile.setMinimumSize(QSize(24, 0))
        self.pushButtonChooseMgitFile.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/img/icons8-open-folder-64.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonChooseMgitFile.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.pushButtonChooseMgitFile)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_2 = QLabel(ExportMgit)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.lineEditDescMgit = QLineEdit(ExportMgit)
        self.lineEditDescMgit.setObjectName(u"lineEditDescMgit")

        self.verticalLayout.addWidget(self.lineEditDescMgit)

        self.verticalSpacer = QSpacerItem(20, 48, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonCancel = QPushButton(ExportMgit)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)

        self.pushButtonExportSnapshot = QPushButton(ExportMgit)
        self.pushButtonExportSnapshot.setObjectName(u"pushButtonExportSnapshot")

        self.horizontalLayout.addWidget(self.pushButtonExportSnapshot)

        self.pushButtonExportProject = QPushButton(ExportMgit)
        self.pushButtonExportProject.setObjectName(u"pushButtonExportProject")

        self.horizontalLayout.addWidget(self.pushButtonExportProject)


        self.verticalLayout.addLayout(self.horizontalLayout)

        QWidget.setTabOrder(self.lineEditMgitFile, self.historyButtonMgitFile)
        QWidget.setTabOrder(self.historyButtonMgitFile, self.pushButtonChooseMgitFile)
        QWidget.setTabOrder(self.pushButtonChooseMgitFile, self.lineEditDescMgit)
        QWidget.setTabOrder(self.lineEditDescMgit, self.pushButtonCancel)
        QWidget.setTabOrder(self.pushButtonCancel, self.pushButtonExportSnapshot)
        QWidget.setTabOrder(self.pushButtonExportSnapshot, self.pushButtonExportProject)

        self.retranslateUi(ExportMgit)

        QMetaObject.connectSlotsByName(ExportMgit)
    # setupUi

    def retranslateUi(self, ExportMgit: QDialog) -> None:
        ExportMgit.setWindowTitle(QCoreApplication.translate("ExportMgit", u"Export to multigit file", None))
        self.label.setText(QCoreApplication.translate("ExportMgit", u"Select destination multigit file :", None))
#if QT_CONFIG(tooltip)
        self.historyButtonMgitFile.setToolTip(QCoreApplication.translate("ExportMgit", u"Choose recent multigit file", None))
#endif // QT_CONFIG(tooltip)
        self.historyButtonMgitFile.setText("")
#if QT_CONFIG(tooltip)
        self.pushButtonChooseMgitFile.setToolTip(QCoreApplication.translate("ExportMgit", u"Select multigit file", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonChooseMgitFile.setText("")
        self.label_2.setText(QCoreApplication.translate("ExportMgit", u"Description of your multigit file", None))
#if QT_CONFIG(tooltip)
        self.lineEditDescMgit.setToolTip(QCoreApplication.translate("ExportMgit", u"Description of your multigit file", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonCancel.setText(QCoreApplication.translate("ExportMgit", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.pushButtonExportSnapshot.setToolTip(QCoreApplication.translate("ExportMgit", u"Export all repos with detached HEAD set on last commit, to create a snapshot of the project", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonExportSnapshot.setText(QCoreApplication.translate("ExportMgit", u"Export as snapshot (commit)", None))
#if QT_CONFIG(tooltip)
        self.pushButtonExportProject.setToolTip(QCoreApplication.translate("ExportMgit", u"Export all repos with HEAD set on current branch or tag for regular project development", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonExportProject.setText(QCoreApplication.translate("ExportMgit", u"Export as project (tag/branch)", None))
    # retranslateUi

