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
        Preferences.resize(862, 767)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxDoubleClickAction.sizePolicy().hasHeightForWidth())
        self.comboBoxDoubleClickAction.setSizePolicy(sizePolicy2)
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

        self.horizontalSpacer_3 = QSpacerItem(254, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

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
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)

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
        self.gridLayout_10 = QGridLayout(self.tab_extprogs)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.groupBoxSublimemerge = QGroupBox(self.tab_extprogs)
        self.groupBoxSublimemerge.setObjectName(u"groupBoxSublimemerge")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.groupBoxSublimemerge.sizePolicy().hasHeightForWidth())
        self.groupBoxSublimemerge.setSizePolicy(sizePolicy4)
        self.groupBoxSublimemerge.setFont(font)
        self.groupBoxSublimemerge.setFlat(False)
        self.groupBoxSublimemerge.setCheckable(False)
        self.gridLayout_4 = QGridLayout(self.groupBoxSublimemerge)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.checkBoxSublimeMerge = QCheckBox(self.groupBoxSublimemerge)
        self.checkBoxSublimeMerge.setObjectName(u"checkBoxSublimeMerge")
        self.checkBoxSublimeMerge.setFont(font1)

        self.gridLayout_4.addWidget(self.checkBoxSublimeMerge, 0, 0, 1, 2)

        self.label_8 = QLabel(self.groupBoxSublimemerge)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)

        self.labelExecSublimemergeChoose = QLabel(self.groupBoxSublimemerge)
        self.labelExecSublimemergeChoose.setObjectName(u"labelExecSublimemergeChoose")
        self.labelExecSublimemergeChoose.setFont(font1)

        self.gridLayout_4.addWidget(self.labelExecSublimemergeChoose, 2, 0, 1, 2)

        self.radioSublimemergeAutoDetect = QRadioButton(self.groupBoxSublimemerge)
        self.radioSublimemergeAutoDetect.setObjectName(u"radioSublimemergeAutoDetect")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.radioSublimemergeAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioSublimemergeAutoDetect.setSizePolicy(sizePolicy5)
        self.radioSublimemergeAutoDetect.setFont(font1)

        self.gridLayout_4.addWidget(self.radioSublimemergeAutoDetect, 3, 0, 1, 1)

        self.lineEditSublimemergeAutoDetect = QLineEdit(self.groupBoxSublimemerge)
        self.lineEditSublimemergeAutoDetect.setObjectName(u"lineEditSublimemergeAutoDetect")
        self.lineEditSublimemergeAutoDetect.setEnabled(False)
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.lineEditSublimemergeAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditSublimemergeAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditSublimemergeAutoDetect.setFont(font1)
        self.lineEditSublimemergeAutoDetect.setReadOnly(True)

        self.gridLayout_4.addWidget(self.lineEditSublimemergeAutoDetect, 3, 1, 1, 1)

        self.radioSublimemergeManual = QRadioButton(self.groupBoxSublimemerge)
        self.radioSublimemergeManual.setObjectName(u"radioSublimemergeManual")
        sizePolicy5.setHeightForWidth(self.radioSublimemergeManual.sizePolicy().hasHeightForWidth())
        self.radioSublimemergeManual.setSizePolicy(sizePolicy5)
        self.radioSublimemergeManual.setFont(font1)

        self.gridLayout_4.addWidget(self.radioSublimemergeManual, 4, 0, 1, 1)

        self.lineEditSublimemergeManual = QLineEdit(self.groupBoxSublimemerge)
        self.lineEditSublimemergeManual.setObjectName(u"lineEditSublimemergeManual")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(10)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.lineEditSublimemergeManual.sizePolicy().hasHeightForWidth())
        self.lineEditSublimemergeManual.setSizePolicy(sizePolicy7)
        self.lineEditSublimemergeManual.setFont(font1)

        self.gridLayout_4.addWidget(self.lineEditSublimemergeManual, 4, 1, 1, 1)

        self.pushButtonSublimemergeManualBrowse = QPushButton(self.groupBoxSublimemerge)
        self.pushButtonSublimemergeManualBrowse.setObjectName(u"pushButtonSublimemergeManualBrowse")
        sizePolicy8 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(1)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.pushButtonSublimemergeManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonSublimemergeManualBrowse.setSizePolicy(sizePolicy8)
        self.pushButtonSublimemergeManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonSublimemergeManualBrowse.setFont(font1)

        self.gridLayout_4.addWidget(self.pushButtonSublimemergeManualBrowse, 4, 2, 1, 1)


        self.gridLayout_10.addWidget(self.groupBoxSublimemerge, 2, 0, 1, 1)

        self.groupBoxGitGui = QGroupBox(self.tab_extprogs)
        self.groupBoxGitGui.setObjectName(u"groupBoxGitGui")
        sizePolicy4.setHeightForWidth(self.groupBoxGitGui.sizePolicy().hasHeightForWidth())
        self.groupBoxGitGui.setSizePolicy(sizePolicy4)
        self.groupBoxGitGui.setFont(font)
        self.groupBoxGitGui.setFlat(False)
        self.groupBoxGitGui.setCheckable(False)
        self.gridLayout_9 = QGridLayout(self.groupBoxGitGui)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.pushButtonGitGuiManualBrowse = QPushButton(self.groupBoxGitGui)
        self.pushButtonGitGuiManualBrowse.setObjectName(u"pushButtonGitGuiManualBrowse")
        sizePolicy8.setHeightForWidth(self.pushButtonGitGuiManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonGitGuiManualBrowse.setSizePolicy(sizePolicy8)
        self.pushButtonGitGuiManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonGitGuiManualBrowse.setFont(font1)

        self.gridLayout_9.addWidget(self.pushButtonGitGuiManualBrowse, 4, 2, 1, 1)

        self.radioGitGuiAutoDetect = QRadioButton(self.groupBoxGitGui)
        self.radioGitGuiAutoDetect.setObjectName(u"radioGitGuiAutoDetect")
        sizePolicy5.setHeightForWidth(self.radioGitGuiAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioGitGuiAutoDetect.setSizePolicy(sizePolicy5)
        self.radioGitGuiAutoDetect.setFont(font1)

        self.gridLayout_9.addWidget(self.radioGitGuiAutoDetect, 3, 0, 1, 1)

        self.label_15 = QLabel(self.groupBoxGitGui)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_9.addWidget(self.label_15, 1, 0, 1, 3)

        self.lineEditGitGuiManual = QLineEdit(self.groupBoxGitGui)
        self.lineEditGitGuiManual.setObjectName(u"lineEditGitGuiManual")
        sizePolicy7.setHeightForWidth(self.lineEditGitGuiManual.sizePolicy().hasHeightForWidth())
        self.lineEditGitGuiManual.setSizePolicy(sizePolicy7)
        self.lineEditGitGuiManual.setFont(font1)

        self.gridLayout_9.addWidget(self.lineEditGitGuiManual, 4, 1, 1, 1)

        self.checkBoxGitGui = QCheckBox(self.groupBoxGitGui)
        self.checkBoxGitGui.setObjectName(u"checkBoxGitGui")
        self.checkBoxGitGui.setFont(font1)

        self.gridLayout_9.addWidget(self.checkBoxGitGui, 0, 0, 1, 2)

        self.radioGitGuiManual = QRadioButton(self.groupBoxGitGui)
        self.radioGitGuiManual.setObjectName(u"radioGitGuiManual")
        sizePolicy5.setHeightForWidth(self.radioGitGuiManual.sizePolicy().hasHeightForWidth())
        self.radioGitGuiManual.setSizePolicy(sizePolicy5)
        self.radioGitGuiManual.setFont(font1)

        self.gridLayout_9.addWidget(self.radioGitGuiManual, 4, 0, 1, 1)

        self.lineEditGitGuiAutoDetect = QLineEdit(self.groupBoxGitGui)
        self.lineEditGitGuiAutoDetect.setObjectName(u"lineEditGitGuiAutoDetect")
        self.lineEditGitGuiAutoDetect.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.lineEditGitGuiAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditGitGuiAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditGitGuiAutoDetect.setFont(font1)
        self.lineEditGitGuiAutoDetect.setReadOnly(True)

        self.gridLayout_9.addWidget(self.lineEditGitGuiAutoDetect, 3, 1, 1, 1)

        self.label_16 = QLabel(self.groupBoxGitGui)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font1)

        self.gridLayout_9.addWidget(self.label_16, 2, 0, 1, 2)


        self.gridLayout_10.addWidget(self.groupBoxGitGui, 1, 0, 1, 1)

        self.groupBoxGitK = QGroupBox(self.tab_extprogs)
        self.groupBoxGitK.setObjectName(u"groupBoxGitK")
        sizePolicy4.setHeightForWidth(self.groupBoxGitK.sizePolicy().hasHeightForWidth())
        self.groupBoxGitK.setSizePolicy(sizePolicy4)
        self.groupBoxGitK.setFont(font)
        self.groupBoxGitK.setFlat(False)
        self.groupBoxGitK.setCheckable(False)
        self.gridLayout_7 = QGridLayout(self.groupBoxGitK)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.radioGitKManual = QRadioButton(self.groupBoxGitK)
        self.radioGitKManual.setObjectName(u"radioGitKManual")
        sizePolicy5.setHeightForWidth(self.radioGitKManual.sizePolicy().hasHeightForWidth())
        self.radioGitKManual.setSizePolicy(sizePolicy5)
        self.radioGitKManual.setFont(font1)

        self.gridLayout_7.addWidget(self.radioGitKManual, 4, 0, 1, 1)

        self.radioGitKAutoDetect = QRadioButton(self.groupBoxGitK)
        self.radioGitKAutoDetect.setObjectName(u"radioGitKAutoDetect")
        sizePolicy5.setHeightForWidth(self.radioGitKAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioGitKAutoDetect.setSizePolicy(sizePolicy5)
        self.radioGitKAutoDetect.setFont(font1)

        self.gridLayout_7.addWidget(self.radioGitKAutoDetect, 3, 0, 1, 1)

        self.checkBoxGitK = QCheckBox(self.groupBoxGitK)
        self.checkBoxGitK.setObjectName(u"checkBoxGitK")
        self.checkBoxGitK.setFont(font1)

        self.gridLayout_7.addWidget(self.checkBoxGitK, 0, 0, 1, 2)

        self.pushButtonGitKManualBrowse = QPushButton(self.groupBoxGitK)
        self.pushButtonGitKManualBrowse.setObjectName(u"pushButtonGitKManualBrowse")
        sizePolicy8.setHeightForWidth(self.pushButtonGitKManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonGitKManualBrowse.setSizePolicy(sizePolicy8)
        self.pushButtonGitKManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonGitKManualBrowse.setFont(font1)

        self.gridLayout_7.addWidget(self.pushButtonGitKManualBrowse, 4, 2, 1, 1)

        self.lineEditGitKManual = QLineEdit(self.groupBoxGitK)
        self.lineEditGitKManual.setObjectName(u"lineEditGitKManual")
        sizePolicy7.setHeightForWidth(self.lineEditGitKManual.sizePolicy().hasHeightForWidth())
        self.lineEditGitKManual.setSizePolicy(sizePolicy7)
        self.lineEditGitKManual.setFont(font1)

        self.gridLayout_7.addWidget(self.lineEditGitKManual, 4, 1, 1, 1)

        self.lineEditGitKAutoDetect = QLineEdit(self.groupBoxGitK)
        self.lineEditGitKAutoDetect.setObjectName(u"lineEditGitKAutoDetect")
        self.lineEditGitKAutoDetect.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.lineEditGitKAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditGitKAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditGitKAutoDetect.setFont(font1)
        self.lineEditGitKAutoDetect.setReadOnly(True)

        self.gridLayout_7.addWidget(self.lineEditGitKAutoDetect, 3, 1, 1, 1)

        self.label_17 = QLabel(self.groupBoxGitK)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_7.addWidget(self.label_17, 1, 0, 1, 1)

        self.labelExecGitkChoose = QLabel(self.groupBoxGitK)
        self.labelExecGitkChoose.setObjectName(u"labelExecGitkChoose")
        self.labelExecGitkChoose.setFont(font1)

        self.gridLayout_7.addWidget(self.labelExecGitkChoose, 2, 0, 1, 2)


        self.gridLayout_10.addWidget(self.groupBoxGitK, 1, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 38, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer_3, 6, 1, 1, 1)

        self.groupBoxTGit = QGroupBox(self.tab_extprogs)
        self.groupBoxTGit.setObjectName(u"groupBoxTGit")
        sizePolicy4.setHeightForWidth(self.groupBoxTGit.sizePolicy().hasHeightForWidth())
        self.groupBoxTGit.setSizePolicy(sizePolicy4)
        self.groupBoxTGit.setFont(font)
        self.groupBoxTGit.setFlat(False)
        self.groupBoxTGit.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBoxTGit)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_9 = QLabel(self.groupBoxTGit)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 1, 0, 1, 1)

        self.label_2 = QLabel(self.groupBoxTGit)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 3)

        self.radioTGitAutoDetect = QRadioButton(self.groupBoxTGit)
        self.radioTGitAutoDetect.setObjectName(u"radioTGitAutoDetect")
        sizePolicy5.setHeightForWidth(self.radioTGitAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioTGitAutoDetect.setSizePolicy(sizePolicy5)
        self.radioTGitAutoDetect.setFont(font1)

        self.gridLayout_2.addWidget(self.radioTGitAutoDetect, 3, 0, 1, 1)

        self.lineEditTGitAutoDetect = QLineEdit(self.groupBoxTGit)
        self.lineEditTGitAutoDetect.setObjectName(u"lineEditTGitAutoDetect")
        self.lineEditTGitAutoDetect.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.lineEditTGitAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditTGitAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditTGitAutoDetect.setFont(font1)
        self.lineEditTGitAutoDetect.setReadOnly(True)

        self.gridLayout_2.addWidget(self.lineEditTGitAutoDetect, 3, 1, 1, 1)

        self.radioTGitManual = QRadioButton(self.groupBoxTGit)
        self.radioTGitManual.setObjectName(u"radioTGitManual")
        sizePolicy5.setHeightForWidth(self.radioTGitManual.sizePolicy().hasHeightForWidth())
        self.radioTGitManual.setSizePolicy(sizePolicy5)
        self.radioTGitManual.setFont(font1)

        self.gridLayout_2.addWidget(self.radioTGitManual, 4, 0, 1, 1)

        self.lineEditTGitManual = QLineEdit(self.groupBoxTGit)
        self.lineEditTGitManual.setObjectName(u"lineEditTGitManual")
        sizePolicy7.setHeightForWidth(self.lineEditTGitManual.sizePolicy().hasHeightForWidth())
        self.lineEditTGitManual.setSizePolicy(sizePolicy7)
        self.lineEditTGitManual.setFont(font1)

        self.gridLayout_2.addWidget(self.lineEditTGitManual, 4, 1, 1, 1)

        self.pushButtonTGitManualBrowse = QPushButton(self.groupBoxTGit)
        self.pushButtonTGitManualBrowse.setObjectName(u"pushButtonTGitManualBrowse")
        sizePolicy8.setHeightForWidth(self.pushButtonTGitManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonTGitManualBrowse.setSizePolicy(sizePolicy8)
        self.pushButtonTGitManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonTGitManualBrowse.setFont(font1)

        self.gridLayout_2.addWidget(self.pushButtonTGitManualBrowse, 4, 2, 1, 1)

        self.checkBoxTortoiseGit = QCheckBox(self.groupBoxTGit)
        self.checkBoxTortoiseGit.setObjectName(u"checkBoxTortoiseGit")
        self.checkBoxTortoiseGit.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBoxTortoiseGit, 0, 0, 1, 2)


        self.gridLayout_10.addWidget(self.groupBoxTGit, 2, 1, 1, 1)

        self.groupBoxExplorer = QGroupBox(self.tab_extprogs)
        self.groupBoxExplorer.setObjectName(u"groupBoxExplorer")
        sizePolicy4.setHeightForWidth(self.groupBoxExplorer.sizePolicy().hasHeightForWidth())
        self.groupBoxExplorer.setSizePolicy(sizePolicy4)
        self.groupBoxExplorer.setFont(font)
        self.groupBoxExplorer.setFlat(False)
        self.groupBoxExplorer.setCheckable(False)
        self.gridLayout_5 = QGridLayout(self.groupBoxExplorer)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_11 = QLabel(self.groupBoxExplorer)
        self.label_11.setObjectName(u"label_11")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy9)
        self.label_11.setFont(font1)

        self.gridLayout_5.addWidget(self.label_11, 0, 0, 1, 3)

        self.radioExplorerAutoDetect = QRadioButton(self.groupBoxExplorer)
        self.radioExplorerAutoDetect.setObjectName(u"radioExplorerAutoDetect")
        sizePolicy5.setHeightForWidth(self.radioExplorerAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioExplorerAutoDetect.setSizePolicy(sizePolicy5)
        self.radioExplorerAutoDetect.setFont(font1)

        self.gridLayout_5.addWidget(self.radioExplorerAutoDetect, 1, 0, 1, 1)

        self.lineEditExplorerAutoDetect = QLineEdit(self.groupBoxExplorer)
        self.lineEditExplorerAutoDetect.setObjectName(u"lineEditExplorerAutoDetect")
        self.lineEditExplorerAutoDetect.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.lineEditExplorerAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditExplorerAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditExplorerAutoDetect.setFont(font1)
        self.lineEditExplorerAutoDetect.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineEditExplorerAutoDetect, 1, 1, 1, 1)

        self.radioExplorerManual = QRadioButton(self.groupBoxExplorer)
        self.radioExplorerManual.setObjectName(u"radioExplorerManual")
        sizePolicy5.setHeightForWidth(self.radioExplorerManual.sizePolicy().hasHeightForWidth())
        self.radioExplorerManual.setSizePolicy(sizePolicy5)
        self.radioExplorerManual.setFont(font1)

        self.gridLayout_5.addWidget(self.radioExplorerManual, 2, 0, 1, 1)

        self.lineEditExplorerManual = QLineEdit(self.groupBoxExplorer)
        self.lineEditExplorerManual.setObjectName(u"lineEditExplorerManual")
        sizePolicy7.setHeightForWidth(self.lineEditExplorerManual.sizePolicy().hasHeightForWidth())
        self.lineEditExplorerManual.setSizePolicy(sizePolicy7)
        self.lineEditExplorerManual.setFont(font1)

        self.gridLayout_5.addWidget(self.lineEditExplorerManual, 2, 1, 1, 1)

        self.pushButtonExplorerManualBrowse = QPushButton(self.groupBoxExplorer)
        self.pushButtonExplorerManualBrowse.setObjectName(u"pushButtonExplorerManualBrowse")
        sizePolicy8.setHeightForWidth(self.pushButtonExplorerManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonExplorerManualBrowse.setSizePolicy(sizePolicy8)
        self.pushButtonExplorerManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonExplorerManualBrowse.setFont(font1)

        self.gridLayout_5.addWidget(self.pushButtonExplorerManualBrowse, 2, 2, 1, 1)


        self.gridLayout_10.addWidget(self.groupBoxExplorer, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 16, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_10.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.groupBoxGitBash = QGroupBox(self.tab_extprogs)
        self.groupBoxGitBash.setObjectName(u"groupBoxGitBash")
        sizePolicy4.setHeightForWidth(self.groupBoxGitBash.sizePolicy().hasHeightForWidth())
        self.groupBoxGitBash.setSizePolicy(sizePolicy4)
        self.groupBoxGitBash.setFont(font)
        self.groupBoxGitBash.setFlat(False)
        self.groupBoxGitBash.setCheckable(False)
        self.gridLayout_6 = QGridLayout(self.groupBoxGitBash)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.lineEditGitBashAutoDetect = QLineEdit(self.groupBoxGitBash)
        self.lineEditGitBashAutoDetect.setObjectName(u"lineEditGitBashAutoDetect")
        self.lineEditGitBashAutoDetect.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.lineEditGitBashAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditGitBashAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditGitBashAutoDetect.setFont(font1)
        self.lineEditGitBashAutoDetect.setReadOnly(True)

        self.gridLayout_6.addWidget(self.lineEditGitBashAutoDetect, 3, 1, 1, 1)

        self.radioGitBashManual = QRadioButton(self.groupBoxGitBash)
        self.radioGitBashManual.setObjectName(u"radioGitBashManual")
        sizePolicy5.setHeightForWidth(self.radioGitBashManual.sizePolicy().hasHeightForWidth())
        self.radioGitBashManual.setSizePolicy(sizePolicy5)
        self.radioGitBashManual.setFont(font1)

        self.gridLayout_6.addWidget(self.radioGitBashManual, 4, 0, 1, 1)

        self.lineEditGitBashManual = QLineEdit(self.groupBoxGitBash)
        self.lineEditGitBashManual.setObjectName(u"lineEditGitBashManual")
        sizePolicy7.setHeightForWidth(self.lineEditGitBashManual.sizePolicy().hasHeightForWidth())
        self.lineEditGitBashManual.setSizePolicy(sizePolicy7)
        self.lineEditGitBashManual.setFont(font1)

        self.gridLayout_6.addWidget(self.lineEditGitBashManual, 4, 1, 1, 1)

        self.radioGitBashAutoDetect = QRadioButton(self.groupBoxGitBash)
        self.radioGitBashAutoDetect.setObjectName(u"radioGitBashAutoDetect")
        sizePolicy5.setHeightForWidth(self.radioGitBashAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioGitBashAutoDetect.setSizePolicy(sizePolicy5)
        self.radioGitBashAutoDetect.setFont(font1)

        self.gridLayout_6.addWidget(self.radioGitBashAutoDetect, 3, 0, 1, 1)

        self.label_13 = QLabel(self.groupBoxGitBash)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)

        self.gridLayout_6.addWidget(self.label_13, 2, 0, 1, 2)

        self.checkBoxGitBash = QCheckBox(self.groupBoxGitBash)
        self.checkBoxGitBash.setObjectName(u"checkBoxGitBash")
        self.checkBoxGitBash.setFont(font1)

        self.gridLayout_6.addWidget(self.checkBoxGitBash, 0, 0, 1, 2)

        self.label_14 = QLabel(self.groupBoxGitBash)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_6.addWidget(self.label_14, 1, 0, 1, 1)

        self.pushButtonGitBashManualBrowse = QPushButton(self.groupBoxGitBash)
        self.pushButtonGitBashManualBrowse.setObjectName(u"pushButtonGitBashManualBrowse")
        sizePolicy8.setHeightForWidth(self.pushButtonGitBashManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonGitBashManualBrowse.setSizePolicy(sizePolicy8)
        self.pushButtonGitBashManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonGitBashManualBrowse.setFont(font1)

        self.gridLayout_6.addWidget(self.pushButtonGitBashManualBrowse, 4, 2, 1, 1)


        self.gridLayout_10.addWidget(self.groupBoxGitBash, 3, 1, 1, 1)

        self.groupBoxGit = QGroupBox(self.tab_extprogs)
        self.groupBoxGit.setObjectName(u"groupBoxGit")
        self.groupBoxGit.setFont(font)
        self.groupBoxGit.setFlat(False)
        self.groupBoxGit.setCheckable(False)
        self.gridLayout = QGridLayout(self.groupBoxGit)
        self.gridLayout.setObjectName(u"gridLayout")
        self.radioGitManual = QRadioButton(self.groupBoxGit)
        self.radioGitManual.setObjectName(u"radioGitManual")
        sizePolicy5.setHeightForWidth(self.radioGitManual.sizePolicy().hasHeightForWidth())
        self.radioGitManual.setSizePolicy(sizePolicy5)
        self.radioGitManual.setFont(font1)

        self.gridLayout.addWidget(self.radioGitManual, 2, 0, 1, 1)

        self.radioGitAutoDetect = QRadioButton(self.groupBoxGit)
        self.radioGitAutoDetect.setObjectName(u"radioGitAutoDetect")
        sizePolicy8.setHeightForWidth(self.radioGitAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioGitAutoDetect.setSizePolicy(sizePolicy8)
        self.radioGitAutoDetect.setFont(font1)

        self.gridLayout.addWidget(self.radioGitAutoDetect, 1, 0, 1, 1)

        self.lineEditGitManual = QLineEdit(self.groupBoxGit)
        self.lineEditGitManual.setObjectName(u"lineEditGitManual")
        sizePolicy7.setHeightForWidth(self.lineEditGitManual.sizePolicy().hasHeightForWidth())
        self.lineEditGitManual.setSizePolicy(sizePolicy7)
        self.lineEditGitManual.setFont(font1)

        self.gridLayout.addWidget(self.lineEditGitManual, 2, 1, 1, 1)

        self.labelExecGitChoose = QLabel(self.groupBoxGit)
        self.labelExecGitChoose.setObjectName(u"labelExecGitChoose")
        sizePolicy9.setHeightForWidth(self.labelExecGitChoose.sizePolicy().hasHeightForWidth())
        self.labelExecGitChoose.setSizePolicy(sizePolicy9)
        self.labelExecGitChoose.setFont(font1)

        self.gridLayout.addWidget(self.labelExecGitChoose, 0, 0, 1, 3)

        self.lineEditGitAutoDetect = QLineEdit(self.groupBoxGit)
        self.lineEditGitAutoDetect.setObjectName(u"lineEditGitAutoDetect")
        self.lineEditGitAutoDetect.setEnabled(False)
        sizePolicy7.setHeightForWidth(self.lineEditGitAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditGitAutoDetect.setSizePolicy(sizePolicy7)
        self.lineEditGitAutoDetect.setFont(font1)
        self.lineEditGitAutoDetect.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEditGitAutoDetect, 1, 1, 1, 1)

        self.pushButtonGitManualBrowse = QPushButton(self.groupBoxGit)
        self.pushButtonGitManualBrowse.setObjectName(u"pushButtonGitManualBrowse")
        sizePolicy8.setHeightForWidth(self.pushButtonGitManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonGitManualBrowse.setSizePolicy(sizePolicy8)
        self.pushButtonGitManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonGitManualBrowse.setFont(font1)

        self.gridLayout.addWidget(self.pushButtonGitManualBrowse, 2, 2, 1, 1)


        self.gridLayout_10.addWidget(self.groupBoxGit, 0, 0, 1, 1)

        self.groupBoxSourceTree = QGroupBox(self.tab_extprogs)
        self.groupBoxSourceTree.setObjectName(u"groupBoxSourceTree")
        sizePolicy4.setHeightForWidth(self.groupBoxSourceTree.sizePolicy().hasHeightForWidth())
        self.groupBoxSourceTree.setSizePolicy(sizePolicy4)
        self.groupBoxSourceTree.setFont(font)
        self.groupBoxSourceTree.setFlat(False)
        self.groupBoxSourceTree.setCheckable(False)
        self.gridLayout_8 = QGridLayout(self.groupBoxSourceTree)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.checkBoxSourceTree = QCheckBox(self.groupBoxSourceTree)
        self.checkBoxSourceTree.setObjectName(u"checkBoxSourceTree")
        self.checkBoxSourceTree.setFont(font1)

        self.gridLayout_8.addWidget(self.checkBoxSourceTree, 0, 0, 1, 2)

        self.label_7 = QLabel(self.groupBoxSourceTree)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_8.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_4 = QLabel(self.groupBoxSourceTree)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.gridLayout_8.addWidget(self.label_4, 2, 0, 1, 3)

        self.radioSourcetreeAutoDetect = QRadioButton(self.groupBoxSourceTree)
        self.radioSourcetreeAutoDetect.setObjectName(u"radioSourcetreeAutoDetect")
        sizePolicy5.setHeightForWidth(self.radioSourcetreeAutoDetect.sizePolicy().hasHeightForWidth())
        self.radioSourcetreeAutoDetect.setSizePolicy(sizePolicy5)
        self.radioSourcetreeAutoDetect.setFont(font1)

        self.gridLayout_8.addWidget(self.radioSourcetreeAutoDetect, 3, 0, 1, 1)

        self.lineEditSourcetreeAutoDetect = QLineEdit(self.groupBoxSourceTree)
        self.lineEditSourcetreeAutoDetect.setObjectName(u"lineEditSourcetreeAutoDetect")
        self.lineEditSourcetreeAutoDetect.setEnabled(False)
        sizePolicy6.setHeightForWidth(self.lineEditSourcetreeAutoDetect.sizePolicy().hasHeightForWidth())
        self.lineEditSourcetreeAutoDetect.setSizePolicy(sizePolicy6)
        self.lineEditSourcetreeAutoDetect.setFont(font1)
        self.lineEditSourcetreeAutoDetect.setReadOnly(True)

        self.gridLayout_8.addWidget(self.lineEditSourcetreeAutoDetect, 3, 1, 1, 1)

        self.radioSourcetreeManual = QRadioButton(self.groupBoxSourceTree)
        self.radioSourcetreeManual.setObjectName(u"radioSourcetreeManual")
        sizePolicy5.setHeightForWidth(self.radioSourcetreeManual.sizePolicy().hasHeightForWidth())
        self.radioSourcetreeManual.setSizePolicy(sizePolicy5)
        self.radioSourcetreeManual.setFont(font1)

        self.gridLayout_8.addWidget(self.radioSourcetreeManual, 4, 0, 1, 1)

        self.lineEditSourcetreeManual = QLineEdit(self.groupBoxSourceTree)
        self.lineEditSourcetreeManual.setObjectName(u"lineEditSourcetreeManual")
        sizePolicy7.setHeightForWidth(self.lineEditSourcetreeManual.sizePolicy().hasHeightForWidth())
        self.lineEditSourcetreeManual.setSizePolicy(sizePolicy7)
        self.lineEditSourcetreeManual.setFont(font1)

        self.gridLayout_8.addWidget(self.lineEditSourcetreeManual, 4, 1, 1, 1)

        self.pushButtonSourcetreeManualBrowse = QPushButton(self.groupBoxSourceTree)
        self.pushButtonSourcetreeManualBrowse.setObjectName(u"pushButtonSourcetreeManualBrowse")
        sizePolicy8.setHeightForWidth(self.pushButtonSourcetreeManualBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonSourcetreeManualBrowse.setSizePolicy(sizePolicy8)
        self.pushButtonSourcetreeManualBrowse.setMinimumSize(QSize(24, 0))
        self.pushButtonSourcetreeManualBrowse.setFont(font1)

        self.gridLayout_8.addWidget(self.pushButtonSourcetreeManualBrowse, 4, 2, 1, 1)


        self.gridLayout_10.addWidget(self.groupBoxSourceTree, 3, 0, 1, 1)

        self.tabWidget.addTab(self.tab_extprogs, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(Preferences)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

#if QT_CONFIG(shortcut)
        self.labelExecSublimemergeChoose.setBuddy(self.radioSublimemergeAutoDetect)
        self.label_16.setBuddy(self.radioGitGuiAutoDetect)
        self.labelExecGitkChoose.setBuddy(self.radioGitKAutoDetect)
        self.label_2.setBuddy(self.radioTGitAutoDetect)
        self.label_11.setBuddy(self.radioExplorerAutoDetect)
        self.label_13.setBuddy(self.radioGitBashAutoDetect)
        self.labelExecGitChoose.setBuddy(self.radioGitAutoDetect)
        self.label_4.setBuddy(self.radioSourcetreeAutoDetect)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.radioGitAutoDetect, self.lineEditGitAutoDetect)
        QWidget.setTabOrder(self.lineEditGitAutoDetect, self.radioGitManual)
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
        QWidget.setTabOrder(self.pushButtonSublimemergeManualBrowse, self.radioExplorerAutoDetect)
        QWidget.setTabOrder(self.radioExplorerAutoDetect, self.lineEditExplorerAutoDetect)
        QWidget.setTabOrder(self.lineEditExplorerAutoDetect, self.radioExplorerManual)
        QWidget.setTabOrder(self.radioExplorerManual, self.lineEditExplorerManual)
        QWidget.setTabOrder(self.lineEditExplorerManual, self.pushButtonExplorerManualBrowse)
        QWidget.setTabOrder(self.pushButtonExplorerManualBrowse, self.checkBoxGitBash)
        QWidget.setTabOrder(self.checkBoxGitBash, self.radioGitBashAutoDetect)
        QWidget.setTabOrder(self.radioGitBashAutoDetect, self.lineEditGitBashAutoDetect)
        QWidget.setTabOrder(self.lineEditGitBashAutoDetect, self.radioGitBashManual)
        QWidget.setTabOrder(self.radioGitBashManual, self.lineEditGitBashManual)
        QWidget.setTabOrder(self.lineEditGitBashManual, self.pushButtonGitBashManualBrowse)
        QWidget.setTabOrder(self.pushButtonGitBashManualBrowse, self.checkBoxGitGui)
        QWidget.setTabOrder(self.checkBoxGitGui, self.radioGitGuiAutoDetect)
        QWidget.setTabOrder(self.radioGitGuiAutoDetect, self.lineEditGitGuiAutoDetect)
        QWidget.setTabOrder(self.lineEditGitGuiAutoDetect, self.radioGitGuiManual)
        QWidget.setTabOrder(self.radioGitGuiManual, self.lineEditGitGuiManual)
        QWidget.setTabOrder(self.lineEditGitGuiManual, self.pushButtonGitGuiManualBrowse)
        QWidget.setTabOrder(self.pushButtonGitGuiManualBrowse, self.checkBoxGitK)
        QWidget.setTabOrder(self.checkBoxGitK, self.radioGitKAutoDetect)
        QWidget.setTabOrder(self.radioGitKAutoDetect, self.lineEditGitKAutoDetect)
        QWidget.setTabOrder(self.lineEditGitKAutoDetect, self.radioGitKManual)
        QWidget.setTabOrder(self.radioGitKManual, self.lineEditGitKManual)
        QWidget.setTabOrder(self.lineEditGitKManual, self.pushButtonGitKManualBrowse)
        QWidget.setTabOrder(self.pushButtonGitKManualBrowse, self.comboUpdateFrequency)
        QWidget.setTabOrder(self.comboUpdateFrequency, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.checkBoxFetchOnStartup)
        QWidget.setTabOrder(self.checkBoxFetchOnStartup, self.spinBoxLimitValue)
        QWidget.setTabOrder(self.spinBoxLimitValue, self.radioButtonGitProcLimit)
        QWidget.setTabOrder(self.radioButtonGitProcLimit, self.pushButtonColorBranch)
        QWidget.setTabOrder(self.pushButtonColorBranch, self.comboBoxDoubleClickAction)
        QWidget.setTabOrder(self.comboBoxDoubleClickAction, self.pushButtonColorTag)
        QWidget.setTabOrder(self.pushButtonColorTag, self.radioButtonGitProcUnlimited)

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
        self.checkBoxSourceTree.toggled.connect(self.label_4.setEnabled)
        self.checkBoxSublimeMerge.toggled.connect(self.labelExecSublimemergeChoose.setEnabled)
        self.checkBoxSublimeMerge.toggled.connect(self.radioSublimemergeAutoDetect.setEnabled)
        self.checkBoxSublimeMerge.toggled.connect(self.radioSublimemergeManual.setEnabled)
        self.checkBoxTortoiseGit.toggled.connect(self.label_2.setEnabled)
        self.checkBoxTortoiseGit.toggled.connect(self.radioTGitAutoDetect.setEnabled)
        self.checkBoxTortoiseGit.toggled.connect(self.radioTGitManual.setEnabled)
        self.radioButtonGitProcUnlimited.toggled.connect(self.spinBoxLimitValue.setDisabled)
        self.radioButtonGitProcLimit.toggled.connect(self.spinBoxLimitValue.setEnabled)
        self.radioExplorerManual.toggled.connect(self.lineEditExplorerManual.setEnabled)
        self.radioExplorerManual.toggled.connect(self.pushButtonExplorerManualBrowse.setEnabled)
        self.radioGitBashManual.toggled.connect(self.lineEditGitBashManual.setEnabled)
        self.radioGitBashManual.toggled.connect(self.pushButtonGitBashManualBrowse.setEnabled)
        self.checkBoxGitBash.toggled.connect(self.radioGitBashAutoDetect.setEnabled)
        self.checkBoxGitBash.toggled.connect(self.radioGitBashManual.setEnabled)
        self.checkBoxGitBash.toggled.connect(self.label_13.setEnabled)
        self.radioGitKManual.toggled.connect(self.lineEditGitKManual.setEnabled)
        self.radioGitKManual.toggled.connect(self.pushButtonGitKManualBrowse.setEnabled)
        self.radioGitGuiManual.toggled.connect(self.lineEditGitGuiManual.setEnabled)
        self.radioGitGuiManual.toggled.connect(self.pushButtonGitGuiManualBrowse.setEnabled)

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
        self.groupBoxSublimemerge.setTitle(QCoreApplication.translate("Preferences", u"SublimeMerge", None))
        self.checkBoxSublimeMerge.setText(QCoreApplication.translate("Preferences", u"Activate SublimeMerge  in the Git Program menu", None))
        self.label_8.setText("")
        self.labelExecSublimemergeChoose.setText(QCoreApplication.translate("Preferences", u"Choose sublime_merge.exe executable location :", None))
        self.radioSublimemergeAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.radioSublimemergeManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.pushButtonSublimemergeManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.groupBoxGitGui.setTitle(QCoreApplication.translate("Preferences", u"Git Gui", None))
        self.pushButtonGitGuiManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.radioGitGuiAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.label_15.setText("")
        self.checkBoxGitGui.setText(QCoreApplication.translate("Preferences", u"Activate Git GUI  in the Git Program menu", None))
        self.radioGitGuiManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.label_16.setText(QCoreApplication.translate("Preferences", u"Choose git-gui.exe executable location :", None))
        self.groupBoxGitK.setTitle(QCoreApplication.translate("Preferences", u"GitK", None))
        self.radioGitKManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.radioGitKAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.checkBoxGitK.setText(QCoreApplication.translate("Preferences", u"Activate GitK in the Git Program menu", None))
        self.pushButtonGitKManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.label_17.setText("")
        self.labelExecGitkChoose.setText(QCoreApplication.translate("Preferences", u"Choose gitk.exe executable location :", None))
        self.groupBoxTGit.setTitle(QCoreApplication.translate("Preferences", u"TortoiseGit", None))
        self.label_9.setText("")
        self.label_2.setText(QCoreApplication.translate("Preferences", u"Choose TortoiseGitProc.exe executable location :", None))
        self.radioTGitAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.radioTGitManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.pushButtonTGitManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.checkBoxTortoiseGit.setText(QCoreApplication.translate("Preferences", u"Activate TortoiseGit in the Git Program menu", None))
        self.groupBoxExplorer.setTitle(QCoreApplication.translate("Preferences", u"File Explorer", None))
        self.label_11.setText(QCoreApplication.translate("Preferences", u"Choose File Explorer program to open directories :", None))
        self.radioExplorerAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.radioExplorerManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.pushButtonExplorerManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.groupBoxGitBash.setTitle(QCoreApplication.translate("Preferences", u"Git Bash", None))
        self.radioGitBashManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.radioGitBashAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.label_13.setText(QCoreApplication.translate("Preferences", u"Choose git-bash.exe executable location :", None))
        self.checkBoxGitBash.setText(QCoreApplication.translate("Preferences", u"Activate Git Bash in the Git Program menu", None))
        self.label_14.setText("")
        self.pushButtonGitBashManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.groupBoxGit.setTitle(QCoreApplication.translate("Preferences", u"Git executable", None))
        self.radioGitManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.radioGitAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.labelExecGitChoose.setText(QCoreApplication.translate("Preferences", u"Choose git.exe executable location :", None))
        self.pushButtonGitManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.groupBoxSourceTree.setTitle(QCoreApplication.translate("Preferences", u"SourceTree", None))
        self.checkBoxSourceTree.setText(QCoreApplication.translate("Preferences", u"Activate SourceTree in the Git Program menu", None))
        self.label_7.setText("")
        self.label_4.setText(QCoreApplication.translate("Preferences", u"Choose SourceTree.exe executable location :", None))
        self.radioSourcetreeAutoDetect.setText(QCoreApplication.translate("Preferences", u"Auto-detected", None))
        self.radioSourcetreeManual.setText(QCoreApplication.translate("Preferences", u"Manual path", None))
        self.pushButtonSourcetreeManualBrowse.setText(QCoreApplication.translate("Preferences", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_extprogs), QCoreApplication.translate("Preferences", u"External Programs", None))
    # retranslateUi

