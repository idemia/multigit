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


from typing import TYPE_CHECKING, List, Optional
import logging, pathlib, json, os, subprocess, time

from PySide2.QtGui import QRegExpValidator, QColor
from PySide2.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox, QTreeWidgetItem, QPushButton, QDialogButtonBox
from PySide2.QtCore import Qt, QTimer, QRegExp

if TYPE_CHECKING:
    from src.mg_window import MgMainWindow
from src.gui.ui_clone_from_mgit import Ui_CloneFromMgitFile
from src.mg_json_mgit_parser import ProjectStructure
from src.mg_repo_info import MgRepoInfo
import src.mg_config as mgc
from src.mg_exec_window import MgExecWindow
from src.mg_exec_task_item import MgExecTaskGroup, after_other_taskgroup_is_started_and_dir_exists
from src.mg_dialog_utils import reBranchTagValues
from src.mg_utils import set_username_on_git_url, deleteDirList
from src.mg_plugin_mgr import pluginMgrInstance

logger = logging.getLogger('mg_dialog_clone_from_mgit')
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



class MgDialogCloneFromMgitFile(QDialog):

    def __init__(self, window: QWidget) -> None:
        super().__init__(window)
        # noinspection PyTypeChecker
        self.setWindowFlags( self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.ui = Ui_CloneFromMgitFile()
        self.ui.setupUi(self)
        self.ui.labelProjDesc.setVisible(False)
        self.ui.textEditProjectDesc.setVisible(False)
        self.cloneButton = QPushButton('Clone', self)
        self.ui.buttonBox.addButton(self.cloneButton, QDialogButtonBox.AcceptRole)

        self.userFinishedTypingMgitFileTimer = QTimer(self)
        self.userFinishedTypingMgitFileTimer.setSingleShot(True)
        self.userFinishedTypingMgitFileTimer.setInterval(1000)
        self.userFinishedTypingMgitFileTimer.timeout.connect(lambda: self.propagateMgitFileUpdated(False, True))
        self.ui.lineEditMgitFile.textEdited.connect(self.slotMgitFileTimer)

        self.userFinishedTypingDestDirTimer = QTimer(self)
        self.userFinishedTypingDestDirTimer.setSingleShot(True)
        self.userFinishedTypingDestDirTimer.setInterval(1000)
        self.userFinishedTypingDestDirTimer.timeout.connect(self.updateDestDir)
        self.ui.lineEditDestDir.textEdited.connect(self.slotDestDirTimer)

        self.userFinishedTypingUsernameTimer = QTimer(self)
        self.userFinishedTypingUsernameTimer.setSingleShot(True)
        self.userFinishedTypingUsernameTimer.setInterval(1000)
        self.userFinishedTypingUsernameTimer.timeout.connect(self.slotUsernameUpdated)
        self.ui.lineEditUsername.textEdited.connect(self.slotUsernameTimer)

        self.proj = ProjectStructure()

        validator = QRegExpValidator(QRegExp(reBranchTagValues))
        self.ui.lineEditUsername.setValidator(validator)

        # set last values
        self.ui.historyButtonMgitFile.fillHistory(mgc.get_config_instance().lruAsList(mgc.CONFIG_LAST_MGIT_FILE))
        self.ui.lineEditMgitFile.setText('')
        self.ui.historyButtonDestDir.fillHistory(mgc.get_config_instance().lruAsList(mgc.CONFIG_LAST_PROJECT_DIR))
        self.ui.lineEditDestDir.setText('')
        self.ui.historyButtonUsername.fillHistory(mgc.get_config_instance().lruAsList(mgc.CONFIG_CLONE_USERNAME))

        # configure QtreeWidget to display list of repositories
        f = self.ui.treeWidgetRepoList.header().font()
        f.setBold(True)
        self.ui.treeWidgetRepoList.header().setFont(f)
        self.ui.treeWidgetRepoList.sortByColumn(0, Qt.AscendingOrder)

        # if both items are filled and exist, updates repos

        # connect buttons to their slot
        self.ui.pushButtonChooseMgitFile.clicked.connect(self.slotChooseMgitFile)
        self.ui.pushButtonChooseDestDir.clicked.connect(self.slotChooseDestDir)
        self.ui.historyButtonMgitFile.historyItemTriggered.connect(self.slotMgitFileHistoryTriggered)
        self.ui.historyButtonDestDir.historyItemTriggered.connect(self.slotDestDirHistoryTriggered)
        self.ui.historyButtonUsername.historyItemTriggered.connect(self.slotUsernameHistoryTriggered)

        pluginMgrInstance.setupCloneDialog(self)

        QTimer.singleShot(500, lambda: self.propagateMgitFileUpdated(False, True))


    def slotMgitFileTimer(self, _text: str) -> None:
        '''Called when user modifies the text'''
        # we wait for 0.5 s then refresh the analysis of the file
        self.userFinishedTypingMgitFileTimer.start()


    def slotDestDirTimer(self, _text: str) -> None:
        '''Called when user modifies the text'''
        # we wait for 0.5 s then refresh the analysis of the file
        self.userFinishedTypingDestDirTimer.start()


    def slotUsernameTimer(self, _text: str) -> None:
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
            item = QTreeWidgetItem(self.ui.treeWidgetRepoList, [repo.destination, repo.head, repo.dest_fullpath, repo.url])
            if repo.url == '':
                item.setText(3, '  -- WARNING: Empty URL --  ')
                f = item.font(3)
                f.setBold(True)
                item.setFont(3, f)
                item.setForeground(3, QColor(Qt.red))
            # adjust columns size
            for i in range(self.ui.treeWidgetRepoList.columnCount()):
                self.ui.treeWidgetRepoList.resizeColumnToContents(i)


    def slotMgitFileHistoryTriggered(self, title: str, _message: str) -> None:
        '''History of Mgit file triggered, open the targeted mgit file'''
        self.ui.lineEditMgitFile.setText(title)
        self.propagateMgitFileUpdated(True, True)


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
        self.propagateMgitFileUpdated(True, True)


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


    def slotDestDirHistoryTriggered(self, title: str, _message: str) -> None:
        '''History of Destination dir triggered, open the targeted destination directory'''
        self.ui.lineEditDestDir.setText(title)
        self.updateDestDir()


    def slotChooseDestDir(self) -> None:
        """
        Called when pushing button to select project destination directory.

        Updates the display of the project file
        :return:
        """
        dbg('slotChooseDestDir')
        # default directory
        destDir = self.ui.lineEditDestDir.text()
        # ask user to select a destination directory for the user
        destDir = QFileDialog.getExistingDirectory(self, 'Choose directory where project will be cloned', destDir)
        if destDir == '':
            return

        self.ui.lineEditDestDir.setText(destDir)
        self.updateDestDir()


    def updateDestDir(self) -> None:
        # set the destination directory in the project object
        destDir = self.ui.lineEditDestDir.text()
        self.proj.set_base_path(pathlib.Path(destDir))
        self.updateDisplayOfMultigitFile()


    def accept(self) -> None:
        '''Called when the dialog is validated'''
        if self.ui.lineEditDestDir.text() == '':
            QMessageBox.warning(None, 'Destination directory error', 'Destination directory is not defined\n')
            return

        targetBaseDir = pathlib.Path(self.ui.lineEditDestDir.text())
        if targetBaseDir.exists() and not targetBaseDir.is_dir():
            QMessageBox.warning(None, 'Destination directory error', 'Destination is not a directory\n')
            return

        if not self.propagateMgitFileUpdated(True, True):
            # there are errors, can not accept the dialog
            return

        repoWithEmptyUrl: List[str] = []
        for repo in self.proj.repos:
            if repo.url == '':
                repoWithEmptyUrl.append(repo.destination)


        if len(repoWithEmptyUrl):
            msg = 'The following repositories have an empty URL. They will not be cloned:\n- ' + '\n- '.join(repoWithEmptyUrl)
            buttonSelectedWarning = QMessageBox.warning(self, 'Repository with empty URL', msg, QMessageBox.Ok | QMessageBox.Abort)
            if buttonSelectedWarning == QMessageBox.Abort:
                # user wants to check what is going on
                return

        repoWithSsh = False
        for repo in self.proj.repos:
            if repo.url.startswith('ssh:'):
                repoWithSsh = True
                break

        if repoWithSsh and self.ui.lineEditUsername.text() == '':
            # ssh cloning requires a username
            msg = 'You are cloning repositories with the ssh:// method, but you forgot to define the username in the dialog.\nSopping the operation'
            buttonSelectedWarning = QMessageBox.warning(self, 'Repository with ssh URL and no user defined', msg, QMessageBox.Abort)
            return


        mgc.get_config_instance().lruSetRecent(mgc.CONFIG_LAST_PROJECT_DIR, self.ui.lineEditDestDir.text())
        mgc.get_config_instance().lruSetRecent(mgc.CONFIG_LAST_MGIT_FILE, self.ui.lineEditMgitFile.text())
        mgc.get_config_instance().lruSetRecent(mgc.CONFIG_CLONE_USERNAME, self.ui.lineEditUsername.text())
        mgc.get_config_instance().save()
        # everyting is fine, accept the dialog
        super().accept()





def runDialogCloneFromMgitFile(window: 'MgMainWindow') -> None:
    """
    This is the dialog to build project structure folders using json configuration file
    :param window: application window
    :return:
    """

    dialogCloneFromMgitFile = MgDialogCloneFromMgitFile(window)

    # display dialog
    dlg_result = dialogCloneFromMgitFile.exec()
    if not dlg_result:
        # Cancel was clicked, do nothing
        return

    # user clicked on OK, display the folder in the main window
    # performing clone

    taskGroups: List[MgExecTaskGroup] = []
    reposToClone = dialogCloneFromMgitFile.proj.repos[:]
    reposToClone.sort(key=lambda r: r.destination)

    skipDir  = []
    toDelDir = []
    alreadyExists = []

    for jsonFileRepo in reposToClone:
        if jsonFileRepo.url == '':
            # the user was informed about this, skip the repo
            continue

        if os.path.exists(jsonFileRepo.dest_fullpath):
            # oh oh, directory exists, let see what user want us to do:
            if dialogCloneFromMgitFile.ui.radioButtonDirExistsSkipDir.isChecked():
                skipDir.append(jsonFileRepo.dest_fullpath)
                # the best way to skip is to do nothing
                continue

            if dialogCloneFromMgitFile.ui.radioButtonDirExistsDelDir.isChecked():
                toDelDir.append(jsonFileRepo.dest_fullpath)

            if dialogCloneFromMgitFile.ui.radioButtonDirExistsGitFail.isChecked():
                # this is the default behavior, so do nothing
                alreadyExists.append(jsonFileRepo.dest_fullpath)


        repoInfo = MgRepoInfo(jsonFileRepo.destination, jsonFileRepo.dest_fullpath, jsonFileRepo.destination)
        taskGroup = MgExecTaskGroup(f'Cloning {repoInfo.name}', repoInfo)
        taskGroup.appendGitTask(f'git clone {repoInfo.name}',
                                ['clone', '--progress', jsonFileRepo.url, jsonFileRepo.dest_fullpath],
                                run_inside_git_repo=False,
                                )

        if len(jsonFileRepo.head):
            # use checkout and not switch because HEAD may point to a branch, tag or commit SHA1
            taskGroup.appendGitTask( f'git checkout {jsonFileRepo.head}', ['checkout', jsonFileRepo.head, '--' ] )

        # if head is empty, the repo is probably empty, so do nothing

        taskGroups.append( taskGroup )

    if len(alreadyExists):
        msg = 'The following repositories already exists:\n'
        msg += '- ' + '\n- '.join(alreadyExists) + '\n\n'
        msg += 'Continue will trigger a git error for these repositories, please consider Deleting them.'
        msgBox = QMessageBox(window)
        msgBox.setWindowTitle('Confirm clone on existing')
        msgBox.setText(msg)
        continueButton = msgBox.addButton('Continue', QMessageBox.AcceptRole)
        delButton = msgBox.addButton('Delete directories', QMessageBox.AcceptRole)
        abortButton = msgBox.addButton(QMessageBox.Abort)
        msgBox.exec()
        buttonSelected = msgBox.clickedButton()

        if buttonSelected == abortButton:
            # user changed its mind ...
            return

        elif buttonSelected == delButton:
            # mark the directories to be deleted
            toDelDir = alreadyExists


    if len(skipDir):
        msg = 'The following repositories already exists and will NOT be cloned (skip behavior):\n'
        msg += '- ' + '\n- '.join(skipDir) + '\n'
        buttonSelectedWarning = QMessageBox.warning(window, 'Confirm skip of repositories', msg, QMessageBox.Ok | QMessageBox.Abort)
        if buttonSelectedWarning == QMessageBox.Abort:
            # user changed its mind ...
            return

    if len(toDelDir):
        # sorting in reverse order allows to remove subdirectories before updirectories
        toDelDir.sort(reverse=True)

        # alreadyExists is set when user chose no special action in the clone dialog, but
        # choose to delete in the second dialog
        if not alreadyExists:
            # the user has not yet validated the list of repos
            msg = 'The following repositories already exists and will be DELETED (delete behavior):\n'
            msg += '- ' + '\n- '.join(toDelDir) + '\n'
            buttonSelectedWarning = QMessageBox.warning(window, 'Confirm deletion of repositories', msg, QMessageBox.Ok | QMessageBox.Abort)
            if buttonSelectedWarning == QMessageBox.Abort:
                # user changed its mind ...
                return

        # kill tgitcache before anything. If it was running, it would prevent deletion of directories
        subprocess.call(['taskkill', '/t', '/f', '/im', 'tgitcache.exe'])

        deleteDirList(toDelDir)

        stillExists = [v for v in toDelDir if os.path.exists(v)]
        if len(stillExists):
            # let's try a second time with some delay
            time.sleep(0.5)
            deleteDirList(stillExists)

        results = ''
        stillExists = [v for v in toDelDir if os.path.exists(v)]
        if len(stillExists):
            # let's try a third time with more delay
            time.sleep(0.5)
            results = deleteDirList(stillExists)

        if len(results):
            msg = 'The deletion of repositories returned the following errors:\n' + results
            buttonSelectedWarning = QMessageBox.warning(window, 'Directory deletion error', msg, QMessageBox.Ok | QMessageBox.Abort)
            if buttonSelectedWarning == QMessageBox.Abort:
                # user wants to check what is going on
                return

        if len(stillExists):
            msg = 'Deletion of the following repositories failed:\n'
            msg += '- ' + '\n- '.join(stillExists)
            buttonSelectedWarning = QMessageBox.warning(window, 'Directory not deleted', msg, QMessageBox.Ok | QMessageBox.Abort)
            if buttonSelectedWarning == QMessageBox.Abort:
                # user wants to check what is going on
                return

    # Ensure that clone will work with nested subdirectories
    taskGroups = addPreconditionToEnsureCloneOrderLogic(taskGroups)

    # Give some time between two clones to make sure a clone is fully started
    # before the next one starts, because the next one may create some subdirectories
    # which would then prevent the first clone.
    gitExecWindow = MgExecWindow(window, 0.5)
    gitExecWindow.execTaskGroups('Clone project repositories', taskGroups)

    # show the newly created path in MultiGit
    gitExecWindow.finished.connect( lambda result: window.openDir(dialogCloneFromMgitFile.ui.lineEditDestDir.text()))


class TaskNode:
    def __init__(self, parent: Optional['TaskNode'], name: str, taskGroup: Optional[MgExecTaskGroup]) -> None:
        self.parent = parent
        self.name = name
        self.taskGroup = taskGroup
        self.children: List['TaskNode'] = []


    def addChild(self, parts: List[str], taskGroup: MgExecTaskGroup ) -> 'TaskNode':
        '''Add a child in the graph, in the right node'''
        if len(parts) == 0:
            # we are ready to set the task group
            self.taskGroup = taskGroup
            return self

        for child in self.children:
            if child.name == parts[0]:
                # we have found our children !
                break
        else:
            # we have found no children, create one
            child = TaskNode(self, parts[0], None)
            self.children.append(child)

        # continue the search
        return child.addChild(parts[1:], taskGroup)


def build_taskgroup_dep_graph(taskGroups: List[MgExecTaskGroup]) -> TaskNode:
    '''Build a dependency graph with the nodes and return the top node of the graph'''
    topNode = TaskNode(None, '', None)

    for taskGroup in taskGroups:
        splitter = '/'
        if not splitter in taskGroup.repo.name and '\\' in taskGroup.repo.name:
            splitter = '\\'
        topNode.addChild( taskGroup.repo.name.split(splitter), taskGroup )

    return topNode


def findParentTaskGroup(node: TaskNode) -> Optional[TaskNode]:
    '''Walk the parent of this tasknode until another tasknode is found and return it.

    If no tasknode is found, return None'''
    while node.parent is not None:
        if node.parent.taskGroup is not None:
            return node.parent

        node = node.parent

    return None


def addPreconditionsToTaskGroup(node: TaskNode) -> None:
    '''Using the graph, modify the taskGroup objects in place by adding preconditions
    when one taskGroup depends on another one.'''

    if node.taskGroup is not None:
        # add precondition for this node
        parentTaskGroupNode = findParentTaskGroup(node)

        if parentTaskGroupNode is not None:
            assert parentTaskGroupNode.taskGroup is not None
            node.taskGroup.pre_condition = after_other_taskgroup_is_started_and_dir_exists(parentTaskGroupNode.taskGroup)

    # add preconditions for this nodes children
    for n in node.children:
        addPreconditionsToTaskGroup(n)



def addPreconditionToEnsureCloneOrderLogic(taskGroups: List[MgExecTaskGroup]) -> List[MgExecTaskGroup]:
    '''Generate preconditions so that a subdirectory of a git repo is cloned after the git parent git repo.

    The taskGroup inside the list are modifed in place, with a new precondition.

    Example, with the structure:
    dev/ (git repo)
      + subdev1 (git repo)
        + subdev1_sub1 (git repo)
        + subdev1_sub2 (git repo)
      + subdev2 (git repo)
        + toto
           + subdev2_sub1 (git repo)

    It will generate the following pre-conditions:
    - subdev1 is cloned after dev/ clone has started
    - subdev1_sub1 is cloned after subdev1/ clone has started
    - subdev1_sub2 is cloned after subdev1/ clone has started
    - subdev2 is cloned after dev/ clone has started
    - subdev2_sub1 is cloned after subdev2/ clone has started
    '''
    topNode = build_taskgroup_dep_graph(taskGroups)

    addPreconditionsToTaskGroup(topNode)

    return taskGroups

# TODO
# - rename Structure  to JsonFileStructure
# - rename Repository to JsonFileRepo
# - rename Repository to JsonFilePostCloneCommand


