#     Copyright (c) 2024 IDEMIA
#     Author: IDEMIA (Philippe Fremy, Florent Oulieres)
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
from typing import Any
from PySide6.QtWidgets import QTabBar, QTabWidget
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Qt, Signal, QPoint


class MgTabBar(QTabBar):

    showTabMenu = Signal(int, QPoint)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


    def mouseReleaseEvent(self, qme: QMouseEvent) -> None:
        idx = self.tabAt(qme.pos())
        if idx >= 0:
            if qme.button() == Qt.MouseButton.MiddleButton:
                qme.accept()
                self.tabCloseRequested.emit(idx)

            if qme.button() == Qt.MouseButton.RightButton:
                qme.accept()
                self.showTabMenu.emit(idx, qme.globalPos())

        return super().mouseReleaseEvent(qme)



class MgTabWidget(QTabWidget):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.setTabBar(MgTabBar())
        self.tabBar().tabCloseRequested.connect(self.removeTab)



