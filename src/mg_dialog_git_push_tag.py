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

import logging, itertools

from PySide2.QtWidgets import QWidget

from src.mg_dialog_utils import MgDialogWithRepoList
from src.gui.ui_git_push_tag import Ui_GitPushTag
from src.mg_exec_window import MgExecWindow
from src.mg_repo_info import MgRepoInfo
from src.mg_ensure_info_available import MgEnsureInfoAvailable, RepoInfoFlags

logger = logging.getLogger('mg_dialog_git_push_tag')
dbg = logger.debug

MSG_PUSH_ALL_TAGS = 'Push all tags'

class MgDialogGitPushTag(MgDialogWithRepoList):
    ui: Ui_GitPushTag

    def __init__(self, parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
        super().__init__(parent, Ui_GitPushTag, selectedRepos, allRepos)
        self.sigRepoListAdjusted.connect(self.updateTagContent)
        self.updateTagContent()


    def updateTagContent(self) -> None:
        self.ensureInfoAvailable = MgEnsureInfoAvailable(self, self.getTargetedRepoList(), showProgressDialog=True)
        self.ensureInfoAvailable.ensureInfoAvailable(RepoInfoFlags.ALL_TAGS, blocking=True)
        self.ui.comboBoxTagName.clear()
        self.ui.comboBoxTagName.addItem(MSG_PUSH_ALL_TAGS)
        self.ui.comboBoxTagName.insertSeparator(self.ui.comboBoxTagName.count())
        allTags = list(set(itertools.chain.from_iterable(repo.all_tags for repo in self.getTargetedRepoList())))
        allTags.sort()
        self.ui.comboBoxTagName.addItems(allTags)
        self.ui.comboBoxTagName.setCurrentIndex(0)


    def isPushAllTags(self) -> bool:
        return self.ui.comboBoxTagName.currentIndex() == 0


    def getTagName(self) -> str:
        return self.ui.comboBoxTagName.currentText()


def runDialogGitPushTag(parent: QWidget, selectedRepos: List[MgRepoInfo], allRepos: List[MgRepoInfo]) -> None:
    dbg('runDialogGitPushTag')

    dlg = MgDialogGitPushTag(parent, selectedRepos, allRepos)
    result = dlg.exec()
    if not result:
        # command execution canceled
        return

    if dlg.isPushAllTags():
        desc = 'Pushing all tags'
        cmdPush = ['push', 'origin', '--tags', '--verbose']
    else:
        tagName = dlg.getTagName()
        desc = 'Pushing tag ' + tagName
        cmdPush = ['push', 'origin', 'tag', tagName  ]

    # show window for executing git
    gitExecWindow = MgExecWindow(parent)
    gitExecWindow.execOneGitCommand(desc, cmdPush, dlg.getTargetedRepoList())


