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


from typing import Any, TYPE_CHECKING, Optional, cast, Tuple
import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QColor, QPalette
from PySide6.QtWidgets import QTreeWidgetItem, QApplication, QWidget, QTreeWidget

from src.mg_utils import extractInt, ignoreCppObjectDeletedError
from src import mg_config as mgc
from src.mg_const import COL_UPDATE, COL_REPO_NAME, COL_HEAD, COL_STATUS, COL_REMOTE_SYNCHRO, DISPLAY_IN_BOLD_MSG, \
    DISPLAY_IN_ITALIC_MSG, COL_SHA1, SHORT_SHA1_NB_DIGITS, COL_URL, MSG_LOCAL_BRANCH, MSG_LOCAL_BRANCH_TOOLTIP, \
    MSG_TOOLTIP_UPDATE, MSG_TOOLTIP_STATUS, MSG_TOOLTIP_REMOTE_SYNCHRO
from src.mg_exec_task_item import getIcon, IconSet
from src.mg_repo_info import MgRepoInfo

dbg = logging.getLogger('mg_repo_tree_item').debug
error = logging.getLogger('mg_repo_tree_item').error

DELTA_ROTATION = 30
TOTAL_ROTATION = 360

from src.mg_utils import istrcmp

from enum import Flag, auto

def shallBoldItalizeSynchro(remote_synchro: str) -> Tuple[bool, bool]:
    '''Return whether message shall be in bold and in italic'''
    doBoldSynchro = False
    for msg in DISPLAY_IN_BOLD_MSG:
        if msg in remote_synchro:
            doBoldSynchro = True
            break

    doItalicSynchro = remote_synchro in DISPLAY_IN_ITALIC_MSG
    return (doBoldSynchro, doItalicSynchro)

