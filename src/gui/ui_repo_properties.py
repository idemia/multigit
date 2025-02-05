# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_repo_properties.ui'
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
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_RepoProperties(object):
    def setupUi(self, RepoProperties: QDialog) -> None:
        if not RepoProperties.objectName():
            RepoProperties.setObjectName(u"RepoProperties")
        RepoProperties.resize(844, 804)
        self.gridLayout = QGridLayout(RepoProperties)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(RepoProperties)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditDir = QLineEdit(RepoProperties)
        self.lineEditDir.setObjectName(u"lineEditDir")
        self.lineEditDir.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditDir, 0, 1, 1, 1)

        self.label_3 = QLabel(RepoProperties)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.lineEditFullPath = QLineEdit(RepoProperties)
        self.lineEditFullPath.setObjectName(u"lineEditFullPath")
        self.lineEditFullPath.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditFullPath, 1, 1, 1, 1)

        self.buttonCopyPath = QPushButton(RepoProperties)
        self.buttonCopyPath.setObjectName(u"buttonCopyPath")

        self.gridLayout.addWidget(self.buttonCopyPath, 1, 2, 1, 1)

        self.label_4 = QLabel(RepoProperties)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.lineEditUrl = QLineEdit(RepoProperties)
        self.lineEditUrl.setObjectName(u"lineEditUrl")
        self.lineEditUrl.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditUrl, 2, 1, 1, 1)

        self.buttonCopyUrl = QPushButton(RepoProperties)
        self.buttonCopyUrl.setObjectName(u"buttonCopyUrl")

        self.gridLayout.addWidget(self.buttonCopyUrl, 2, 2, 1, 1)

        self.label_5 = QLabel(RepoProperties)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.lineEditHead = QLineEdit(RepoProperties)
        self.lineEditHead.setObjectName(u"lineEditHead")
        self.lineEditHead.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditHead, 3, 1, 1, 1)

        self.label_7 = QLabel(RepoProperties)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)

        self.lineEditStatus = QLineEdit(RepoProperties)
        self.lineEditStatus.setObjectName(u"lineEditStatus")
        self.lineEditStatus.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditStatus, 4, 1, 1, 1)

        self.label_6 = QLabel(RepoProperties)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.lineEditRemoteBranch = QLineEdit(RepoProperties)
        self.lineEditRemoteBranch.setObjectName(u"lineEditRemoteBranch")
        self.lineEditRemoteBranch.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditRemoteBranch, 5, 1, 1, 1)

        self.label_9 = QLabel(RepoProperties)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_9, 6, 0, 1, 1)

        self.lineEditRemoteSynchro = QLineEdit(RepoProperties)
        self.lineEditRemoteSynchro.setObjectName(u"lineEditRemoteSynchro")
        self.lineEditRemoteSynchro.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditRemoteSynchro, 6, 1, 1, 1)

        self.label_10 = QLabel(RepoProperties)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 7, 0, 1, 1)

        self.lineEditTags = QLineEdit(RepoProperties)
        self.lineEditTags.setObjectName(u"lineEditTags")

        self.gridLayout.addWidget(self.lineEditTags, 7, 1, 1, 1)

        self.label_8 = QLabel(RepoProperties)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(3)
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.textEditLastCommit = QTextEdit(RepoProperties)
        self.textEditLastCommit.setObjectName(u"textEditLastCommit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(3)
        sizePolicy2.setHeightForWidth(self.textEditLastCommit.sizePolicy().hasHeightForWidth())
        self.textEditLastCommit.setSizePolicy(sizePolicy2)
        self.textEditLastCommit.setReadOnly(True)
        self.textEditLastCommit.setAcceptRichText(False)

        self.gridLayout.addWidget(self.textEditLastCommit, 8, 1, 1, 1)

        self.label_13 = QLabel(RepoProperties)
        self.label_13.setObjectName(u"label_13")
        sizePolicy1.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_13, 9, 0, 1, 1)

        self.textEditDiffSummary = QTextEdit(RepoProperties)
        self.textEditDiffSummary.setObjectName(u"textEditDiffSummary")
        sizePolicy2.setHeightForWidth(self.textEditDiffSummary.sizePolicy().hasHeightForWidth())
        self.textEditDiffSummary.setSizePolicy(sizePolicy2)
        self.textEditDiffSummary.setReadOnly(True)

        self.gridLayout.addWidget(self.textEditDiffSummary, 9, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(RepoProperties)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout.addWidget(self.buttonBox, 10, 1, 1, 1)


        self.retranslateUi(RepoProperties)
        self.buttonBox.accepted.connect(RepoProperties.accept)
        self.buttonBox.rejected.connect(RepoProperties.reject)

        QMetaObject.connectSlotsByName(RepoProperties)
    # setupUi

    def retranslateUi(self, RepoProperties: QDialog) -> None:
        RepoProperties.setWindowTitle(QCoreApplication.translate("RepoProperties", u"Git Repository properties", None))
        self.label.setText(QCoreApplication.translate("RepoProperties", u"Directory :", None))
        self.label_3.setText(QCoreApplication.translate("RepoProperties", u"Full repository path :", None))
#if QT_CONFIG(tooltip)
        self.buttonCopyPath.setToolTip(QCoreApplication.translate("RepoProperties", u"Copy full path to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.buttonCopyPath.setText("")
        self.label_4.setText(QCoreApplication.translate("RepoProperties", u" URL :", None))
#if QT_CONFIG(tooltip)
        self.buttonCopyUrl.setToolTip(QCoreApplication.translate("RepoProperties", u"Copy URL to clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.buttonCopyUrl.setText("")
        self.label_5.setText(QCoreApplication.translate("RepoProperties", u"Head :", None))
        self.label_7.setText(QCoreApplication.translate("RepoProperties", u"Status :", None))
        self.label_6.setText(QCoreApplication.translate("RepoProperties", u"Remote Branch :", None))
        self.label_9.setText(QCoreApplication.translate("RepoProperties", u"Remote Synchro :", None))
        self.label_10.setText(QCoreApplication.translate("RepoProperties", u"Tags for this commit :", None))
        self.label_8.setText(QCoreApplication.translate("RepoProperties", u"Last commit :", None))
        self.label_13.setText(QCoreApplication.translate("RepoProperties", u"Diff summary :", None))
    # retranslateUi

