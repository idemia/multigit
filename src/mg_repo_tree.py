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


from typing import List, Any, Optional, Dict, Callable, cast
import logging, subprocess

from PySide2.QtWidgets import QTreeWidget, QMenu, QAction, QApplication, QMessageBox, QAbstractItemView, QTreeWidgetItem
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, QPoint

from src.mg_const import COL_UPDATE, COL_REPO_NAME, COL_NB, COL_TITLES, COL_SHA1, DoubleClickActions, COL_URL
from src import mg_config as mgc
from src.mg_tools import ExecTortoiseGit, ExecGitBash, ExecSourceTree, ExecSublimeMerge, ExecGit, ExecGitK
from src.mg_repo_info import MgRepoInfo
from src.mg_repo_tree_item import MgRepoTreeItem
from src.mg_exec_window import MgExecWindow
from src.mg_dialog_view_properties import runDialogGitProperties
from src.mg_dialog_settings import runDialogEditSettings
from src.mg_actions import MgActions
from src.mg_plugin_mgr import pluginMgrInstance

logger = logging.getLogger('mg_repo_tree')
dbg = logger.debug
warn = logger.warning

'''
What to keep in mg_window:
--------------------------
- Everything related to window menu management
- everything related to main window: last commit, last file, ...

What to put in mg_repo_tree:
----------------------------
- operations specific to the repo being listed in the view
    + the rmb menu
    + operations related to selected items
'''


class MgRepoTree(QTreeWidget):
    '''Widget managing a list of repositories'''

    rmbMenu: QMenu
    rmbTgitMenu: QMenu

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)

        # to allow right-mouse-button click signal
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        f = self.header().font()
        f.setBold(True)
        # the column for the refresh icon
        self.headerItem().setText(0, '')
        self.header().setFont(f)
        self.sortByColumn(COL_REPO_NAME, Qt.AscendingOrder)
        self.setColumnWidth(COL_UPDATE, 40)

        if self.columnCount() < COL_NB:
            self.setColumnCount(COL_NB)
            self.setHeaderLabels(COL_TITLES)
            self.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.setAllColumnsShowFocus(True)
            self.header().setSortIndicatorShown(True)

        # calling slot to adjust the status of the column
        self.slotViewColSha1Changed(mgc.get_config_instance().get(mgc.CONFIG_VIEW_COL_SHA1, True))
        self.slotViewColUrlChanged (mgc.get_config_instance().get(mgc.CONFIG_VIEW_COL_URL, True))

        self.gitExecWindow: Optional[MgExecWindow] = None

        self.mgActions = MgActions(self)
        self.rmbMenu = QMenu(self)
        self.mgActions.setupMenuView(self.rmbMenu)
        self.rmbGitMenu = self.rmbMenu.addMenu("Git")
        self.rmbGitMenu.setIcon(QIcon(":/img/git_black.png"))
        self.mgActions.setupMenuGit(self.rmbGitMenu)
        self.mgActions.setupMenuGitPrograms(self.rmbMenu, includeConfigureGitPrograms=False)
        self.setupConnections()
        pluginMgrInstance.setupRepoRmbMenu(self)


    def clear(self) -> None:
        '''Called when clearing the list of repoItem and also of removing all repoInfo items.'''
        # we want to disconnect all signals emitted from repoInfo to our items, to avoid C++ object already
        # deleted being called by Python objects still present
        for repoItem in self.allRepoItems():
            # disconnect all signals, what so ever
            # it does not work on PySide2
            # QObject.disconnect(cast(QObject, repoItem.repoInfo))
            pass

        super().clear()


    def slotViewColSha1Changed(self, showColSha1: bool) -> None:
        '''Called when menu item View->Columns->Sha1 changes value'''
        self.setColumnHidden(COL_SHA1, not showColSha1)
        if showColSha1:
            # ensure that sha1 information is fetched from all repos
            for repoItem in self.allRepoItems():
                repoItem.repoInfo.ensure_sha1(repoItem.cbSha1available)


    def slotViewColUrlChanged(self, showColUrl: bool) -> None:
        '''Called when menu item View->Columns->Url changes value'''
        self.setColumnHidden(COL_URL, not showColUrl)
        if showColUrl:
            # ensure that URL information is fetched from all repos
            for repoItem in self.allRepoItems():
                repoItem.repoInfo.ensure_url(repoItem.cbUrlAvailable)


    def availableScmUpdated(self) -> None:
        '''Called when the configuration for available SCM has changed, to update our RMB menu'''
        self.mgActions.enableAvailableScm()


