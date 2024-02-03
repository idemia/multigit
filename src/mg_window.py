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


from typing import cast, List, Optional, Callable, Any, Union
import subprocess, functools, logging, pathlib
from typing_extensions import Literal

from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QAction, QApplication, QLineEdit, QTabBar
from PySide2.QtCore import QTimer, Qt, QSignalMapper
from PySide2.QtGui import QCloseEvent

from src.gui.ui_main_window import Ui_MainWindow
from src.mg_actions import MgActions
from src.mg_dialog_whatisnew import showWhatIsNew, showWhatisnewIfAppropriate
from src.mg_dialog_export_mgit import runDialogExportMgit
from src.mg_dialog_export_csv import runDialogExportCsv
from src.mg_dialog_clone_from_mgit import runDialogCloneFromMgitFile
from src.mg_dialog_apply_mgit_file import runDialogApplyMgitFile
from src.mg_dialog_about import showDialogAbout
from src.mg_plugin_mgr import pluginMgrInstance
from src.mg_multigit_widget import MgMultigitWidget
from src.mg_repo_tree_item import MgRepoTreeItem
from src.mg_repo_tree import MgRepoTree
from src.mg_tools import git_exec, ExecExplorer
from src.mg_dialog_settings import runDialogEditSettings
from src.mg_exec_window import MgExecWindow
from src import mg_config as mgc
from src.mg_const import VERSION


logger = logging.getLogger('mg_main_window')
dbg = logger.debug
info = logger.info


class MgMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, argv: List[str] ) -> None:
        super().__init__()
        self.refreshOnFocusBack = True
        self.setupUi(self)

        self.config = mgc.get_config_instance()
        self.gitIsOk = False
        self.argv = argv

        if self.config[mgc.CONFIG_MAINWINDOW_GEOMETRY]:
            (x, y, w, h) = self.config[mgc.CONFIG_MAINWINDOW_GEOMETRY]
            self.setGeometry(x, y, w, h)
        else:
            self.setGeometry(self.x(), self.y(), 1000, 700)  # default reasonable window size when no configuration

        self.setupActions()
        self.setupMenus()
        self.setupConnections()
        pluginMgrInstance.setupTopMenu(self)

        self.setWindowTitle('MultiGit OpenSource v{}'.format(VERSION))

        QTimer.singleShot(0, self.checkGitOkAndOpenDefaultRepo)
        QTimer.singleShot(0, showWhatisnewIfAppropriate)


    def currentMultigit(self) -> MgMultigitWidget:
        '''Return the MgMultigitWidget active in the current tab'''
        # Note: in theory, self.tabRepos.currentWidget() can be None, when no tab have been created.
        #       However, in practice in our code, creating one or multiple tabs is the first thing we do
        #       after showing the window. So, we consider that it is never None
        return cast(MgMultigitWidget, self.tabRepos.currentWidget())


    def multigitWidgetFromIdx(self, idx: int) -> MgMultigitWidget:
        '''Return the MgMultigitWidget active in the current tab'''
        return cast(MgMultigitWidget, self.tabRepos.widget(idx))


