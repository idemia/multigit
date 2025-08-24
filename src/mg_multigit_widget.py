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


from typing import cast, List, Optional, Dict
import logging, pathlib

from PySide6.QtWidgets import QMessageBox, QApplication, QWidget
from PySide6.QtCore import Qt, Signal, QByteArray, QTimer, QPoint

from src.mg_repo_info import MultiRepo
from src.mg_repo_tree_item import MgRepoTreeItem
from src.mg_repo_tree import TWI_TYPE_GROUP
from src.mg_utils import htmlize_diff
from src import mg_config as mgc
from src.mg_const import COL_REPO_NAME, MAX_DIFF_LINES
from src.gui.ui_multigit_widget import Ui_MultigitWidget

logger = logging.getLogger('mg_multigit_widget')
dbg = logger.debug
info = logger.info


class MgMultigitWidget(QWidget, Ui_MultigitWidget):

    multiRepo: MultiRepo

    sig_request_dir_open = Signal()
    sig_dir_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        # we need to apply this after setupUi()
        self.repoTree.configureColumns()

        self.multiRepo = MultiRepo('')

        self.config = mgc.get_config_instance()

        # basedir buttons
        self.buttonHistoryBaseDir.historyItemTriggered.connect( lambda title, message: self.openDir(title) )
        self.buttonHistoryBaseDir.fillHistory(self.config.lruAsList(mgc.CONFIG_LAST_OPENED))
        self.buttonOpenBaseDir.clicked.connect(self.sig_request_dir_open)


        if self.config[mgc.CONFIG_SPLITTER_STATE_V2]:
            state: List[int] =  self.config[mgc.CONFIG_SPLITTER_STATE_V2]
            bstate = QByteArray(bytes(state))
            self.splitter.restoreState(bstate)
        elif self.config[mgc.CONFIG_SPLITTER_STATE]:
            self.splitter.restoreState(self.config[mgc.CONFIG_SPLITTER_STATE_V2])

        self.repoTree.itemSelectionChanged.connect(self.slotItemSelectionChanged)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect( self.slotTabWidgetIndexChanged )


