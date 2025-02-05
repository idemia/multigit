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


from typing import Optional, List, Sequence

import logging, enum

from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QMessageBox

from src.mg_utils import isGitCommandRequiringAuth

logger = logging.getLogger('mg_auth_failure_mgr')
dbg = logger.debug
warn = logger.warning

AUTH_FAILED_LIMIT_BEFORE_WARNING_USER = 2

class ActionAfterManyAuthFailure(enum.Enum):
    ReportWithDialog = enum.auto()
    IgnoreAllAuthErrors = enum.auto()
    BlockFutureGitcommand = enum.auto()
    DialogQuestionInProgress = enum.auto()


class MgAuthFailureMgr(QObject):

    __instance: Optional['MgAuthFailureMgr'] = None
    nbGitAuthFail: int
    actionAfterManyAuthFailure: ActionAfterManyAuthFailure

    def __init__(self) -> None:
        super().__init__()
        dbg('instance created')
        MgAuthFailureMgr.__instance = self
        MgAuthFailureMgr.newSession()


    @staticmethod
    def shouldStopBecauseAuthFailureInProgress(cmdline: Sequence[str]) -> bool:
        if not isGitCommandRequiringAuth(cmdline):
            ret = False
        else:
            ret = (MgAuthFailureMgr.instance().actionAfterManyAuthFailure == ActionAfterManyAuthFailure.BlockFutureGitcommand)

        dbg(f'shouldStopBecauseAuthFailureInProgress() -> {ret}')
        return ret


    @staticmethod
    def gitAuthFailed(cmdline: str) -> None:
        '''Called each time a git authentication fails for a git command'''
        self = MgAuthFailureMgr.instance()
        self.nbGitAuthFail += 1
        warn(f'Git authentication failure: {self.nbGitAuthFail} on {AUTH_FAILED_LIMIT_BEFORE_WARNING_USER} authorized')
        if self.nbGitAuthFail > AUTH_FAILED_LIMIT_BEFORE_WARNING_USER \
                and self.actionAfterManyAuthFailure == ActionAfterManyAuthFailure.ReportWithDialog:
            self.actionAfterManyAuthFailure = ActionAfterManyAuthFailure.DialogQuestionInProgress
            msg = f'We have already detected {self.nbGitAuthFail} authentication failures.'
            msg += ' Be careful that too many authentication failures may lock your account.'
            msg += '<p>To update your git login/password, open the <i>Windows Credentials Manager (in french: Gérer les mots de passe réseau</i>)'
            msg += '<p>What to you want to do next ?'

            msgBox = QMessageBox(QMessageBox.Icon.Warning, "Many authentication failures", '')
            msgBox.setTextFormat(Qt.TextFormat.RichText)
            msgBox.setText(msg)
            buttonContinue = msgBox.addButton('Continue', QMessageBox.ButtonRole.AcceptRole)
            buttonContinueAndIgnore = msgBox.addButton('Continue && Ignore all authentication failures', QMessageBox.ButtonRole.AcceptRole)
            buttonCancelAll = msgBox.addButton('Cancel all git operations', QMessageBox.ButtonRole.AcceptRole)
            msgBox.exec()
            buttonSelected = msgBox.clickedButton()
            if buttonSelected == buttonCancelAll:
                self.actionAfterManyAuthFailure = ActionAfterManyAuthFailure.BlockFutureGitcommand
            elif buttonSelected == buttonContinueAndIgnore:
                self.actionAfterManyAuthFailure = ActionAfterManyAuthFailure.IgnoreAllAuthErrors
            elif buttonSelected == buttonContinue:
                self.actionAfterManyAuthFailure = ActionAfterManyAuthFailure.ReportWithDialog


    @classmethod
    def instance(cls) -> 'MgAuthFailureMgr':
        '''Return an existing instance of this class, creating one if necessary'''
        if cls.__instance is None:
            cls.__instance = MgAuthFailureMgr()

        return cls.__instance

    @classmethod
    def newSession(cls) -> None:
        '''A new session of git commands is started, so reset all counters and actions'''
        self = cls.instance()
        self.nbGitAuthFail = 0
        self.actionAfterManyAuthFailure = ActionAfterManyAuthFailure.ReportWithDialog