##########################################################################
#
#       Methods related to the display updates and internal machinery
#
##########################################################################

    def setupActions(self) -> None:
        self.mgActions = MgActions(self)

        self.mgActions.actionGitFetchAll = QAction(self)
        self.mgActions.actionGitFetchAll.setText(u"Fetch All (current tab)")
        self.mgActions.actionGitFetchAll.setToolTip("Run <code>git fetch</code> on all repositories of the current tab")
        self.mgActions.actionGitFetchAll.setShortcut("F6")

        self.mgActions.actionGitFetchAllOnAllTabs = QAction(self)
        self.mgActions.actionGitFetchAllOnAllTabs.setText(u"Fetch All (all tabs)")
        self.mgActions.actionGitFetchAllOnAllTabs.setToolTip("Run <code>git fetch</code> on all repositories of all tabs")
        self.mgActions.actionGitFetchAllOnAllTabs.setShortcut("F7")


    def setupMenus(self) -> None:
        '''Setup all menu which were not already prepared by the Designer UI'''
        # menu File
        self.fillRecentDirMenu()
        self.mgActions.setupMenuView(self.menuView)

        # menu git
        self.menuGit.addAction(self.mgActions.actionGitFetchAll)
        self.menuGit.addAction(self.mgActions.actionGitFetchAllOnAllTabs)
        self.menuGit.addSeparator()
        self.mgActions.setupMenuGit(self.menuGit)

        # menu git programs
        self.mgActions.setupMenuGitPrograms(self.menuGitPrograms, includeConfigureGitPrograms=True)


    def fillRecentDirMenu(self) -> None:
        dbg('fillRecentDirMenu()')
        self.menuOpenRecentDirectory.clear()
        for dirname in self.config.lruAsList(mgc.CONFIG_LAST_OPENED):    # type: str
            action = QAction(dirname, self.menuOpenRecentDirectory)
            action.setData( dirname )
            self.menuOpenRecentDirectory.addAction( action )


    def dispatchToActiveMultigitTab(self, methodName: str) -> Callable[[], None]:
        '''Return a function which calls the methodName on the active tab widget
        (at the time where the method is called)'''
        def callActiveMultigitTabMethod() -> None:
            targetMethod = getattr(self.currentMultigit(), methodName)
            targetMethod()

        return callActiveMultigitTabMethod


    def dispatchToActiveTreeOfMultigitTab(self, methodName: str, with_arg1: bool = False) -> Union[Callable[[], None], Callable[[Any], None]]:
        '''Return a function which calls the methodName on all tab widget
        (at the time where the method is called).

        The method may support an argument if with_arg1 is True
        '''
        callActiveTreeOfMultigitTabMethod: Union[Callable[[], None], Callable[[Any], None]]
        if with_arg1:
            def callActiveTreeOfMultigitTabMethod(arg1: Any) -> None:
                targetMethod = getattr(self.currentMultigit().repoTree, methodName)
                targetMethod(arg1)

        else:
            def callActiveTreeOfMultigitTabMethod() -> None:
                targetMethod = getattr(self.currentMultigit().repoTree, methodName)
                targetMethod()

        return callActiveTreeOfMultigitTabMethod


    def allTreeOfMultigitTab(self) -> List[MgRepoTree]:
        return [
            cast(MgMultigitWidget, self.tabRepos.widget(tabIdx)).repoTree
            for tabIdx in range(self.tabRepos.count())
        ]


    def setupConnections(self) -> None:
        '''Setup all actions and corresponding slots'''

        ### menu File
        self.actionOpenDirectory.triggered.connect(self.slotOpenDir)
        self.menuOpenRecentDirectory.triggered.connect(self.slotOpenRecentDirTriggered)
        self.actionExportCSV.triggered.connect(self.slotExportCsv)
        self.actionEditPreferences.triggered.connect( self.slotEditSettings )
        # ----
        self.actionAddTab.triggered.connect( lambda checked: self.slotAddTab() )  # note: ignore the checked parameter
        self.actionDupTab.triggered.connect( self.slotDupTab )
        self.actionRenameTab.triggered.connect( self.slotRenameTab )
        self.actionCloseTab.triggered.connect( self.slotCloseTab )
        # ----
        self.actionOpenProject.triggered.connect(self.slotCloneFromMgitFile)
        self.actionApplyMultigitFile.triggered.connect(self.slotApplyMgitFile)
        self.actionExportToMgit.triggered.connect(self.slotExportToMgit)
        self.actionQuit.triggered.connect( self.close )

        ### menu View
        self.actionViewLastCommit.setChecked(mgc.get_config_instance().get(mgc.CONFIG_VIEW_TAB_LAST_COMMIT, False))
        self.actionViewLastCommit.changed.connect(self.slotViewTabChanged)
        self.actionViewModifiedFiles.setChecked(mgc.get_config_instance().get(mgc.CONFIG_VIEW_TAB_MOD_FILES, False))
        self.actionViewModifiedFiles.changed.connect(self.slotViewTabChanged)

        # trigger the slot once to setup the GUI
        self.actionViewColSha1.setChecked(mgc.get_config_instance().get(mgc.CONFIG_VIEW_COL_SHA1, True))
        self.actionViewColSha1.changed.connect(self.slotViewColSha1Changed)
        self.actionViewColURL.setChecked(mgc.get_config_instance().get(mgc.CONFIG_VIEW_COL_URL, True))
        self.actionViewColURL.changed.connect(self.slotViewColUrlChanged)
        self.actionRefreshAll.triggered.connect(self.dispatchToActiveMultigitTab('slotRefreshAll'))

        self.mgActions.actionRefreshSelected.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotRefreshSelected'))
        self.mgActions.actionShowInExplorer.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotShowInExplorer'))
        self.mgActions.menuCopy.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotMenuCopyAction', True))
        self.mgActions.menuCopy.aboutToShow.connect(self.slotMenuCopyAboutToShow)
        self.mgActions.menuCopy.aboutToHide.connect(self.slotMenuCopyAboutToHide)


        ### menu Git
        self.mgActions.actionGitFetchAll.triggered.connect(self.dispatchToActiveMultigitTab('slotGitFetchAll'))
        self.mgActions.actionGitFetchAllOnAllTabs.triggered.connect(self.slotFetchAllReposOnAllTabs)
        self.mgActions.actionGitProperties.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitProperties'))
        self.mgActions.actionGitCommit.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitCommit'))
        self.mgActions.actionGitRevert.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitRevert'))
        self.mgActions.actionGitPush.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitPush'))
        self.mgActions.actionGitPushTag.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitPushTag'))
        self.mgActions.actionGitPull.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitPull'))
        self.mgActions.actionGitFetch.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitFetch'))
        self.mgActions.actionGitTag.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitTag'))
        self.mgActions.actionGitCreateBranch.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitCreateBranch'))
        self.mgActions.actionGitSwitchBranch.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitSwitchBranch'))
        self.mgActions.actionGitCheckoutTag.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitCheckoutTag'))
        self.mgActions.actionGitDeleteBranch.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitDeleteBranch'))
        self.mgActions.actionGitBash.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitBash'))
        self.mgActions.actionGitRunCommand.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitRunCommand'))

        # Menu Git programs
        self.mgActions.actionSourceTree.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotSourcetree'))
        self.mgActions.actionSublimeMerge.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotSublimemerge'))
        self.mgActions.actionGitGui.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitGui'))
        self.mgActions.actionGitK.triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotGitK'))

        self.mgActions.actionTGitShowLog  .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitShowLog'))
        self.mgActions.actionTGitCommit   .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitCommit'))
        self.mgActions.actionTGitDiff     .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitDiff'))
        self.mgActions.actionTGitRevert   .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitRevert'))
        self.mgActions.actionTGitPush     .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitPush'))
        self.mgActions.actionTGitPull     .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitPull'))
        self.mgActions.actionTGitFetch    .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitFetch'))
        self.mgActions.actionTGitTag      .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitTag'))
        self.mgActions.actionTGitSwitch   .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitSwitch'))
        self.mgActions.actionTGitBranch   .triggered.connect(self.dispatchToActiveTreeOfMultigitTab('slotTGitBranch'))

        self.mgActions.actionConfigureGitProgram.triggered.connect(self.slotEditSettingsGitProgram)

        # menu About
        self.actionWhatIsNew.triggered.connect( self.slotWhatIsNew )
        self.actionAbout.triggered.connect( self.slotAbout )
        self.actionShowMultiGitLogFiles.triggered.connect(self.slotShowLogFileDirectory)

        # we enable refresh on focus in
        cast(QApplication, QApplication.instance()).applicationStateChanged.connect(self.slotAppStateChanged)
        self.tabRepos.currentChanged.connect( self.slotCurrentTabChanged )


    def closeEvent(self, event: QCloseEvent) -> None:
        dbg('closeEvent()')
        rect = self.geometry()
        self.config[mgc.CONFIG_MAINWINDOW_GEOMETRY] = (rect.x(), rect.y(), rect.width(), rect.height())

        # save splitter state as a list of bytes, to avoid accessing the QSplitter buffer directly. I suspect
        # that there are sometimes buffer overflow in this buffer, creating bugs in the config file.
        self.config[mgc.CONFIG_SPLITTER_STATE_V2] = [int(v) for v in bytes(self.currentMultigit().splitter.saveState())]

        all_open_tabs = [(self.tabRepos.tabText(tabIdx), cast(MgMultigitWidget, self.tabRepos.widget(tabIdx)).multiRepo.base_dir)
                         for tabIdx in range(self.tabRepos.count())
                         ]
        self.config[mgc.CONFIG_TABS_OPENED] = all_open_tabs
        self.config[mgc.CONFIG_TABS_CURRENT] = self.tabRepos.currentIndex()
        self.config.save()
        return super().closeEvent(event)


    def slotAppStateChanged(self, state: int) -> None:
        if state == Qt.ApplicationActive:
            # window just got activated
            if self.refreshOnFocusBack:
                dbg('slotAppChangedState: %s' % state)
                if self.currentMultigit():
                    selectedItems = self.currentMultigit().repoTree.selectedRepoItems()
                    # only refresh the first item on focus back
                    self.currentMultigit().repoTree.doRefreshItems(selectedItems[:1])


    def checkGitOkAndOpenDefaultRepo(self) -> None:
        '''Check performed on first launch of the UI, to verify that Git is working.'''
        try:
            git_exec('--version', allow_errors=True)
            self.gitIsOk = True
            # git OK

        except (ValueError, FileNotFoundError):
            QMessageBox.warning(self, 'Could not locate git.exe', 'Warning: could not locate the git.exe program\n' +
                                'MultiGit needs git to work.\nPlease configure the location in the preference dialog.\n')
            self.slotEditSettingsGitProgram()
        except subprocess.CalledProcessError as exc:
            QMessageBox.warning(self, 'Could not execute git.exe', 'Error: could not execute git.exe\n{}'.format(exc) +
                                '\nMultiGit needs git to work.\nPlease configure the location in the preference dialog.\n')
            self.slotEditSettingsGitProgram()

        # Open repositories passed as arguments
        if len(self.argv) > 1:
            tabsToOpen = [
                (None, pathlib.Path(argv).resolve().as_posix())
                for argv in self.argv[1:]
            ]
        else:
            tabsToOpen = self.config.lruAsList(mgc.CONFIG_TABS_OPENED)
            if tabsToOpen == []:
                # note: this returns an empty list of the config key does not exist
                #       in this case, we use the last opened directory (previous behavior with no tabs)
                tabsToOpen = [(None, self.config.lruGetFirst(mgc.CONFIG_LAST_OPENED))]

        for tabName, base_dir in reversed(tabsToOpen):
            idx = self.addTab(base_dir, pos=0)
            if tabName:
                self.tabRepos.setTabText(idx, tabName)

        fetchReposOnStartup = self.config[mgc.CONFIG_FETCH_ON_STARTUP]
        if fetchReposOnStartup is None:
            answer = QMessageBox.question(self, 'Activate fetch on startup ?', 'Multigit can fetch all your repositories when you launch it. '
                                 'Do you want to activate this setting ?\n\nNote that you can change it later in the settings dialog.\n')
            fetchReposOnStartup = (answer == QMessageBox.Yes)
            self.config[mgc.CONFIG_FETCH_ON_STARTUP] = fetchReposOnStartup
            self.config.save()


        if fetchReposOnStartup:
            QTimer.singleShot(1000, self.slotFetchAllReposOnAllTabs)



