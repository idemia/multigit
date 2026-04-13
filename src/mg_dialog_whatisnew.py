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

from PySide6.QtWidgets import QWidget, QDialog, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
from PySide6.QtCore import Qt

from src.gui.content_whatisnew import content_html as whatsnew_html_content
from src.gui.content_getting_started import content_html as getting_started_html_content
from src.mg_const import *
import src.mg_config as mgc


def showLaunchDialog() -> None:
    '''Show the `Getting started` dialog if this is the very first launch.

    If not the first launch, show the 'What is new' dialog if it was never shown for the current version of MultiGit'''

    config = mgc.get_config_instance()
    show_getting_started = config[mgc.CONFIG_SHOW_GETTING_STARTED]
    if show_getting_started is None:
        config[mgc.CONFIG_SHOW_GETTING_STARTED] = False
        config.save()
        showGettingStarted()
        return


    last_whatsnew_showed = config[mgc.CONFIG_LAST_SHOWN_WHATISNEW]
    if last_whatsnew_showed is not None and last_whatsnew_showed < VERSION:
        config[mgc.CONFIG_LAST_SHOWN_WHATISNEW] = VERSION
        config.save()
        showWhatIsNew()
        return


    if config[mgc.CONFIG_DISPLAY_FETCH_ON_STARTUP_COUNTDOWN] == 0:
        answer = QMessageBox.question(None, 'Activate fetch on startup ?', 'Multigit can fetch all your repositories when you launch it. '
                                'Do you want to activate this behavior ?\n\nNote that you can change it later in the settings dialog.\n')
        fetchReposOnStartup = (answer == QMessageBox.StandardButton.Yes)
        config[mgc.CONFIG_FETCH_ON_STARTUP] = fetchReposOnStartup
        config.save()
        return


def showWhatIsNew(parent: Optional[QWidget] = None) -> None:
    showDialogWithHtmlContent(whatsnew_html_content, parent)


def showGettingStarted(parent: Optional[QWidget] = None) -> None:
    showDialogWithHtmlContent(getting_started_html_content, parent)


def showDialogWithHtmlContent(html_content: str, parent: Optional[QWidget] = None) -> None:
    '''Show what's new dialog'''
    dialog = QDialog(parent)
    dialog.setWindowTitle("What's New")
    dialog.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

    text = QTextEdit(dialog)
    text.setReadOnly(True)
    text.setHtml(html_content)
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
