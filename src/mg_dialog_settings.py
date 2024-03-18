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
import sys
from typing import TYPE_CHECKING, Union, Literal

from PySide2.QtWidgets import QFileDialog, QDialog, QColorDialog, QWidget
from PySide2.QtGui import QColor
from PySide2.QtCore import Qt

if TYPE_CHECKING:
    from src.mg_repo_tree import MgRepoTree
from src.gui.ui_preferences import Ui_Preferences
from src.mg_tools import ExecGit, ExecTortoiseGit, ExecSourceTree, ExecSublimeMerge, ExecGitBash, ExecExplorer, \
    ExecGitGui, ExecGitK
import src.mg_const as mg_const
import src.mg_config as mgc


class MgDialogSettings(QDialog):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        config = mgc.get_config_instance()

        self.ui = Ui_Preferences()
        self.ui.setupUi(self)

        # disable multigit update feature as it is not available
        self.ui.groupBox_6.setVisible(False)

        ### First tab stuff
        self.colorBranch = QColor()
        self.colorBranch.setRgb(mgc.get_config_instance().get(mgc.CONFIG_HEAD_COLOR_BRANCH, mgc.DEFAULT_CONFIG_HEAD_COLOR_BRANCH))
        self.colorTag = QColor()
        self.colorTag.setRgb(mgc.get_config_instance().get(mgc.CONFIG_HEAD_COLOR_TAG, mgc.DEFAULT_CONFIG_HEAD_COLOR_TAG))

        self.ui.pushButtonColorBranch.clicked.connect( self.slotSetColorBranch )
        self.ui.pushButtonColorTag.clicked.connect( self.slotSetColorTag )
        self.updateColorButtons()

        self.ui.comboBoxDoubleClickAction.clear()
        universalDoubleClickActions = [
            mg_const.DBC_DONOTHING,
            mg_const.DBC_GITCOMMIT,
            mg_const.DBC_GITCREATEBRANCH,
            mg_const.DBC_GITSWITCHBRANCH,
            mg_const.DBC_GITPUSH,
            mg_const.DBC_GITPULL,
            mg_const.DBC_GITFETCH,
            mg_const.DBC_REPOSITORYPROPERTIES,
            mg_const.DBC_SHOWINEXPLORER,
        ]

        doubleClickActions = universalDoubleClickActions
        doubleClickActions.extend( ExecTortoiseGit.doubleClickActions() )
        doubleClickActions.extend( ExecSourceTree.doubleClickActions() )
        doubleClickActions.extend( ExecSublimeMerge.doubleClickActions() )
        doubleClickActions.extend( ExecGitK.doubleClickActions() )
        doubleClickActions.extend( ExecGitGui.doubleClickActions() )
        doubleClickActions.extend( ExecGitBash.doubleClickActions() )

        for action in doubleClickActions:
            self.ui.comboBoxDoubleClickAction.addItem(action)
        double_click_action = config[mgc.CONFIG_DOUBLE_CLICK_ACTION] or ''
        self.ui.comboBoxDoubleClickAction.setCurrentText(double_click_action)

        nb_git_proc_limit = mgc.get_config_instance().get(mgc.CONFIG_NB_GIT_PROC, 0)
        if nb_git_proc_limit == 0:
            self.ui.radioButtonGitProcUnlimited.setChecked(True)
            self.ui.radioButtonGitProcLimit.setChecked(False)
        else:
            self.ui.radioButtonGitProcUnlimited.setChecked(False)
            self.ui.radioButtonGitProcLimit.setChecked(True)
            self.ui.spinBoxLimitValue.setValue(nb_git_proc_limit)

        self.ui.checkBoxFetchOnStartup.setChecked(bool(config[mgc.CONFIG_FETCH_ON_STARTUP]))


        ### Second tab stuff
        git_auto_detect = (True if config[mgc.CONFIG_GIT_AUTODETECT] is None
                           else config[mgc.CONFIG_GIT_AUTODETECT])
        self.ui.labelExecGitChoose.setText(f'Choose {ExecGit.get_exec_name()} executable location')
        self.ui.radioGitAutoDetect.setChecked(git_auto_detect)
        self.ui.lineEditGitAutoDetect.setText(ExecGit.autodetect_executable())
        self.ui.radioGitManual.setChecked(not git_auto_detect)
        self.ui.lineEditGitManual.setText(config[mgc.CONFIG_GIT_MANUAL_PATH] or '')
        self.ui.lineEditGitManual.setEnabled(not git_auto_detect)
        self.ui.pushButtonGitManualBrowse.setEnabled(not git_auto_detect)
        self.ui.pushButtonGitManualBrowse.clicked.connect(self.slotEditPrefBrowseForGit)

        if ExecTortoiseGit.platform_supported():
            self.ui.checkBoxTortoiseGit.toggled.connect(self.enableTGitIfAcivated)
            self.ui.checkBoxTortoiseGit.setChecked(ExecTortoiseGit.shouldShow())
            tgit_auto_detect = True if config[mgc.CONFIG_TORTOISEGIT_AUTODETECT] is None else config[mgc.CONFIG_TORTOISEGIT_AUTODETECT]
            self.ui.radioTGitAutoDetect.setChecked(tgit_auto_detect)
            self.ui.lineEditTGitAutoDetect.setText(ExecTortoiseGit.autodetect_executable())
            self.ui.radioTGitManual.setChecked(not tgit_auto_detect)
            self.ui.lineEditTGitManual.setText(config[mgc.CONFIG_TORTOISEGIT_MANUAL_PATH] or '')
            self.ui.lineEditTGitManual.setEnabled(not tgit_auto_detect)
            self.ui.pushButtonTGitManualBrowse.setEnabled(not tgit_auto_detect)
            self.ui.pushButtonTGitManualBrowse.clicked.connect(self.slotEditPrefBrowseForTortoiseGit)
            self.enableTGitIfAcivated()
        else:
            self.ui.groupBoxTGit.setVisible(False)


        if ExecSourceTree.platform_supported():
            self.ui.checkBoxSourceTree.toggled.connect(self.enableSTreeIfActivated)
            self.ui.checkBoxSourceTree.setChecked(ExecSourceTree.shouldShow())
            stree_auto_detect = True if config[mgc.CONFIG_SOURCETREE_AUTODETECT] is None else config[mgc.CONFIG_SOURCETREE_AUTODETECT]
            self.ui.radioSourcetreeAutoDetect.setChecked(stree_auto_detect)
            self.ui.lineEditSourcetreeAutoDetect.setText(ExecSourceTree.autodetect_executable())
            self.ui.radioSourcetreeManual.setChecked(not stree_auto_detect)
            self.ui.lineEditSourcetreeManual.setText(config[mgc.CONFIG_SOURCETREE_MANUAL_PATH] or '')
            self.ui.lineEditSourcetreeManual.setEnabled(not stree_auto_detect)
            self.ui.pushButtonSourcetreeManualBrowse.setEnabled(not stree_auto_detect)
            self.ui.pushButtonSourcetreeManualBrowse.clicked.connect(self.slotEditPrefBrowseForSourcetree)
            self.enableSTreeIfActivated()
        else:
            self.ui.groupBoxSourceTree.setVisible(False)


        if ExecSublimeMerge.platform_supported():
            self.ui.labelExecSublimemergeChoose.setText(f'Choose {ExecSublimeMerge.get_exec_name()} executable location')
            self.ui.checkBoxSublimeMerge.toggled.connect(self.enableSublimeIfActivated)
            self.ui.checkBoxSublimeMerge.setChecked(ExecSublimeMerge.shouldShow())
            smerge_auto_detect = True if config[mgc.CONFIG_SUBLIMEMERGE_AUTODETECT] is None else config[mgc.CONFIG_SUBLIMEMERGE_AUTODETECT]
            self.ui.radioSublimemergeAutoDetect.setChecked(smerge_auto_detect)
            self.ui.lineEditSublimemergeAutoDetect.setText(ExecSublimeMerge.autodetect_executable())
            self.ui.radioSublimemergeManual.setChecked(not smerge_auto_detect)
            self.ui.lineEditSublimemergeManual.setText(config[mgc.CONFIG_SUBLIMEMERGE_MANUAL_PATH] or '')
            self.ui.lineEditSublimemergeManual.setEnabled(not smerge_auto_detect)
            self.ui.pushButtonSublimemergeManualBrowse.setEnabled(not smerge_auto_detect)
            self.ui.pushButtonSublimemergeManualBrowse.clicked.connect(self.slotEditPrefBrowseForSublime)
            self.enableSublimeIfActivated()
        else:
            self.ui.groupBoxSublimemerge.setVisible(False)


        if ExecGitBash.platform_supported():
            self.ui.checkBoxGitBash.toggled.connect(self.enableGitBashIfActivated)
            self.ui.checkBoxGitBash.setChecked(ExecGitBash.shouldShow())
            gitbash_auto_detect = True if config[mgc.CONFIG_GITBASH_AUTODETECT] is None else config[mgc.CONFIG_GITBASH_AUTODETECT]
            self.ui.radioGitBashAutoDetect.setChecked(gitbash_auto_detect)
            self.ui.lineEditGitBashAutoDetect.setText(ExecGitBash.autodetect_executable())
            self.ui.radioGitBashManual.setChecked(not gitbash_auto_detect)
            self.ui.lineEditGitBashManual.setText(config[mgc.CONFIG_GIT_MANUAL_PATH] or '')
            self.ui.lineEditGitBashManual.setEnabled(not gitbash_auto_detect)
            self.ui.pushButtonGitBashManualBrowse.setEnabled(not gitbash_auto_detect)
            self.ui.pushButtonGitBashManualBrowse.clicked.connect(self.slotEditPrefBrowseForGitBash)
            self.enableGitBashIfActivated()
        else:
            self.ui.groupBoxGitBash.setVisible(False)


        if ExecGitGui.platform_supported():
            self.ui.checkBoxGitGui.toggled.connect(self.enableGitGuiIfActivated)
            self.ui.checkBoxGitGui.setChecked(ExecGitGui.shouldShow())
            gitgui_auto_detect = True if config[mgc.CONFIG_GITGUI_AUTODETECT] is None else config[mgc.CONFIG_GITGUI_AUTODETECT]
            self.ui.radioGitGuiAutoDetect.setChecked(gitgui_auto_detect)
            self.ui.lineEditGitGuiAutoDetect.setText(ExecGitGui.autodetect_executable())
            self.ui.radioGitGuiManual.setChecked(not gitgui_auto_detect)
            self.ui.lineEditGitGuiManual.setText(config[mgc.CONFIG_GITGUI_MANUAL_PATH] or '')
            self.ui.lineEditGitGuiManual.setEnabled(not gitgui_auto_detect)
            self.ui.pushButtonGitGuiManualBrowse.setEnabled(not gitgui_auto_detect)
            self.ui.pushButtonGitGuiManualBrowse.clicked.connect(self.slotEditPrefBrowseForGitGui)
            self.enableGitGuiIfActivated()
        else:
            self.ui.groupBoxGitGui.setVisible(False)


        if ExecGitK.platform_supported():
            self.ui.labelExecGitkChoose.setText(f'Choose {ExecGitK.get_exec_name()} executable location')
            self.ui.checkBoxGitK.toggled.connect(self.enableGitKIfActivated)
            self.ui.checkBoxGitK.setChecked(ExecGitK.shouldShow())
            gitk_auto_detect = True if config[mgc.CONFIG_GITK_AUTODETECT] is None else config[mgc.CONFIG_GITK_AUTODETECT]
            self.ui.radioGitKAutoDetect.setChecked(gitk_auto_detect)
            self.ui.lineEditGitKAutoDetect.setText(ExecGitK.autodetect_executable())
            self.ui.radioGitKManual.setChecked(not gitk_auto_detect)
            self.ui.lineEditGitKManual.setText(config[mgc.CONFIG_GITK_MANUAL_PATH] or '')
            self.ui.lineEditGitKManual.setEnabled(not gitk_auto_detect)
            self.ui.pushButtonGitKManualBrowse.setEnabled(not gitk_auto_detect)
            self.ui.pushButtonGitKManualBrowse.clicked.connect(self.slotEditPrefBrowseForGitK)
            self.enableGitKIfActivated()
        else:
            self.ui.groupBoxGitBash.setVisible(False)



        explorer_auto_detect = True if config[mgc.CONFIG_EXPLORER_AUTODETECT] is None else config[mgc.CONFIG_EXPLORER_AUTODETECT]
        self.ui.radioExplorerAutoDetect.setChecked(explorer_auto_detect)
        self.ui.lineEditExplorerAutoDetect.setText(ExecExplorer.autodetect_executable())
        self.ui.radioExplorerManual.setChecked(not explorer_auto_detect)
        self.ui.lineEditExplorerManual.setText(config[mgc.CONFIG_GIT_MANUAL_PATH] or '')
        self.ui.lineEditExplorerManual.setEnabled(not explorer_auto_detect)
        self.ui.pushButtonExplorerManualBrowse.setEnabled(not explorer_auto_detect)
        self.ui.pushButtonExplorerManualBrowse.clicked.connect( self.slotEditPrefBrowseForExplorer )



    ### First tab stuff

    def updateColorButtons(self) -> None:
        self.ui.pushButtonColorBranch.setStyleSheet('background-color: '+self.colorBranch.name())
        self.ui.pushButtonColorTag.setStyleSheet('background-color: '+self.colorTag.name())

    def slotSetColorBranch(self) -> None:
        color = QColorDialog.getColor(self.colorBranch)
        if color.isValid():
            self.colorBranch.setNamedColor(color.name())
            self.updateColorButtons()

    def slotSetColorTag(self) -> None:
        color = QColorDialog.getColor(self.colorTag)
        if color.isValid():
            self.colorTag.setNamedColor(color.name())
            self.updateColorButtons()


    ### Second tab stuff

    def slotEditPrefBrowseForGit(self) -> None:
        '''Browse for git executable and set the result in the ui dialog'''
        current_git_exe = str(self.ui.lineEditGitManual.text())
        result, _ = QFileDialog.getOpenFileName(self, "Select Git Executable", current_git_exe, ExecGit.get_exec_name())
        if result:
            self.ui.lineEditGitManual.setText(result)


    def slotEditPrefBrowseForTortoiseGit(self) -> None:
        '''Browse for TortoiseGitProc executable and set the result in the ui dialog'''
        current_tgit_exe = str(self.ui.lineEditTGitManual.text())
        result, _ = QFileDialog.getOpenFileName(self, "Select the TortoiseGitProc Executable", current_tgit_exe, ExecTortoiseGit.get_exec_name())
        if result:
            self.ui.lineEditTGitManual.setText(result)


    def slotEditPrefBrowseForSourcetree(self) -> None:
        '''Browse for Sourcetree executable and set the result in the ui dialog'''
        current_st_exe = str(self.ui.lineEditSourcetreeManual.text())
        result, _ = QFileDialog.getOpenFileName(self, "Select Sourcetree Executable", current_st_exe, ExecSourceTree.get_exec_name())
        if result:
            self.ui.lineEditSourcetreeManual.setText(result)


    def slotEditPrefBrowseForSublime(self) -> None:
        '''Browse for SublimeMerge executable and set the result in the ui dialog'''
        current_exe = str(self.ui.lineEditSublimemergeManual.text())
        result, _ = QFileDialog.getOpenFileName(self, "Select SublimeMerge Executable", current_exe, ExecSublimeMerge.get_exec_name())
        if result:
            self.ui.lineEditSublimemergeManual.setText(result)


    def slotEditPrefBrowseForGitBash(self) -> None:
        '''Browse for git-bash executable and set the result in the ui dialog'''
        current_exe = str(self.ui.lineEditGitBashManual.text())
        result, _ = QFileDialog.getOpenFileName(self, "Select git-bash Executable", current_exe, ExecGitBash.get_exec_name())
        if result:
            self.ui.lineEditGitBashManual.setText(result)


    def slotEditPrefBrowseForGitGui(self) -> None:
        '''Browse for git-gui executable and set the result in the ui dialog'''
        current_exe = str(self.ui.lineEditGitGuiManual.text())
        result, _ = QFileDialog.getOpenFileName(self, "Select git-gui Executable", current_exe, ExecGitGui.get_exec_name())
        if result:
            self.ui.lineEditGitGuiManual.setText(result)


    def slotEditPrefBrowseForGitK(self) -> None:
        '''Browse for gitk executable and set the result in the ui dialog'''
        current_exe = str(self.ui.lineEditGitKManual.text())
        result, _ = QFileDialog.getOpenFileName(self, "Select gitk Executable", current_exe, ExecGitK.get_exec_name())
        if result:
            self.ui.lineEditGitKManual.setText(result)


    def slotEditPrefBrowseForExplorer(self) -> None:
        '''Browse for explorer program executable and set the result in the ui dialog'''
        current_st_exe = str(self.ui.lineEditExplorerManual.text())
        pattern = ''
        if sys.platform == 'win32':
            pattern = '.exe'
        result, _ = QFileDialog.getOpenFileName(self, "Select a directory explorer program", current_st_exe, pattern)
        if result:
            self.ui.lineEditExplorerManual.setText(result)


    def enableTGitIfAcivated(self) -> None:
        enable_tgit_stuff = self.ui.checkBoxTortoiseGit.isChecked()
        self.ui.radioTGitAutoDetect.setEnabled(enable_tgit_stuff)
        self.ui.radioTGitManual.setEnabled(enable_tgit_stuff)

        enable_manual_widgets = enable_tgit_stuff and self.ui.radioTGitManual.isChecked()
        self.ui.lineEditTGitManual.setEnabled( enable_manual_widgets )
        self.ui.pushButtonTGitManualBrowse.setEnabled( enable_manual_widgets )


    def enableSTreeIfActivated(self) -> None:
        enable_stree_stuff = self.ui.checkBoxSourceTree.isChecked() 
        self.ui.radioSourcetreeManual.setEnabled(enable_stree_stuff)
        self.ui.radioSourcetreeAutoDetect.setEnabled(enable_stree_stuff)

        enable_manual_widgets = enable_stree_stuff and self.ui.radioSourcetreeManual.isChecked()
        self.ui.lineEditSourcetreeManual.setEnabled( enable_manual_widgets )
        self.ui.pushButtonSourcetreeManualBrowse.setEnabled( enable_manual_widgets )


    def enableSublimeIfActivated(self) -> None:
        enable_sublime_stuff = self.ui.checkBoxSublimeMerge.isChecked() 
        self.ui.radioSublimemergeManual.setEnabled(enable_sublime_stuff)
        self.ui.radioSublimemergeAutoDetect.setEnabled(enable_sublime_stuff)

        enable_manual_widgets = enable_sublime_stuff and self.ui.radioSublimemergeManual.isChecked()
        self.ui.lineEditSublimemergeManual.setEnabled( enable_manual_widgets )
        self.ui.pushButtonSublimemergeManualBrowse.setEnabled( enable_manual_widgets )


    def enableGitBashIfActivated(self) -> None:
        enable_gitbash_stuff = self.ui.checkBoxGitBash.isChecked() 
        self.ui.radioGitBashManual.setEnabled(enable_gitbash_stuff)
        self.ui.radioGitBashAutoDetect.setEnabled(enable_gitbash_stuff)

        enable_manual_widgets = enable_gitbash_stuff and self.ui.radioGitBashManual.isChecked()
        self.ui.lineEditGitBashManual.setEnabled( enable_manual_widgets )
        self.ui.pushButtonGitBashManualBrowse.setEnabled( enable_manual_widgets )


    def enableGitGuiIfActivated(self) -> None:
        enable_stuff = self.ui.checkBoxGitGui.isChecked() 
        self.ui.radioGitGuiManual.setEnabled(enable_stuff)
        self.ui.radioGitGuiAutoDetect.setEnabled(enable_stuff)

        enable_manual_widgets = enable_stuff and self.ui.radioGitGuiManual.isChecked()
        self.ui.lineEditGitGuiManual.setEnabled( enable_manual_widgets )
        self.ui.pushButtonGitGuiManualBrowse.setEnabled( enable_manual_widgets )


    def enableGitKIfActivated(self) -> None:
        enable_stuff = self.ui.checkBoxGitK.isChecked() 
        self.ui.radioGitKManual.setEnabled(enable_stuff)
        self.ui.radioGitKAutoDetect.setEnabled(enable_stuff)

        enable_manual_widgets = enable_stuff and self.ui.radioGitKManual.isChecked()
        self.ui.lineEditGitKManual.setEnabled( enable_manual_widgets )
        self.ui.pushButtonGitKManualBrowse.setEnabled( enable_manual_widgets )