class MgRepoTreeItem(QTreeWidgetItem):

    class ColumnFlags(Flag):
        '''Enum to track which column have already been filled'''
        fieldSHA = auto()
        fieldURL = auto()


    def __init__(self, repoInfo: MgRepoInfo, *args: Any) -> None:
        super().__init__(*args)
        self.ignoreUpdates = False
        if self.text(COL_REPO_NAME) == '':
            # we are completely empty, fill with minimalistic information
            self.setText(COL_UPDATE, '')
            self.setText(COL_REPO_NAME, repoInfo.name)
            self.setText(COL_HEAD, '...')
            self.setText(COL_STATUS, '...')
            self.setText(COL_REMOTE_SYNCHRO, '...')

        f = self.font(COL_SHA1)
        f.setFixedPitch(True)
        self.setFont(COL_SHA1, f)

        self.repoInfo = repoInfo
        self.repoInfo.repo_info_available.connect(self.slotRepoInfoAvailable)
        self.repoInfo.repo_update_in_progress.connect(self.slotRepoUpdateInProgress)
        self.repoInfo.repo_deleted.connect(self.slotRepoDeleted)

        self.filledColumns = MgRepoTreeItem.ColumnFlags(0)

        self.setToolTips()


    def setToolTips(self) -> None:
        '''Set tooltip for all columns'''
        self.setToolTip(COL_REPO_NAME, self.repoInfo.name)
        self.setToolTip(COL_STATUS, MSG_TOOLTIP_STATUS)
        self.setToolTip(COL_REMOTE_SYNCHRO, MSG_TOOLTIP_REMOTE_SYNCHRO)


    def clearRepoConnections(self) -> None:
        '''Clear all connections to avoid RunTime errors'''
        dbg('MgRepoTreeItem.clearRepoConnections()')
        # if we do not clear connections, the python MgRepoTreeItem lives longer than the C++ QTreeWidgetItem and
        # we might get RunTime errors when the signal is triggered
        self.ignoreUpdates = True
        self.repoInfo.repo_info_available.disconnect(self.slotRepoInfoAvailable)
        self.repoInfo.repo_update_in_progress.disconnect(self.slotRepoUpdateInProgress)
        self.repoInfo.repo_deleted.disconnect(self.slotRepoDeleted)


    @ignoreCppObjectDeletedError
    def markItemInProgress(self) -> None:
        dbg('markItemInProgress(%s)' % self.repoInfo.name)
        self.setText(COL_UPDATE, '')
        self.setIcon(COL_UPDATE, QIcon(':img/icons8-loader-96.png'))
        self.setToolTip(COL_UPDATE, MSG_TOOLTIP_UPDATE)
        QApplication.processEvents()


    def slotRepoDeleted(self, repo_name: str) -> None:
        '''The repo mapped to this item was deleted'''
        dbg('MgRepoTreeItem.slotRepoDeleted(%s)' % repo_name)
        treeWidget = self.treeWidget()
        # note: when item has already been removed from MgTreeWidget, this is None

        if treeWidget is not None:
            idx = treeWidget.indexOfTopLevelItem(self)
            if idx == -1:
                dbg('Item already deleted')
                return
            treeWidget.takeTopLevelItem(idx)


    def slotRepoUpdateInProgress(self, repo_name: str) -> None:
        '''Called when the update of the repo info has completed'''
        dbg('slotRepoUpdateInProgress(%s)' % repo_name)
        if repo_name != self.repoInfo.name:
            error('Item slotRepoUpdateInProgress() of repo %s is called with argument %s' % (self.repoInfo.name, repo_name))
            error('This happens usually when the base directory is changed while repositories are still fetching information')
            error('We should try a better way to avoid this in the future!')
            return
        self.markItemInProgress()


    @ignoreCppObjectDeletedError
    def slotRepoInfoAvailable(self, repo_name: str) -> None:
        '''Called when the update of the repo info has completed'''
        dbg('slotRepoInfoAvailable(%s)' % repo_name)
        if repo_name != self.repoInfo.name:
            raise AssertionError('Item slotRepoInfoAvailable() of repo %s is called with argument %s' % (self.repoInfo.name, repo_name))
        self.fillRepoItem()


    @ignoreCppObjectDeletedError
    def fillRepoItem(self) -> None:
        '''Fill a QTreeWidgetItem from the associated repoInfo'''
        dbg('fillRepoItem(%s, ...)' % self.repoInfo.name)
        self.setIcon(COL_UPDATE, getIcon(IconSet.Empty))
        self.setText(COL_UPDATE, '')
        self.setToolTip(COL_UPDATE, '')
        self.setText(COL_REPO_NAME, self.repoInfo.name)
        self.setToolTip(COL_REPO_NAME, self.repoInfo.name)
        self.setText(COL_HEAD, self.repoInfo.head)
        self.setText(COL_STATUS, self.repoInfo.status)
        self.setText(COL_REMOTE_SYNCHRO, self.repoInfo.remote_synchro )
        if self.repoInfo.remote_synchro == MSG_LOCAL_BRANCH:
            # add a tooltip to give an easy-fix for the missing remote branch
            self.setToolTip(COL_REMOTE_SYNCHRO, MSG_LOCAL_BRANCH_TOOLTIP)
        else:
            self.setToolTip(COL_REMOTE_SYNCHRO, MSG_TOOLTIP_REMOTE_SYNCHRO)

        # get rid of previous updated state
        self.filledColumns = MgRepoTreeItem.ColumnFlags(0)

        if self.repoInfo.commit_sha1:
            self.setText(COL_SHA1, (self.repoInfo.commit_sha1 or '')[:SHORT_SHA1_NB_DIGITS])
            self.setToolTip(COL_SHA1, self.repoInfo.commit_sha1 or '') # non truncated
            self.filledColumns |= self.ColumnFlags.fieldSHA


        if self.repoInfo.url:
            self.setText(COL_URL, self.repoInfo.url or '')
            self.filledColumns |= self.ColumnFlags.fieldURL


        doBoldStatus = self.repoInfo.status != 'OK'
        f = self.font(COL_STATUS)
        f.setBold(doBoldStatus)
        self.setFont(COL_STATUS, f)

        doColorConflicted = 'conflicted' in self.repoInfo.status
        if doColorConflicted:
            self.setForeground(COL_STATUS, Qt.GlobalColor.red )
        else:
            self.setForeground(COL_STATUS, QApplication.palette().brush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText))

        self.adjustColumnFontFromSynchro(COL_REMOTE_SYNCHRO, self.repoInfo.remote_synchro)

        doColorHeadBranch = 'branch' in self.repoInfo.head
        doColorHeadTag    = 'tag'    in self.repoInfo.head
        if doColorHeadTag or doColorHeadBranch:
            colorRgb = self.foreground(COL_HEAD).color()
            if doColorHeadBranch:
                colorRgb = mgc.get_config_instance().get(mgc.CONFIG_HEAD_COLOR_BRANCH, mgc.DEFAULT_CONFIG_HEAD_COLOR_BRANCH)
            elif doColorHeadTag:
                colorRgb = mgc.get_config_instance().get(mgc.CONFIG_HEAD_COLOR_TAG, mgc.DEFAULT_CONFIG_HEAD_COLOR_TAG)
            self.setForeground(COL_HEAD, QColor(colorRgb))
        else:
            self.setForeground(COL_HEAD, QApplication.palette().brush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText ))

        MgRepoTreeItem.autoAdjustColumnSize(self.treeWidget())

        self.fillNextColumns()


    def adjustColumnFontFromSynchro(self, col: int, synchro: str) -> None:
        '''Apply bold/italic to column font depending on synchro message'''
        doBoldSynchro, doItalicSynchro = shallBoldItalizeSynchro(synchro)
        f = self.font(col)
        f.setBold(doBoldSynchro)
        f.setItalic(doItalicSynchro)
        self.setFont(col, f)


    @ignoreCppObjectDeletedError
    def fillNextColumns(self) -> None:
        """ fills columns in a precise order StatusInt, StatusDev,SHA1,URL"""

        ### Strange, but we have seen that in the field!
        if self.treeWidget() is None:
            return

        if not self.filledColumns & self.ColumnFlags.fieldSHA and not self.treeWidget().isColumnHidden(COL_SHA1):
            # to avoid starting to fill a column multiple times
            self.filledColumns |= self.ColumnFlags.fieldSHA
            self.repoInfo.ensure_sha1(self.cbSha1available)
            return

        if not self.filledColumns & self.ColumnFlags.fieldURL and not self.treeWidget().isColumnHidden(COL_URL):
            # to avoid starting to fill a column multiple times
            self.filledColumns |= self.ColumnFlags.fieldURL
            self.repoInfo.ensure_url(self.cbUrlAvailable)
            return

        # hey, all columns are filled! :-)


    @ignoreCppObjectDeletedError
    def cbSha1available(self, commit_sha1: str) -> None:
        '''Called when sha1 information is eventually available'''
        self.setText(COL_SHA1, commit_sha1[:SHORT_SHA1_NB_DIGITS])
        self.setToolTip(COL_SHA1, commit_sha1)  # full sha1
        self.autoAdjustColumnSize(self.treeWidget())
        self.fillNextColumns()


    @ignoreCppObjectDeletedError
    def cbUrlAvailable(self, url: str) -> None:
        '''Called when url information is eventually available'''
        self.setText(COL_URL, url)
        self.autoAdjustColumnSize(self.treeWidget())
        self.fillNextColumns()


    @staticmethod
    def autoAdjustColumnSize(treeWidget: Optional[QTreeWidget]) -> None:
        '''Adjust automatically the column size to the largest item'''
        if treeWidget is None:
            return

        for i in range(treeWidget.columnCount()):
            treeWidget.resizeColumnToContents(i)
        QApplication.processEvents()


    def __lt__(self, other: 'QTreeWidgetItem') -> bool:
        col = self.treeWidget().sortColumn()
        if not col in [COL_STATUS, COL_REMOTE_SYNCHRO]:
            # regular sorting
            return istrcmp(self.text(col), other.text(col))

        colTextSelf = self.text(col)
        colTextOther = other.text(col)
        if len(colTextSelf) and len(colTextOther) and colTextSelf[0].isdigit() and colTextOther[0].isdigit():
            # natural number sorting if we can
            return extractInt(colTextSelf) < extractInt(colTextOther)

        # regular sort strategy will compare strings and place all number starting strings before others
        return istrcmp(self.text(col), other.text(col))



