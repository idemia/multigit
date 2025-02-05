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

import logging

from PySide6.QtWidgets import QWidget, QDialogButtonBox

from src.mg_dialog_utils import MgDialogWithRepoList
from src.gui.ui_git_revert import Ui_GitRevert
from src.mg_exec_window import MgExecWindow
from src.mg_repo_info import MgRepoInfo
from src.mg_utils import htmlize_diff
from src.mg_ensure_info_available import MgEnsureInfoAvailable, RepoInfoFlags

logger = logging.getLogger('mg_dialog_git_revert')
dbg = logger.debug


class MgDialogGitRevert(MgDialogWithRepoList):
    ui: Ui_GitRevert

    def __init__(self, parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
        super().__init__(parent, Ui_GitRevert, selectedRepos, allRepos)
        self.sigRepoListAdjusted.connect(self.updateDiffContent)
        self.updateDiffContent()
        buttonYes = self.ui.buttonBox.button( QDialogButtonBox.StandardButton.Yes )
        buttonYes.setText('Revert')


    def updateDiffContent(self) -> None:
        content = []
        self.ensureInfoAvailable = MgEnsureInfoAvailable(self, self.getTargetedRepoList(), showProgressDialog=True)
        self.ensureInfoAvailable.ensureInfoAvailable(RepoInfoFlags.DIFF_SUMMARY, blocking=True)
        for repo in self.getTargetedRepoList():
            # repo.ensure_diff_summary(blocking=True)
            if repo.diff_summary and len(repo.diff_summary):
                content.append(f'<b>{repo.name}:<b>')
                content.append( htmlize_diff(repo.diff_summary or '') + '<p>' )

        self.ui.textEditRevertContent.setText('\n'.join(content))



def runDialogGitRevert(parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
    dbg('runDialogGitRevert')

    dlg = MgDialogGitRevert(parent, selectedRepos, allRepos)
    result = dlg.exec()
    if not result:
        # command execution canceled
        return

    desc = 'Reverting repositories'
    cmd = ['checkout', '--', '.']

    # show window for executing git
    gitExecWindow = MgExecWindow(parent)
    gitExecWindow.execOneGitCommand(desc, cmd, dlg.getTargetedRepoList())