##########################################################################
#
#       Methods related to the display updates and internal machinery
#
##########################################################################

    def setBaseDir(self, baseDir: Optional[str]) -> None:
        '''Set the base directory from which all git repos are searched.'''
        dbg('setBaseDir( %s )' % str(baseDir) )

        if baseDir and not pathlib.Path(baseDir).exists():
            QMessageBox.warning(self, 'Could not open path', 'Error: could not open path: %s' % baseDir)
            return

        self.sig_dir_changed.emit( baseDir or '' )
        self.repoTree.clear()
        if baseDir is None:
            self.lineEditBaseDir.setEnabled(False)
            self.lineEditBaseDir.setText("")
            self.multiRepo = MultiRepo('')
            return

        self.lineEditBaseDir.setEnabled(True)
        self.lineEditBaseDir.setText(baseDir)
        self.multiRepo = MultiRepo(baseDir)
        QTimer.singleShot(0, self.fillRepoView)


    def fillRepoView(self) -> None:
        '''Fill the repoTree with the repository information'''
        dbg('fillRepoView()')
        if self.multiRepo.isEmpty():
            # very first launch of MultiGit without base dir defined
            # or selection of a directory with no git repo
            self.repoTree.clear()
            return

        self.repoTree.setFocus(Qt.FocusReason.OtherFocusReason)
        try:
            self.setCursor(Qt.CursorShape.WaitCursor)
            QApplication.processEvents()
            # we keep that one blocking, it's very quick anyways
            self.multiRepo.find_git_repos()

            items = self.repoTree.addRepos(self.multiRepo.repo_list)

        finally:
            # all items are visible now, we can restore the cursor
            self.setCursor(Qt.CursorShape.ArrowCursor)

        # 2nd step, we fill the repo information
        for it in items:
            it.repoInfo.refresh()


    def slotItemSelectionChanged(self) -> None:
        items = self.repoTree.selectedRepoItems()
        dbg('slotItemSelectionChanged() - %d items, %s' % (len(items), items[0].text(COL_REPO_NAME) if len(items) else ''))

        if not self.tabWidget.isVisible():
            # if tab widget is not visible, we don't need to update its content when current item changes
            return

        if len(items) == 0:
            # nothing is selected
            self.textEditModFiles.setText('')
            self.textEditCommit.setText('')
            return

        # force refresh of the correct tab item
        self.slotTabWidgetIndexChanged(self.tabWidget.currentIndex())


    def slotTabWidgetIndexChanged(self, idx: int) -> None:
        '''Called when the tab widget between diff and modified files is changed'''
        dbg('slotTabWidgetIndexChanged(%d)' % idx)
        items = self.repoTree.selectedRepoItems()
        if len(items) == 0:
            return

        currentRepo = items[0].repoInfo
        if self.tabWidget.widget(idx) == self.tabLastCommit:
            # showing last commit currently
            currentRepo.ensure_last_commit(self.slotSetLastCommit)
        else:
            # showing diff currently
            currentRepo.ensure_diff(self.displayRepoDiff)


    def slotSetLastCommit(self, repo_name: str, last_commit: str) -> None:
        dbg('slotSetLastCommit("%s", ...)' % repo_name)
        currentItem = self.repoTree.currentItem()
        if currentItem is None or currentItem.type() == TWI_TYPE_GROUP:
            return

        currentRepoName = currentItem.text(COL_REPO_NAME)
        if repo_name != currentRepoName:
            logger.warning('Received last commit result for repo "%s" but repo selected is "%s". Call ignored' % (repo_name, currentRepoName))
            # the selection changed between the time where the lastCommit info was requested and it was received
            # just ignore it
            return

        self.textEditCommit.setText(last_commit)


    def displayRepoDiff(self, repo_name: str, repo_diff: str) -> None:
        dbg('displayRepoDiff("%s", ...)' % repo_name)
        currentItem = self.repoTree.currentItem()
        if currentItem is None:
            return

        currentRepoName = currentItem.text(COL_REPO_NAME)
        if repo_name != currentRepoName:
            logger.warning('Received diff result for repo "%s" but repo selected is "%s". Call ignored' % (repo_name, currentRepoName))
            # the selection changed between the time where the lastCommit info was requested and it was received
            # just ignore it
            return

        self.textEditModFiles.setText(htmlize_diff(repo_diff or '', MAX_DIFF_LINES))


    def slotViewTabChanged(self, showTabLastCommit: bool, showTabModFiles: bool) -> None:
        '''Called when the menu Edit->View->Tab Last Commit or View->Tab Modified Files changes'''
        dbg('slotViewTabChanged')
        if (not showTabLastCommit) and (not showTabModFiles):
            # nothing to show in the tab, hide it
            self.tabWidget.setVisible(False)
        else:
            self.tabWidget.setVisible(True)
            showHideTabLastCommitFuncDict = {
                (False, False): lambda: None, # hidden and requested hidden, do nothing
                (False, True):  lambda: self.tabWidget.insertTab(0, self.tabLastCommit, 'Last Commit'),  # hidden and requested visible, show it
                (True, False):  lambda: self.tabWidget.removeTab(self.tabWidget.indexOf(self.tabLastCommit)),
                (True, True) :  lambda: None, # visible and requested visible, do nothing
            }
            showHideTabLastCommitFuncDict[(self.tabWidget.indexOf(self.tabLastCommit) != -1, showTabLastCommit)]()


            showHideTabModFilesFuncDict = {
                (False, False): lambda: None, # hidden and requested hidden, do nothing
                (False, True):  lambda: self.tabWidget.insertTab(1, self.tabModifiedFiles, 'Modified Files'),  # hidden and requested visible, show it
                (True, False):  lambda: self.tabWidget.removeTab(self.tabWidget.indexOf(self.tabModifiedFiles)),
                (True, True) :  lambda: None, # visible and requested visible, do nothing
            }
            showHideTabModFilesFuncDict[(self.tabWidget.indexOf(self.tabModifiedFiles) != -1, showTabModFiles)]()

        # trigger refresh of the tab widget if it was hidden
        self.slotTabWidgetIndexChanged(self.tabWidget.currentIndex())


##########################################################################
#
#       Methods related to menu entries NOT acting on selected items
#
##########################################################################

    def openDir(self, newDir: str, ignoreNonExisting: bool = False) -> None:
        info('Opening dir: %s' % newDir)
        self.buttonHistoryBaseDir.fillHistory(self.config.lruAsList(mgc.CONFIG_LAST_OPENED))
        self.setBaseDir(newDir)


    def slotRefreshAll(self) -> None:
        dbg('slotRefreshAll()')
        self.repoTree.setFocus(Qt.FocusReason.OtherFocusReason)
        try:
            self.setCursor(Qt.CursorShape.WaitCursor)
            QApplication.processEvents()
            # we keep that one blocking, it's very quick anyways
            added_repo, rm_repo = self.multiRepo.find_git_repos_added_removed()

            self.repoTree.deleteRepos(rm_repo)

            # Add items related to new repositories
            self.repoTree.addRepos(added_repo)

        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            QApplication.processEvents()

        # 2nd step, update multi-repo
        self.multiRepo.adjust_git_repos(added_repo, rm_repo)

        # 3rd step: update all the repos
        for it in self.multiRepo.repo_list:
            it.refresh()


    def slotGitFetchAll(self) -> None:
        '''Run git fetch on all repos'''
        dbg('slotGitFetchAll()')
        # collect the items in the order they are shown
        items = [cast(MgRepoTreeItem, self.repoTree.topLevelItem(idx))
                 for idx in range(0, self.repoTree.topLevelItemCount())]
        repos = [item.repoInfo for item in items]

        cmd = ['fetch', '--prune']
        self.repoTree.getGitExecWindow().execOneGitCommand('Fetching all repositories', cmd, repos)



