# -*- coding: utf-8 -*-

#    Copyright (c) 2019-2023 IDEMIA
#    Author: IDEMIA (Philippe Fremy, Florent Oulieres)
# 
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
# 
#         http://www.apache.org/licenses/LICENSE-2.0
# 
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#


################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# import multigit_resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow) -> None:
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(290, 625)
        self.actionOpenDirectory = QAction(MainWindow)
        self.actionOpenDirectory.setObjectName(u"actionOpenDirectory")
        icon = QIcon()
        icon.addFile(u":/img/icons8-open-folder-64.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpenDirectory.setIcon(icon)
        self.actionOpenDirectory.setShortcutContext(Qt.ApplicationShortcut)
        self.actionEditPreferences = QAction(MainWindow)
        self.actionEditPreferences.setObjectName(u"actionEditPreferences")
        self.actionEditPreferences.setShortcutContext(Qt.ApplicationShortcut)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionQuit.setShortcutContext(Qt.ApplicationShortcut)
        self.actionRefreshAll = QAction(MainWindow)
        self.actionRefreshAll.setObjectName(u"actionRefreshAll")
        self.actionDir1 = QAction(MainWindow)
        self.actionDir1.setObjectName(u"actionDir1")
        self.actionDir2 = QAction(MainWindow)
        self.actionDir2.setObjectName(u"actionDir2")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionWhatIsNew = QAction(MainWindow)
        self.actionWhatIsNew.setObjectName(u"actionWhatIsNew")
        self.actionExportCSV = QAction(MainWindow)
        self.actionExportCSV.setObjectName(u"actionExportCSV")
        self.actionOpenProject = QAction(MainWindow)
        self.actionOpenProject.setObjectName(u"actionOpenProject")
        self.actionExportToMgit = QAction(MainWindow)
        self.actionExportToMgit.setObjectName(u"actionExportToMgit")
        self.actionShowMultiGitLogFiles = QAction(MainWindow)
        self.actionShowMultiGitLogFiles.setObjectName(u"actionShowMultiGitLogFiles")
        self.actionViewLastCommit = QAction(MainWindow)
        self.actionViewLastCommit.setObjectName(u"actionViewLastCommit")
        self.actionViewLastCommit.setCheckable(True)
        self.actionViewLastCommit.setChecked(True)
        self.actionViewModifiedFiles = QAction(MainWindow)
        self.actionViewModifiedFiles.setObjectName(u"actionViewModifiedFiles")
        self.actionViewModifiedFiles.setCheckable(True)
        self.actionViewColSha1 = QAction(MainWindow)
        self.actionViewColSha1.setObjectName(u"actionViewColSha1")
        self.actionViewColSha1.setCheckable(True)
        self.actionApplyMultigitFile = QAction(MainWindow)
        self.actionApplyMultigitFile.setObjectName(u"actionApplyMultigitFile")
        self.actionViewColURL = QAction(MainWindow)
        self.actionViewColURL.setObjectName(u"actionViewColURL")
        self.actionViewColURL.setCheckable(True)
        self.actionAddTab = QAction(MainWindow)
        self.actionAddTab.setObjectName(u"actionAddTab")
        self.actionDupTab = QAction(MainWindow)
        self.actionDupTab.setObjectName(u"actionDupTab")
        self.actionCloseTab = QAction(MainWindow)
        self.actionCloseTab.setObjectName(u"actionCloseTab")
        self.actionRenameTab = QAction(MainWindow)
        self.actionRenameTab.setObjectName(u"actionRenameTab")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabRepos = QTabWidget(self.centralwidget)
        self.tabRepos.setObjectName(u"tabRepos")
        self.tabRepos.setMovable(True)

        self.horizontalLayout_2.addWidget(self.tabRepos)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 290, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setToolTipsVisible(True)
        self.menuOpenRecentDirectory = QMenu(self.menuFile)
        self.menuOpenRecentDirectory.setObjectName(u"menuOpenRecentDirectory")
        self.menuOpenRecentDirectory.setToolTipsVisible(True)
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuView.setToolTipsVisible(True)
        self.menuShow = QMenu(self.menuView)
        self.menuShow.setObjectName(u"menuShow")
        self.menuColumns = QMenu(self.menuShow)
        self.menuColumns.setObjectName(u"menuColumns")
        self.menuGit = QMenu(self.menubar)
        self.menuGit.setObjectName(u"menuGit")
        self.menuGit.setToolTipsVisible(True)
        self.menuGitPrograms = QMenu(self.menubar)
        self.menuGitPrograms.setObjectName(u"menuGitPrograms")
        self.menuGitPrograms.setToolTipsVisible(True)
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        self.menuAbout.setToolTipsVisible(True)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuGit.menuAction())
        self.menubar.addAction(self.menuGitPrograms.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionOpenDirectory)
        self.menuFile.addAction(self.menuOpenRecentDirectory.menuAction())
        self.menuFile.addAction(self.actionEditPreferences)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAddTab)
        self.menuFile.addAction(self.actionDupTab)
        self.menuFile.addAction(self.actionRenameTab)
        self.menuFile.addAction(self.actionCloseTab)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpenProject)
        self.menuFile.addAction(self.actionApplyMultigitFile)
        self.menuFile.addAction(self.actionExportToMgit)
        self.menuFile.addAction(self.actionExportCSV)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuOpenRecentDirectory.addAction(self.actionDir1)
        self.menuOpenRecentDirectory.addAction(self.actionDir2)
        self.menuView.addAction(self.menuShow.menuAction())
        self.menuView.addAction(self.actionRefreshAll)
        self.menuShow.addAction(self.actionViewLastCommit)
        self.menuShow.addAction(self.actionViewModifiedFiles)
        self.menuShow.addAction(self.menuColumns.menuAction())
        self.menuColumns.addAction(self.actionViewColSha1)
        self.menuColumns.addAction(self.actionViewColURL)
        self.menuAbout.addAction(self.actionWhatIsNew)
        self.menuAbout.addAction(self.actionShowMultiGitLogFiles)
        self.menuAbout.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tabRepos.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow: QMainWindow) -> None:
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MultiGit", None))
        self.actionOpenDirectory.setText(QCoreApplication.translate("MainWindow", u"Open base directory", None))
