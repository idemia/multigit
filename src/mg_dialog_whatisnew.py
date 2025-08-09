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


from typing import Optional

from PySide6.QtWidgets import QWidget, QDialog, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt

from src.gui.content_whatisnew import content_html
from src.mg_const import *
import src.mg_config as mgc


def showWhatisnewIfAppropriate() -> None:
    '''Show the 'What is new' dialog if it was never shown for the current version of MultiGit'''
    last_shown = mgc.get_config_instance()[mgc.CONFIG_LAST_SHOWN_WHATISNEW]
    if last_shown is not None and last_shown < VERSION:
        showWhatIsNew()
        mgc.get_config_instance()[mgc.CONFIG_LAST_SHOWN_WHATISNEW] = VERSION


def showWhatIsNew(parent: Optional[QWidget] = None) -> None:
    '''Show what's new dialog'''
    dialog = QDialog(parent)
    dialog.setWindowTitle("What's New")
    dialog.setWindowFlags( dialog.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

    text = QTextEdit(dialog)
    text.setReadOnly(True)
    text.setHtml(content_html)
    text.setFrameShape( QFrame.Shape.NoFrame )
    text.zoomIn(2)

    okButton = QPushButton('OK', dialog)
    okButton.clicked.connect( dialog.accept )

    vlayout = QVBoxLayout(dialog)
    vlayout.addWidget(text)
    hbutlayout = QHBoxLayout(dialog)
    hbutlayout.addStretch()
    hbutlayout.addWidget(okButton)
    vlayout.addLayout(hbutlayout)

    dialog.resize(700, 700)
    dialog.exec()
