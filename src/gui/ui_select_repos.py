# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_select_repos.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from src.mg_repo_tree import MgRepoTree

class Ui_SelectRepos(object):
    def setupUi(self, SelectRepos: QDialog) -> None:
        if not SelectRepos.objectName():
            SelectRepos.setObjectName(u"SelectRepos")
        SelectRepos.resize(671, 573)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(SelectRepos.sizePolicy().hasHeightForWidth())
        SelectRepos.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(SelectRepos)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(SelectRepos)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout_5.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_7)

        self.label_3 = QLabel(SelectRepos)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label_3)

        self.lineEditFilterList = QLineEdit(SelectRepos)
        self.lineEditFilterList.setObjectName(u"lineEditFilterList")
        self.lineEditFilterList.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.lineEditFilterList)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_8)

        self.labelLineHidden = QLabel(SelectRepos)
        self.labelLineHidden.setObjectName(u"labelLineHidden")
        sizePolicy1.setHeightForWidth(self.labelLineHidden.sizePolicy().hasHeightForWidth())
        self.labelLineHidden.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.labelLineHidden)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.treeWidgetAvailRepos = MgRepoTree(SelectRepos)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidgetAvailRepos.setHeaderItem(__qtreewidgetitem)
        self.treeWidgetAvailRepos.setObjectName(u"treeWidgetAvailRepos")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.treeWidgetAvailRepos.sizePolicy().hasHeightForWidth())
        self.treeWidgetAvailRepos.setSizePolicy(sizePolicy2)
        self.treeWidgetAvailRepos.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidgetAvailRepos.setSortingEnabled(True)
        self.treeWidgetAvailRepos.setAllColumnsShowFocus(True)
        self.treeWidgetAvailRepos.header().setProperty(u"showSortIndicator", True)

        self.horizontalLayout_2.addWidget(self.treeWidgetAvailRepos)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_11)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.pushButtonMoveAllUp = QPushButton(SelectRepos)
        self.pushButtonMoveAllUp.setObjectName(u"pushButtonMoveAllUp")

        self.horizontalLayout_4.addWidget(self.pushButtonMoveAllUp)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.pushButtonMoveUp = QPushButton(SelectRepos)
        self.pushButtonMoveUp.setObjectName(u"pushButtonMoveUp")

        self.horizontalLayout_4.addWidget(self.pushButtonMoveUp)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.pushButtonMoveDown = QPushButton(SelectRepos)
        self.pushButtonMoveDown.setObjectName(u"pushButtonMoveDown")

        self.horizontalLayout_4.addWidget(self.pushButtonMoveDown)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.pushButtonMoveAllDown = QPushButton(SelectRepos)
        self.pushButtonMoveAllDown.setObjectName(u"pushButtonMoveAllDown")

        self.horizontalLayout_4.addWidget(self.pushButtonMoveAllDown)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label_2 = QLabel(SelectRepos)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.treeWidgetSelectedRepos = MgRepoTree(SelectRepos)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.treeWidgetSelectedRepos.setHeaderItem(__qtreewidgetitem1)
        self.treeWidgetSelectedRepos.setObjectName(u"treeWidgetSelectedRepos")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.treeWidgetSelectedRepos.sizePolicy().hasHeightForWidth())
        self.treeWidgetSelectedRepos.setSizePolicy(sizePolicy3)
        self.treeWidgetSelectedRepos.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidgetSelectedRepos.setSortingEnabled(True)
        self.treeWidgetSelectedRepos.setAllColumnsShowFocus(True)
        self.treeWidgetSelectedRepos.header().setProperty(u"showSortIndicator", True)

        self.horizontalLayout_3.addWidget(self.treeWidgetSelectedRepos)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelRepoSelected = QLabel(SelectRepos)
        self.labelRepoSelected.setObjectName(u"labelRepoSelected")

        self.horizontalLayout_6.addWidget(self.labelRepoSelected)

        self.buttonBox = QDialogButtonBox(SelectRepos)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_6.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout_6)


        self.retranslateUi(SelectRepos)
        self.buttonBox.accepted.connect(SelectRepos.accept)
        self.buttonBox.rejected.connect(SelectRepos.reject)

        QMetaObject.connectSlotsByName(SelectRepos)
    # setupUi

    def retranslateUi(self, SelectRepos: QDialog) -> None:
        SelectRepos.setWindowTitle(QCoreApplication.translate("SelectRepos", u"Select repositories", None))
        self.label.setText(QCoreApplication.translate("SelectRepos", u"Available repositories :", None))
        self.label_3.setText(QCoreApplication.translate("SelectRepos", u"Apply filter :", None))
        self.labelLineHidden.setText(QCoreApplication.translate("SelectRepos", u"3 lines hidden", None))
        self.pushButtonMoveAllUp.setText(QCoreApplication.translate("SelectRepos", u"AllDown", None))
        self.pushButtonMoveUp.setText(QCoreApplication.translate("SelectRepos", u"Down", None))
        self.pushButtonMoveDown.setText(QCoreApplication.translate("SelectRepos", u"Up", None))
        self.pushButtonMoveAllDown.setText(QCoreApplication.translate("SelectRepos", u"AllUp", None))
        self.label_2.setText(QCoreApplication.translate("SelectRepos", u"Targeted repositories :", None))
        self.labelRepoSelected.setText(QCoreApplication.translate("SelectRepos", u"TextLabel", None))
    # retranslateUi

