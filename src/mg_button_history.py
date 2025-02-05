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


from typing import List, Tuple, Any

from PySide6.QtWidgets import QPushButton, QMenu
from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QIcon, QMouseEvent, QAction

class MgButtonHistory(QPushButton):
    '''A button to recall history of a text field'''

    historyItemTriggered = Signal(str, str)

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.setIcon(QIcon(':img/icons8-history-64.png'))
        self.clicked.connect(self.slotPopupMenu)

        self.popupMenu = QMenu(self)
        self.popupMenu.setToolTipsVisible(True)
        self.popupMenu.triggered.connect(self.slotMenuItemTriggered)
        self.emptyAction = QAction('No items', self)
        self.emptyAction.setEnabled(False)
        self.popupMenu.addAction(self.emptyAction)

        self.clickPoint = QPoint()


    def fillHistory(self, titleList: List[str]) -> None:
        '''Fill the history with a list of items'''
        self.fillHistoryWithTitleAndContent([(v, '') for v in titleList])


    def fillHistoryWithTitleAndContent(self, content: List[Tuple[str, str]]) -> None:
        '''Fill the history with a list of title and content'''
        self.popupMenu.clear()
        for title, message in content:
            action = QAction(title, self)
            action.setToolTip(message)
            self.popupMenu.addAction(action)

        if not self.popupMenu.isEmpty():
            self.emptyAction.setVisible(False)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        # catch event to locate where to put the menu
        self.clickPoint = event.globalPos()
        super().mousePressEvent(event)


    def slotPopupMenu(self) -> None:
        '''Show the menu with the history items'''
        self.popupMenu.popup(self.clickPoint)


    def slotMenuItemTriggered(self, action: QAction) -> None:
        '''One menu item was selected'''
        title = action.text()
        message = action.toolTip()
        self.historyItemTriggered.emit(title, message)


