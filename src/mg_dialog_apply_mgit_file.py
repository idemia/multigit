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


from typing import List, Any, TYPE_CHECKING, Set
import logging, pathlib, json, os, subprocess, shutil, time, stat

from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox, QTreeWidgetItem, QPushButton, QDialogButtonBox
from PySide6.QtCore import Qt, QTimer, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

if TYPE_CHECKING:
    from src.mg_window import MgMainWindow
from src.gui.ui_apply_mgit_file import Ui_ApplyMgitFile
from src.mg_json_mgit_parser import ProjectStructure
import src.mg_config as mgc
from src.mg_exec_window import MgExecWindow
from src.mg_repo_info import MgRepoInfo
from src.mg_utils import deleteDirList, set_username_on_git_url
from src.mg_dialog_utils import reBranchTagValues
from src.mg_exec_task_item import MgExecTaskGroup
from src.mg_dialog_clone_from_mgit import addPreconditionToEnsureCloneOrderLogic

logger = logging.getLogger('mg_dialog_adjust_project_from_mgit')
dbg = logger.debug
warn = logger.warning


# Cases:
# 1. projConfFile and projDestDir are valid
# 2. update projConfFile
#       2.a -> parse the file -> valid file -> update full GUI
#       2.b -> parse the file -> invalid file -> report error, clear the GUI
# 3. update projDestDir
#       3.a update proj repos destination -> update the display of repo items
#       3.b json file was invalid -> do nothing


