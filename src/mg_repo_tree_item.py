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

from PySide6.QtGui import QIcon, QColor, QPalette
from PySide6.QtWidgets import QTreeWidgetItem, QApplication, QWidget, QTreeWidget

from src.mg_utils import extractInt
from src import mg_config as mgc
from src.mg_const import COL_UPDATE, COL_REPO_NAME, COL_HEAD, COL_STATUS, COL_REMOTE_SYNCHRO, DISPLAY_IN_BOLD_MSG, \
    DISPLAY_IN_ITALIC_MSG, COL_SHA1, SHORT_SHA1_NB_DIGITS, COL_URL, MSG_LOCAL_BRANCH, MSG_LOCAL_BRANCH_TOOLTIP
from src.mg_exec_task_item import getIcon, IconSet
from src.mg_repo_info import MgRepoInfo

dbg = logging.getLogger('mg_repo_tree_item').debug
error = logging.getLogger('mg_repo_tree_item').error

DELTA_ROTATION = 30
TOTAL_ROTATION = 360

from src.mg_utils import istrcmp

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

    def __init__(self, repoInfo: MgRepoInfo, *args: Any) -> None:
        super().__init__(*args)
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


    def markItemInProgress(self) -> None:
        try:
            dbg('markItemInProgress(%s)' % self.repoInfo.name)
            self.setText(COL_UPDATE, '')
            self.setIcon(COL_UPDATE, QIcon(':img/icons8-loader-96.png'))
        except RuntimeError:
            # happens when updating an item, which is a Python object, but the C++
            # underlying object has already been deleted
            # just ignore the error
            error('Trying to update an item which has already been deleted!')
            error('Just ignore the error for now but we should find a better way!')
            return
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


    def slotRepoInfoAvailable(self, repo_name: str) -> None:
        '''Called when the update of the repo info has completed'''
        dbg('slotRepoInfoAvailable(%s)' % repo_name)

        # sometimes, the view is modified, the item is deleted but we still
        # receive the signal from Python.
        try:
            # just to trigger access to C++ object
            self.setExpanded(self.isExpanded())
        except RuntimeError:
            error('Trying to update an item which has already been deleted!')
            error('Just ignore the error for now but we should find a better way!')
            return

        if repo_name != self.repoInfo.name:
            raise AssertionError('Item slotRepoInfoAvailable() of repo %s is called with argument %s' % (self.repoInfo.name, repo_name))
        self.fillRepoItem()


    def fillRepoItem(self) -> None:
        '''Fill a QTreeWidgetItem from the associated repoInfo'''
        dbg('fillRepoItem(%s, ...)' % self.repoInfo.name)
        self.setIcon(COL_UPDATE, getIcon(IconSet.Empty))
        self.setText(COL_UPDATE, '')
        self.setText(COL_REPO_NAME, self.repoInfo.name)
        self.setText(COL_HEAD, self.repoInfo.head)
        self.setText(COL_STATUS, self.repoInfo.status)
        self.setText(COL_REMOTE_SYNCHRO, self.repoInfo.remote_synchro )
        if self.repoInfo.remote_synchro == MSG_LOCAL_BRANCH:
            # add a tooltip to give an easy-fix for the missing remote branch
            self.setToolTip(COL_REMOTE_SYNCHRO, MSG_LOCAL_BRANCH_TOOLTIP)
        else:
            self.setToolTip(COL_REMOTE_SYNCHRO, '')
        self.setText(COL_SHA1, (self.repoInfo.commit_sha1 or '')[:SHORT_SHA1_NB_DIGITS])
        self.setText(COL_URL, self.repoInfo.url or '')

        doBoldStatus = self.repoInfo.status != 'OK'
        f = self.font(COL_STATUS)
        f.setBold(doBoldStatus)
        self.setFont(COL_STATUS, f)

        doBoldSynchro, doItalicSynchro = shallBoldItalizeSynchro(self.repoInfo.remote_synchro)
        f = self.font(COL_REMOTE_SYNCHRO)
        f.setBold(doBoldSynchro)
        f.setItalic(doItalicSynchro)
        self.setFont(COL_REMOTE_SYNCHRO, f)

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

        try:
            # we refresh the columns one by one, to give priority to the other repo still processing their basic information
            # So, we don't request URL before SHA1 is available
            if not self.treeWidget().isColumnHidden(COL_SHA1):
                self.repoInfo.ensure_sha1(self.cbSha1available)

            elif not self.treeWidget().isColumnHidden(COL_URL):
                self.repoInfo.ensure_url(self.cbUrlAvailable)
        except RuntimeError:
            error('Trying to update an item which has already been deleted!')
            error('Just ignore the error for now but we should find a better way!')
            return



    def cbSha1available(self, commit_sha1: str) -> None:
        '''Called when sha1 information is eventually available'''

        # sometimes, the view is modified, the item is deleted but we still
        # receive the signal from Python.
        try:
            self.setText(COL_SHA1, commit_sha1[:SHORT_SHA1_NB_DIGITS])
            self.autoAdjustColumnSize(self.treeWidget())

            if not self.treeWidget().isColumnHidden(COL_URL):
                self.repoInfo.ensure_url(self.cbUrlAvailable)

        except RuntimeError:
            error('Trying to update an item which has already been deleted!')
            error('Just ignore the error for now but we should find a better way!')
            return



    def cbUrlAvailable(self, url: str) -> None:
        '''Called when url information is eventually available'''

        # sometimes, the view is modified, the item is deleted but we still
        # receive the signal from Python.
        try:
            # just to trigger access to C++ object
            self.setExpanded(self.isExpanded())
        except RuntimeError:
            error('Trying to update an item which has already been deleted!')
            error('Just ignore the error for now but we should find a better way!')
            return

        self.setText(COL_URL, url)
        self.autoAdjustColumnSize(self.treeWidget())


    @staticmethod
    def autoAdjustColumnSize(treeWidget: QTreeWidget) -> None:
        '''Adjust automatically the column size to the largest item'''
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



