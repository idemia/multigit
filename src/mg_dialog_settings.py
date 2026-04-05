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
from typing import TYPE_CHECKING, Union, Literal, Type, Optional
from dataclasses import dataclass

from PySide6.QtWidgets import QFileDialog, QDialog, QColorDialog, QWidget, QLabel, QLineEdit, QRadioButton, QCheckBox, QPushButton, QGroupBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from src.mg_repo_tree import MgRepoTree
from src.gui.ui_preferences import Ui_Preferences
from src.mg_tools import ExecGit, ExecTortoiseGit, ExecSourceTree, ExecSublimeMerge, ExecGitBash, ExecExplorer, \
    ExecGitGui, ExecGitK, CmdType, MgExecutable, ExecTool
import src.mg_const as mg_const
import src.mg_config as mgc


@dataclass
class ProgramUiElements:
    '''Container for all the UI elements describing a possible program execution'''
    groupBoxProgram: QGroupBox
    labelChoose: QLabel
    checkBoxActivated: Optional[QCheckBox]
    radioAutoDetect: QRadioButton
    lineEditAutoDetect: QLineEdit
    radioManual: QRadioButton
    lineEditManual: QLineEdit
    pushButtonManualBrowse: QPushButton
    radioFlatpak: Optional[QRadioButton]
    lineEditFlatpak: Optional[QLineEdit]
    radioSnap: Optional[QRadioButton]
    lineEditSnap: Optional[QLineEdit]


class ProgramUiAdjuster:
    '''Class responsible to setup and adjust the UI according to configuration and user actions'''

    def __init__(self, execClass: Type[ExecTool], ui: ProgramUiElements) -> None:
        self.execClass = execClass
        self.ui = ui


    def setup_ui(self) -> None:

        if self.execClass.platform_supported():
            # Case 1: autodetect works, with either direct command output, snap in a direct command, flatapak id through flatpak,
            #         direct command through flatpak-spawn, snap command through flatpak-spawn (last two when running inside flatpak)
            # Case 2: autodetect does not work, command must be manually specified by user
            #      2.1: direct path
            #      2.2: snap name 
            #      2.3: flatpak id

            exec = self.execClass.config_read_exec()
            program_auto_detect = self.execClass.config_read_entry(mgc.SUFFIX_AUTODETECT, True)
            auto_detect_exec = self.execClass.autodetect_executable()

            # if config is invalid, switch back to auto-detect
            program_auto_detect = program_auto_detect or exec.is_empty()

            self.ui.labelChoose.setText(f'Choose {self.execClass.get_exec_name()} executable')
            if self.ui.checkBoxActivated is not None:
                self.ui.checkBoxActivated.toggled.connect(self.enable_if_activated)
                self.ui.checkBoxActivated.setChecked(self.execClass.shouldShow())

            self.ui.radioAutoDetect.setChecked(program_auto_detect)
            self.ui.lineEditAutoDetect.setText(auto_detect_exec.path or auto_detect_exec.name)

            self.ui.radioManual.setChecked(exec.cmd_type == CmdType.DirectCmd)
            self.ui.lineEditManual.setText(exec.path)
            self.ui.lineEditManual.setEnabled(exec.cmd_type == CmdType.DirectCmd)
            self.ui.pushButtonManualBrowse.setEnabled(exec.cmd_type == CmdType.DirectCmd)
            self.ui.pushButtonManualBrowse.clicked.connect(self.slotBrowseExecutable)

            if self.execClass.flatpak_supported() and self.ui.radioFlatpak and self.ui.lineEditFlatpak :
                self.ui.radioFlatpak.setVisible(True)
                self.ui.lineEditFlatpak.setVisible(True)
                if exec.cmd_type == CmdType.FlatpakProgram:
                    self.ui.radioFlatpak.setChecked(True)
                    self.ui.lineEditFlatpak.setText(exec.name)
                else:
                    self.ui.radioFlatpak.setChecked(False)
                    self.ui.lineEditFlatpak.setText('')
            else:
                if self.ui.radioFlatpak:
                    self.ui.radioFlatpak.setVisible(False)
                if self.ui.lineEditFlatpak:
                    self.ui.lineEditFlatpak.setVisible(False)

            if self.execClass.snap_supported() and self.ui.radioSnap and self.ui.lineEditSnap :
                self.ui.radioSnap.setVisible(True)
                self.ui.lineEditSnap.setVisible(True)
                if exec.cmd_type == CmdType.SnapProgram:
                    self.ui.radioSnap.setChecked(True)
                    self.ui.lineEditSnap.setText(exec.name)
                else:
                    self.ui.radioSnap.setChecked(False)
                    self.ui.lineEditSnap.setText('')
            else:
                if self.ui.radioSnap:
                    self.ui.radioSnap.setVisible(False)
                if self.ui.lineEditSnap:
                    self.ui.lineEditSnap.setVisible(False)
        else:
            self.ui.groupBoxProgram.setVisible(False)

        self.enable_if_activated(self.ui.checkBoxActivated.isChecked() if self.ui.checkBoxActivated else False)


    def enable_if_activated(self, activated: bool) -> None:
        self.ui.radioAutoDetect.setEnabled(activated)

        self.ui.radioManual.setEnabled(activated)
        enable_manual_widgets = activated and self.ui.radioManual.isChecked()
        self.ui.lineEditManual.setEnabled( enable_manual_widgets )
        self.ui.pushButtonManualBrowse.setEnabled( enable_manual_widgets )

        if self.execClass.flatpak_supported() and self.ui.radioFlatpak and self.ui.lineEditFlatpak :
            self.ui.radioFlatpak.setEnabled(activated)
            enable_flatpak_widgets = activated and self.ui.radioFlatpak.isChecked()
            self.ui.lineEditFlatpak.setEnabled( enable_flatpak_widgets )

        if self.execClass.snap_supported() and self.ui.radioSnap and self.ui.lineEditSnap :
            self.ui.radioSnap.setEnabled(activated)
            enable_snap_widgets = activated and self.ui.radioSnap.isChecked()
            self.ui.lineEditSnap.setEnabled( enable_snap_widgets )


    def slotBrowseExecutable(self) -> None:
        '''Browse for executable and set the result in the ui dialog'''
        current_exe = str(self.ui.lineEditManual.text())
        
        filter = ''
        # how to browser for the executable: 
        if self.execClass.GENERIC_PROGRAM:
            if sys.platform == 'win32':
                filter = '.exe'
        else:
            filter = self.execClass.get_exec_name()

        result, _ = QFileDialog.getOpenFileName(None, f"Select {self.execClass.DISPLAY_NAME} Executable", current_exe, filter)
        if result:
            self.ui.lineEditManual.setText(result)