class MgDialogApplyMgitFile(QDialog):

    def __init__(self, window: QWidget, destDir: str, currentRepos: List[MgRepoInfo]) -> None:
        super().__init__(window)
        # noinspection PyTypeChecker
        self.setWindowFlags( self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.ui = Ui_ApplyMgitFile()
        self.ui.setupUi(self)
        self.ui.lineEditDestDir.setText(destDir)
        self.ui.labelProjDesc.setVisible(False)
        self.ui.textEditProjectDesc.setVisible(False)
        self.adjustButton = QPushButton(' Adjust Project ', self)
        self.ui.buttonBox.addButton(self.adjustButton, QDialogButtonBox.ButtonRole.AcceptRole)

        self.userFinishedTypingMgitFileTimer = QTimer(self)
        self.userFinishedTypingMgitFileTimer.setSingleShot(True)
        self.userFinishedTypingMgitFileTimer.setInterval(1000)
        self.userFinishedTypingMgitFileTimer.timeout.connect(lambda: self.propagateMgitFileUpdated(False, True))
        self.ui.lineEditMgitFile.textEdited.connect(self.slotMgitFileEdited)

        self.userFinishedTypingUsernameTimer = QTimer(self)
        self.userFinishedTypingUsernameTimer.setSingleShot(True)
        self.userFinishedTypingUsernameTimer.setInterval(1000)
        self.userFinishedTypingUsernameTimer.timeout.connect(self.slotUsernameUpdated)
        self.ui.lineEditUsername.textEdited.connect(self.slotUsernameEdited)
        validator = QRegularExpressionValidator(QRegularExpression(reBranchTagValues))
        self.ui.lineEditUsername.setValidator(validator)
        self.ui.historyButtonUsername.fillHistory(mgc.get_config_instance().lruAsList(mgc.CONFIG_CLONE_USERNAME))
        self.ui.lineEditUsername.setText(mgc.get_config_instance().lruGetFirst(mgc.CONFIG_CLONE_USERNAME) or '')


        self.currentRepos = currentRepos
        self.proj = ProjectStructure()
        self.reposToClone: List[str] = []

        # set last values
        self.ui.historyButtonMgitFile.fillHistory(mgc.get_config_instance().lruAsList(mgc.CONFIG_LAST_MGIT_FILE))
        self.ui.lineEditMgitFile.setText('')

        # configure QtreeWidget to display list of repositories
        f = self.ui.treeWidgetRepoList.header().font()
        f.setBold(True)
        self.ui.treeWidgetRepoList.header().setFont(f)
        self.ui.treeWidgetRepoList.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        # if both items are filled and exist, updates repos

        # connect buttons to their slot
        self.ui.pushButtonChooseMgitFile.clicked.connect(self.slotChooseMgitFile)
        self.ui.historyButtonMgitFile.historyItemTriggered.connect(self.slotMgitFileHistoryTriggered)
        self.ui.historyButtonUsername.historyItemTriggered.connect(self.slotUsernameHistoryTriggered)

        QTimer.singleShot(500, lambda: self.propagateMgitFileUpdated(False, True))


    def slotMgitFileEdited(self, _text: str) -> None:
        '''Called when user modifies the text'''
        # we wait for 0.5 s then refresh the analysis of the file
        self.userFinishedTypingMgitFileTimer.start()


    def slotUsernameEdited(self, _text: str) -> None:
        '''Called when user modifies the text of the username'''
        # we wait for 0.5 s then refresh the analysis of the file
        self.userFinishedTypingUsernameTimer.start()


    def slotUsernameHistoryTriggered(self, title: str, _message: str) -> None:
        '''Username history button triggered, update the line edit box and update the view of repos'''
        self.ui.lineEditUsername.setText(title)
        self.slotUsernameUpdated()


    def slotUsernameUpdated(self) -> None:
        '''Called when the timer of username update is triggered or when history of username is used'''
        username = self.ui.lineEditUsername.text()
        for repo in self.proj.repos:
            repo.url = set_username_on_git_url(username, repo.url)
        self.updateDisplayOfMultigitFile()


    def updateDisplayOfMultigitFile(self) -> None:
        '''Display the project content: items and and in text form'''
        self.ui.textEditProj.setText(str(self.proj))
        # first clear the QTreeWidget
        self.ui.treeWidgetRepoList.clear()
        if len(self.proj.description):
            self.ui.labelProjDesc.setVisible(True)
            self.ui.textEditProjectDesc.setVisible(True)
            self.ui.textEditProjectDesc.setText('<p style="vertical-align: middle">%s</p>' % self.proj.description)
        else:
            self.ui.labelProjDesc.setVisible(False)
            self.ui.textEditProjectDesc.setVisible(False)

        for repo in self.proj.repos:
            # create an item for each repository using MgRepoTreeItem
            # redefined columns for needs of cloning
            QTreeWidgetItem(self.ui.treeWidgetRepoList, [repo.destination, repo.pretty_head(), repo.dest_fullpath])
            # adjust columns size
            for i in range(self.ui.treeWidgetRepoList.columnCount()):
                self.ui.treeWidgetRepoList.resizeColumnToContents(i)


    def slotMgitFileHistoryTriggered(self, title: str, _message: str) -> None:
        '''History of Mgit file triggered, open the targeted mgit file'''
        self.ui.lineEditMgitFile.setText(title)
        self.propagateMgitFileUpdated(False, True)


    def slotChooseMgitFile(self) -> None:
        """
        function called when pushing button to select configuration files
        """
        dbg('slotChooseMgitFile')
        # default configuration file
        mgitFile = self.ui.lineEditMgitFile.text()
        # ask user to select configuration file
        mgitFile, _ = QFileDialog.getOpenFileName(self,
                                                        "Select Multigit File",
                                                        mgitFile,
                                                        "Multigit files (*.mgit);;Project Configuration File (*.json)")

        if not mgitFile:
            # dialog canceled, do nothing
            return

        self.ui.lineEditMgitFile.setText(mgitFile)
        # this will trigger a redisplay of all repos, no need for explicit call to self.updateDisplayOfMultigitFile()
        self.slotUsernameUpdated()


    def propagateMgitFileUpdated(self, report_file_errors: bool = True, report_parse_errors: bool = True) -> bool:
        '''Parse the json file and udpate the full dialog.

        For report_file_errors, open a warning dialog when the file text is empty or the file does not exist.
        For report_parse_erorrs, open a warning dialog when the multigit file does not parse correctly.

        Report parse errors
        in a dilog if report_errors is set to True.

        Input data is taken from the widgets:
        * lineEditMgitFile
        * lineEditProjDir

        Return True if everything is valid
        '''
        # clear the project analysis widgets
        self.ui.textEditProj.setText(str(self.proj))
        self.ui.treeWidgetRepoList.clear()

        mgitFile = self.ui.lineEditMgitFile.text()

        # reset proj so that in case of error, all information displayed is empty
        self.proj = ProjectStructure()

        if mgitFile == '':
            if report_file_errors:
                QMessageBox.warning(self, 'Multigit file error',
                                    'Multigit file path is empty.')
            self.updateDisplayOfMultigitFile()
            return False

        if not os.path.exists(mgitFile):
            if report_file_errors:
                QMessageBox.warning(None, 'Multigit file error', 'File does not exist: %s' % mgitFile)
            self.updateDisplayOfMultigitFile()
            return False

        if not os.path.isfile(mgitFile):
            if report_file_errors:
                QMessageBox.warning(None, 'Multigit file error', 'This is not a file: %s' % mgitFile)
            self.updateDisplayOfMultigitFile()
            return False

        try:
            self.proj.fill_from_json_file(mgitFile,
                                    pathlib.Path(self.ui.lineEditDestDir.text()))
        except json.JSONDecodeError as exc:
            if report_parse_errors:
                QMessageBox.warning(None, 'Multigit parse error', 'Error during parsing of multigit file %s\n%s' % (mgitFile, str(exc)))
            self.updateDisplayOfMultigitFile()
            return False

        # this will trigger a redisplay of all repos, no need for explicit call to self.updateDisplayOfMultigitFile()
        self.slotUsernameUpdated()

        return True


    def accept(self) -> None:
        '''Called when the dialog is validated'''
        if not self.propagateMgitFileUpdated(True, True):
            # there are errors, can not accept the dialog
            return

        targetRepoSet = set(repo.destination for repo in self.proj.repos)
        currentRepoSet = set(repo.name for repo in self.currentRepos)

        repoNameToCreate = targetRepoSet - currentRepoSet
        repoPathToCreateDirExists = set(repo.dest_fullpath for repo in self.proj.repos
                                            if repo.destination in repoNameToCreate and os.path.exists(repo.dest_fullpath))
        repoNameToRemove = currentRepoSet - targetRepoSet
        repoPathToRemove = [repo.fullpath for repo in self.currentRepos if repo.name in repoNameToRemove]


        if len(repoNameToCreate):
            msg = ''
            msg += 'The following repositories do not exist. They will be cloned:\n - '
            msg += '\n - '.join(repoNameToCreate)
            msg += '\n'
            buttonPressed = QMessageBox.warning(self, 'Cloning repositories', msg, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if buttonPressed != QMessageBox.StandardButton.Ok:
                return

            repoWithEmptyUrl = [
                repo.destination
                for repo in self.proj.repos
                if repo.destination in repoNameToCreate and repo.url == ''
            ]


            if len(repoWithEmptyUrl):
                msg = 'The following repositories to clone have an empty URL. They can not be cloned and will be skipped:\n- ' + '\n- '.join(repoWithEmptyUrl)
                buttonSelectedWarning = QMessageBox.warning(self, 'Repository with empty URL', msg, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort)
                if buttonSelectedWarning == QMessageBox.StandardButton.Abort:
                    # user wants to check what is going on
                    return

            self.reposToClone = list(sorted(repoNameToCreate))


        if len(repoPathToCreateDirExists):
            msg = ''
            msg += 'The following directories will be removed to allow the git clone:\n - '
            msg += '\n - '.join(repoPathToCreateDirExists)
            msg += '\n'
            buttonPressed = QMessageBox.warning(self, 'Removing directories', msg, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if buttonPressed != QMessageBox.StandardButton.Ok:
                return
            # remove target directory if it already exists to make clone smooth
            result = deleteDirList(repoPathToCreateDirExists)
            if len(result):
                buttonPressed = QMessageBox.warning(self, 'Error during removal of directories',
                                                    'Error during removal of directories: ' + result,
                                                    QMessageBox.StandardButton.Abort | QMessageBox.StandardButton.Ok)
                if buttonPressed != QMessageBox.StandardButton.Ok:
                    return

        if len(repoNameToRemove):
            msg = ''
            msg += 'The following repositories are not in the multigit file and will be removed:\n - '
            msg += '\n - '.join(repoNameToRemove)
            msg += '\n'
            buttonPressed = QMessageBox.warning(self, 'Removing repositories', msg, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if buttonPressed != QMessageBox.StandardButton.Ok:
                return
            # TODO: create a button "delete" for more clarity, and "skip" for even more clarity
            result = deleteDirList(repoPathToRemove)
            if len(result):
                buttonPressed = QMessageBox.warning(self, 'Error during removal of repositories',
                                                    'Error during removal of repositories: ' + result,
                                                    QMessageBox.StandardButton.Abort | QMessageBox.StandardButton.Ok)
                if buttonPressed != QMessageBox.StandardButton.Ok:
                    return

        mgc.get_config_instance().lruSetRecent(mgc.CONFIG_CLONE_USERNAME, self.ui.lineEditUsername.text())
        mgc.get_config_instance().lruSetRecent(mgc.CONFIG_LAST_MGIT_FILE, self.ui.lineEditMgitFile.text())
        mgc.get_config_instance().save()
        # everyting is fine, accept the dialog
        super().accept()


def runDialogApplyMgitFile(window: 'MgMainWindow', baseDir: str, allRepos: List[MgRepoInfo]) -> None:
    """
    This is the dialog to build project structure folders using json configuration file
    :param window: application window
    :return:
    """
    dialogApplyMgitFile = MgDialogApplyMgitFile(window, baseDir, allRepos)

    # display dialog
    dlg_result = dialogApplyMgitFile.exec()
    if not dlg_result:
        # Cancel was clicked, do nothing
        return

    # user clicked on OK, display the folder in the main window
    # performing project adjustment

    taskGroups: List[MgExecTaskGroup] = []
    reposToAdjust =  dialogApplyMgitFile.proj.repos[:]
    reposToAdjust.sort(key=lambda r: r.destination)

    for repoDictInfo in reposToAdjust:
        repoInfo = MgRepoInfo(repoDictInfo.destination, repoDictInfo.dest_fullpath, repoDictInfo.destination)
        if repoDictInfo.destination in dialogApplyMgitFile.reposToClone:
            if repoDictInfo.url == '':
                # user has already been warned about this
                continue

            # we must clone these, no checkout them
            taskGroup = MgExecTaskGroup(f'Cloning and checkouting repository {repoInfo.name}', repoInfo)
            taskGroup.appendGitTask(f'git clone {repoInfo.name}',
                                    ['clone', '--progress', repoDictInfo.url, repoDictInfo.dest_fullpath])
            taskGroup.appendGitTask(f'git checkout {repoDictInfo.head}',
                                    ['checkout', repoDictInfo.head])
        else:
            seq_of_git_cmd = [
                ['fetch', '--prune', '--tags'],
                ['checkout', repoDictInfo.head],
            ]
            taskGroup = MgExecTaskGroup(f'Fetching and checkouting repository {repoInfo.name}', repoInfo)
            taskGroup.appendGitTask(f'git fetch {repoInfo.name}',
                                    ['fetch', '--prune', '--tags'])
            taskGroup.appendGitTask(f'git checkout {repoDictInfo.head}',
                                    ['checkout', repoDictInfo.head, '--']
                                    )

        taskGroups.append( taskGroup )


    # Ensure that clone will work with nested subdirectories
    taskGroups = addPreconditionToEnsureCloneOrderLogic(taskGroups)

    gitExecWindow = MgExecWindow(window)
    gitExecWindow.execTaskGroups('Adjusting project repositories', taskGroups)
    gitExecWindow.finished.connect(lambda _result: window.actionRefreshAll.trigger())


# TODO:
# use colors just like in main repo display branch/tag/commit
# use colors just like in main repo display branch/tag/commit
