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


import logging
from typing import TYPE_CHECKING, cast, Type, Union, Optional, List, Protocol

from PySide6.QtWidgets import QMessageBox, QDialog, QTreeWidget, QAbstractItemView, QPushButton, QLabel, QWidget
from PySide6.QtCore import Qt, Signal

if TYPE_CHECKING:
    from src.mg_window import MgMainWindow
    from src.mg_repo_tree import MgRepoTree
from src.mg_repo_info import MgRepoInfo
from src.mg_repo_tree_item import MgRepoTreeItem
from src.mg_const import COL_NB, COL_TITLES, COL_REPO_NAME, COL_UPDATE

logger = logging.getLogger('mg_dialog_utils')
dbg = logger.debug

reBranchTagValues = "[^ ~^:]*"


if TYPE_CHECKING:
    class UiOfDialogWithRepos(Protocol):
        '''Typing helper class to declare that we need an object with the follwing attributes:
        - has a setupUI() method
        - has a treeWidgetRepoList attribute of type MgRepoTree
        '''
        # typing helper class
        def setupUi(self, dialog: QDialog) -> None:
            ...

        treeWidgetRepoList: 'MgRepoTree'
        pushButtonAdjustRepoList: QPushButton
        labelRepoSelected: QLabel


def prepareTreeWidgetRepoList(treeWidget: QTreeWidget) -> None:
    '''Prepare the tree widget headers and other attributes'''
    if treeWidget.columnCount() < COL_NB:
        treeWidget.setColumnCount(COL_NB)
        treeWidget.setHeaderLabels(COL_TITLES)
        treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        treeWidget.setAllColumnsShowFocus(True)
        treeWidget.header().setSortIndicatorShown(True)
    f = treeWidget.header().font()
    f.setBold(True)
    treeWidget.header().setFont(f)
    treeWidget.sortByColumn(COL_REPO_NAME, Qt.SortOrder.AscendingOrder)
    treeWidget.headerItem().setText(COL_UPDATE, "")
    treeWidget.setColumnHidden(COL_UPDATE, True)
    treeWidget.clear()


class MgDialogWithRepoList(QDialog):
    '''Inherit from this dialog to manage a dialog with a list of Repositories'''

    sigRepoListAdjusted = Signal()

    def __init__(self, parent: QWidget, Ui_Class: Type['UiOfDialogWithRepos'],
                 selectedRepos: Optional[List[MgRepoInfo]] = None, allRepos: Optional[List[MgRepoInfo]] = None) -> None:
        '''This __init__ method has two ways of being used:
        * new style:
            __init__(ui_class, parentWidget, [repos, ...], [repos, ...])

        Eventually, the legacy style should disappear

        '''
        super().__init__(parent)

        self.ui = Ui_Class()
        self.ui.setupUi(self)

        self.allRepos = allRepos or []
        selectedRepos = selectedRepos or []

        assert parent is not None
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # prepare repository list
        prepareTreeWidgetRepoList(self.ui.treeWidgetRepoList)

        # fill the list of repositories
        for repo in selectedRepos:
            repoTreeItem = MgRepoTreeItem(repo, self.ui.treeWidgetRepoList)
            repoTreeItem.fillRepoItem()

        MgRepoTreeItem.autoAdjustColumnSize(self.ui.treeWidgetRepoList)

        self.ui.pushButtonAdjustRepoList.clicked.connect(self.slotAdjutRepoList)
        self.updateRepoSelectedLabel()
        self.allReposStatus = "all"


    def setAllReposStatus(self, status:str) -> None:
        self.allReposStatus = status


    def updateRepoSelectedLabel(self) -> None:
        self.ui.labelRepoSelected.setText( '%d repositories targeted' % self.ui.treeWidgetRepoList.topLevelItemCount())


    def getTargetedRepoList(self) -> List[MgRepoInfo]:
        '''Return a list of MgRepoInfo items'''
        targetedRepos = [cast(MgRepoTreeItem, self.ui.treeWidgetRepoList.topLevelItem(idx)).repoInfo
                         for idx in range(self.ui.treeWidgetRepoList.topLevelItemCount())]
        return targetedRepos


    def slotAdjutRepoList(self) -> None:
        # to avoid a circular dependency, perform a local import
        from src.mg_dialog_select_repo import MgDialogSelectRepos
        dialog = MgDialogSelectRepos(self, self.getTargetedRepoList(), self.allRepos)

        result = dialog.exec()
        if not result:
            # dialog canceled
            return

        # adjust list of repos to operate on
        itemToRemove = []
        selectedRepoInfo = dialog.selectedRepoInfo()
        for idx in range(self.ui.treeWidgetRepoList.topLevelItemCount()):
            repoItem = cast(MgRepoTreeItem, self.ui.treeWidgetRepoList.topLevelItem(idx))
            if repoItem.repoInfo not in selectedRepoInfo:
                itemToRemove.append(idx)

        for idx in reversed(itemToRemove):
            self.ui.treeWidgetRepoList.takeTopLevelItem(idx)

        currentlySelectedRepoInfo = [
            cast(MgRepoTreeItem, self.ui.treeWidgetRepoList.topLevelItem(idx)).repoInfo
            for idx in range(self.ui.treeWidgetRepoList.topLevelItemCount())
        ]

        repoToAdd = set(selectedRepoInfo) - set(currentlySelectedRepoInfo)
        for repoInfo in repoToAdd:
            repoTreeItem = MgRepoTreeItem(repoInfo, self.ui.treeWidgetRepoList)
            repoTreeItem.fillRepoItem()

        self.updateRepoSelectedLabel()
        # noinspection PyUnresolvedReferences
        self.sigRepoListAdjusted.emit()


    def accept(self) -> None:
        if self.ui.treeWidgetRepoList.topLevelItemCount() == 0:
            # no item in the list !
            QMessageBox.warning(self, "No repository",
                                "No repository selected.\nYou must select at least one repository!")
            return

        super().accept()