##########################################################################
#
#       Menu and actions setup
#
##########################################################################

    def setupConnections(self) -> None:
        '''Install all action connections'''

        self.customContextMenuRequested.connect(self.slotContextMenuRequested)
        self.itemActivated.connect(self.slotItemActivated)

        # menu Edit
        self.mgActions.actionRefreshSelected.triggered.connect(self.slotRefreshSelected)
        self.mgActions.actionShowInExplorer.triggered.connect(self.slotShowInExplorer)
        self.mgActions.menuCopy.triggered.connect(self.slotMenuCopyAction)

        # Menu Git
        self.mgActions.actionGitProperties.triggered.connect(self.slotGitProperties)
        self.mgActions.actionGitCommit.triggered.connect(self.slotGitCommit)
        self.mgActions.actionGitRevert.triggered.connect(self.slotGitRevert)
        self.mgActions.actionGitPush.triggered.connect(self.slotGitPush)
        self.mgActions.actionGitPushTag.triggered.connect(self.slotGitPushTag)
        self.mgActions.actionGitPull.triggered.connect(self.slotGitPull)
        self.mgActions.actionGitFetch.triggered.connect(self.slotGitFetch)
        self.mgActions.actionGitTag.triggered.connect(self.slotGitTag)
        self.mgActions.actionGitCreateBranch.triggered.connect(self.slotGitCreateBranch)
        self.mgActions.actionGitSwitchBranch.triggered.connect(self.slotGitSwitchBranch)
        self.mgActions.actionGitCheckoutTag.triggered.connect(self.slotGitCheckoutTag)
        self.mgActions.actionGitDeleteBranch.triggered.connect(self.slotGitDeleteBranch)
        self.mgActions.actionGitBash.triggered.connect(self.slotGitBash)
        self.mgActions.actionGitRunCommand.triggered.connect(self.slotGitRunCommand)

        # Menu Git programs
        self.mgActions.actionSourceTree.triggered.connect(self.slotSourcetree)
        self.mgActions.actionSublimeMerge.triggered.connect(self.slotSublimemerge)
        self.mgActions.actionGitGui.triggered.connect(self.slotGitGui)
        self.mgActions.actionGitK.triggered.connect(self.slotGitK)

        self.mgActions.actionTGitShowLog  .triggered.connect(self.slotTGitShowLog)
        self.mgActions.actionTGitCommit   .triggered.connect(self.slotTGitCommit)
        self.mgActions.actionTGitDiff     .triggered.connect(self.slotTGitDiff)
        self.mgActions.actionTGitRevert   .triggered.connect(self.slotTGitRevert)
        self.mgActions.actionTGitPush     .triggered.connect(self.slotTGitPush)
        self.mgActions.actionTGitPull     .triggered.connect(self.slotTGitPull)
        self.mgActions.actionTGitFetch    .triggered.connect(self.slotTGitFetch)
        self.mgActions.actionTGitTag      .triggered.connect(self.slotTGitTag)
        self.mgActions.actionTGitSwitch   .triggered.connect(self.slotTGitSwitch)
        self.mgActions.actionTGitBranch   .triggered.connect(self.slotTGitBranch)

        self.mgActions.menuCopy.aboutToShow.connect(self.slotMenuCopyAboutToShow)
        self.mgActions.menuCopy.aboutToHide.connect(self.slotMenuCopyAboutToHide)


    def slotContextMenuRequested(self, p: QPoint) -> None:
        '''Capture the right-button mouse release action to display a menu'''
        self.rmbMenu.exec_(self.viewport().mapToGlobal(p)) # qme.globalPos())