def runDialogEditSettings(parent: QWidget, tabPage: Union[Literal[0], Literal[1]]) -> None:
    '''Show the Edit Settings dialog'''
    dlg = MgDialogSettings(parent)
    dlg.ui.tabWidget.setCurrentIndex(tabPage)

    dlg_result = dlg.exec()
    if not dlg_result:
        # changes not accepted
        return

    config = mgc.get_config_instance()

    ### First tab stuff
    config[mgc.CONFIG_DOUBLE_CLICK_ACTION]  = dlg.ui.comboBoxDoubleClickAction.currentText()
    config[mgc.CONFIG_HEAD_COLOR_BRANCH]  = dlg.colorBranch.rgb()
    config[mgc.CONFIG_HEAD_COLOR_TAG]  = dlg.colorTag.rgb()
    config[mgc.CONFIG_NB_GIT_PROC] = (0 if dlg.ui.radioButtonGitProcUnlimited.isChecked()
                                                else dlg.ui.spinBoxLimitValue.value())
    config[mgc.CONFIG_FETCH_ON_STARTUP]  = dlg.ui.checkBoxFetchOnStartup.isChecked()

    ### Second tab stuff
    config[mgc.CONFIG_GIT_AUTODETECT] = dlg.ui.radioGitAutoDetect.isChecked()
    config[mgc.CONFIG_GIT_MANUAL_PATH] = dlg.ui.lineEditGitManual.text()
    config[mgc.CONFIG_TORTOISEGIT_ACTIVATED] = dlg.ui.checkBoxTortoiseGit.isChecked()
    config[mgc.CONFIG_TORTOISEGIT_AUTODETECT] = dlg.ui.radioTGitAutoDetect.isChecked()
    config[mgc.CONFIG_TORTOISEGIT_MANUAL_PATH] = dlg.ui.lineEditTGitManual.text()
    config[mgc.CONFIG_SOURCETREE_ACTIVATED] = dlg.ui.checkBoxSourceTree.isChecked()
    config[mgc.CONFIG_SOURCETREE_AUTODETECT] = dlg.ui.radioSourcetreeAutoDetect.isChecked()
    config[mgc.CONFIG_SOURCETREE_MANUAL_PATH] = dlg.ui.lineEditSourcetreeManual.text()
    config[mgc.CONFIG_SUBLIMEMERGE_ACTIVATED] = dlg.ui.checkBoxSublimeMerge.isChecked()
    config[mgc.CONFIG_SUBLIMEMERGE_AUTODETECT] = dlg.ui.radioSublimemergeAutoDetect.isChecked()
    config[mgc.CONFIG_SUBLIMEMERGE_MANUAL_PATH] = dlg.ui.lineEditSublimemergeManual.text()
    config[mgc.CONFIG_GITBASH_ACTIVATED] = dlg.ui.checkBoxGitBash.isChecked()
    config[mgc.CONFIG_GITBASH_AUTODETECT] = dlg.ui.radioGitBashAutoDetect.isChecked()
    config[mgc.CONFIG_GITBASH_MANUAL_PATH] = dlg.ui.lineEditGitBashManual.text()
    config[mgc.CONFIG_GITGUI_ACTIVATED] = dlg.ui.checkBoxGitGui.isChecked()
    config[mgc.CONFIG_GITGUI_AUTODETECT] = dlg.ui.radioGitGuiAutoDetect.isChecked()
    config[mgc.CONFIG_GITGUI_MANUAL_PATH] = dlg.ui.lineEditGitGuiManual.text()
    config[mgc.CONFIG_GITK_ACTIVATED] = dlg.ui.checkBoxGitK.isChecked()
    config[mgc.CONFIG_GITK_AUTODETECT] = dlg.ui.radioGitKAutoDetect.isChecked()
    config[mgc.CONFIG_GITK_MANUAL_PATH] = dlg.ui.lineEditGitKManual.text()
    config[mgc.CONFIG_EXPLORER_AUTODETECT] = dlg.ui.radioExplorerAutoDetect.isChecked()
    config[mgc.CONFIG_EXPLORER_MANUAL_PATH] = dlg.ui.lineEditExplorerManual.text()
    config.save()