class MgDialogSettings(QDialog):
    ui: Ui_Preferences

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_Preferences()
        self.ui.setupUi(self)

        config = mgc.get_config_instance()

        ### First tab stuff

        # disable multigit update feature as it is not available
        self.ui.groupBox_6.setVisible(False)

        self.colorBranch = QColor()
        self.colorBranch.setRgb(mgc.get_config_instance().get(mgc.CONFIG_HEAD_COLOR_BRANCH, mgc.DEFAULT_CONFIG_HEAD_COLOR_BRANCH))
        self.colorTag = QColor()
        self.colorTag.setRgb(mgc.get_config_instance().get(mgc.CONFIG_HEAD_COLOR_TAG, mgc.DEFAULT_CONFIG_HEAD_COLOR_TAG))
        self.updateColorButtons()
        self.ui.pushButtonColorBranch.clicked.connect( self.slotSetColorBranch )
        self.ui.pushButtonColorTag.clicked.connect( self.slotSetColorTag )


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

        confirmBeforeQuit = config[mgc.CONFIG_CONFIRM_BEFORE_QUIT]
        self.ui.checkBoxConfirmWhenQuitting.setChecked( (confirmBeforeQuit is None) or confirmBeforeQuit)

        ### Second tab stuff

        self.adjusterGit = ProgramUiAdjuster(ExecGit, ProgramUiElements(
            groupBoxProgram=self.ui.groupBoxGit,
            labelChoose=self.ui.labelExecGitChoose,
            checkBoxActivated=None,
            radioAutoDetect=self.ui.radioGitAutoDetect,
            lineEditAutoDetect=self.ui.lineEditGitAutoDetect,
            radioManual=self.ui.radioGitManual,
            lineEditManual=self.ui.lineEditGitManual,
            pushButtonManualBrowse=self.ui.pushButtonGitManualBrowse,
            radioFlatpak=None, # git does not support flatpak execution
            lineEditFlatpak=None,
            radioSnap=None, # git does not support snap execution
            lineEditSnap=None
        ))
        self.adjusterGit.setup_ui()

        self.adjusterTortoiseGit = ProgramUiAdjuster(ExecTortoiseGit, ProgramUiElements(
            groupBoxProgram=self.ui.groupBoxTGit,
            labelChoose=self.ui.labelExecTGitChoose,
            checkBoxActivated=self.ui.checkBoxTortoiseGit,
            radioAutoDetect=self.ui.radioTGitAutoDetect,
            lineEditAutoDetect=self.ui.lineEditTGitAutoDetect,
            radioManual=self.ui.radioTGitManual,
            lineEditManual=self.ui.lineEditTGitManual,
            pushButtonManualBrowse=self.ui.pushButtonTGitManualBrowse,
            radioFlatpak=None, # TortoiseGit does not support flatpak execution
            lineEditFlatpak=None,
            radioSnap=None, # TortoiseGit does not support snap execution
            lineEditSnap=None
        ))
        self.adjusterTortoiseGit.setup_ui()

        self.adjusterSourceTree = ProgramUiAdjuster(ExecSourceTree, ProgramUiElements(
            groupBoxProgram=self.ui.groupBoxSourcetree,
            labelChoose=self.ui.labelExecSourcetreeChoose,
            checkBoxActivated=self.ui.checkBoxSourcetree,
            radioAutoDetect=self.ui.radioSourcetreeAutoDetect,
            lineEditAutoDetect=self.ui.lineEditSourcetreeAutoDetect,
            radioManual=self.ui.radioSourcetreeManual,
            lineEditManual=self.ui.lineEditSourcetreeManual,
            pushButtonManualBrowse=self.ui.pushButtonSourcetreeManualBrowse,
            radioFlatpak=None, # SourceTree does not support flatpak execution
            lineEditFlatpak=None,
            radioSnap=None, # SourceTree does not support snap execution
            lineEditSnap=None
        ))
        self.adjusterSourceTree.setup_ui()

        self.adjusterSublime = ProgramUiAdjuster(ExecSublimeMerge, ProgramUiElements(
            groupBoxProgram=self.ui.groupBoxSublimemerge,
            labelChoose=self.ui.labelExecSublimemergeChoose,
            checkBoxActivated=self.ui.checkBoxSublimeMerge,
            radioAutoDetect=self.ui.radioSublimemergeAutoDetect,
            lineEditAutoDetect=self.ui.lineEditSublimemergeAutoDetect,
            radioManual=self.ui.radioSublimemergeManual,
            lineEditManual=self.ui.lineEditSublimemergeManual,
            pushButtonManualBrowse=self.ui.pushButtonSublimemergeManualBrowse,
            radioFlatpak=self.ui.radioSublimemergeFlatpak,
            lineEditFlatpak=self.ui.lineEditSublimemergeFlatpak,
            radioSnap=self.ui.radioSublimemergeSnap,
            lineEditSnap=self.ui.lineEditSublimemergeSnap
        ))
        self.adjusterSublime.setup_ui()

        self.adjusterGitBash = ProgramUiAdjuster(ExecGitBash, ProgramUiElements(
            groupBoxProgram=self.ui.groupBoxGitBash,
            labelChoose=self.ui.labelExecGitBashChoose,
            checkBoxActivated=self.ui.checkBoxGitBash,
            radioAutoDetect=self.ui.radioGitBashAutoDetect,
            lineEditAutoDetect=self.ui.lineEditGitBashAutoDetect,
            radioManual=self.ui.radioGitBashManual,
            lineEditManual=self.ui.lineEditGitBashManual,
            pushButtonManualBrowse=self.ui.pushButtonGitBashManualBrowse,
            radioFlatpak=None, # git-bash does not support flatpak execution
            lineEditFlatpak=None,
            radioSnap=None, # git-bash does not support snap execution
            lineEditSnap=None
        ))
        self.adjusterGitBash.setup_ui()

        self.adjusterGitGui = ProgramUiAdjuster(ExecGitGui, ProgramUiElements(
            groupBoxProgram=self.ui.groupBoxGitGui,
            labelChoose=self.ui.labelExecGitGuiChoose,
            checkBoxActivated=self.ui.checkBoxGitGui,
            radioAutoDetect=self.ui.radioGitGuiAutoDetect,
            lineEditAutoDetect=self.ui.lineEditGitGuiAutoDetect,
            radioManual=self.ui.radioGitGuiManual,
            lineEditManual=self.ui.lineEditGitGuiManual,
            pushButtonManualBrowse=self.ui.pushButtonGitGuiManualBrowse,
            radioFlatpak=None, # git-gui does not support flatpak execution
            lineEditFlatpak=None,
            radioSnap=None, # git-gui does not support snap execution
            lineEditSnap=None
        ))
        self.adjusterGitGui.setup_ui()

        self.adjusterGitK = ProgramUiAdjuster(ExecGitK, ProgramUiElements(
            groupBoxProgram=self.ui.groupBoxGitK,
            labelChoose=self.ui.labelExecGitkChoose,
            checkBoxActivated=self.ui.checkBoxGitK,
            radioAutoDetect=self.ui.radioGitKAutoDetect,
            lineEditAutoDetect=self.ui.lineEditGitKAutoDetect,
            radioManual=self.ui.radioGitKManual,
            lineEditManual=self.ui.lineEditGitKManual,
            pushButtonManualBrowse=self.ui.pushButtonGitKManualBrowse,
            radioFlatpak=None, # gitk does not support flatpak execution
            lineEditFlatpak=None,
            radioSnap=None, # gitk does not support snap execution
            lineEditSnap=None
        ))
        self.adjusterGitK.setup_ui()

        self.adjusterExplorer = ProgramUiAdjuster(ExecExplorer, ProgramUiElements(
            groupBoxProgram=self.ui.groupBoxExplorer,
            labelChoose=self.ui.labelExecExplorerChoose,
            checkBoxActivated=None, # explorer is always activated, no checkbox
            radioAutoDetect=self.ui.radioExplorerAutoDetect,
            lineEditAutoDetect=self.ui.lineEditExplorerAutoDetect,
            radioManual=self.ui.radioExplorerManual,
            lineEditManual=self.ui.lineEditExplorerManual,
            pushButtonManualBrowse=self.ui.pushButtonExplorerManualBrowse,
            radioFlatpak=None, # we do not support flatpak execution for explorer
            lineEditFlatpak=None,
            radioSnap=None, # we do not support snap execution for explorer
            lineEditSnap=None
        ))



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
    config[mgc.CONFIG_CONFIRM_BEFORE_QUIT] = dlg.ui.checkBoxConfirmWhenQuitting.isChecked()

    ### Second tab stuff
    config[mgc.CONFIG_GIT_AUTODETECT] = dlg.ui.radioGitAutoDetect.isChecked()
    config[mgc.CONFIG_GIT_MANUAL_PATH] = dlg.ui.lineEditGitManual.text()
    config[mgc.CONFIG_TORTOISEGIT_ACTIVATED] = dlg.ui.checkBoxTortoiseGit.isChecked()
    config[mgc.CONFIG_TORTOISEGIT_AUTODETECT] = dlg.ui.radioTGitAutoDetect.isChecked()
    config[mgc.CONFIG_TORTOISEGIT_MANUAL_PATH] = dlg.ui.lineEditTGitManual.text()
    config[mgc.CONFIG_SOURCETREE_ACTIVATED] = dlg.ui.checkBoxSourcetree.isChecked()
    config[mgc.CONFIG_SOURCETREE_AUTODETECT] = dlg.ui.radioSourcetreeAutoDetect.isChecked()
    config[mgc.CONFIG_SOURCETREE_MANUAL_PATH] = dlg.ui.lineEditSourcetreeManual.text()
    ExecSublimeMerge.config_write(
        activated=dlg.ui.checkBoxSublimeMerge.isChecked(),
        autodetect_checked=dlg.ui.radioSublimemergeAutoDetect.isChecked(),
        manual_checked=dlg.ui.radioSublimemergeManual.isChecked(),
        flatpak_checked=dlg.ui.radioSublimemergeFlatpak.isChecked(),
        snap_checked=dlg.ui.radioSublimemergeSnap.isChecked(),
        flatpak_name=dlg.ui.lineEditSublimemergeFlatpak.text(),
        snap_name=dlg.ui.lineEditSublimemergeSnap.text(),
        manual_path=dlg.ui.lineEditSublimemergeManual.text(),
    )
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