##########################################################################
#
#       Item and repo management
#
##########################################################################

    def deleteRepos(self, deletedRepo: List[MgRepoInfo]) -> None:
        '''Remove all the items related to the listed repositories'''
        for repoInfo in deletedRepo:
            for itemIdx in range(self.topLevelItemCount()):
                if self.topLevelItem(itemIdx).text(COL_REPO_NAME) == repoInfo.name:     # type: ignore # topLevelItem(itemIdx) exists and is not None
                    self.takeTopLevelItem(itemIdx)
                    break  # we only have one such item per repo, no need to continue searching
            else:
                warn('Item not found for deleted repo: %s' % repoInfo.name)

        # show visually that the repo were deleted
        QApplication.processEvents()


    def addRepos(self, repoInfoList: List[MgRepoInfo]) -> List[MgRepoTreeItem]:
        '''Add the listed repos as items to this repoTree.
        Return the list of MgRepoTreeItem created'''
        noSelectedItem = (self.topLevelItemCount() == 0)

        items: List[MgRepoTreeItem] = []

        # first step, we fill the list of repo
        for repoInfo in repoInfoList:
            item = MgRepoTreeItem(repoInfo, self)
            items.append(item)
            if noSelectedItem:
                self.setCurrentItem(item)
                noSelectedItem = False

            self.autoAdjustColumnSize()

        return items


    def autoAdjustColumnSize(self) -> None:
        '''Adjust automatically the column size to the largest item'''
        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)
        QApplication.processEvents()


    def selectedRepoItems(self) -> List[MgRepoTreeItem]:
        '''Return the list of selected MgRepoTreeItem'''
        items = cast(List[MgRepoTreeItem], list(super().selectedItems()))
        return items


    def selectedRepos(self) -> List[MgRepoInfo]:
        '''Return the list of selected Repositories'''
        repos = [item.repoInfo for item in self.selectedRepoItems()]
        return repos


    def allRepos(self) -> List[MgRepoInfo]:
        '''Return the list of all Repositories'''
        repos = [item.repoInfo for item in self.allRepoItems()]
        return repos


    def allRepoItems(self) -> List[MgRepoTreeItem]:
        '''Return the list of all MgRepoTreeItem of the widget'''
        items = []
        for idx in range(self.topLevelItemCount()):
            items.append(cast(MgRepoTreeItem, self.topLevelItem(idx)))
        return items

