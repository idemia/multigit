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


from typing import List, cast, Optional

from PySide6.QtWidgets import QDialog, QWidget, QTreeWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from src.gui.ui_select_repos import Ui_SelectRepos
from src.mg_repo_info import MgRepoInfo
from src.mg_repo_tree_item import MgRepoTreeItem
from src.mg_dialog_utils import prepareTreeWidgetRepoList
from src.mg_const import *


class MgDialogSelectRepos(QDialog):
    '''Select a list of repositories from a given set of repositories'''

    def __init__(self, parent: QWidget, selectedRepoList: List[MgRepoInfo],
                 allRepoList: List[MgRepoInfo]) -> None:
        super().__init__(parent)

        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.ui = Ui_SelectRepos()
        self.ui.setupUi(self)
        prepareTreeWidgetRepoList(self.ui.treeWidgetSelectedRepos)
        prepareTreeWidgetRepoList(self.ui.treeWidgetAvailRepos)

        firstItem = True
        for repoInfo in selectedRepoList:
            repoTreeItem = MgRepoTreeItem(repoInfo, self.ui.treeWidgetSelectedRepos)
            repoTreeItem.fillRepoItem()
            if firstItem:
                repoTreeItem.setSelected(True)
                firstItem = False


        firstItem = True
        for repoInfo in allRepoList:
            if repoInfo in selectedRepoList:
                continue
            repoTreeItem = MgRepoTreeItem(repoInfo, self.ui.treeWidgetAvailRepos)
            repoTreeItem.fillRepoItem()
            if firstItem:
                repoTreeItem.setSelected(True)
                firstItem = False

        MgRepoTreeItem.autoAdjustColumnSize(self.ui.treeWidgetSelectedRepos)
        MgRepoTreeItem.autoAdjustColumnSize(self.ui.treeWidgetAvailRepos)

        self.ui.pushButtonMoveUp.setIconSize(QSize(32, 32))
        self.ui.pushButtonMoveDown.setIconSize(QSize(32, 32))
        self.ui.pushButtonMoveAllDown.setIconSize(QSize(32, 32))
        self.ui.pushButtonMoveAllUp.setIconSize(QSize(32, 32))
        self.ui.pushButtonMoveUp.setIcon(QIcon(':img/icons8-chevron-up-52.png'))
        self.ui.pushButtonMoveDown.setIcon(QIcon(':img/icons8-chevron-down-52.png'))
        self.ui.pushButtonMoveAllDown.setIcon(QIcon(':img/icons8-double-down-52.png'))
        self.ui.pushButtonMoveAllUp.setIcon(QIcon(':img/icons8-double-up-52.png'))
        self.ui.pushButtonMoveUp.setText('')
        self.ui.pushButtonMoveDown.setText('')
        self.ui.pushButtonMoveAllUp.setText('')
        self.ui.pushButtonMoveAllDown.setText('')
        self.ui.pushButtonMoveUp.clicked.connect(self.slotMoveToAvailable)
        self.ui.pushButtonMoveDown.clicked.connect(self.slotMoveToTargeted)
        self.ui.pushButtonMoveAllUp.clicked.connect(self.slotMoveAllToAvailable)
        self.ui.pushButtonMoveAllDown.clicked.connect(self.slotMoveAllToTargeted)
        self.ui.pushButtonMoveDown.setToolTip('Move selected repositories to targeted list')
        self.ui.pushButtonMoveUp.setToolTip('Remove selected repository from targeted list')
        self.ui.pushButtonMoveAllDown.setToolTip('Move all repositories to targeted list')
        self.ui.pushButtonMoveAllUp.setToolTip('Remove all repositories from targeted list')
        self.updateLabelSelectedRepoNb()

        self.ui.treeWidgetAvailRepos.setFocus()

        # we must freeze the size of the labelLineHidden because else, it keeps
        # changing size and make the lineEditFilter widget move
        self.ui.labelLineHidden.setText(' ' * len('XXX repositories hidden'))
        self.ui.labelLineHidden.setFixedSize(self.ui.labelLineHidden.size())
        self.ui.labelLineHidden.setText('')

        self.ui.lineEditFilterList.textEdited.connect(self.showHideRepoFromFilter)


    def showHideRepoFromFilter(self, text: Optional[str]) -> None:
        '''Called when the filter is updated, hide/show the relevant items'''
        text = text or self.ui.lineEditFilterList.text()
        text = text.lower()
        nbHidden = 0
        for idx in range(self.ui.treeWidgetAvailRepos.topLevelItemCount()):
            item = self.ui.treeWidgetAvailRepos.topLevelItem(idx)
            assert item is not None
            item.setHidden(True)
            nbHidden += 1
            for i in range(COL_NB):
                if text in item.text(i).lower():
                    item.setHidden(False)
                    nbHidden -= 1
                    break

        if nbHidden == 0 and text == '':
            self.ui.labelLineHidden.setText('')
        else:
            self.ui.labelLineHidden.setText('%d repositories hidden' % nbHidden)


    def selectedRepoInfo(self) -> List[MgRepoInfo]:
        '''Return the list of chosen repositories'''
        return [cast(MgRepoTreeItem, self.ui.treeWidgetSelectedRepos.topLevelItem(idx)).repoInfo
                for idx in range(self.ui.treeWidgetSelectedRepos.topLevelItemCount())]


    def slotMoveAllToAvailable(self) -> None:
        '''Move item seleccted to the treeWidgetAvailableRepos'''
        self.moveItemsToOtherTreeWidget(self.ui.treeWidgetSelectedRepos, self.ui.treeWidgetAvailRepos,
                                        True)


    def slotMoveToAvailable(self) -> None:
        '''Move item seleccted to the treeWidgetAvailableRepos'''
        self.moveItemsToOtherTreeWidget(self.ui.treeWidgetSelectedRepos, self.ui.treeWidgetAvailRepos)


    def slotMoveAllToTargeted(self) -> None:
        '''Move item seleccted to the treeWidgetSelectedRepos'''
        self.moveItemsToOtherTreeWidget(self.ui.treeWidgetAvailRepos, self.ui.treeWidgetSelectedRepos,
                                        True)


    def slotMoveToTargeted(self) -> None:
        '''Move item seleccted to the treeWidgetSelectedRepos'''
        self.moveItemsToOtherTreeWidget(self.ui.treeWidgetAvailRepos, self.ui.treeWidgetSelectedRepos)


    def moveItemsToOtherTreeWidget(self, treeWidgetSource: QTreeWidget,
                                         treeWidgetDest: QTreeWidget,
                                         moveAll: bool = False) -> None:
        '''Remove items from one treeWidget and create items on the other tree Widget'''
        if moveAll:
            treeWidgetSource.selectAll()
        selectedItems = treeWidgetSource.selectedItems()

        for item in selectedItems:
            # add item to destination
            assert isinstance(item, MgRepoTreeItem)
            repoTreeItem = MgRepoTreeItem(item.repoInfo, treeWidgetDest)
            repoTreeItem.fillRepoItem()
            if treeWidgetDest.topLevelItemCount() == 1:
                # we are moving our first item there, select it
                repoTreeItem.setSelected(True)

            # remove item from source
            idx = treeWidgetSource.indexOfTopLevelItem(item)
            treeWidgetSource.takeTopLevelItem(idx)

            # select another item after the move
            if treeWidgetSource.topLevelItemCount():
                # if there are still items to select

                # find a valid index
                idx =  min(idx, treeWidgetSource.topLevelItemCount()-1)
                treeWidgetSource.topLevelItem(idx).setSelected(True)    # type: ignore # topLevelItem(idx) exists and is not None

        self.updateLabelSelectedRepoNb()
        self.showHideRepoFromFilter(None)


    def updateLabelSelectedRepoNb(self) -> None:
        self.ui.labelRepoSelected.setText('%d repositories targeted' % self.ui.treeWidgetSelectedRepos.topLevelItemCount())



