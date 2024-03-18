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


from typing import List

import functools, logging

from PySide2.QtCore import QMetaObject, QObject
from PySide2.QtGui import QIcon, QPixmap, QTransform
from PySide2.QtWidgets import QAction, QMenu, QWidget

from src.mg_const import SHORT_SHA1_NB_DIGITS
from src.mg_tools import ExecSublimeMerge, ExecTortoiseGit, ExecSourceTree, ExecGitBash, ExecGitGui, ExecGitK
from src.mg_repo_info import MgRepoInfo

logger = logging.getLogger('mg_actions')
dbg = logger.debug


@functools.lru_cache(maxsize=1)
def getFetchIcon() -> QIcon:
    '''Generate the QIcon for fetch and cache it'''
    # Fetch needs push icon, but rotated
    pixmap_push = QPixmap(":/img/tgit_push.ico")
    transform = QTransform()
    transform.rotate(180)
    pixmap_fetch = pixmap_push.transformed(transform)
    return QIcon(pixmap_fetch)


class MgActions(QObject):
    '''Class to hold all the actions which are duplicated between the main window and each MgRepoTree'''

    actionGitFetchAll: QAction          # added externally to MgActions
    actionGitFetchAllOnAllTabs: QAction          # added externally to MgActions

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.menuCopyConnections = []    # type: List[QMetaObject.Connection]

        ######## Edit actions ##########

        self.actionRefreshSelected = QAction(self)
        self.actionRefreshSelected.setText("Refresh selected repositories")
        self.actionRefreshSelected.setShortcut("Ctrl+F5")
        self.actionRefreshSelected.setIcon(QIcon(":img/tgit_refresh.ico"))
        self.actionRefreshSelected.setToolTip("Refresh selected repositories information from disk")

        self.actionShowInExplorer = QAction(self)
        self.actionShowInExplorer.setText("Show in Explorer")
        self.actionShowInExplorer.setShortcut("Ctrl+E")
        self.actionShowInExplorer.setIcon( QIcon(":img/tgit_explorer.ico"))
        self.actionShowInExplorer.setToolTip('Open Explorer for each repository')

        self.actionCopyFullPath = QAction(self)
        self.actionCopyFullPath.setText('...')
        self.actionCopyFullPath.setToolTip('Copy full path to repository')

        self.actionCopyDirectory = QAction(self)
        self.actionCopyDirectory.setText('...')
        self.actionCopyDirectory.setToolTip('Copy relative directory path to base dir')

        self.actionCopyHead = QAction(self)
        self.actionCopyHead.setText('...')
        self.actionCopyHead.setToolTip('Copy HEAD branch name or tag name')

        self.actionCopyShortSha1 = QAction(self)
        self.actionCopyShortSha1.setText('...')
        self.actionCopyShortSha1.setToolTip('Copy short SHA1 of current commit')

        self.actionCopyLongSha1 = QAction(self)
        self.actionCopyLongSha1.setText('...')
        self.actionCopyLongSha1.setToolTip('Copy full SHA1 of current commit')

        self.actionCopyUrl = QAction(self)
        self.actionCopyUrl.setText('...')
        self.actionCopyUrl.setToolTip('Copy remote URL of repository')


        ######## Git actions ##########

        self.actionGitProperties = QAction(self)
        self.actionGitProperties.setText("Git properties")
        self.actionGitProperties.setShortcut("Alt+Return")
        self.actionGitProperties.setIcon(QIcon(":img/icons8-show-property-96.png"))
        self.actionGitProperties.setToolTip('Open dialog showing all properties of the repository')

        self.actionGitCommit = QAction(self)
        self.actionGitCommit.setText("Commit")
        self.actionGitCommit.setShortcut("Ctrl+Shift+C")
        self.actionGitCommit.setIcon(QIcon(":/img/tgit_commit.ico"))
        self.actionGitCommit.setToolTip('Open dialog to commit on the repositories')

        self.actionGitRevert = QAction(self)
        self.actionGitRevert.setText("Revert modified")
        self.actionGitRevert.setShortcut("Ctrl+R")
        self.actionGitRevert.setIcon(QIcon(":/img/tgit_revert.ico"))
        self.actionGitRevert.setToolTip('Open dialog to revert modified files on repositories')

        self.actionGitPush = QAction(self)
        self.actionGitPush.setText("Push")
        self.actionGitPush.setShortcut("Ctrl+P")
        self.actionGitPush.setIcon(QIcon(":/img/tgit_push.ico"))
        self.actionGitPush.setToolTip('Run <code>git push</code> on repositories')

        self.actionGitPushTag = QAction(self)
        self.actionGitPushTag.setText("Push tag")
        self.actionGitPushTag.setIcon(QIcon(":/img/tgit_push.ico"))
        self.actionGitPushTag.setToolTip('Open dialog to choose which tag to push to remote repository on repositories')

        self.actionGitPull = QAction(self)
        self.actionGitPull.setText("Pull")
        self.actionGitPull.setShortcut("Ctrl+Shift+P")
        self.actionGitPull.setIcon(QIcon(":/img/tgit_pull.ico"))
        self.actionGitPull.setToolTip('Run <code>git pull</code> on repositories')

        self.actionGitFetch = QAction(self)
        self.actionGitFetch.setText("Fetch")
        self.actionGitFetch.setShortcut("Ctrl+F")
        self.actionGitFetch.setIcon(getFetchIcon())
        self.actionGitFetch.setToolTip('Run <code>git fetch</code> on repositories')

        self.actionGitTag = QAction(self)
        self.actionGitTag.setText("Tag")
        self.actionGitTag.setShortcut("Ctrl+T")
        self.actionGitTag.setIcon(QIcon(":/img/tgit_tag.ico"))
        self.actionGitTag.setToolTip('Open dialog for setting tag on repositories')

        self.actionGitCreateBranch = QAction(self)
        self.actionGitCreateBranch.setText("Create branch")
        self.actionGitCreateBranch.setShortcut("Ctrl+B")
        self.actionGitCreateBranch.setToolTip('Open dialog for branch creation')

        self.actionGitSwitchBranch = QAction(self)
        self.actionGitSwitchBranch.setText("Switch to branch")
        self.actionGitSwitchBranch.setShortcut("Ctrl+Shift+S")
        self.actionGitSwitchBranch.setToolTip('Open dialog for switching to a branch')

        self.actionGitCheckoutTag = QAction(self)
        self.actionGitCheckoutTag.setText("Checkout tag")
        # self.actionGitCheckoutTag.setShortcut("Ctrl+Shift+S")
        self.actionGitCheckoutTag.setToolTip('Open dialog for checkouting a tag')

        self.actionGitDeleteBranch = QAction(self)
        self.actionGitDeleteBranch.setText("Delete branch")
        self.actionGitDeleteBranch.setShortcut("Ctrl+Shift+D")
        self.actionGitDeleteBranch.setToolTip('Open dialog for deleting a branch')

        self.actionGitBash = QAction(self)
        self.actionGitBash.setText("Git bash here")
        self.actionGitBash.setIcon(QIcon(":/img/git-bash.ico"))
        self.actionGitBash.setToolTip('Open a git bash window for each repository')

        self.actionGitRunCommand = QAction(self)
        self.actionGitRunCommand.setText("Run git command")
        self.actionGitRunCommand.setShortcut("Ctrl+G")
        self.actionGitRunCommand.setToolTip('Open dialog to run a custom git command')

        ### Git Programs actions
        self.actionConfigureGitProgram = QAction(self)
        self.actionConfigureGitProgram.setEnabled(True)
        self.actionConfigureGitProgram.setText("Open settings to configure a Git Program")

        self.actionSublimeMerge = QAction(self)
        self.actionSublimeMerge.setText("Run SublimeMerge")
        self.actionSublimeMerge.setIcon(QIcon(":/img/sublime_merge.ico"))
        self.actionSublimeMerge.setToolTip('Open a SublimeMerge tab for each repository')

        self.actionSourceTree = QAction(self)
        self.actionSourceTree.setText("Run SourceTree")
        self.actionSourceTree.setIcon(QIcon(":/img/sourcetree.ico"))
        self.actionSourceTree.setToolTip('Open a SourceTree tab for each repository')

        self.actionGitGui = QAction(self)
        self.actionGitGui.setText("Run Git GUI")
        # self.actionGitGui.setIcon(QIcon(":/img/sourcetree.ico"))
        self.actionGitGui.setToolTip('Open a git GUI tab for each repository')

        self.actionGitK = QAction(self)
        self.actionGitK.setText("Run GitK")
        # self.actionGitK.setIcon(QIcon(":/img/sourcetree.ico"))
        self.actionGitK.setToolTip('Open a GitK tab for each repository')

        ######## TortoiseGit actions ##########

        self.actionTGitShowLog = QAction(self)
        self.actionTGitShowLog.setText("Show Log")
        self.actionTGitShowLog.setShortcut("Alt+S")
        self.actionTGitShowLog.setIcon(QIcon(":/img/tgit_log.ico"))
        self.actionTGitShowLog.setToolTip('Open TortoiseGit dialog for Show Log')

        self.actionTGitCommit = QAction(self)
        self.actionTGitCommit.setText("Commit")
        self.actionTGitCommit.setShortcut("Alt+C")
        self.actionTGitCommit.setIcon(QIcon(":/img/tgit_commit.ico"))
        self.actionTGitCommit.setToolTip('Open TortoiseGit dialog for Commit')

        self.actionTGitDiff = QAction(self)
        self.actionTGitDiff.setText("Diff")
        self.actionTGitDiff.setShortcut("Alt+D")
        self.actionTGitDiff.setIcon(QIcon(":/img/tgit_diff.ico"))
        self.actionTGitDiff.setToolTip('Open TortoiseGit dialog for Diff')

        self.actionTGitRevert = QAction(self)
        self.actionTGitRevert.setText("Revert")
        self.actionTGitRevert.setShortcut("Alt+R")
        self.actionTGitRevert.setIcon(QIcon(":/img/tgit_revert.ico"))
        self.actionTGitRevert.setToolTip('Open TortoiseGit dialog for Revert')

        self.actionTGitPush = QAction(self)
        self.actionTGitPush.setText("Push")
        self.actionTGitPush.setShortcut("Alt+P")
        self.actionTGitPush.setIcon(QIcon(":/img/tgit_push.ico"))
        self.actionTGitPush.setToolTip('Open TortoiseGit dialog for Push')

        self.actionTGitPull = QAction(self)
        self.actionTGitPull.setText("Pull")
        self.actionTGitPull.setShortcut("Alt+Shift+P")
        self.actionTGitPull.setIcon(QIcon(":/img/tgit_pull.ico"))
        self.actionTGitPull.setToolTip('Open TortoiseGit dialog for Pull')

        self.actionTGitFetch = QAction(self)
        self.actionTGitFetch.setText("Fetch")
        self.actionTGitFetch.setShortcut("Alt+F")
        self.actionTGitFetch.setIcon(getFetchIcon())
        self.actionTGitFetch.setToolTip('Open TortoiseGit dialog for Fetch')

        self.actionTGitTag = QAction(self)
        self.actionTGitTag.setText("Tag")
        self.actionTGitTag.setShortcut("Alt+T")
        self.actionTGitTag.setIcon(QIcon(":/img/tgit_tag.ico"))
        self.actionTGitTag.setToolTip('Open TortoiseGit dialog for Tag')

        self.actionTGitSwitch = QAction(self)
        self.actionTGitSwitch.setText("Switch")
        self.actionTGitSwitch.setShortcut("Alt+W")
        self.actionTGitSwitch.setIcon(QIcon(":/img/tgit_switch.ico"))
        self.actionTGitSwitch.setToolTip('Open TortoiseGit dialog for Switch')

        self.actionTGitBranch = QAction(self)
        self.actionTGitBranch.setText("Branch")
        self.actionTGitBranch.setShortcut("Alt+B")
        self.actionTGitBranch.setIcon(QIcon(":/img/tgit_branch.ico"))
        self.actionTGitBranch.setToolTip('Open TortoiseGit dialog for Branch')


    def setupMenuView(self, menuView: QMenu) -> None:
        '''Install more actions in the menu View'''
        menuView.addAction(self.actionShowInExplorer)
        menuView.addAction(self.actionRefreshSelected)
        self.menuCopy = QMenu('Copy', menuView)
        menuView.addMenu(self.menuCopy)

        '''Setup the internal menu copy used in menu edit'''
        self.menuCopy.setToolTip('Copy repository information to clipboard')
        self.menuCopy.setToolTipsVisible(True)
        self.menuCopy.addAction(self.actionCopyFullPath)
        self.menuCopy.addAction(self.actionCopyDirectory)
        self.menuCopy.addAction(self.actionCopyHead)
        self.menuCopy.addAction(self.actionCopyShortSha1)
        self.menuCopy.addAction(self.actionCopyLongSha1)
        self.menuCopy.addAction(self.actionCopyUrl)



    def setupMenuGit(self, menuGit: QMenu) -> None:
        '''Install all actions in the git menu'''
        menuGit.addAction( self.actionGitProperties)
        menuGit.addAction( self.actionGitCommit )
        menuGit.addAction( self.actionGitRevert )
        menuGit.addAction( self.actionGitPush )
        menuGit.addAction( self.actionGitPushTag )
        menuGit.addAction( self.actionGitPull )
        menuGit.addAction( self.actionGitFetch )
        menuGit.addAction( self.actionGitTag )
        menuGit.addAction( self.actionGitCreateBranch )
        menuGit.addAction( self.actionGitSwitchBranch)
        menuGit.addAction( self.actionGitCheckoutTag)
        menuGit.addAction( self.actionGitDeleteBranch)
        menuGit.addSeparator()
        menuGit.addAction( self.actionGitBash )
        menuGit.addAction( self.actionGitRunCommand )


    def setupMenuGitPrograms(self, menuGitPrograms: QMenu, includeConfigureGitPrograms: bool) -> None:
        '''Install more actions in the GitPrograms menu'''
        menuGitPrograms.addAction(self.actionSourceTree)
        menuGitPrograms.addAction(self.actionSublimeMerge)
        menuGitPrograms.addAction(self.actionGitGui)
        menuGitPrograms.addAction(self.actionGitK)
        self.menuTGit = menuGitPrograms.addMenu("Tortoise Git")
        self.menuTGit.setIcon(QIcon(":/img/tgit_tortoise.ico"))
        self.setupMenuTortoiseGit(self.menuTGit)
        if includeConfigureGitPrograms:
            menuGitPrograms.addAction(self.actionConfigureGitProgram)
        self.enableAvailableScm()


    def setupMenuTortoiseGit(self, menuTGit: QMenu) -> None:
        '''Install all actions in the TortoiseGit menu'''
        menuTGit.addAction( self.actionTGitShowLog )
        menuTGit.addAction( self.actionTGitCommit )
        menuTGit.addAction( self.actionTGitDiff )
        menuTGit.addAction( self.actionTGitRevert )
        menuTGit.addAction( self.actionTGitPush )
        menuTGit.addAction( self.actionTGitPull )
        menuTGit.addAction( self.actionTGitFetch )
        menuTGit.addAction( self.actionTGitTag )
        menuTGit.addAction( self.actionTGitSwitch )
        menuTGit.addAction( self.actionTGitBranch )


    def enableAvailableScm(self) -> None:
        '''Adjust Git Programs menu and RMB menu'''
        showTortoiseGit = ExecTortoiseGit.shouldShow()
        showSourceTree = ExecSourceTree.shouldShow()
        showSublimeMerge = ExecSublimeMerge.shouldShow()
        showGitBash = ExecGitBash.shouldShow()
        showGitGui = ExecGitGui.shouldShow()
        showGitK = ExecGitK.shouldShow()

        # fix menu actions
        self.actionSourceTree.setVisible(showSourceTree)
        self.actionSublimeMerge.setVisible(showSublimeMerge)
        self.actionGitBash.setVisible(showGitBash)
        self.actionGitGui.setVisible(showGitGui)
        self.actionGitK.setVisible(showGitK)
        self.menuTGit.menuAction().setVisible(showTortoiseGit)

        if showTortoiseGit or showSourceTree or showSublimeMerge or showGitGui or showGitK:
            self.actionConfigureGitProgram.setVisible(False)
        else:
            self.actionConfigureGitProgram.setVisible(True)


    def setupDynamicMenuCopy(self, repoInfo: MgRepoInfo) -> None:
        self.actionCopyFullPath.setText(repoInfo.fullpath)
        self.actionCopyDirectory.setText(repoInfo.name)

        if repoInfo.head:
            self.actionCopyHead.setText(repoInfo.head.split(' ')[1])
            self.actionCopyHead.setEnabled(True)
        else:
            self.actionCopyHead.setText('...head...')
            self.actionCopyHead.setEnabled(False)
            # if head is missing, this is because the refresh has not completed yet
            # we just have to wait
            def local_set_head(_repoName: str) -> None:
                self.actionCopyHead.setText(repoInfo.head.split(' ')[1])
                self.actionCopyHead.setEnabled(True)
            self.menuCopyConnections.append( repoInfo.repo_info_available.connect(local_set_head) ) # type: ignore

        if repoInfo.commit_sha1:
            self.actionCopyShortSha1.setText(repoInfo.commit_sha1[:SHORT_SHA1_NB_DIGITS])
            self.actionCopyShortSha1.setEnabled(True)
            self.actionCopyLongSha1.setText(repoInfo.commit_sha1)
            self.actionCopyLongSha1.setEnabled(True)
        else:
            self.actionCopyShortSha1.setText('...short sha1...')
            self.actionCopyShortSha1.setEnabled(False)
            self.actionCopyLongSha1.setText('...sha1...')
            self.actionCopyLongSha1.setEnabled(False)
            # if sha1 is missing, we probably need to request it
            def local_set_sha1(_sha1: str) -> None:
                self.actionCopyShortSha1.setText((repoInfo.commit_sha1 or '')[:SHORT_SHA1_NB_DIGITS])
                self.actionCopyShortSha1.setEnabled(True)
                self.actionCopyLongSha1.setText(repoInfo.commit_sha1 or '')
                self.actionCopyLongSha1.setEnabled(True)
            repoInfo.ensure_sha1(local_set_sha1)

        if repoInfo.url is not None:
            self.actionCopyUrl.setText(repoInfo.url)
            self.actionCopyUrl.setEnabled(True)
        else:
            self.actionCopyUrl.setText('...url...')
            self.actionCopyUrl.setEnabled(False)
            def local_set_url(url: str) -> None:
                self.actionCopyUrl.setText(url)
                self.actionCopyUrl.setEnabled(True)
            repoInfo.ensure_url(local_set_url)


    def clearMenuCopyConnections(self) -> None:
        '''Called when Copy menu is going to hide. We disable the connections created
        by the Copy menu to capture the repo missing info'''
        for c in self.menuCopyConnections:
            if bool(c):
                # QObject.disconnect(c)
                # this is not working in pyside2
                # re-enable it in pyside6
                pass
        self.menuCopyConnections = []