##########################################################################
#
#       Actions on selected items
#
##########################################################################

    def getGitExecWindow(self) -> MgExecWindow:
        '''Get the running git execution window if any, or create it if necessary'''
        if self.gitExecWindow is None:
            self.gitExecWindow = MgExecWindow(self)
            self.gitExecWindow.finished.connect(self.clearGitExecWindow)
        return self.gitExecWindow


    def clearGitExecWindow(self) -> None:
        '''Called when execution is done, to clear the variable.

        That way, new tasks will use a new instance.'''
        # this prevents a bug where the window was hidden but still visible when hovering
        # over the taskbar window of MultiGit
        del self.gitExecWindow
        self.gitExecWindow = None


    def confirmIfNoSelectedItems(self) -> bool:
        '''Display a warning of no items are selected and return False. Return True if everything is OK'''
        items = self.selectedRepoItems()
        if len(items) == 0:
            QMessageBox.warning(self, 'No repository selected',
                                'Warning: you must select at least one repository to run this command!')
            return False
        return True


    def confirmIfTooManySelectedItems(self, dialogName: str) -> bool:
        '''If too many items are selected, ask the user to confirm the action.
        Returns True if the user confirmed, else False.
        '''
        items = self.selectedRepoItems()
        if len(items) <= 3:
            return True
        
        buttonSelected = QMessageBox.warning(self, 'Many repositories selected',
                                             'You are about to launch %d %s\nDo you want to continue ?' % (len(items), dialogName),
                                             QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)
        return not (buttonSelected != QMessageBox.Ok)


    def confirmIfNoOrTooManySelectedItems(self, dialogName: str) -> bool:
        '''Convenience method grouping confirmIfNoSelectedItems() and confirmIfTooManySelectedItems().
        Returns False if we should abort processing
        '''
        return self.confirmIfTooManySelectedItems(dialogName) and self.confirmIfNoSelectedItems()


    def slotItemActivated(self, _item: QTreeWidgetItem, _col: int) -> None:
        '''Called when user double-clicked or presses enter on an item. Call user-defined action'''
        dbg('slotItemActivated()')

        actionToPerform = {
            DoubleClickActions.GitCommit.value           : self.slotGitCommit,
            DoubleClickActions.GitCreateBranch.value     : self.slotGitCreateBranch,
            DoubleClickActions.GitSwitchBranch.value     : self.slotGitSwitchBranch,
            DoubleClickActions.GitPush.value             : self.slotGitPush,
            DoubleClickActions.GitPull.value             : self.slotGitPull,
            DoubleClickActions.GitFetch.value            : self.slotGitFetch,

            DoubleClickActions.TortoiseGitShowLog.value  : self.slotTGitShowLog,
            DoubleClickActions.TortoiseGitSwitch.value   : self.slotTGitSwitch,
            DoubleClickActions.TortoiseGitBranch.value   : self.slotTGitBranch,
            DoubleClickActions.TortoiseGitCommit.value   : self.slotTGitCommit,
            DoubleClickActions.TortoiseGitDiff.value     : self.slotTGitDiff,
            DoubleClickActions.TortoiseGitPush.value     : self.slotTGitPush,
            DoubleClickActions.TortoiseGitPull.value     : self.slotTGitPull,
            DoubleClickActions.TortoiseGitFetch.value    : self.slotTGitFetch,

            DoubleClickActions.RunSourceTree.value       : self.slotSourcetree,
            DoubleClickActions.RunSublimeMerge.value     : self.slotSublimemerge,
            DoubleClickActions.RepositoryProperties.value: self.slotGitProperties,
            DoubleClickActions.ShowInExplorer.value      : self.slotShowInExplorer,
            DoubleClickActions.DoNothing.value           : lambda: None,
        } # type: Dict[str, Callable[[], None]]

        if mgc.get_config_instance()[mgc.CONFIG_DOUBLE_CLICK_ACTION] in actionToPerform:
            actionToPerform[mgc.get_config_instance()[mgc.CONFIG_DOUBLE_CLICK_ACTION]]()
        else:
            button = QMessageBox.question(self, "Action for double-click", "Action for double-click is not yet defined.\nDo you want to open the settings dialog to define it ?")
            if button == QMessageBox.Yes:
                runDialogEditSettings(self, tabPage=0)


    def slotRefreshSelected(self) -> None:
        dbg('slotRefreshSelected()')
        if not self.confirmIfNoSelectedItems():
            return
        self.doRefreshItems(self.selectedRepoItems())


    def doRefreshItems(self, items: List[MgRepoTreeItem]) -> None:
        for it in items:
            # clear items before updating them, this is better visually
            it.markItemInProgress()

        for it in items:
            it.repoInfo.refresh()


    def slotMenuCopyAboutToShow(self) -> None:
        '''Called when user clicked on the copy submenu. Fills the items of the menu'''
        items = self.selectedRepoItems()
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


    def slotMenuCopyAction(self, action: QAction) -> None:
        '''An item in the copy menu has been selected'''
        text = action.text()
        dbg(f'slotMenuCopyAction() - setting clipboard to "{text}"')
        QApplication.clipboard().setText(text)


    def slotShowInExplorer(self) -> None:
        '''Open one explorer window for each git repo'''
        dbg('slotShowInExplorer()')
        if not self.confirmIfNoOrTooManySelectedItems('Explorer'):
            return

        for it in self.selectedRepoItems():
            cmdline = ['explorer', it.repoInfo.fullpath]
            dbg('Executing: %s' % str(cmdline))
            subprocess.Popen(cmdline)


    ##########################################################################
    #
    #       Git actions
    #
    ##########################################################################

    def runGitCommand(self, desc: str, cmd: List[str]) -> None:
        '''Run a git command on all selected repos

        desc: a description of the command to run, used as title of the execution dialog
        cmd: a list of string of a git command to run, without the git itself

        Dialog rejecting command if no item is selected should be shown prior to calling this.
        '''
        items = self.selectedRepoItems()
        if len(items) == 0:
            QMessageBox.warning(self, 'No repository selected',
                                'Warning: you must select at least one repository to run this command!')
            return

        # collect all repos to act upon
        repos = [ item.repoInfo for item in items ]

        # show window for executing git
        self.getGitExecWindow().execOneGitCommand(desc, cmd, repos)


    def slotGitProperties(self) -> None:
        dbg('slotGitProperties()')
        if not self.confirmIfNoSelectedItems():
            return
        runDialogGitProperties(self, self.selectedRepoItems()[0].repoInfo)


    def slotGitCommit(self) -> None:
        '''Commit on all listed repos'''
        dbg('slotGitCommit()')
        if not self.confirmIfNoSelectedItems():
            return

        # local import to avoid circular dependency
        from src.mg_dialog_git_commit import runDialogGitCommit
        runDialogGitCommit(self, self.selectedRepos(), self.allRepos())


    def slotGitRevert(self) -> None:
        '''Run git Revert on all listed repos'''
        dbg('slotGitRevert()')
        if not self.confirmIfNoSelectedItems():
            return

        # local import to avoid circular dependency
        from src.mg_dialog_git_revert import runDialogGitRevert
        runDialogGitRevert(self, self.selectedRepos(), self.allRepos())


    def slotGitPush(self) -> None:
        '''Run git Push on all listed repos'''
        dbg('slotGitPush()')
        if not self.confirmIfNoSelectedItems():
            return
        items = self.selectedRepoItems()

        desc = 'Pushing current branch'

        repoAndListOfGitCmd = []
        # collect all repos to act upon
        repos = [item.repoInfo for item in items]
        for repoInfo in repos:
            cmd = ['push', '-u', '--progress', '--verbose', 'origin', '{0}'.format(repoInfo.branch)]
            repoAndListOfGitCmd.append(('Push branch %s' % repoInfo.branch,
                                        repoInfo,
                                        [cmd],
                                        ))

        # show window for executing git
        self.getGitExecWindow().execEachRepoWithHisSeqOfGitCommand(desc, repoAndListOfGitCmd)


    def slotGitPushTag(self) -> None:
        '''Choose tags to push for all repos'''
        dbg('slotGitPushTag()')
        if not self.confirmIfNoSelectedItems():
            return

        from src.mg_dialog_git_push_tag import runDialogGitPushTag
        runDialogGitPushTag(self, self.selectedRepos(), self.allRepos())



    def slotGitPull(self) -> None:
        '''Run git Pull on all listed repos'''
        dbg('slotGitPull()')
        # checking for empty selected repos is done inside runGitCommand()
        self.runGitCommand('Pulling repositories', ['pull', '--verbose'])


    def slotGitFetch(self) -> None:
        '''Run git fetch on all listed repos'''
        dbg('slotGitFetch()')
        # checking for empty selected repos is done inside runGitCommand()
        self.runGitCommand('Fetching repositories', ['fetch', '--verbose', '--prune'])


    def slotGitTag(self) -> None:
        '''Run git Tag on all listed repos'''
        dbg('slotGitTag()')
        if not self.confirmIfNoSelectedItems():
            return

        # local import to prevent circular dependencies
        from src.mg_dialog_git_tag import runDialogGitTag
        runDialogGitTag(self, self.selectedRepos(), self.allRepos())


    def slotGitCreateBranch(self) -> None:
        '''Create a branch on all listed repos'''
        dbg('slotGitCreateBranch()')
        if not self.confirmIfNoSelectedItems():
            return

        # local import to prevent circular dependencies
        from src.mg_dialog_git_create_branch import runDialogGitCreateBranch
        runDialogGitCreateBranch(self, self.selectedRepos(), self.allRepos())


    def slotGitSwitchBranch(self) -> None:
        '''Switch to a branch on all listed repos'''
        dbg('slotGitSwitchBranch()')
        # local import to prevent circular dependencies
        from src.mg_dialog_git_switch_delete_branch import runDialogGitSwitchDelete, DeleteOrSwitch
        runDialogGitSwitchDelete(self, DeleteOrSwitch.SWITCH_BRANCH, self.selectedRepos(), self.allRepos())


    def slotGitCheckoutTag(self) -> None:
        '''Switch to a tag on all listed repos'''
        dbg('slotGitCheckoutTag()')
        # local import to prevent circular dependencies
        from src.mg_dialog_git_switch_delete_branch import runDialogGitSwitchDelete, DeleteOrSwitch
        runDialogGitSwitchDelete(self, DeleteOrSwitch.CHECKOUT_TAG, self.selectedRepos(), self.allRepos())


    def slotGitDeleteBranch(self) -> None:
        '''Delete branch on all listed repos'''
        dbg('slotGitDeleteBranch()')
        # local import to prevent circular dependencies
        from src.mg_dialog_git_switch_delete_branch import runDialogGitSwitchDelete, DeleteOrSwitch
        runDialogGitSwitchDelete(self, DeleteOrSwitch.DELETE, self.selectedRepos(), self.allRepos())


    def slotGitBash(self) -> None:
        '''Run git-bash on the current repos'''
        dbg('slotGitBash')
        if not self.confirmIfNoOrTooManySelectedItems('Git bash'):
            return

        try:
            for item in self.selectedRepoItems():
                repo = item.repoInfo
                # after git bash, we also want to refresh the URL
                ExecGitBash.exec_non_blocking([repo.fullpath], callback=repo.deepRefresh)
        except FileNotFoundError:
            # Git Bash was not located
            QMessageBox.warning(self, 'Unable to execute Git Bash', 'Warning: could not locate the git-bash.exe program.\n' +
                                'Can not execute any Git Bash command..\nPlease configure the location in the settings dialog.\n')
            self.mgActions.actionGitBash.setEnabled(False)


    def slotGitRunCommand(self) -> None:
        '''Run a custom git command'''
        dbg('slotGitRunCommand')
        if not self.confirmIfNoSelectedItems():
            return

        # local import to prevent circular dependencies
        from src.mg_dialog_git_run_cmd import runDialogGitCommand
        runDialogGitCommand(self, self.selectedRepos(), self.allRepos())



    ##########################################################################
    #
    #       TortoiseGit actions
    #
    ##########################################################################

    def tortoiseGitCommandOnSelection(self, dialogName: str, cmd: str) -> None:
        '''Verify the condition for running a TortoiseGit dialog.

        Check that one repository is selected, if not warn the user.
        If too many repositories are selected, ask the user to validate.

        dialogName: the name of the dialog to subtitute in the error message
        cmd: the tortoise git command to run
        '''
        if not self.confirmIfNoOrTooManySelectedItems(dialogName):
            return

        self.tortoiseGitCommandOnItems(cmd, self.selectedRepoItems())


    def tortoiseGitCommandOnItems(self, cmd: str, items: List[MgRepoTreeItem]) -> None:
        '''Run a Tortoise Git command on all repos passed in argument'''
        try:
            for item in items:
                repo = item.repoInfo
                # put the path parameter in a separate argument, see: https://gitlab.com/tortoisegit/tortoisegit/-/issues/3518
                ExecTortoiseGit.exec_non_blocking(['/path', repo.fullpath, '/command:%s' % cmd], callback=repo.refresh)
        except FileNotFoundError:
            # TortoiseGit was not located
            QMessageBox.warning(self, 'Unable to execute TortoiseGit', 'Warning: could not locate the TortoiseGitProc.exe program.\n' +
                                'Can not execute any TortoiseGit command..\nPlease configure the location in the settings dialog.\n')


    def slotTGitShowLog(self) -> None:
        dbg('slotTGitShowLog()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Show Log', 'log')


    def slotTGitCommit(self) -> None:
        dbg('slotTGitCommit()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Commit', 'commit')


    def slotTGitDiff(self) -> None:
        dbg('slotTGitDiff()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Diff', 'diff')


    def slotTGitRevert(self) -> None:
        dbg('slotTGitRevert()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Revert', 'revert')


    def slotTGitPull(self) -> None:
        dbg('slotTGitPull()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Pull', 'pull')


    def slotTGitPush(self) -> None:
        dbg('slotTGitPush()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Push', 'push')


    def slotTGitFetch(self) -> None:
        dbg('slotTGitFetch()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Fetch', 'fetch')


    def slotTGitTag(self) -> None:
        dbg('slotTGitTag()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Tag', 'tag')


    def slotTGitSwitch(self) -> None:
        dbg('slotTGitSwitch()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Switch', 'switch')


    def slotTGitBranch(self) -> None:
        dbg('slotTGitBranch()')
        self.tortoiseGitCommandOnSelection('TortoiseGit Branch', 'branch')


    ##########################################################################
    #
    #       Other actions
    #
    ##########################################################################


    def slotSourcetree(self) -> None:
        '''Run sourcetree on the current repos'''
        dbg('slotSourcetree')
        if not self.confirmIfNoOrTooManySelectedItems('SourceTree'):
            return

        try:
            for item in self.selectedRepoItems():
                repo = item.repoInfo
                # run sourcetree
                ExecSourceTree.exec_non_blocking(['-t', str(repo.fullpath)], callback=repo.refresh)
        except FileNotFoundError:
            # TortoiseGit was not located
            QMessageBox.warning(self, 'Unable to execute SourceTree', 'Warning: could not locate the SourceTree.exe program.\n' +
                                'Can not execute any SourceTree command..\nPlease configure the location in the settings dialog.\n')
            self.mgActions.actionSourceTree.setEnabled(False)


    def slotGitGui(self) -> None:
        '''Run git Gui on the current repos'''
        dbg('slotGitGui')
        if not self.confirmIfNoOrTooManySelectedItems('Git GUI'):
            return

        try:
            for item in self.selectedRepoItems():
                repo = item.repoInfo
                # allow errors needed because git-gui never returns 0
                ExecGit.exec_non_blocking(['gui'], workdir=str(repo.fullpath), allow_errors=True, callback=repo.refresh)
        except FileNotFoundError:
            QMessageBox.warning(self, 'Unable to execute Git GUI', 'Warning: could not locate the git-gui.exe program.\n' +
                                'Can not execute any git-gui command..\nPlease configure the location in the settings dialog.\n')
            self.mgActions.actionGitGui.setEnabled(False)


    def slotSublimemerge(self) -> None:
        '''Run SublimeMewrge on the current repos'''
        dbg('slotSublimemerge')
        if not self.confirmIfNoOrTooManySelectedItems('Sublime Merge'):
            return

        try:
            for item in self.selectedRepoItems():
                repo = item.repoInfo
                ExecSublimeMerge.exec_non_blocking([str(repo.fullpath)], callback=repo.refresh)
        except FileNotFoundError:
            # TortoiseGit was not located
            QMessageBox.warning(self, 'Unable to execute SublimeMerge', 'Warning: could not locate the SublimeMerge.exe program.\n' +
                                'Can not execute any SublimeMerge command..\nPlease configure the location in the settings dialog.\n')
            self.mgActions.actionSublimeMerge.setEnabled(False)


    def slotGitK(self) -> None:
        '''Run GitK on the current repos'''
        dbg('slotGitK')
        if not self.confirmIfNoOrTooManySelectedItems('GitK'):
            return

        try:
            for item in self.selectedRepoItems():
                repo = item.repoInfo
                # ExecGitK.exec_non_blocking([], workdir=str(repo.fullpath), callback=repo.refresh)
                ExecGitK.exec_non_blocking([], workdir=str(repo.fullpath), allow_errors=True,callback=repo.refresh)
        except FileNotFoundError:
            QMessageBox.warning(self, 'Unable to execute GitK', 'Warning: could not locate the gitk.exe program.\n' +
                                'Can not execute any GitK command..\nPlease configure the location in the settings dialog.\n')
            self.mgActions.actionSublimeMerge.setEnabled(False)


