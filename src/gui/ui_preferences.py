# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_preferences.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Preferences(object):
    def setupUi(self, Preferences: QDialog) -> None:
        if not Preferences.objectName():
            Preferences.setObjectName(u"Preferences")
        Preferences.resize(636, 704)
        self.verticalLayout = QVBoxLayout(Preferences)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Preferences)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_ui = QWidget()
        self.tab_ui.setObjectName(u"tab_ui")
        self.verticalLayout_4 = QVBoxLayout(self.tab_ui)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_5 = QGroupBox(self.tab_ui)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setFlat(False)
        self.groupBox_5.setCheckable(False)
        self.gridLayout_3 = QGridLayout(self.groupBox_5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_5 = QLabel(self.groupBox_5)
        self.label_5.setObjectName(u"label_5")
        font1 = QFont()
        font1.setBold(False)
        font1.setWeight(50)
        self.label_5.setFont(font1)

        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)

        self.pushButtonColorBranch = QPushButton(self.groupBox_5)
        self.pushButtonColorBranch.setObjectName(u"pushButtonColorBranch")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonColorBranch.sizePolicy().hasHeightForWidth())
        self.pushButtonColorBranch.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.pushButtonColorBranch, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(254, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)

        self.comboBoxDoubleClickAction = QComboBox(self.groupBox_5)
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.addItem("")
        self.comboBoxDoubleClickAction.setObjectName(u"comboBoxDoubleClickAction")
        sizePolicy1.setHeightForWidth(self.comboBoxDoubleClickAction.sizePolicy().hasHeightForWidth())
        self.comboBoxDoubleClickAction.setSizePolicy(sizePolicy1)
        self.comboBoxDoubleClickAction.setFont(font1)

        self.gridLayout_3.addWidget(self.comboBoxDoubleClickAction, 0, 1, 1, 1)

        self.pushButtonColorTag = QPushButton(self.groupBox_5)
        self.pushButtonColorTag.setObjectName(u"pushButtonColorTag")

        self.gridLayout_3.addWidget(self.pushButtonColorTag, 2, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(81, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(254, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_5)

        self.widget_2 = QWidget(self.tab_ui)
        self.widget_2.setObjectName(u"widget_2")

        self.verticalLayout_4.addWidget(self.widget_2)

        self.groupBox_7 = QGroupBox(self.tab_ui)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radioButtonGitProcUnlimited = QRadioButton(self.groupBox_7)
        self.radioButtonGitProcUnlimited.setObjectName(u"radioButtonGitProcUnlimited")
        self.radioButtonGitProcUnlimited.setFont(font1)
        self.radioButtonGitProcUnlimited.setChecked(True)

        self.verticalLayout_2.addWidget(self.radioButtonGitProcUnlimited)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButtonGitProcLimit = QRadioButton(self.groupBox_7)
        self.radioButtonGitProcLimit.setObjectName(u"radioButtonGitProcLimit")
        self.radioButtonGitProcLimit.setFont(font1)

        self.horizontalLayout_2.addWidget(self.radioButtonGitProcLimit)

        self.spinBoxLimitValue = QSpinBox(self.groupBox_7)
        self.spinBoxLimitValue.setObjectName(u"spinBoxLimitValue")
        self.spinBoxLimitValue.setEnabled(False)
        self.spinBoxLimitValue.setFont(font1)
        self.spinBoxLimitValue.setMinimum(1)
        self.spinBoxLimitValue.setValue(10)

        self.horizontalLayout_2.addWidget(self.spinBoxLimitValue)

        self.widget = QWidget(self.groupBox_7)
        self.widget.setObjectName(u"widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.widget)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_4.addWidget(self.groupBox_7)

        self.widget_3 = QWidget(self.tab_ui)
        self.widget_3.setObjectName(u"widget_3")

        self.verticalLayout_4.addWidget(self.widget_3)

        self.groupBox_6 = QGroupBox(self.tab_ui)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setFont(font)
        self.horizontalLayout = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_10 = QLabel(self.groupBox_6)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)

        self.horizontalLayout.addWidget(self.label_10)

        self.comboUpdateFrequency = QComboBox(self.groupBox_6)
        self.comboUpdateFrequency.addItem("")
        self.comboUpdateFrequency.addItem("")
        self.comboUpdateFrequency.addItem("")
        self.comboUpdateFrequency.addItem("")
        self.comboUpdateFrequency.setObjectName(u"comboUpdateFrequency")
        self.comboUpdateFrequency.setFont(font1)

        self.horizontalLayout.addWidget(self.comboUpdateFrequency)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.groupBox_8 = QGroupBox(self.tab_ui)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.checkBoxFetchOnStartup = QCheckBox(self.groupBox_8)
        self.checkBoxFetchOnStartup.setObjectName(u"checkBoxFetchOnStartup")
        self.checkBoxFetchOnStartup.setFont(font1)

        self.verticalLayout_5.addWidget(self.checkBoxFetchOnStartup)


        self.verticalLayout_4.addWidget(self.groupBox_8)

        self.verticalSpacer_2 = QSpacerItem(20, 17, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.verticalSpacer_4 = QSpacerItem(20, 18, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        self.tabWidget.addTab(self.tab_ui, "")
        self.tab_extprogs = QWidget()
        self.tab_extprogs.setObjectName(u"tab_extprogs")
        self.verticalLayout_3 = QVBoxLayout(self.tab_extprogs)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.tab_extprogs)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.radioGitManual = QRadioButton(self.groupBox)
        self.radioGitManual.setObjectName(u"radioGitManual")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.radioGitManual.sizePolicy().hasHeightForWidth())
        self.radioGitManual.setSizePolicy(sizePolicy3)
        self.radioGitManual.setFont(font1)

        self.gridLayout.addWidget(self.radioGitManual, 2, 0, 1, 1)

        self.radioGitAutoDetect = QRadioButton(self.groupBox)
        self.radioGitAutoDetect.setObjectName(u"radioGitAutoDetect")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.radioGitAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioGitAutoDetect.setSizePolicy(sizePolicy4)
        self.radioGitAutoDetect.setFont(font1)

        self.gridLayout.addWidget(self.radioGitAutoDetect, 1, 0, 1, 1)

        self.lineEditGitManual = QLineEdit(self.groupBox)
        self.lineEditGitManual.setObjectName(u"lineEditGitManual")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(10)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lineEditGitManual.sizePolicy().hasHeightForWidth())
        self.lineEditGitManual.setSizePolicy(sizePolicy5)
        self.lineEditGitManual.setFont(font1)

        self.gridLayout.addWidget(self.lineEditGitManual, 2, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.lineEditGitAutoDetect = QLineEdit(self.groupBox)
        self.lineEditGitAutoDetect.setObjectName(u"lineEditGitAutoDetect")
        self.lineEditGitAutoDetect.setEnabled(False)
        sizePolicy5.setHeightForWidth(self.lineEditGitAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditGitAutoDetect.setSizePolicy(sizePolicy5)
        self.lineEditGitAutoDetect.setFont(font1)
        self.lineEditGitAutoDetect.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditGitAutoDetect, 1, 1, 1, 1)

        self.pushButtonGitManualBrowse = QPushButton(self.groupBox)
        self.pushButtonGitManualBrowse.setObjectName(u"pushButtonGitManualBrowse")
        sizePolicy4.setHeightForWidth(self.pushButtonGitManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonGitManualBrowse.setSizePolicy(sizePolicy4)
        self.pushButtonGitManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonGitManualBrowse.setFont(font1)

        self.gridLayout.addWidget(self.pushButtonGitManualBrowse, 2, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_extprogs)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.radioTGitManual = QRadioButton(self.groupBox_2)
        self.radioTGitManual.setObjectName(u"radioTGitManual")
        sizePolicy3.setHeightForWidth(self.radioTGitManual.sizePolicy().hasHeightForWidth())
        self.radioTGitManual.setSizePolicy(sizePolicy3)
        self.radioTGitManual.setFont(font1)

        self.gridLayout_2.addWidget(self.radioTGitManual, 6, 0, 1, 1)

        self.radioTGitAutoDetect = QRadioButton(self.groupBox_2)
        self.radioTGitAutoDetect.setObjectName(u"radioTGitAutoDetect")
        sizePolicy3.setHeightForWidth(self.radioTGitAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioTGitAutoDetect.setSizePolicy(sizePolicy3)
        self.radioTGitAutoDetect.setFont(font1)

        self.gridLayout_2.addWidget(self.radioTGitAutoDetect, 5, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 3, 0, 1, 1)

        self.lineEditTGitManual = QLineEdit(self.groupBox_2)
        self.lineEditTGitManual.setObjectName(u"lineEditTGitManual")
        sizePolicy5.setHeightForWidth(self.lineEditTGitManual.sizePolicy().hasHeightForWidth())
        self.lineEditTGitManual.setSizePolicy(sizePolicy5)
        self.lineEditTGitManual.setFont(font1)

        self.gridLayout_2.addWidget(self.lineEditTGitManual, 6, 1, 1, 1)

        self.pushButtonTGitManualBrowse = QPushButton(self.groupBox_2)
        self.pushButtonTGitManualBrowse.setObjectName(u"pushButtonTGitManualBrowse")
        sizePolicy4.setHeightForWidth(self.pushButtonTGitManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonTGitManualBrowse.setSizePolicy(sizePolicy4)
        self.pushButtonTGitManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonTGitManualBrowse.setFont(font1)

        self.gridLayout_2.addWidget(self.pushButtonTGitManualBrowse, 6, 2, 1, 1)

        self.lineEditTGitAutoDetect = QLineEdit(self.groupBox_2)
        self.lineEditTGitAutoDetect.setObjectName(u"lineEditTGitAutoDetect")
        self.lineEditTGitAutoDetect.setEnabled(False)
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.lineEditTGitAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditTGitAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditTGitAutoDetect.setFont(font1)
        self.lineEditTGitAutoDetect.setReadOnly(True)

        self.gridLayout_2.addWidget(self.lineEditTGitAutoDetect, 5, 1, 1, 1)

        self.checkBoxTortoiseGit = QCheckBox(self.groupBox_2)
        self.checkBoxTortoiseGit.setObjectName(u"checkBoxTortoiseGit")
        self.checkBoxTortoiseGit.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBoxTortoiseGit, 2, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.tab_extprogs)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setCheckable(False)
        self.gridLayout_4_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_4_2.setObjectName(u"gridLayout_4_2")
        self.lineEditSourcetreeManual = QLineEdit(self.groupBox_3)
        self.lineEditSourcetreeManual.setObjectName(u"lineEditSourcetreeManual")
        sizePolicy5.setHeightForWidth(self.lineEditSourcetreeManual.sizePolicy().hasHeightForWidth())
        self.lineEditSourcetreeManual.setSizePolicy(sizePolicy5)
        self.lineEditSourcetreeManual.setFont(font1)

        self.gridLayout_4_2.addWidget(self.lineEditSourcetreeManual, 6, 1, 1, 1)

        self.radioSourcetreeManual = QRadioButton(self.groupBox_3)
        self.radioSourcetreeManual.setObjectName(u"radioSourcetreeManual")
        sizePolicy3.setHeightForWidth(self.radioSourcetreeManual.sizePolicy().hasHeightForWidth())
        self.radioSourcetreeManual.setSizePolicy(sizePolicy3)
        self.radioSourcetreeManual.setFont(font1)

        self.gridLayout_4_2.addWidget(self.radioSourcetreeManual, 6, 0, 1, 1)

        self.pushButtonSourcetreeManualBrowse = QPushButton(self.groupBox_3)
        self.pushButtonSourcetreeManualBrowse.setObjectName(u"pushButtonSourcetreeManualBrowse")
        sizePolicy4.setHeightForWidth(self.pushButtonSourcetreeManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonSourcetreeManualBrowse.setSizePolicy(sizePolicy4)
        self.pushButtonSourcetreeManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonSourcetreeManualBrowse.setFont(font1)

        self.gridLayout_4_2.addWidget(self.pushButtonSourcetreeManualBrowse, 6, 2, 1, 1)

        self.radioSourcetreeAutoDetect = QRadioButton(self.groupBox_3)
        self.radioSourcetreeAutoDetect.setObjectName(u"radioSourcetreeAutoDetect")
        sizePolicy3.setHeightForWidth(self.radioSourcetreeAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioSourcetreeAutoDetect.setSizePolicy(sizePolicy3)
        self.radioSourcetreeAutoDetect.setFont(font1)

        self.gridLayout_4_2.addWidget(self.radioSourcetreeAutoDetect, 5, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.gridLayout_4_2.addWidget(self.label_4, 4, 0, 1, 1)

        self.lineEditSourcetreeAutoDetect = QLineEdit(self.groupBox_3)
        self.lineEditSourcetreeAutoDetect.setObjectName(u"lineEditSourcetreeAutoDetect")
        self.lineEditSourcetreeAutoDetect.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.lineEditSourcetreeAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditSourcetreeAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditSourcetreeAutoDetect.setFont(font1)
        self.lineEditSourcetreeAutoDetect.setReadOnly(True)

        self.gridLayout_4_2.addWidget(self.lineEditSourcetreeAutoDetect, 5, 1, 1, 1)

        self.checkBoxSourceTree = QCheckBox(self.groupBox_3)
        self.checkBoxSourceTree.setObjectName(u"checkBoxSourceTree")
        self.checkBoxSourceTree.setFont(font1)

        self.gridLayout_4_2.addWidget(self.checkBoxSourceTree, 2, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_4_2.addWidget(self.label_7, 3, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.tab_extprogs)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setFlat(False)
        self.groupBox_4.setCheckable(False)
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButtonSublimemergeManualBrowse = QPushButton(self.groupBox_4)
        self.pushButtonSublimemergeManualBrowse.setObjectName(u"pushButtonSublimemergeManualBrowse")
        sizePolicy4.setHeightForWidth(self.pushButtonSublimemergeManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonSublimemergeManualBrowse.setSizePolicy(sizePolicy4)
        self.pushButtonSublimemergeManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonSublimemergeManualBrowse.setFont(font1)

        self.gridLayout_4.addWidget(self.pushButtonSublimemergeManualBrowse, 4, 2, 1, 1)

        self.radioSublimemergeAutoDetect = QRadioButton(self.groupBox_4)
        self.radioSublimemergeAutoDetect.setObjectName(u"radioSublimemergeAutoDetect")
        sizePolicy3.setHeightForWidth(self.radioSublimemergeAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioSublimemergeAutoDetect.setSizePolicy(sizePolicy3)
        self.radioSublimemergeAutoDetect.setFont(font1)

        self.gridLayout_4.addWidget(self.radioSublimemergeAutoDetect, 3, 0, 1, 1)

        self.radioSublimemergeManual = QRadioButton(self.groupBox_4)
        self.radioSublimemergeManual.setObjectName(u"radioSublimemergeManual")
        sizePolicy3.setHeightForWidth(self.radioSublimemergeManual.sizePolicy().hasHeightForWidth())
        self.radioSublimemergeManual.setSizePolicy(sizePolicy3)
        self.radioSublimemergeManual.setFont(font1)

        self.gridLayout_4.addWidget(self.radioSublimemergeManual, 4, 0, 1, 1)

        self.lineEditSublimemergeAutoDetect = QLineEdit(self.groupBox_4)
        self.lineEditSublimemergeAutoDetect.setObjectName(u"lineEditSublimemergeAutoDetect")
        self.lineEditSublimemergeAutoDetect.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.lineEditSublimemergeAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditSublimemergeAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditSublimemergeAutoDetect.setFont(font1)
        self.lineEditSublimemergeAutoDetect.setReadOnly(True)

        self.gridLayout_4.addWidget(self.lineEditSublimemergeAutoDetect, 3, 1, 1, 1)

        self.lineEditSublimemergeManual = QLineEdit(self.groupBox_4)
        self.lineEditSublimemergeManual.setObjectName(u"lineEditSublimemergeManual")
        sizePolicy5.setHeightForWidth(self.lineEditSublimemergeManual.sizePolicy().hasHeightForWidth())
        self.lineEditSublimemergeManual.setSizePolicy(sizePolicy5)
        self.lineEditSublimemergeManual.setFont(font1)

        self.gridLayout_4.addWidget(self.lineEditSublimemergeManual, 4, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_4_2 = QLabel(self.groupBox_4)
        self.label_4_2.setObjectName(u"label_4_2")
        self.label_4_2.setFont(font1)

        self.gridLayout_4.addWidget(self.label_4_2, 2, 0, 1, 1)

        self.checkBoxSublimeMerge = QCheckBox(self.groupBox_4)
        self.checkBoxSublimeMerge.setObjectName(u"checkBoxSublimeMerge")
        self.checkBoxSublimeMerge.setFont(font1)

        self.gridLayout_4.addWidget(self.checkBoxSublimeMerge, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.verticalSpacer = QSpacerItem(20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_extprogs, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(Preferences)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.radioGitAutoDetect)
        self.label_2.setBuddy(self.radioTGitAutoDetect)
        self.label_4.setBuddy(self.radioSourcetreeAutoDetect)
        self.label_4_2.setBuddy(self.radioSublimemergeAutoDetect)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.tabWidget, self.comboBoxDoubleClickAction)
        QWidget.setTabOrder(self.comboBoxDoubleClickAction, self.pushButtonColorBranch)
        QWidget.setTabOrder(self.pushButtonColorBranch, self.pushButtonColorTag)
        QWidget.setTabOrder(self.pushButtonColorTag, self.radioButtonGitProcUnlimited)
        QWidget.setTabOrder(self.radioButtonGitProcUnlimited, self.radioButtonGitProcLimit)
        QWidget.setTabOrder(self.radioButtonGitProcLimit, self.spinBoxLimitValue)
        QWidget.setTabOrder(self.spinBoxLimitValue, self.comboUpdateFrequency)
        QWidget.setTabOrder(self.comboUpdateFrequency, self.checkBoxFetchOnStartup)
        QWidget.setTabOrder(self.checkBoxFetchOnStartup, self.lineEditGitAutoDetect)
        QWidget.setTabOrder(self.lineEditGitAutoDetect, self.radioGitAutoDetect)
        QWidget.setTabOrder(self.radioGitAutoDetect, self.radioGitManual)
        QWidget.setTabOrder(self.radioGitManual, self.lineEditGitManual)
        QWidget.setTabOrder(self.lineEditGitManual, self.pushButtonGitManualBrowse)
        QWidget.setTabOrder(self.pushButtonGitManualBrowse, self.checkBoxTortoiseGit)
        QWidget.setTabOrder(self.checkBoxTortoiseGit, self.radioTGitAutoDetect)
        QWidget.setTabOrder(self.radioTGitAutoDetect, self.lineEditTGitAutoDetect)
        QWidget.setTabOrder(self.lineEditTGitAutoDetect, self.radioTGitManual)
        QWidget.setTabOrder(self.radioTGitManual, self.lineEditTGitManual)
        QWidget.setTabOrder(self.lineEditTGitManual, self.pushButtonTGitManualBrowse)
        QWidget.setTabOrder(self.pushButtonTGitManualBrowse, self.checkBoxSourceTree)
        QWidget.setTabOrder(self.checkBoxSourceTree, self.radioSourcetreeAutoDetect)
        QWidget.setTabOrder(self.radioSourcetreeAutoDetect, self.lineEditSourcetreeAutoDetect)
        QWidget.setTabOrder(self.lineEditSourcetreeAutoDetect, self.radioSourcetreeManual)
        QWidget.setTabOrder(self.radioSourcetreeManual, self.lineEditSourcetreeManual)
        QWidget.setTabOrder(self.lineEditSourcetreeManual, self.pushButtonSourcetreeManualBrowse)
        QWidget.setTabOrder(self.pushButtonSourcetreeManualBrowse, self.checkBoxSublimeMerge)
        QWidget.setTabOrder(self.checkBoxSublimeMerge, self.radioSublimemergeAutoDetect)
        QWidget.setTabOrder(self.radioSublimemergeAutoDetect, self.lineEditSublimemergeAutoDetect)
        QWidget.setTabOrder(self.lineEditSublimemergeAutoDetect, self.radioSublimemergeManual)
        QWidget.setTabOrder(self.radioSublimemergeManual, self.lineEditSublimemergeManual)
        QWidget.setTabOrder(self.lineEditSublimemergeManual, self.pushButtonSublimemergeManualBrowse)

        self.retranslateUi(Preferences)
        self.radioGitManual.toggled.connect(self.pushButtonGitManualBrowse.setEnabled)
        self.radioTGitManual.toggled.connect(self.pushButtonTGitManualBrowse.setEnabled)
        self.radioGitManual.toggled.connect(self.lineEditGitManual.setEnabled)
        self.radioTGitManual.toggled.connect(self.lineEditTGitManual.setEnabled)
        self.radioSourcetreeManual.toggled.connect(self.lineEditSourcetreeManual.setEnabled)
        self.radioSourcetreeManual.toggled.connect(self.pushButtonSourcetreeManualBrowse.setEnabled)
        self.radioSublimemergeManual.toggled.connect(self.lineEditSublimemergeManual.setEnabled)
        self.radioSublimemergeManual.toggled.connect(self.pushButtonSublimemergeManualBrowse.setEnabled)
        self.buttonBox.accepted.connect(Preferences.accept)
        self.buttonBox.rejected.connect(Preferences.reject)
        self.checkBoxSourceTree.toggled.connect(self.radioSourcetreeAutoDetect.setEnabled)
        self.checkBoxSourceTree.toggled.connect(self.radioSourcetreeManual.setEnabled)
        self.checkBoxSourceTree.toggled.connect(self.lineEditSourcetreeManual.setEnabled)
        self.checkBoxSourceTree.toggled.connect(self.pushButtonSourcetreeManualBrowse.setEnabled)
        self.checkBoxSourceTree.toggled.connect(self.label_4.setEnabled)
        self.checkBoxSublimeMerge.toggled.connect(self.label_4_2.setEnabled)
        self.checkBoxSublimeMerge.toggled.connect(self.radioSublimemergeAutoDetect.setEnabled)
        self.checkBoxSublimeMerge.toggled.connect(self.radioSublimemergeManual.setEnabled)
        self.checkBoxSublimeMerge.toggled.connect(self.lineEditSublimemergeManual.setEnabled)
        self.checkBoxSublimeMerge.toggled.connect(self.pushButtonSublimemergeManualBrowse.setEnabled)
        self.checkBoxTortoiseGit.toggled.connect(self.label_2.setEnabled)
        self.checkBoxTortoiseGit.toggled.connect(self.radioTGitAutoDetect.setEnabled)
        self.checkBoxTortoiseGit.toggled.connect(self.radioTGitManual.setEnabled)
        self.checkBoxTortoiseGit.toggled.connect(self.lineEditTGitManual.setEnabled)
        self.checkBoxTortoiseGit.toggled.connect(self.pushButtonTGitManualBrowse.setEnabled)
        self.radioButtonGitProcUnlimited.toggled.connect(self.spinBoxLimitValue.setDisabled)
        self.radioButtonGitProcLimit.toggled.connect(self.spinBoxLimitValue.setEnabled)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Preferences)
    # setupUi

    def retranslateUi(self, Preferences: QDialog) -> None:
        Preferences.setWindowTitle(QCoreApplication.translate("Preferences", u"MultiGit Preferences", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Preferences", u"User Interface", None))
        self.label_5.setText(QCoreApplication.translate("Preferences", u"Color for HEAD on branch", None))
        self.pushButtonColorBranch.setText("")
        self.comboBoxDoubleClickAction.setItemText(0, QCoreApplication.translate("Preferences", u"(not set)", None))
        self.comboBoxDoubleClickAction.setItemText(1, QCoreApplication.translate("Preferences", u"Git Push", None))
        self.comboBoxDoubleClickAction.setItemText(2, QCoreApplication.translate("Preferences", u"Git Pull", None))
        self.comboBoxDoubleClickAction.setItemText(3, QCoreApplication.translate("Preferences", u"Git Fetch", None))
        self.comboBoxDoubleClickAction.setItemText(4, QCoreApplication.translate("Preferences", u"TortoiseGit ShowLog", None))
        self.comboBoxDoubleClickAction.setItemText(5, QCoreApplication.translate("Preferences", u"TortoiseGit Commit", None))
        self.comboBoxDoubleClickAction.setItemText(6, QCoreApplication.translate("Preferences", u"TortoiseGit Diff", None))
        self.comboBoxDoubleClickAction.setItemText(7, QCoreApplication.translate("Preferences", u"TortoiseGit Push", None))
        self.comboBoxDoubleClickAction.setItemText(8, QCoreApplication.translate("Preferences", u"TortoiseGit Pull", None))
        self.comboBoxDoubleClickAction.setItemText(9, QCoreApplication.translate("Preferences", u"TortoiseGit Fetch", None))
        self.comboBoxDoubleClickAction.setItemText(10, QCoreApplication.translate("Preferences", u"Run SourceTree", None))
        self.comboBoxDoubleClickAction.setItemText(11, QCoreApplication.translate("Preferences", u"Run SublimeMerge", None))
        self.comboBoxDoubleClickAction.setItemText(12, QCoreApplication.translate("Preferences", u"View repository properties", None))
        self.comboBoxDoubleClickAction.setItemText(13, QCoreApplication.translate("Preferences", u"Show in Explorer", None))
        self.comboBoxDoubleClickAction.setItemText(14, QCoreApplication.translate("Preferences", u"Do nothing", None))

        self.pushButtonColorTag.setText("")
        self.label_3.setText(QCoreApplication.translate("Preferences", u"Action for double-click on repository", None))
        self.label_6.setText(QCoreApplication.translate("Preferences", u"Color for HEAD on tag", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Preferences", u"Number of parallel git processes", None))
        self.radioButtonGitProcUnlimited.setText(QCoreApplication.translate("Preferences", u"Unlimited", None))
        self.radioButtonGitProcLimit.setText(QCoreApplication.translate("Preferences", u"Limit number to :", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Preferences", u"MultiGit Updates", None))
        self.label_10.setText(QCoreApplication.translate("Preferences", u"Check fo MultiGit new versions : ", None))
        self.comboUpdateFrequency.setItemText(0, QCoreApplication.translate("Preferences", u"every day", None))
        self.comboUpdateFrequency.setItemText(1, QCoreApplication.translate("Preferences", u"every week", None))
        self.comboUpdateFrequency.setItemText(2, QCoreApplication.translate("Preferences", u"every month", None))
        self.comboUpdateFrequency.setItemText(3, QCoreApplication.translate("Preferences", u"never", None))

        self.groupBox_8.setTitle(QCoreApplication.translate("Preferences", u"Startup behavior", None))
        self.checkBoxFetchOnStartup.setText(QCoreApplication.translate("Preferences", u"Fetch all repositories when starting Multigit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ui), QCoreApplication.translate("Preferences", u"Behavior", None))
        self.groupBox.setTitle(QCoreApplication.translate("Preferences", u"Git executable", None))
        self.radioGitManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.radioGitAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.label.setText(QCoreApplication.translate("Preferences", u"Choose git.exe executable location :", None))
        self.pushButtonGitManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Preferences", u"TortoiseGit", None))
        self.radioTGitManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.radioTGitAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.label_2.setText(QCoreApplication.translate("Preferences", u"Choose TortoiseGitProc.exe executable location :", None))
        self.label_9.setText("")
        self.pushButtonTGitManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.checkBoxTortoiseGit.setText(QCoreApplication.translate("Preferences", u"Activate TortoiseGit in the Git Program menu", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Preferences", u"SourceTree", None))
        self.radioSourcetreeManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.pushButtonSourcetreeManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.radioSourcetreeAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.label_4.setText(QCoreApplication.translate("Preferences", u"Choose SourceTree.exe executable location :", None))
        self.checkBoxSourceTree.setText(QCoreApplication.translate("Preferences", u"Activate SourceTree in the Git Program menu", None))
        self.label_7.setText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("Preferences", u"SublimeMerge", None))
        self.pushButtonSublimemergeManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.radioSublimemergeAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.radioSublimemergeManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.label_8.setText("")
        self.label_4_2.setText(QCoreApplication.translate("Preferences", u"Choose sublime_merge.exe executable location :", None))
        self.checkBoxSublimeMerge.setText(QCoreApplication.translate("Preferences", u"Activate SublimeMerge  in the Git Program menu", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_extprogs), QCoreApplication.translate("Preferences", u"External Programs", None))
    # retranslateUi

