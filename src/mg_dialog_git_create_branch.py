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

from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator

from src.gui.ui_git_create_branch import Ui_GitCreateBranch
from src.mg_dialog_utils import reBranchTagValues, MgDialogWithRepoList
from src.mg_exec_window import MgExecWindow
from src import mg_config as mgc
from src.mg_const import *
from src.mg_repo_info import MgRepoInfo

logger = logging.getLogger('mg_dialog_git_create_branch')
dbg = logger.debug


class MgDialogGitCreateBranch(MgDialogWithRepoList):
    ui: Ui_GitCreateBranch

    def __init__(self, parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
        super().__init__(parent, Ui_GitCreateBranch, selectedRepos, allRepos)

        # default branch name is empty
        self.ui.comboBoxBranchName.insertItem(0, "")
        self.ui.comboBoxBranchName.setCurrentIndex(0)
        self.ui.comboBoxBranchName.setFocus()
        validator = QRegularExpressionValidator(QRegularExpression(reBranchTagValues))
        self.ui.comboBoxBranchName.setValidator(validator)
        completer = self.ui.comboBoxBranchName.completer()
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseSensitive)
        # self.ui.comboBoxBranchName.setCompleter(completer)

        # Fill up list of recent branch names
        if len(mgc.get_config_instance().lruAsList(mgc.CONFIG_GIT_BRANCH_HISTORY)):
            self.ui.comboBoxBranchName.insertItems(0, mgc.get_config_instance().lruAsList(mgc.CONFIG_GIT_BRANCH_HISTORY))


    def accept(self) -> None:
        branchName = self.ui.comboBoxBranchName.currentText()
        if len(branchName) == 0:
            QMessageBox.warning(self, "No branch name specified",
                                "You did not specify any branch name!")
            return

        super().accept()


def runDialogGitCreateBranch(parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
    '''Run a dialog to create a branch'''
    dbg('runDialogGitCreateBranch')

    dialog = MgDialogGitCreateBranch(parent, selectedRepos, allRepos)
    result = dialog.exec()
    if not result:
        # command execution canceled
        return

    branchName = dialog.ui.comboBoxBranchName.currentText()

    # archive git branch name in history
    mgc.get_config_instance().lruSetRecent(mgc.CONFIG_GIT_BRANCH_HISTORY, branchName)
    mgc.get_config_instance().save()

    if dialog.ui.checkBoxSwitchBranch.isChecked():
        # use checkout and not switch to support old versions of git
        gitCmdSeq = [['checkout', '-b', branchName, '--']]
        desc = 'Creating and switching to branch %s' % branchName
    else:
        desc = 'Creating branch %s ' % branchName
        gitCmdSeq = [['branch', branchName]]
    if dialog.ui.checkBoxPushToRemote.isChecked():
        gitCmdSeq.append(['push', '-u', 'origin', branchName])

    # show window for executing git
    gitExecWindow = MgExecWindow(parent)
    gitExecWindow.execSeqOfGitCommand(desc, gitCmdSeq, dialog.getTargetedRepoList())
