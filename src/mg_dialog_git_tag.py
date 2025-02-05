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


from typing import TYPE_CHECKING, List, Tuple
import tempfile, logging

from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtCore import QRegExp
from PySide6.QtGui import QRegExpValidator

from src.gui.ui_git_tag import Ui_GitAddTag
from src.mg_dialog_utils import reBranchTagValues, MgDialogWithRepoList
from src.mg_exec_window import MgExecWindow
from src.mg_repo_info import MgRepoInfo
from src.mg_exec_task_item import MgExecTaskGit, MgExecTaskGroup
from src import mg_config as mgc

logger = logging.getLogger('mg_dialog_tag')
dbg = logger.debug


class MgDialogGitAddTag(MgDialogWithRepoList):
    ui: Ui_GitAddTag

    def __init__(self, parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
        super().__init__(parent,
                         Ui_GitAddTag,
                         selectedRepos,
                         allRepos)

        # default branch name is empty
        self.ui.comboBoxTagName.insertItem(0, "")
        self.ui.comboBoxTagName.setCurrentIndex(0)
        self.ui.comboBoxTagName.setFocus()
        validator = QRegExpValidator(QRegExp(reBranchTagValues))
        self.ui.comboBoxTagName.setValidator(validator)

        # Fill up list of recent tags
        if len(mgc.get_config_instance().lruAsList(mgc.CONFIG_TAG_HISTORY)):
            self.ui.comboBoxTagName.insertItems(0, mgc.get_config_instance().lruAsList(mgc.CONFIG_TAG_HISTORY))


    def accept(self) -> None:
        tagName = self.ui.comboBoxTagName.currentText()
        if len(tagName) == 0:
            QMessageBox.Icon.Warning(self, "No tag name specified",
                                "You did not specify any tag name!")
            return

        super().accept()



def runDialogGitTag(parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
    '''Run git Tag on all listed repos'''
    dbg('runDialogGitTag()')

    # use a dialog to define the tag to set
    dialog = MgDialogGitAddTag(parent, selectedRepos, allRepos)

    result = dialog.exec()
    if not result:
        # tag canceled
        return

    # archive tag name
    tagName = dialog.ui.comboBoxTagName.currentText()
    config = mgc.get_config_instance()
    config.lruSetRecent(mgc.CONFIG_TAG_HISTORY, tagName)
    config.save()

    # check if annotated
    annotation = str(dialog.ui.textAnnotated.toPlainText()).encode('utf8', errors='ignore')

    # contains a list of: (ignore_failure_flag, [git commands to run])
    tag_operation: List[Tuple[bool, List[str]]] = []

    desc = ''
    if annotation:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(annotation)
            desc = 'Adding annotated tag ' + tagName
            tag_operation.append( (False, ['tag', tagName, '-F', tmp_file.name] ) )
    else:
        desc = 'Adding lightweight tag ' + tagName
        tag_operation.append( (False, ['tag', tagName] ) )

    if dialog.ui.checkBoxPushToRemote.isChecked():
        desc += ' and pushing it'
        tag_operation.append( (False, ['push', 'origin', tagName]))

    if dialog.ui.checkBoxSwitchToTag.isChecked():
        desc += ' and checkouting it'
        tag_operation.append((True, ['checkout', f'{tagName}~1', '--' ]))
        tag_operation.append((False, ['checkout', tagName, '--']))

    taskGroup = []
    for repo in dialog.getTargetedRepoList():
        taskGroup.append( MgExecTaskGroup(repo.name, repo,
                                          [MgExecTaskGit('', repo, cmdLine, ignore_failure)
                                           for (ignore_failure, cmdLine) in tag_operation]))

    gitExecWindow = MgExecWindow(parent)
    gitExecWindow.execTaskGroups(desc, taskGroup)

