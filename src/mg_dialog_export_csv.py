#    Copyright (c) 2019-2023 IDEMIA
#    Author: IDEMIA (Philippe Fremy, Florent Oulieres)
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#         http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#


from typing import List
import logging

from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox, QApplication
from PySide6.QtCore import Qt

import src.mg_config as mgc
from src.mg_repo_info import MgRepoInfo, MultiRepo
from src.gui.ui_export_csv import Ui_dialogCsvExport

logger = logging.getLogger('mg_dialog_export_mgit')
dbg = logger.debug


def runDialogExportCsv(window: QWidget, multiRepo: MultiRepo) -> None:
    """
    Dialog to export current repository state to a multigit file.
    """
    dbg('runDialogExportCsv')
    allRepos = multiRepo.repo_list
    if len(allRepos) == 0:
        QMessageBox.warning(window, 'No repository defined',
                            'Warning: can not export when base directory is not defined.')
        return

    # trigger an asynchronous all repo refresh to shorten the global time when retrieving the CSV information
    for repo_info in allRepos:
        repo_info.ensure_head_and_url_and_commit_date(blocking=False)

    dlg = QDialog(window)
    dlg.setWindowFlags(dlg.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
    dlg.setWindowTitle('Choose CSV fields')
    ui = Ui_dialogCsvExport()
    ui.setupUi(dlg)

    dbg('slotExportCsv() - Showing dialog for CSV fields')
    result = dlg.exec()
    dbg('slotExportCsv() - dialog done')

    if not result:
        return

    lastdir = mgc.get_config_instance().lruGetFirst(mgc.CONFIG_LAST_OPENED) or ''
    csvFname, _filter = QFileDialog.getSaveFileName(window, 'Choose CSV file to export', lastdir, '*.csv')
    if not csvFname:
        return

    dbg('slotExportCsv() - processing events')
    QApplication.processEvents()  # give a chance to asynchronous jobs to complete

    fieldsRequested = {
        'head':        ui.checkHead.isChecked(),
        'url':         ui.checkUrl.isChecked(),
        'path':        ui.checkPath.isChecked(),
        'commit_sha1': ui.checkCommitSha1.isChecked(),
        'commit_date': ui.checkCommitDate.isChecked(),
        'branch':      ui.checkCurrentBranch.isChecked(),
        'tag':         ui.checkCurrentTag.isChecked(),
    }
    multiRepo.exportCsv(csvFname, fieldsRequested)
    QMessageBox.information(window, "Export configuration file", "Data exported successfully to {}".format(csvFname))

