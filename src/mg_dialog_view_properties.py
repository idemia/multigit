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


from typing import TYPE_CHECKING, List
import logging

from PySide2.QtWidgets import QDialog, QApplication, QWidget
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

from src.mg_repo_info import MgRepoInfo
from src.gui.ui_repo_properties import Ui_RepoProperties
from src.mg_utils import htmlize_diff

logger = logging.getLogger('mg_dialog_view_properties')
dbg = logger.debug

def runDialogGitProperties(parent: QWidget, currentRepo: MgRepoInfo) -> None:
    dbg('runDialogGitProperties()')

    currentRepo.ensure_all_filled()
    dlg = QDialog(parent)
    dlg.setWindowFlags(
        dlg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    dlg.setWindowTitle('Properties of {}'.format(currentRepo.name))
    ui_rp = Ui_RepoProperties()
    ui_rp.setupUi(dlg)

    def slotCopyPathToClipboard() -> None:
        path = ui_rp.lineEditFullPath.text()
        QApplication.clipboard().setText(path)

    def slotCopyUrlToClipboard() -> None:
        url = ui_rp.lineEditUrl.text()
        QApplication.clipboard().setText(url)

    ui_rp.buttonCopyPath.clicked.connect(slotCopyPathToClipboard)
    ui_rp.buttonCopyPath.setIcon(QIcon(':/img/icons8-clipboard-48.png'))
    ui_rp.buttonCopyUrl.clicked.connect(slotCopyUrlToClipboard)
    ui_rp.buttonCopyUrl.setIcon(QIcon(':/img/icons8-clipboard-48.png'))
    ui_rp.lineEditDir.setText(currentRepo.name)
    ui_rp.lineEditStatus.setText(currentRepo.nice_status())
    ui_rp.lineEditRemoteSynchro.setText(currentRepo.remote_synchro)
    ui_rp.lineEditUrl.setText(currentRepo.url or '')
    ui_rp.lineEditFullPath.setText(currentRepo.fullpath)
    ui_rp.lineEditRemoteBranch.setText(currentRepo.remote_branch)
    ui_rp.lineEditHead.setText(currentRepo.head)
    # use double space for more visual splitting
    ui_rp.lineEditTags.setText('  '.join( (currentRepo.tags or '').split(' ')))
    ui_rp.textEditLastCommit.setText(currentRepo.last_commit)
    ui_rp.textEditDiffSummary.setText(htmlize_diff(currentRepo.diff_summary or ''))
    dlg.show()

