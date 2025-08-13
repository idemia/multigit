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


from typing import List, Tuple
import logging

from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtGui import QAction

from src.gui.ui_git_commit import Ui_GitCommit
from src.mg_dialog_utils import MgDialogWithRepoList
from src.mg_exec_window import MgExecWindow
from src.mg_repo_info import MgRepoInfo
import src.mg_config as mgc

logger = logging.getLogger('mg_dialog_git_commit')
dbg = logger.debug


class MgDialogGitCommit(MgDialogWithRepoList):
    ui: Ui_GitCommit

    def __init__(self, parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
        super().__init__(parent,
                         Ui_GitCommit,
                         selectedRepos,
                         allRepos)
        self.ui.buttonHistoryCommit.historyItemTriggered.connect(self.slotHistoryItemTriggered)
        self.fillMenuHistory()


    def fillMenuHistory(self) -> None:
        config = mgc.get_config_instance()
        history = config.lruAsList(mgc.CONFIG_GIT_COMMIT_HISTORY)
        content = []    # type: List[Tuple[str, str]]
        for msg in history:
            if msg.strip() == '':
                # message is empty, do not add action
                continue

            lines = msg.split('\n')
            idx = 0
            # strip empty lines
            while idx < len(lines) and len(lines[idx].strip()) == 0:
                idx += 1

            if idx > len(lines):
                # ok, this message was empty
                continue

            summary = lines[idx].strip()
            content.append((summary, msg))

        self.ui.buttonHistoryCommit.fillHistoryWithTitleAndContent(content)


    def slotHistoryItemTriggered(self, title: str, message: str) -> None:
        '''Triggered when an item from the history menu has been selected'''
        self.ui.textEditCommitMessage.setText(message)


    def accept(self) -> None:
        mgc.get_config_instance().lruSetRecent(mgc.CONFIG_GIT_COMMIT_HISTORY, self.ui.textEditCommitMessage.toPlainText())
        commitMsg = str(self.ui.textEditCommitMessage.toPlainText()).encode('utf8', errors='ignore')
        if len(commitMsg) == 0:
            QMessageBox.warning(self, "Missing commit message",
                                "No commit message specified")
            return

        super().accept()


def runDialogGitCommit(parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
    '''Run commit git command'''
    dbg('runDialogGitCommit')

    dialog = MgDialogGitCommit(parent, selectedRepos, allRepos)
    result = dialog.exec()
    if not result:
        # command execution canceled
        return

    commitMsg = dialog.ui.textEditCommitMessage.toPlainText()
    repoAndListOfGitCmd = []
    desc = "Git Commit"
    for repoInfo in dialog.getTargetedRepoList():
        # commit command
        commandsToRun = [
            ['commit', '-a', '-m', commitMsg]
        ]
        # push command
        if dialog.ui.checkBoxPushToRemote.isChecked():
            commandsToRun.append( ['push', '-u', '--progress', '--verbose', 'origin', '{0}'.format(repoInfo.branch)] )
            desc += f' and Push branch {repoInfo.branch}'

        repoAndListOfGitCmd.append((desc, repoInfo, commandsToRun))

    # show window for executing git
    gitExecWindow = MgExecWindow(parent)
    gitExecWindow.execEachRepoWithHisSeqOfGitCommand(desc, repoAndListOfGitCmd)

