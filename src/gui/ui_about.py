# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_about.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDialog, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTextBrowser, QVBoxLayout, QWidget)
# import multigit_resources_rc

class Ui_dialogAbout(object):
    def setupUi(self, dialogAbout: QDialog) -> None:
        if not dialogAbout.objectName():
            dialogAbout.setObjectName(u"dialogAbout")
        dialogAbout.resize(895, 571)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        dialogAbout.setPalette(palette)
        self.verticalLayout_2 = QVBoxLayout(dialogAbout)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(dialogAbout)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(100, 100))
        self.label.setPixmap(QPixmap(u":/img/multigit-logo-256.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.label)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.textBrowserTitle = QTextBrowser(dialogAbout)
        self.textBrowserTitle.setObjectName(u"textBrowserTitle")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.textBrowserTitle.sizePolicy().hasHeightForWidth())
        self.textBrowserTitle.setSizePolicy(sizePolicy1)
        self.textBrowserTitle.setMinimumSize(QSize(0, 120))
        self.textBrowserTitle.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.textBrowserTitle.setAcceptDrops(False)
        self.textBrowserTitle.setAutoFillBackground(False)
        self.textBrowserTitle.setFrameShape(QFrame.Shape.NoFrame)
        self.textBrowserTitle.setFrameShadow(QFrame.Shadow.Plain)
        self.textBrowserTitle.setLineWidth(0)
        self.textBrowserTitle.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowserTitle.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowserTitle.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout.addWidget(self.textBrowserTitle)

        self.label_2 = QLabel(dialogAbout)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setPixmap(QPixmap(u":/img/idemia-logo.png"))

        self.horizontalLayout.addWidget(self.label_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.textBrowserContent = QTextBrowser(dialogAbout)
        self.textBrowserContent.setObjectName(u"textBrowserContent")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.textBrowserContent.sizePolicy().hasHeightForWidth())
        self.textBrowserContent.setSizePolicy(sizePolicy3)
        self.textBrowserContent.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.textBrowserContent.setFrameShape(QFrame.Shape.NoFrame)
        self.textBrowserContent.setOpenExternalLinks(True)
        self.textBrowserContent.setOpenLinks(True)

        self.verticalLayout_2.addWidget(self.textBrowserContent)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pushButtonFullLicense = QPushButton(dialogAbout)
        self.pushButtonFullLicense.setObjectName(u"pushButtonFullLicense")
        self.pushButtonFullLicense.setMaximumSize(QSize(16777215, 16777214))
        font = QFont()
        font.setPointSize(10)
        self.pushButtonFullLicense.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButtonFullLicense)

        self.widget = QWidget(dialogAbout)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout_2.addWidget(self.widget)

        self.pushButtonOk = QPushButton(dialogAbout)
        self.pushButtonOk.setObjectName(u"pushButtonOk")
        self.pushButtonOk.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButtonOk)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.textBrowserTitle, self.textBrowserContent)
        QWidget.setTabOrder(self.textBrowserContent, self.pushButtonFullLicense)
        QWidget.setTabOrder(self.pushButtonFullLicense, self.pushButtonOk)

        self.retranslateUi(dialogAbout)

        self.pushButtonOk.setDefault(True)


        QMetaObject.connectSlotsByName(dialogAbout)
    # setupUi

    def retranslateUi(self, dialogAbout: QDialog) -> None:
        dialogAbout.setWindowTitle(QCoreApplication.translate("dialogAbout", u"About Multigit", None))
        self.label.setText("")
        self.textBrowserTitle.setHtml(QCoreApplication.translate("dialogAbout", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:6.6pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:18pt; font-weight:600;\">Multigit by IDEMIA</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:e"
                        "mpty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:12pt; font-style:italic;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:12pt; font-style:italic;\">Multigit helps managing multiple Git repositories with one interface</span></p></body></html>", None))
        self.label_2.setText("")
        self.textBrowserContent.setHtml(QCoreApplication.translate("dialogAbout", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:6.6pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">Multigit OpenSource version [version]</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px"
                        "; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">Copyright IDEMIA 2019-2024</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">Multigit is developed at </span><a href=\"https://www.idemia.com/\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; text-decoration: underline; color:#0000ff;\">IDEMIA</span></a><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\"> by Philippe Fremy.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:10pt;\"><br /><"
                        "/p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">Multigit is licensed under </span><a href=\"http://www.apache.org/licenses/LICENSE-2.0\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; text-decoration: underline; color:#0000ff;\">Apache License 2.0</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">Multigit includes the software components:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS"
                        " Shell Dlg 2'; font-size:10pt;\">- </span><a href=\"https://www.python.org\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; text-decoration: underline; color:#0000ff;\">Python 3.8</span></a><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">  (from the Python Software Foundation)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">- </span><a href=\"https://www.qt.io/\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; text-decoration: underline; color:#0000ff;\">Qt for Python 5.15 </span></a><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">(by the Qt Group)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">- </span><a href=\"https://pypi.org/project/concurrent-log-hand"
                        "ler/\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; text-decoration: underline; color:#0000ff;\">Concurrent-log-handler</span></a><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\"> (by Preston Landers)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">- </span><a href=\"https://pyinstaller.org/en/stable/\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; text-decoration: underline; color:#0000ff;\">PyInstaller</span></a><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\"> (by David Cortesi)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text"
                        "-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">Most icons are provided by freely </span><a href=\"https://icons8.com\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; text-decoration: underline; color:#0000ff;\">Icons8</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:10pt;\">Icons from the softwares Git, TortoiseGit, SourceTree, SublimeMerge are used to represent activation of the related software. Icons remain the properties of their copyright owner. IDEMIA logo is copyrighted to IDEMIA and can not be used without IDEMIA's approval (see licensing for details).</span></p></body></html>", None))
        self.pushButtonFullLicense.setText(QCoreApplication.translate("dialogAbout", u"Full Licensing Information", None))
        self.pushButtonOk.setText(QCoreApplication.translate("dialogAbout", u"Ok", None))
    # retranslateUi