##########################################################################
#
#       Methods related to menu entries NOT acting on selected items
#
##########################################################################

    def slotOpenDir(self) -> None:
        dbg('openDirTriggered()')
        lastdir = self.config.lruGetFirst(mgc.CONFIG_LAST_OPENED) or ''
        newDir = QFileDialog.getExistingDirectory(self, 'Open directory containing git repositories', lastdir)
        if not newDir:
            return

        # pass to current main widget
        self.openDir(newDir)


    def slotCloneFromMgitFile(self) -> None:
        dbg('slotCloneFromMgitFile()')
        return runDialogCloneFromMgitFile(self)


    def slotOpenRecentDirTriggered(self, action: QAction) -> None:
        dbg('openRecentDirTriggered()')
        self.openDir(action.data())


    def updateRecentDirMenu(self, newDir: str) -> None:
        self.config.lruSetRecent(mgc.CONFIG_LAST_OPENED, newDir)
        self.config.save()
        self.fillRecentDirMenu()


    def openDir(self, newDir: str, ignoreNonExisting: bool = False) -> None:
        info('Opening dir: %s' % newDir)
        dirPath = pathlib.Path(newDir)
        if not dirPath.exists():
            if not ignoreNonExisting:
                QMessageBox.warning(self, 'No such directory', 'Can not open directory "%s", it does not exist.' % newDir )
            return
        if not dirPath.is_dir():
            if not ignoreNonExisting:
                QMessageBox.warning(self, 'Not a directory', 'Can not open directory "%s", it is not a directory.' % newDir )
            return

        self.updateRecentDirMenu(newDir)

        # pass to main widget
        self.currentMultigit().setBaseDir(newDir)


    def slotFetchAllReposOnAllTabs(self) -> None:
        '''Called during startup, to fetch really all repositories from all tabs'''
        dbg('slotFetchAllReposOnAllTabs()')

        gitExecWindow = MgExecWindow(self)
        gitExecWindow.setWindowTitle('Fetching all repositories on startup')

        for tabIdx in range(self.tabRepos.count()):
            multiRepo = self.multigitWidgetFromIdx(tabIdx).multiRepo
            cmd = ['fetch', '--prune']
            gitExecWindow.execOneGitCommand(f'Fetching all repositories for {multiRepo.base_dir}', cmd, multiRepo.repo_list)


    def slotExportCsv(self) -> None:
        '''Export to a CSV file'''
        dbg('slotExportCsv()')
        runDialogExportCsv(self, self.currentMultigit().multiRepo)


    def slotExportToMgit(self) -> None:
        dbg('slotExportToMgit()')
        runDialogExportMgit(self, self.currentMultigit().multiRepo.repo_list)


    def slotApplyMgitFile(self) -> None:
        dbg('slotApplyMgitFile()')
        baseDir = self.currentMultigit().multiRepo.base_dir
        allRepos = self.currentMultigit().multiRepo.repo_list[:]
        runDialogApplyMgitFile(self, baseDir, allRepos)


    def slotEditSettings(self) -> None:
        '''Show the Edit Settings dialog'''
        self.editSettings(0)


    def slotEditSettingsGitProgram(self) -> None:
        '''Show the Edit Settings dialog'''
        self.editSettings(1)


    def editSettings(self, startingPage: Union[Literal[0], Literal[1]]) -> None:
        runDialogEditSettings(self, tabPage=startingPage)
        self.mgActions.enableAvailableScm()
        for repoTree in self.allTreeOfMultigitTab():
            repoTree.availableScmUpdated()


    def slotAbout(self) -> None:
        '''Show about dialog'''
        showDialogAbout(self)


    def slotWhatIsNew(self) -> None:
        '''Show what's new dialog'''
        showWhatIsNew(self)


    def selectedItems(self) -> List[MgRepoTreeItem]:
        '''Return the list of selected MgRepoTreeItem'''
        items = cast(List[MgRepoTreeItem], list(self.currentMultigit().repoTree.selectedItems()))
        return items


    # noinspection PyMethodMayBeStatic
    def slotShowLogFileDirectory(self) -> None:
        '''Open an explorer on the log file directory'''
        from src import mg_const
        if mg_const.PATH_LOG_NORMAL is None and mg_const.PATH_LOG_DEBUG is None:
            QMessageBox.warning(None, 'No log file directory', 'MultiGit was unable to use a log file directory!')
            return

        path_log_file = mg_const.PATH_LOG_NORMAL or mg_const.PATH_LOG_DEBUG
        assert path_log_file is not None
        path_log_dir = str(path_log_file.parent)

        if not ExecExplorer.checkFound():
            return
        ExecExplorer.exec_non_blocking([path_log_dir])


    ##########################################################################
    #
    #       Methods to dispatch to or from one or all multigit tabs
    #
    ##########################################################################

    def slotViewTabChanged(self) -> None:
        showTabLastCommit = self.actionViewLastCommit.isChecked()
        showTabModFiles = self.actionViewModifiedFiles.isChecked()
        for tabIdx in range(self.tabRepos.count()):
            self.multigitWidgetFromIdx(tabIdx).slotViewTabChanged(showTabLastCommit, showTabModFiles)

        self.config[mgc.CONFIG_VIEW_TAB_LAST_COMMIT] = showTabLastCommit
        self.config[mgc.CONFIG_VIEW_TAB_MOD_FILES] = showTabModFiles


    def slotViewColSha1Changed(self) -> None:
        '''Called when menu Edit->View->Columns->Sha1 changes'''
        dbg('slotViewColSha1Changed')
        showColSha1 = self.actionViewColSha1.isChecked()
        for repoTree in self.allTreeOfMultigitTab():
            repoTree.slotViewColSha1Changed(showColSha1)
        mgc.get_config_instance()[mgc.CONFIG_VIEW_COL_SHA1] = showColSha1
        mgc.get_config_instance().save()


    def slotViewColUrlChanged(self) -> None:
        '''Called when menu Edit->View->Columns->Sha1 changes'''
        dbg('slotViewColUrlChanged')
        showColUrl = self.actionViewColURL.isChecked()
        for repoTree in self.allTreeOfMultigitTab():
            repoTree.slotViewColUrlChanged(showColUrl)
        mgc.get_config_instance()[mgc.CONFIG_VIEW_COL_URL] = showColUrl
        mgc.get_config_instance().save()


    def slotMenuCopyAboutToShow(self) -> None:
        '''Called when user clicked on the copy submenu. Fills the items of the menu'''
        items = self.currentMultigit().repoTree.selectedRepoItems()
        if len(items) == 0:
            return

        repoInfo = items[0].repoInfo
        self.mgActions.setupDynamicMenuCopy(repoInfo)


    def slotMenuCopyAboutToHide(self) -> None:
        '''Called when Copy menu is going to hide. We disable the connections created
        by the Copy menu to capture the repo missing info'''

        # connections are used to update the menu after is has been shown, when
        # information is missing. We must disconnect everything when the menu
        # goes to hide
        self.mgActions.clearMenuCopyConnections()


    ##########################################################################
    #
    #       Methods to manage tabs
    #
    ##########################################################################

    def slotAddTab(self, pos: int = -1) -> int:
        '''Create a new empty tab, and return the tab index. If pos is not specified or is -1, add the tab
        at the end of the tab list. Else, add it add the expected position.'''
        multigitWidget = MgMultigitWidget()
        if pos == -1:
            pos = self.tabRepos.count()
        tabIdx = self.tabRepos.insertTab(pos, multigitWidget, 'MultiGit')
        self.tabRepos.setCurrentIndex(tabIdx)
        multigitWidget.sig_dir_changed.connect(self.slotTabBaseDirChanged)
        multigitWidget.sig_dir_changed.connect(self.updateRecentDirMenu)
        multigitWidget.sig_request_dir_open.connect( self.slotOpenDir )
        multigitWidget.repoTree.itemSelectionChanged.connect( self.updateStatusBar )
        self.slotViewTabChanged()
        return tabIdx


    def addTab(self, base_dir: Optional[str], pos: int = -1) -> int:
        '''Add a new tab, by default at the end of the tab page. If pos is specified, position of the new tab.
        If base_dir is None, a new empty tab is added

        Return the index of the new tab.
        '''
        tabIdx = self.slotAddTab(pos)
        if base_dir is not None:
            cast(MgMultigitWidget, self.tabRepos.widget(tabIdx)).openDir(base_dir)
        return tabIdx


    def slotDupTab(self) -> None:
        '''Duplicate the current active tab'''
        currentBaseDir = self.currentMultigit().multiRepo.base_dir
        tabIdx = self.slotAddTab()
        self.multigitWidgetFromIdx(tabIdx).openDir( currentBaseDir  )


    def slotRenameTab(self) -> None:
        '''Open a dialog to rename the active tab'''
        curIdx = self.tabRepos.currentIndex()
        oldName = self.tabRepos.tabText(curIdx)
        self.tabRepos.setTabText(curIdx, '')
        tabRenameLineEdit = QLineEdit(oldName)
        self.tabRepos.tabBar().setTabButton(curIdx, QTabBar.LeftSide, tabRenameLineEdit)
        tabRenameLineEdit.selectAll()
        tabRenameLineEdit.setFocus()

        def setNewName() -> None:
            self.tabRepos.setTabText(curIdx, tabRenameLineEdit.text())
            self.tabRepos.tabBar().setTabButton(curIdx, QTabBar.LeftSide, None)     # type: ignore[arg-type]    # the None is not accepted in the stubs yet

        tabRenameLineEdit.returnPressed.connect(setNewName)


    def slotCloseTab(self) -> None:
        '''Close the current tab, unless it is the last one.'''
        if self.tabRepos.count() <= 1:
            QMessageBox.warning(self, 'Can not close tab', 'Can not close last tab!\nOperation canceled.')
            return
        self.tabRepos.removeTab(self.tabRepos.currentIndex())


    def slotCurrentTabChanged(self, tabIdx: int) -> None:
        '''Called when active tab changes'''
        baseDir = self.currentMultigit().multiRepo.base_dir
        self.updateWindowTitleFromBaseDir(baseDir)


    def slotTabBaseDirChanged(self, baseDir: str) -> None:
        '''Called when opening a new base directory in a tab'''
        dirName = pathlib.Path(baseDir).name
        tabidx = self.tabRepos.currentIndex()
        self.tabRepos.setTabToolTip(tabidx, baseDir)
        self.tabRepos.setTabText(tabidx, dirName)
        self.updateWindowTitleFromBaseDir(baseDir)


    def updateWindowTitleFromBaseDir(self, baseDir: str) -> None:
        if len(baseDir):
            self.setWindowTitle('MultiGit OpenSource v{} - {}'.format(VERSION, baseDir))
            self.updateStatusBar()
        else:
            self.setWindowTitle('MultiGit OpenSource v{}'.format(VERSION))
            self.updateStatusBar()


    def updateStatusBar(self) -> None:
        if self.currentMultigit() is None:
            self.statusbar.clearMessage()
            return

        nbRepo = len(self.currentMultigit().multiRepo)
        nbRepoSelected = len(self.currentMultigit().selectedItems())
        msg = f'{nbRepo} repositories, {nbRepoSelected} selected'
        self.statusbar.showMessage(msg, 0)