#if QT_CONFIG(tooltip)
        self.actionOpenDirectory.setToolTip(QCoreApplication.translate("MainWindow", u"Open base directory", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOpenDirectory.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionEditPreferences.setText(QCoreApplication.translate("MainWindow", u"Edit settings", None))
#if QT_CONFIG(tooltip)
        self.actionEditPreferences.setToolTip(QCoreApplication.translate("MainWindow", u"Edit settings", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionEditPreferences.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionQuit.setIconText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(tooltip)
        self.actionQuit.setToolTip(QCoreApplication.translate("MainWindow", u"Quit", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.actionRefreshAll.setText(QCoreApplication.translate("MainWindow", u"Refresh local view", None))
#if QT_CONFIG(tooltip)
        self.actionRefreshAll.setToolTip(QCoreApplication.translate("MainWindow", u"Refresh repository information from disk", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionRefreshAll.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionDir1.setText(QCoreApplication.translate("MainWindow", u"Dir1", None))
        self.actionDir2.setText(QCoreApplication.translate("MainWindow", u"Dir2", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About MultiGit", None))
        self.actionWhatIsNew.setText(QCoreApplication.translate("MainWindow", u"What's new", None))
#if QT_CONFIG(tooltip)
        self.actionWhatIsNew.setToolTip(QCoreApplication.translate("MainWindow", u"Show dialog with What's New information", None))
#endif // QT_CONFIG(tooltip)
        self.actionExportCSV.setText(QCoreApplication.translate("MainWindow", u"Export to CSV", None))
#if QT_CONFIG(tooltip)
        self.actionExportCSV.setToolTip(QCoreApplication.translate("MainWindow", u"Export repository informations to a CSV files", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpenProject.setText(QCoreApplication.translate("MainWindow", u"Clone from Multigit file", None))
#if QT_CONFIG(tooltip)
        self.actionOpenProject.setToolTip(QCoreApplication.translate("MainWindow", u"Clone repositories described in a Multigit file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOpenProject.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+J", None))
#endif // QT_CONFIG(shortcut)
        self.actionExportToMgit.setText(QCoreApplication.translate("MainWindow", u"Export to Multigit file", None))
#if QT_CONFIG(tooltip)
        self.actionExportToMgit.setToolTip(QCoreApplication.translate("MainWindow", u"Export repositories setup to a Multigit file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionExportToMgit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+J", None))
#endif // QT_CONFIG(shortcut)
        self.actionShowMultiGitLogFiles.setText(QCoreApplication.translate("MainWindow", u"Open directory of log files", None))
#if QT_CONFIG(tooltip)
        self.actionShowMultiGitLogFiles.setToolTip(QCoreApplication.translate("MainWindow", u"Open directory containing log files and configuration", None))
#endif // QT_CONFIG(tooltip)
        self.actionViewLastCommit.setText(QCoreApplication.translate("MainWindow", u"Show Last Commit tab", None))
        self.actionViewModifiedFiles.setText(QCoreApplication.translate("MainWindow", u"Show Modified Files tab", None))
        self.actionViewColSha1.setText(QCoreApplication.translate("MainWindow", u"Sha1", None))
        self.actionApplyMultigitFile.setText(QCoreApplication.translate("MainWindow", u"Apply Multigit file", None))
#if QT_CONFIG(tooltip)
        self.actionApplyMultigitFile.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust existing repositories according to content of Multigit file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionApplyMultigitFile.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+A", None))
#endif // QT_CONFIG(shortcut)
        self.actionViewColURL.setText(QCoreApplication.translate("MainWindow", u"Remote URL", None))
        self.actionAddTab.setText(QCoreApplication.translate("MainWindow", u"New tab", None))
#if QT_CONFIG(shortcut)
        self.actionAddTab.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionDupTab.setText(QCoreApplication.translate("MainWindow", u"Duplicate tab", None))
#if QT_CONFIG(shortcut)
        self.actionDupTab.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.actionCloseTab.setText(QCoreApplication.translate("MainWindow", u"Close current tab", None))
#if QT_CONFIG(shortcut)
        self.actionCloseTab.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.actionRenameTab.setText(QCoreApplication.translate("MainWindow", u"Rename tab", None))
#if QT_CONFIG(shortcut)
        self.actionRenameTab.setShortcut(QCoreApplication.translate("MainWindow", u"F2", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOpenRecentDirectory.setTitle(QCoreApplication.translate("MainWindow", u"Open recent directory", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuShow.setTitle(QCoreApplication.translate("MainWindow", u"Show", None))
        self.menuColumns.setTitle(QCoreApplication.translate("MainWindow", u"Show Columns", None))
        self.menuGit.setTitle(QCoreApplication.translate("MainWindow", u"Git", None))
        self.menuGitPrograms.setTitle(QCoreApplication.translate("MainWindow", u"Git Programs", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

