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


from typing import List, Dict, Callable, Any

import enum

from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QWidget, QProgressDialog, QApplication

from src.mg_repo_info import MgRepoInfo



class RepoInfoFlags(enum.Flag):
    HEAD = enum.auto()
    URL = enum.auto()
    SHA1 = enum.auto()
    ALL_TAGS = enum.auto()
    ALL_BRANCHES = enum.auto()
    DIFF_SUMMARY = enum.auto()
    FILES_SHA1 = enum.auto()


class MgEnsureInfoAvailable(QObject):

    sigInfoAvailable = Signal()

    def __init__(self, parent: QWidget, repoList: List['MgRepoInfo'], showProgressDialog: bool = False) -> None:
        super().__init__(parent)
        self.progressDialog = None
        if showProgressDialog:
            self.progressDialog = QProgressDialog(parent)
            self.progressDialog.setCancelButton(None)
            self.progressDialog.setMinimum(0)
            self.progressDialog.setMinimumDuration(1000)    # 1s before showing the dialog
            self.progressDialog.setWindowTitle('Progress')
            self.progressDialog.setLabelText('Collecting repository information')
            self.progressDialog.setWindowFlags(self.progressDialog.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint & ~Qt.WindowType.WindowCloseButtonHint)
            self.progressDialog.setMinimumWidth(300)
            self.progressDialog.setMinimumHeight(50)
        self.repoList = repoList

        # number of repo where information is expected/available
        self.infoAvailable = {} # type: Dict[RepoInfoFlags, int]
        self.infoExpected = {}  # type: Dict[RepoInfoFlags, int]
        self.clear()


    def clear(self) -> None:
        '''Clear the dictionnaries tracking the number of information expected and available'''
        for infoType in RepoInfoFlags:
            self.infoAvailable[infoType] = 0
            self.infoExpected[infoType] = 0


    def ensureInfoAvailable(self, infoTypes: 'RepoInfoFlags', blocking: bool = False) -> None:
        '''Ensure that the requested information is available in all listed repos.

        blocking: True - do not return before all information is available
                   False - return immediately and emit a completed() signal when all info is avaialble.
        '''
        self.clear()
        if len(self.repoList) == 0 or infoTypes.value == 0:
            # sometimes, we request information from an empty list or we reqest empty information

            # ensure progress dialog does not show up
            if self.progressDialog:
                self.progressDialog.setMaximum(1)
                self.progressDialog.setValue(1)

            self.sigInfoAvailable.emit()
            return

        steps = 0
        for infoFlag in RepoInfoFlags:
            if infoTypes & infoFlag:
                self.infoExpected[infoFlag] = len(self.repoList)
                steps += len(self.repoList)

        if self.progressDialog:
            self.progressDialog.setMaximum(steps)
            self.progressDialog.setValue(0)
            # self.progressDialog.show()
            QApplication.processEvents()

        # collect HEAD + URL at the same time
        # The code is kind of weird because we always call the same function. The trick is that since genCallbackInfoAvailable()
        # uses the number of info fields to advance the steps toward completion, if we request only URL but use genCallbackInfoAvailable()
        # with 2 fields, it will advance by 2 steps and mess the count
        if (RepoInfoFlags.HEAD in infoTypes) or (RepoInfoFlags.URL in infoTypes):
            flagsToFill: RepoInfoFlags
            if (RepoInfoFlags.HEAD in infoTypes) and (RepoInfoFlags.URL in infoTypes):
                flagsToFill = RepoInfoFlags.HEAD | RepoInfoFlags.URL
            elif (RepoInfoFlags.HEAD in infoTypes):
                flagsToFill = RepoInfoFlags.HEAD
            else:
                flagsToFill = RepoInfoFlags.URL
            for repo in self.repoList:
                repo.ensure_head_and_url(blocking, self.genCallbackInfoAvailable(flagsToFill))
                QApplication.processEvents()

        if RepoInfoFlags.SHA1 in infoTypes:
            for repo in self.repoList:
                repo.ensure_sha1(self.genCallbackInfoAvailable(RepoInfoFlags.SHA1), blocking)
                QApplication.processEvents()

        if RepoInfoFlags.ALL_TAGS in infoTypes:
            for repo in self.repoList:
                repo.ensure_all_tags_filled(self.genCallbackInfoAvailable(RepoInfoFlags.ALL_TAGS), blocking)
                QApplication.processEvents()

        if RepoInfoFlags.DIFF_SUMMARY in infoTypes:
            for repo in self.repoList:
                repo.ensure_diff_summary(self.genCallbackInfoAvailable(RepoInfoFlags.DIFF_SUMMARY), blocking)
                QApplication.processEvents()

        if RepoInfoFlags.ALL_BRANCHES in infoTypes:
            for repo in self.repoList:
                repo.ensure_branches_filled(self.genCallbackInfoAvailable(RepoInfoFlags.ALL_BRANCHES), blocking)
                QApplication.processEvents()

        if RepoInfoFlags.FILES_SHA1 in infoTypes:
            for repo in self.repoList:
                repo.ensure_files_sha1_filled(self.genCallbackInfoAvailable(RepoInfoFlags.FILES_SHA1), blocking)
                QApplication.processEvents()


    def genCallbackInfoAvailable(self, repoInfos: RepoInfoFlags) -> Callable[..., None]:
        '''Return a function which will call self.repoInfoAvailable() with the repoInfos argument.

        To be used to generate a callback .
        '''
        def callbackRepoInfoAvailable(*args: Any) -> None:
            self.repoInfoAvailable(repoInfos)

        return callbackRepoInfoAvailable


    def repoInfoAvailable(self, infoTypes: 'RepoInfoFlags') -> None:
        '''Notify that the given information is available on a new repo.

        Emit sigInfoAvailable() if all information expected is now available.
        '''
        for infoFlag in RepoInfoFlags:
            if infoTypes & infoFlag:
                self.infoAvailable[infoFlag] += 1
                if self.progressDialog:
                    self.progressDialog.setValue(self.progressDialog.value() + 1)
                    QApplication.processEvents()  # give a chance to asynchronous jobs to complete + refresh dialog
        self.emitSigInfoAvailableIfDone()


    def emitSigInfoAvailableIfDone(self) -> None:
        if self.isAllInfoAvailable():
            self.sigInfoAvailable.emit()


    def isAllInfoAvailable(self) -> bool:
        '''Return True if all expectations are met'''
        for infoFlag in RepoInfoFlags:
            if self.infoExpected[infoFlag] != self.infoAvailable[infoFlag]:
                return False

        return True