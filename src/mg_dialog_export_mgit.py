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


from typing import List, Any, TYPE_CHECKING
import logging

from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QTimer

if TYPE_CHECKING:
    from src.mg_window import MgMainWindow
from src.gui.ui_export_mgit import Ui_ExportMgit
from src.mg_repo_info import MgRepoInfo
from src.mg_ensure_info_available import MgEnsureInfoAvailable, RepoInfoFlags
from src.mg_json_mgit_parser import exportToMgit
from src.mg_utils import add_suffix_if_missing
import src.mg_config as mgc
from src.mg_const import MSG_EMPTY_REPO, MSG_LOCAL_BRANCH, MSG_REMOTE_BRANCH_GONE

logger = logging.getLogger('mg_dialog_export_mgit')
dbg = logger.debug
warn = logger.warning


class MgDialogExportMgit(QDialog):

    def __init__(self, window: QWidget, allRepos: List[MgRepoInfo]) -> None:
        super().__init__(window)
        # noinspection PyTypeChecker
        self.setWindowFlags( self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.ui = Ui_ExportMgit()
        self.ui.setupUi(self)

        self.mgitFname = ''
        self.exportAsSnapshot = False
        self.allRepos = allRepos

        # set last values
        self.ui.historyButtonMgitFile.fillHistory(mgc.get_config_instance().lruAsList(mgc.CONFIG_LAST_MGIT_FILE))
        self.ui.lineEditMgitFile.setText('')

        # connect buttons to their slot
        self.ui.pushButtonChooseMgitFile.clicked.connect(self.slotChooseMgitFile)
        self.ui.historyButtonMgitFile.historyItemTriggered.connect(self.slotMgitFileHistoryTriggered)
        self.ui.pushButtonExportProject.clicked.connect(self.slotExportAsProject)
        self.ui.pushButtonExportSnapshot.clicked.connect(self.slotExportAsSnapshot)
        self.ui.pushButtonCancel.clicked.connect(self.reject)

        QTimer.singleShot(0, self.slotEnsureRepoFilled)


    def slotEnsureRepoFilled(self) -> None:
        '''While showing the dialog, start filling all repos'''
        self.ensureInfoAvailable = MgEnsureInfoAvailable(self, self.allRepos)
        # request all information in advance while the user is manipulating the dialog
        self.ensureInfoAvailable.ensureInfoAvailable(RepoInfoFlags.HEAD | RepoInfoFlags.URL, blocking=False)
        # call it in a second step because maybe we don't need it
        self.ensureInfoAvailable.ensureInfoAvailable(RepoInfoFlags.SHA1, blocking=False)


    def slotMgitFileHistoryTriggered(self, title: str, _message: str) -> None:
        '''History of Mgit file triggered, open the targeted mgit file'''
        self.ui.lineEditMgitFile.setText(title)


    def slotChooseMgitFile(self) -> None:
        """
        function called when pushing button to select configuration files
        """
        dbg('slotChooseMgitFile')

        mgitFile = self.ui.lineEditMgitFile.text()

        # ask user to select configuration file
        lastdir = mgc.get_config_instance().lruGetFirst(mgc.CONFIG_LAST_OPENED) or ''

        mgitFile, _ = QFileDialog.getSaveFileName(self, "Select destination multigit file",
                    mgitFile or lastdir, "Multigit files (*.mgit)")

        if not mgitFile:
            # dialog canceled, do nothing
            return

        self.ui.lineEditMgitFile.setText(mgitFile)


    def slotExportAsProject(self) -> None:
        '''Called when exporting as project'''
        self.exportAsSnapshot = False
        self.accept()


    def slotExportAsSnapshot(self) -> None:
        '''Called when exporting as snapshot'''
        self.exportAsSnapshot = True
        self.accept()


    def accept(self) -> None:
        '''Called when the dialog is validated'''
        if self.ui.lineEditMgitFile.text() == '':
            QMessageBox.warning(self, 'No multigit file', 'You must choose a destination multigit file.')
            return

        # We had a bug report once that a repo may have been deleted in the meantime. This is
        # confusing for the user because the deletion of repo updated the main window with the list of repositories
        # and the list of repo is updated by removing the repo. So, the user legitimately believes that the deleted
        # directory is not included in the export. However, the list we use here has not yet been updated.
        # So, add a warning for this case.

        # filter directly without warning if the repo no longer exists
        for repo in self.allRepos:
            if repo.is_deleted:
                dbg(f'Removing deleted repo from list: {repo.name}')
        self.allRepos = [repo for repo in self.allRepos if not repo.is_deleted ]


        # we want to have the URL available
        ensureInfoAvailable = MgEnsureInfoAvailable(self, self.allRepos, showProgressDialog=False)
        ensureInfoAvailable.ensureInfoAvailable(RepoInfoFlags.URL, blocking=True)

        repoWithEmtpyUrl = [repo.name for repo in self.allRepos if repo.url == '']
        if len(repoWithEmtpyUrl):
            msg = '''The following repositories have no remote URL defined and can not be used for a future 
            clone operation:<ul>\n<li>'''
            msg += '\n<li> '.join(repoWithEmtpyUrl)
            msg += '''</ul>What do you want to do ?<p>'''
            msgBox = QMessageBox(QMessageBox.Icon.Warning, 'Repositories with empty remote URL', msg)
            msgBox.setTextFormat(Qt.TextFormat.RichText)
            buttonCancel = msgBox.addButton(QMessageBox.StandardButton.Cancel)
            buttonSkip = msgBox.addButton('Skip repositories', QMessageBox.ButtonRole.AcceptRole)
            buttonContinue = msgBox.addButton('Continue', QMessageBox.ButtonRole.AcceptRole)
            msgBox.exec()
            buttonSelected = msgBox.clickedButton()
            if buttonSelected == buttonCancel:
                return
            elif buttonSelected == buttonSkip:
                # adjust the list of repositories before accepting the dialog
                self.allRepos = [repo for repo in self.allRepos if repo.url != '']

        repoWithLocalOnlyBranch = [repo for repo in self.allRepos
                                   if repo.branch != '' and repo.remote_synchro in (MSG_REMOTE_BRANCH_GONE, MSG_LOCAL_BRANCH)]
        if len(repoWithLocalOnlyBranch):
            msg = '''Some repositories are on a branch which does not exist remotely. The clone operation 
            from this multigit file will fail. The repositories are:<ul><li>'''
            msg += '\n<li> '.join(f'Repository {repo.name} - branch {repo.branch}' for repo in repoWithLocalOnlyBranch)
            msg += '''</ul>What do you want to do ?<p>'''
            msgBox = QMessageBox(QMessageBox.Icon.Warning, 'Repositories with local only branch', msg)
            msgBox.setTextFormat(Qt.TextFormat.RichText)
            msgBox.setText(msg)
            buttonCancel = msgBox.addButton(QMessageBox.StandardButton.Cancel)
            buttonContinue = msgBox.addButton('Continue', QMessageBox.ButtonRole.AcceptRole)
            msgBox.exec()
            buttonSelected = msgBox.clickedButton()
            if buttonSelected == buttonCancel:
                return

        self.mgitFname = add_suffix_if_missing(self.ui.lineEditMgitFile.text(), '.mgit')

        mgc.get_config_instance().lruSetRecent(mgc.CONFIG_LAST_MGIT_FILE, self.mgitFname)
        mgc.get_config_instance().save()
        # everyting is fine, accept the dialog
        super().accept()


def runDialogExportMgit(window: QWidget, allRepos: List[MgRepoInfo]) -> None:
    """
    Dialog to export current repository state to a multigit file.
    """
    dbg('runDialogExportMgit')
    if len(allRepos) == 0:
        QMessageBox.warning(window, 'No repository defined',
                            'Warning: can not export when base directory is not defined.')
        return

    dialogExportMgit = MgDialogExportMgit(window, allRepos)

    # display dialog
    dlg_result = dialogExportMgit.exec()
    if not dlg_result:
        # Cancel was clicked, do nothing
        return

    # now, ensure all information is really available with a progress bar before calling exportToMgit()
    ensureInfoAvailable = MgEnsureInfoAvailable(dialogExportMgit, dialogExportMgit.allRepos, showProgressDialog=True)
    infoRequested = RepoInfoFlags.HEAD | RepoInfoFlags.URL
    if dialogExportMgit.exportAsSnapshot:
        infoRequested |= RepoInfoFlags.SHA1

    ensureInfoAvailable.ensureInfoAvailable(infoRequested, blocking=True)


    exportToMgit(dialogExportMgit.mgitFname,
                 dialogExportMgit.ui.lineEditDescMgit.text(),
                 dialogExportMgit.allRepos, snapshotMode=dialogExportMgit.exportAsSnapshot)


    QMessageBox.information(window, 'Information exported',
                            'Export done to %s' % dialogExportMgit.mgitFname,
                            QMessageBox.StandardButton.Ok)
