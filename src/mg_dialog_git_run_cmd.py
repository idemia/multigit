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

from PySide6.QtWidgets import QMessageBox, QWidget

from src.mg_exec_window import MgExecWindow
from src.mg_dialog_utils import MgDialogWithRepoList
from src.gui.ui_git_run_command import Ui_GitRunCommand
from src import mg_config as mgc
from src.mg_const import *
from src.mg_repo_info import MgRepoInfo

logger = logging.getLogger('mg_dialog_git_cmd')
dbg = logger.debug


class MgDialogGitRunCmd(MgDialogWithRepoList):
    ui: Ui_GitRunCommand

    def __init__(self, parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
        super().__init__(parent, Ui_GitRunCommand, selectedRepos, allRepos)
        self.fillMenuHistory()
        self.ui.historyButton.historyItemTriggered.connect(self.slotHistoryItemTriggered)


    def slotHistoryItemTriggered(self, title: str, message: str) -> None:
        '''Triggered when an item from the history menu has been selected'''
        self.ui.lineEditGitCmd.setText(message)


    def fillMenuHistory(self) -> None:
        config = mgc.get_config_instance()

        # Fill up list of recent git commands
        self.ui.historyButton.fillHistoryWithTitleAndContent(
            [(f'git {gitCmd}', gitCmd) for gitCmd in config.lruAsList(mgc.CONFIG_GIT_CMD_HISTORY)]
        )


    def accept(self) -> None:
        gitCmd = self.ui.lineEditGitCmd.text()
        if len(gitCmd) == 0:
            QMessageBox.warning(self, "Empty git command", "You dit not specify any git command. Operation canceled!")
            return

        # archive git command
        config = mgc.get_config_instance()
        config.lruSetRecent(mgc.CONFIG_GIT_CMD_HISTORY, gitCmd)
        config.save()

        super().accept()


def runDialogGitCommand(parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
    '''Run a custom git command'''
    dbg('runGitCommand')

    dlg = MgDialogGitRunCmd(parent, selectedRepos, allRepos)
    result = dlg.exec()
    if not result:
        # command execution canceled
        return

    # perform run git command
    gitCmdText = dlg.ui.lineEditGitCmd.text()
    desc = 'Running git command: git ' + gitCmdText
    gitCmd = gitCmdText.split(' ')

    gitExecWindow = MgExecWindow(parent)
    gitExecWindow.execOneGitCommand(desc, gitCmd, dlg.getTargetedRepoList())

