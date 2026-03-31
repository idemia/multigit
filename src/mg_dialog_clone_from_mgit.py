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


from typing import TYPE_CHECKING, List, Optional, cast
import logging, pathlib, json, os, subprocess, time, sys

from PySide6.QtGui import QRegularExpressionValidator, QColor
from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox, QTreeWidgetItem, QPushButton, QDialogButtonBox
from PySide6.QtCore import Qt, QTimer, QRegularExpression

if TYPE_CHECKING:
    from src.mg_window import MgMainWindow
from src.gui.ui_clone_from_mgit import Ui_CloneFromMgitFile
from src.mg_json_mgit_parser import ProjectStructure
import src.mg_config as mgc
from src.mg_dialog_utils import reBranchTagValues
from src.mg_utils import set_username_on_git_url
from src.mg_plugin_mgr import pluginMgrInstance
from src.mg_clone_execution import cloneFromDialog, CloneExistDirBehavior

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
        self.setWindowFlags( self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.ui = Ui_CloneFromMgitFile()
        self.ui.setupUi(self)
        self.ui.labelProjDesc.setVisible(False)
        self.ui.textEditProjectDesc.setVisible(False)
        self.cloneButton = QPushButton('Clone', self)
        self.ui.buttonBox.addButton(self.cloneButton, QDialogButtonBox.ButtonRole.AcceptRole)

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

        self.ui.radioDoNotAlterUrl.clicked.connect(self.slotUsernameUpdated)
        self.ui.radioForceUsername.clicked.connect(self.slotUsernameUpdated)
        self.ui.radioStripUsername.clicked.connect(self.slotUsernameUpdated)

        self.userFinishedTypingUsernameTimer = QTimer(self)
        self.userFinishedTypingUsernameTimer.setSingleShot(True)
        self.userFinishedTypingUsernameTimer.setInterval(1000)
        self.userFinishedTypingUsernameTimer.timeout.connect(self.slotUsernameUpdated)
        self.ui.lineEditUsername.textEdited.connect(self.slotUsernameTimer)

        self.proj = ProjectStructure()
        self.proj_copy: Optional[ProjectStructure] = None

        validator = QRegularExpressionValidator(QRegularExpression(reBranchTagValues))
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
        self.ui.treeWidgetRepoList.sortByColumn(0, Qt.SortOrder.AscendingOrder)

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
        dbg('slotUsernameUpdated')
        username = self.ui.lineEditUsername.text()

        # we use the original repository url for performing the transformation, if possible
        if self.proj_copy is None:
            proj_src = self.proj
        else:
            proj_src = self.proj_copy
        orig_url_dict = { repo.destination: repo.url for repo in proj_src.repos }
        for repo in self.proj.repos:
            orig_url = orig_url_dict[repo.destination]
            if self.ui.radioDoNotAlterUrl.isChecked():
                repo.url = orig_url
            elif self.ui.radioStripUsername.isChecked():
                repo.url = set_username_on_git_url( '', orig_url )
            elif self.ui.radioForceUsername.isChecked():
                repo.url = set_username_on_git_url(username, orig_url)
            else:
                raise AssertionError('No radio for url behavior is checked!')

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
                item.setForeground(3, QColor(Qt.GlobalColor.red))
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
        For report_parse_errors, open a warning dialog when the multigit file does not parse correctly.

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
        self.proj_copy = None

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

        self.proj_copy = ProjectStructure()
        self.proj_copy.fill_from_json_file(mgitFile,
                                      pathlib.Path(self.ui.lineEditDestDir.text()))
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


    def getExistingDirBehavior(self) -> CloneExistDirBehavior:
        if self.ui.radioButtonDirExistsDelDir.isChecked():
            return CloneExistDirBehavior.deleteDirectory

        if self.ui.radioButtonDirExistsSkipDir.isChecked():
            return CloneExistDirBehavior.skipClone

        if self.ui.radioButtonDirExistsGitFail.isChecked():
            return CloneExistDirBehavior.gitFails

        assert False, "No radio button checked for directory behavior"


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
            buttonSelectedWarning = QMessageBox.warning(self, 'Repository with empty URL', msg, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort)
            if buttonSelectedWarning == QMessageBox.StandardButton.Abort:
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
            buttonSelectedWarning = QMessageBox.warning(self, 'Repository with ssh URL and no user defined', msg, QMessageBox.StandardButton.Abort)
            return


        mgc.get_config_instance().lruSetRecent(mgc.CONFIG_LAST_PROJECT_DIR, self.ui.lineEditDestDir.text())
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
    dbg('runDialogCloneFromMgitFile')

    dialogCloneFromMgitFile = MgDialogCloneFromMgitFile(window)

    # display dialog
    dlg_result = dialogCloneFromMgitFile.exec()
    if not dlg_result:
        # Cancel was clicked, do nothing
        return

    mgc.get_config_instance().lruSetRecent(mgc.CONFIG_LAST_MGIT_FILE, dialogCloneFromMgitFile.ui.lineEditMgitFile.text())
    cloneFromDialog(dialogCloneFromMgitFile.proj, window, dialogCloneFromMgitFile.getExistingDirBehavior())

