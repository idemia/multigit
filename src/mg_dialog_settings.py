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


from typing import TYPE_CHECKING, Literal, Union

import pathlib

from PySide2.QtWidgets import QFileDialog, QDialog, QColorDialog, QWidget
from PySide2.QtGui import QColor
from PySide2.QtCore import Qt


if TYPE_CHECKING:
    from src.mg_repo_tree import MgRepoTree
from src.gui.ui_preferences import Ui_Preferences
from src.mg_tools import autodetect_git_exec, autodetect_tortoise_git_exec, autodetect_sourcetree_exec, autodetect_sublimemerge_exec
from src.mg_const import DoubleClickActions
import src.mg_config as mgc


def runDialogEditSettings(parent: QWidget, tabPage: Union[Literal[0], Literal[1]]) -> None:
    '''Show the Edit Settings dialog'''
    dlg = QDialog(parent)
    dlg.setWindowFlags( dlg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    ui_pref = Ui_Preferences()
    ui_pref.setupUi(dlg)
    config = mgc.get_config_instance()

    # disable multigit update feature as it is not available
    ui_pref.groupBox_6.setVisible(False)

    ui_pref.tabWidget.setCurrentIndex(tabPage)

    def slotEditPrefBrowseForGit() -> None:
        '''Browse for git executable and set the result in the ui dialog'''
        current_git_exe = str(ui_pref.lineEditGitManual.text()) or 'C:\\'
        result, _ = QFileDialog.getOpenFileName(parent, "Select Git Executable", current_git_exe, "git.exe")
        if result:
            ui_pref.lineEditGitManual.setText(result)

    def slotEditPrefBrowseForTortoiseGit() -> None:
        '''Browse for TortoiseGitProc executable and set the result in the ui dialog'''
        current_tgit_exe = str(ui_pref.lineEditTGitManual.text()) or 'C:\\'
        result, _ = QFileDialog.getOpenFileName(parent, "Select the TortoiseGitProc Executable", current_tgit_exe, "TortoiseGitProc.exe")
        if result:
            ui_pref.lineEditTGitManual.setText(result)

    def slotEditPrefBrowseForSourcetree() -> None:
        '''Browse for Sourcetree executable and set the result in the ui dialog'''
        current_st_exe = str(ui_pref.lineEditSourcetreeManual.text()) or 'C:\\'
        result, _ = QFileDialog.getOpenFileName(parent, "Select Sourcetree Executable", current_st_exe, "SourceTree.exe")
        if result:
            ui_pref.lineEditSourcetreeManual.setText(result)

    colorBranch = QColor()
    colorBranch.setRgb(mgc.get_config_instance().get(mgc.CONFIG_HEAD_COLOR_BRANCH, mgc.DEFAULT_CONFIG_HEAD_COLOR_BRANCH))
    colorTag = QColor()
    colorTag.setRgb(mgc.get_config_instance().get(mgc.CONFIG_HEAD_COLOR_TAG, mgc.DEFAULT_CONFIG_HEAD_COLOR_TAG))

    def updateColorButtons() -> None:
        ui_pref.pushButtonColorBranch.setStyleSheet('background-color: '+colorBranch.name())
        ui_pref.pushButtonColorTag.setStyleSheet('background-color: '+colorTag.name())

    def slotSetColorBranch() -> None:
        color = QColorDialog.getColor(colorBranch)
        if color.isValid():
            colorBranch.setNamedColor(color.name())
            updateColorButtons()

    def slotSetColorTag() -> None:
        color = QColorDialog.getColor(colorTag)
        if color.isValid():
            colorTag.setNamedColor(color.name())
            updateColorButtons()

    ui_pref.pushButtonGitManualBrowse.clicked.connect( slotEditPrefBrowseForGit )
    ui_pref.pushButtonTGitManualBrowse.clicked.connect( slotEditPrefBrowseForTortoiseGit )
    ui_pref.pushButtonSourcetreeManualBrowse.clicked.connect( slotEditPrefBrowseForSourcetree )
    ui_pref.pushButtonColorBranch.clicked.connect( slotSetColorBranch )
    ui_pref.pushButtonColorTag.clicked.connect( slotSetColorTag )

    updateColorButtons()

    git_auto_detect = (True if config[mgc.CONFIG_GIT_AUTODETECT] is None
                             else config[mgc.CONFIG_GIT_AUTODETECT])
    ui_pref.radioGitAutoDetect.setChecked(git_auto_detect)
    ui_pref.lineEditGitAutoDetect.setText(autodetect_git_exec())
    ui_pref.radioGitManual.setChecked(not git_auto_detect)
    ui_pref.lineEditGitManual.setText(config[mgc.CONFIG_GIT_MANUAL_PATH] or '')
    ui_pref.lineEditGitManual.setEnabled(not git_auto_detect)
    ui_pref.pushButtonGitManualBrowse.setEnabled(not git_auto_detect)

    def enableTGitLineEditIfActivatedAndManual() -> None:
        ui_pref.lineEditTGitManual.setEnabled(
            ui_pref.checkBoxTortoiseGit.isChecked() and ui_pref.radioTGitManual.isChecked()
        )
    ui_pref.checkBoxTortoiseGit.toggled.connect(enableTGitLineEditIfActivatedAndManual)
    ui_pref.checkBoxTortoiseGit.setChecked(mgc.get_config_instance().get(mgc.CONFIG_TORTOISEGIT_ACTIVATED))
    tgit_auto_detect = True if config[mgc.CONFIG_TORTOISEGIT_AUTODETECT] is None else config[mgc.CONFIG_TORTOISEGIT_AUTODETECT]
    ui_pref.radioTGitAutoDetect.setChecked(tgit_auto_detect)
    ui_pref.lineEditTGitAutoDetect.setText(autodetect_tortoise_git_exec())
    ui_pref.radioTGitManual.setChecked(not tgit_auto_detect)
    ui_pref.lineEditTGitManual.setText(config[mgc.CONFIG_TORTOISEGIT_MANUAL_PATH] or '')
    ui_pref.lineEditTGitManual.setEnabled(not tgit_auto_detect)
    ui_pref.pushButtonTGitManualBrowse.setEnabled(not tgit_auto_detect)

    def enableSTreeLineEditIfActivatedAndManual() -> None:
        ui_pref.lineEditSourcetreeManual.setEnabled(
            ui_pref.checkBoxSourceTree.isChecked() and ui_pref.radioSourcetreeManual.isChecked()
        )
    ui_pref.checkBoxSourceTree.toggled.connect(enableSTreeLineEditIfActivatedAndManual)
    ui_pref.checkBoxSourceTree.setChecked(bool(mgc.get_config_instance().get(mgc.CONFIG_SOURCETREE_ACTIVATED)))
    stree_auto_detect = True if config[mgc.CONFIG_SOURCETREE_AUTODETECT] is None else config[mgc.CONFIG_SOURCETREE_AUTODETECT]
    ui_pref.radioSourcetreeAutoDetect.setChecked(stree_auto_detect)
    ui_pref.lineEditSourcetreeAutoDetect.setText(autodetect_sourcetree_exec())
    ui_pref.radioSourcetreeManual.setChecked(not stree_auto_detect)
    ui_pref.lineEditSourcetreeManual.setText(config[mgc.CONFIG_SOURCETREE_MANUAL_PATH] or '')
    ui_pref.lineEditSourcetreeManual.setEnabled(not stree_auto_detect)
    ui_pref.pushButtonSourcetreeManualBrowse.setEnabled(not stree_auto_detect)

    def enableSublimeLineEditIfActivatedAndManual() -> None:
        ui_pref.lineEditSublimemergeManual.setEnabled(
            ui_pref.checkBoxSublimeMerge.isChecked() and ui_pref.radioSublimemergeManual.isChecked()
        )
    ui_pref.checkBoxSublimeMerge.toggled.connect(enableSublimeLineEditIfActivatedAndManual)
    ui_pref.checkBoxSublimeMerge.setChecked(bool(mgc.get_config_instance().get(mgc.CONFIG_SUBLIMEMERGE_ACTIVATED)))
    smerge_auto_detect = True if config[mgc.CONFIG_SUBLIMEMERGE_AUTODETECT] is None else config[mgc.CONFIG_SUBLIMEMERGE_AUTODETECT]
    ui_pref.radioSublimemergeAutoDetect.setChecked(smerge_auto_detect)
    ui_pref.lineEditSublimemergeAutoDetect.setText(autodetect_sublimemerge_exec())
    ui_pref.radioSublimemergeManual.setChecked(not smerge_auto_detect)
    ui_pref.lineEditSublimemergeManual.setText(config[mgc.CONFIG_SUBLIMEMERGE_MANUAL_PATH] or '')
    ui_pref.lineEditSublimemergeManual.setEnabled(not smerge_auto_detect)
    ui_pref.pushButtonSublimemergeManualBrowse.setEnabled(not smerge_auto_detect)

    ui_pref.comboBoxDoubleClickAction.clear()
    for action in DoubleClickActions:
        ui_pref.comboBoxDoubleClickAction.addItem(action.value)
    double_click_action = config[mgc.CONFIG_DOUBLE_CLICK_ACTION] or ''
    ui_pref.comboBoxDoubleClickAction.setCurrentText(double_click_action)

    nb_git_proc_limit = mgc.get_config_instance().get(mgc.CONFIG_NB_GIT_PROC, 0)
    if nb_git_proc_limit == 0:
        ui_pref.radioButtonGitProcUnlimited.setChecked(True)
        ui_pref.radioButtonGitProcLimit.setChecked(False)
    else:
        ui_pref.radioButtonGitProcUnlimited.setChecked(False)
        ui_pref.radioButtonGitProcLimit.setChecked(True)
        ui_pref.spinBoxLimitValue.setValue(nb_git_proc_limit)

    ui_pref.checkBoxFetchOnStartup.setChecked( bool(config[mgc.CONFIG_FETCH_ON_STARTUP]) )

    dlg_result = dlg.exec()
    if not dlg_result:
        # changes not accepted
        return

    config[mgc.CONFIG_GIT_AUTODETECT] = ui_pref.radioGitAutoDetect.isChecked()
    config[mgc.CONFIG_GIT_MANUAL_PATH] = ui_pref.lineEditGitManual.text()
    config[mgc.CONFIG_TORTOISEGIT_ACTIVATED] = ui_pref.checkBoxTortoiseGit.isChecked()
    config[mgc.CONFIG_TORTOISEGIT_AUTODETECT] = ui_pref.radioTGitAutoDetect.isChecked()
    config[mgc.CONFIG_TORTOISEGIT_MANUAL_PATH] = ui_pref.lineEditTGitManual.text()
    config[mgc.CONFIG_SOURCETREE_ACTIVATED] = ui_pref.checkBoxSourceTree.isChecked()
    config[mgc.CONFIG_SOURCETREE_AUTODETECT] = ui_pref.radioSourcetreeAutoDetect.isChecked()
    config[mgc.CONFIG_SOURCETREE_MANUAL_PATH] = ui_pref.lineEditSourcetreeManual.text()
    config[mgc.CONFIG_SUBLIMEMERGE_ACTIVATED] = ui_pref.checkBoxSublimeMerge.isChecked()
    config[mgc.CONFIG_SUBLIMEMERGE_AUTODETECT] = ui_pref.radioSublimemergeAutoDetect.isChecked()
    config[mgc.CONFIG_SUBLIMEMERGE_MANUAL_PATH] = ui_pref.lineEditSublimemergeManual.text()
    config[mgc.CONFIG_DOUBLE_CLICK_ACTION]  = ui_pref.comboBoxDoubleClickAction.currentText()
    config[mgc.CONFIG_HEAD_COLOR_BRANCH]  = colorBranch.rgb()
    config[mgc.CONFIG_HEAD_COLOR_TAG]  = colorTag.rgb()
    config[mgc.CONFIG_NB_GIT_PROC] = (0 if ui_pref.radioButtonGitProcUnlimited.isChecked()
                                                else ui_pref.spinBoxLimitValue.value())
    config[mgc.CONFIG_FETCH_ON_STARTUP]  = ui_pref.checkBoxFetchOnStartup.isChecked()

    config.save()

