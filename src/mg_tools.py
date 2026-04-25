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


from typing import Sequence, Union, Optional, Callable, Tuple, Any, List, Dict, Type, Generator, TYPE_CHECKING

import logging, sys, os
from pathlib import Path
from collections import deque
from enum import Enum, auto
from dataclasses import dataclass

from PySide6.QtCore import QObject, QProcess, Signal, SignalInstance
from PySide6.QtWidgets import QMessageBox, QApplication, QWidget

from src import mg_config
if TYPE_CHECKING:
    from src.mg_repo_info import MgRepoInfo
from src.mg_utils import hasGitAuthFailureMsg
import src.mg_const as mg_const
from src.mg_auth_failure_mgr import MgAuthFailureMgr

logger = logging.getLogger('mg_tools')
dbg = logger.debug
warn = logger.warning
error = logger.error
log_git_cmd = logging.getLogger(mg_const.LOGGER_GIT_CMD).info

GIT_EXIT_CODE_SEGFAULT_OF_GIT_WITH_STACKTRACE = -100
GIT_EXIT_CODE_SEGFAULT_OF_GIT_NO_STACKTRACE = -101
EXIT_CODE_COULD_NOT_START_PROCESS = -102
GIT_EXIT_CODE_STOPPED_BECAUSE_AUTH_FAILURE = -103
EXIT_CODE_CRASHED = -104

FLATPAK_SPAWN = ['flatpak-spawn', '--host']
SNAP_BIN_DIR = '/snap/bin'

class CmdType(Enum):
    NoCmd               = 'NoCmd'         # empty value, means that the program could not be found
    DirectCmd           = 'DirectCmd'
    FlatpakProgram      = 'FlatpakProgram'
    SnapProgram         = 'SnapProgram'


class ExecStatus(Enum):
    Ok            = 'Ok'
    FailedToStart = 'Failed to start'
    Crashed       = 'Crash'
    OtherError    = 'Other error'


@dataclass
class MgExecutable:
    '''Class to represent an executable program with its type and path'''
    cmd_type: CmdType = CmdType.NoCmd

    # used to launch the command, this is the name of the executable available on the command-line
    # or the path to the executable, to be launched either directly or with flatpak spawn depending on cmd_type
    path: str = ''

    # flatpak program ID, when cmd_type is CmdType.FlatpakProgram
    name: str = ''

    def is_empty(self) -> bool:
        '''Shortcut to check if the executable is empty (not found)'''
        return self.cmd_type == CmdType.NoCmd
    
    def __str__(self) -> str:
        if self.is_empty():
            return 'NoCmd()'
        elif self.cmd_type == CmdType.FlatpakProgram:
            return f'FlatpakProgram({self.name})'
        else:
            return f'{self.cmd_type}({self.path})'


def isRunningInsideFlatpak() -> bool:
    """Return TTrue if running inside a flatpak container.

    Used to use proper flatpak launcher when launching an external program"""
    return 'FLATPAK_ID' in os.environ


class ExecTool:
    # Program display name to use when presenting to the user
    DISPLAY_NAME: str = ''

    # List of platform (as returned by sys.platform()) where we can run this tool
    SUPPORTED_PLATFORMS: List[str]

    WIN32_PATH_CANDIDATES: List[Path] = []
    LINUX_PATH_CANDIDATES: List[Path] = []
    DARWIN_PATH_CANDIDATES: List[Path] = []

    EXEC_NAME_WIN32: str = ''
    EXEC_NAME_DARWIN: str = ''
    EXEC_NAME_LINUX: str = ''
    # Snap executable name under /snap/bin 
    EXEC_NAME_SNAP: str = ''
    # Flatpak application ID (for example org.gnome.gitg). Empty means "no Flatpak app".
    EXEC_NAME_FLATPAK: str = ''

    # When False,the program we are looking for is specific and we can filter the browse dialog with
    # the program executable name. If True, the program is generic and we will not filter the the browse
    # dialog box.
    GENERIC_PROGRAM: bool = False

    # if not None, this is a command which we can run to detect the program. Typically, this is ['--version']
    INNOCUOUS_COMMAND: Optional[List[str]] = None

    # name of the configuration entry to store the executable configuration
    # information (path, auto-detection, flatpak app name, ...). The prefix 
    # is completed with CONFIG_SUFFIX_* to store the different information.
    CONFIG_ENTRY_BASE: str

    DOUBLE_CLICK_ACTIONS: List[str] = []

    SESSION_CACHE: Dict[Type['ExecTool'], MgExecutable] = {
    }


    @staticmethod
    def runDoubleClick(selectedRepos: List['MgRepoInfo']) -> None:
        raise NotImplementedError('runDoubleClick() not implemented for this tool')


    @classmethod
    def platform_supported(cls) -> bool:
        '''Return whether the current platform is supported'''
        return sys.platform in cls.SUPPORTED_PLATFORMS


    @classmethod
    def flatpak_supported(cls) -> bool:
        '''Return whether the current platform supports Flatpak'''
        return sys.platform == 'linux'


    @classmethod
    def snap_supported(cls) -> bool:
        '''Return whether the current platform supports Snap'''
        return sys.platform == 'linux'


    @classmethod
    def config_read_entry(cls, suffix: str, default_value: Any = None) -> Any:
        '''Read the configuration entry CONFIG_ENTRY_BASE + suffix and return its value'''
        config = mg_config.get_config_instance()
        return config.get(cls.CONFIG_ENTRY_BASE + suffix, default_value=default_value)


    @classmethod
    def config_write_entry(cls, suffix: str, value: Any) -> None:
        '''Write the value in the configuration entry CONFIG_ENTRY_BASE + suffix'''
        config = mg_config.get_config_instance()
        config[cls.CONFIG_ENTRY_BASE + suffix] = value


    @classmethod
    def config_read_exec(cls) -> MgExecutable:
        '''Read the configuration entry and return an MgExecutanble with the stored information.

        A default empty exec is returned if:
        - the config entry does not exist
        - the config entry for cmd_type has an unknown value
        - the config entry declares flatpak but this is not supported on this platform
        - the config entry declares snap but this is not supported on this platform
        '''
        config = mg_config.get_config_instance()
        cmd_type_config_entry = cls.CONFIG_ENTRY_BASE + mg_config.SUFFIX_CMD_TYPE
        cmd_type_str = config.get(cmd_type_config_entry)
        if cmd_type_str is None:
            dbg(f'config_read_exec() - no config entry for cmd type: {cmd_type_config_entry}, returning empty MgExecutable')
            return MgExecutable()
        name = config.get(cls.CONFIG_ENTRY_BASE + mg_config.SUFFIX_APP_NAME, '')
        path = config.get(cls.CONFIG_ENTRY_BASE + mg_config.SUFFIX_MANUAL_PATH, '')
        try:
            exec = MgExecutable(cmd_type=CmdType(cmd_type_str), name=name, path=path)
        except ValueError:
            warn(f'config_read_exec() - Unsupported config value for {cmd_type_config_entry} : {cmd_type_str}')
            dbg('config_read_exec() - Returning empty MgExecutable')
            return MgExecutable()

        if (not cls.flatpak_supported()) and exec.cmd_type == CmdType.FlatpakProgram \
                or (not cls.snap_supported()) and exec.cmd_type == CmdType.SnapProgram:
            # config is inconsistent, fix it
            warn(f'config_read_exec() - Config inconsistent with platform capabilities: cmd_type={exec.cmd_type}')
            dbg('config_read_exec() - Returning empty MgExecutable')
            return MgExecutable()

        dbg(f'config_read_exec() - Returning {exec}')
        return exec


    @classmethod
    def autodetect_executable(cls) -> MgExecutable:
        '''Autodetect the executable location according to the command defintions and return a MgExecutable.

        The order of detection is:
        - run the on the command line the command defined in INNOCUOUS_COMMAND
        - scan the locations defined in the relevant *_PATH_CANDIDATES for the current platform
        - if EXEC_NAME_FLATPAK is defined, look for a Flatpak app with this ID

        The MgExecutable is empty when the program could not be found. Else it contains the information to launch the program.
        '''
        if not cls.platform_supported():
            return MgExecutable()

        # check if we have it in cache
        if cls in cls.SESSION_CACHE:
            return cls.SESSION_CACHE[cls]

        if cls.INNOCUOUS_COMMAND:
            exec = MgExecutable(CmdType.DirectCmd, path=cls.get_exec_name())

            exec_status, exit_code, _output = RunProcess().exec_blocking(exec, cmd_args=cls.INNOCUOUS_COMMAND)
            if exec_status == ExecStatus.Ok and exit_code == 0:
                # program is on the path, use it
                cls.SESSION_CACHE[cls] = exec
                return exec

        exec = cls.find_prog_exec()

        # put it in cash for next time
        if not exec.is_empty():
            cls.SESSION_CACHE[cls] = exec

        # return the result even if we could not find anything
        return exec


    @classmethod
    def get_executable(cls) -> MgExecutable:
        '''Check if the configuration `autodetect` is True or None and in this case,
        auto-detects the program location. 
        
        Else, simply return the value stored in the configuration file.
        '''
        if not cls.platform_supported():
            return MgExecutable()

        if cls.config_read_entry(mg_config.SUFFIX_AUTODETECT) in (None, True):
            result = cls.autodetect_executable()
        else:
            result = cls.config_read_exec()
        return result


    @classmethod
    def get_exec_name(cls) -> str:
        if sys.platform == 'win32':
            return cls.EXEC_NAME_WIN32
        elif sys.platform == 'linux':
            return cls.EXEC_NAME_LINUX
        elif sys.platform == 'darwin':
            return cls.EXEC_NAME_DARWIN
        else:
            raise ValueError('Platform not supported: ', sys.platform)


    @classmethod
    def get_path_candidates(cls) -> List[Path]:
        if sys.platform == 'win32':
            path_candidates = list(cls.WIN32_PATH_CANDIDATES)
        elif sys.platform == 'linux':
            path_candidates = list(cls.LINUX_PATH_CANDIDATES)
        elif sys.platform == 'darwin':
            path_candidates = list(cls.DARWIN_PATH_CANDIDATES)
        else:
            raise ValueError(f'Unsupported platform for find_prog_exed(): {sys.platform}')

        return path_candidates


    @classmethod
    def find_prog_exec(cls) -> MgExecutable:
        '''Scans locations path_candidates to see if the expected program exists. When running inside a flatpak sandbox,
        looks for the program on the host file system with flatpak-spawn.

        If not found, and if EXEC_NAME_SNAP is defined, looks for a an executable with this name in /snap/bin.

        If not found, and if EXEC_NAME_FLATPAK is defined, looks for a Flatpak app with this ID.
        
        Return the program at this location if found or an empty MgExecutable
        '''
        path_candidates = cls.get_path_candidates()
        exec_name = cls.get_exec_name()
        
        dbg(f'find_prog_exec({cls.__name__}) - exec_name={exec_name}, path_candidates={path_candidates}')

        possible_full_paths = [
            Path(possible_path) / exec_name for possible_path in path_candidates
        ]
        if cls.EXEC_NAME_SNAP:
            possible_full_paths.append(Path(SNAP_BIN_DIR) / cls.EXEC_NAME_SNAP)
        
        for candidate_path in possible_full_paths:
            dbg('find_prog_exec() - looking at: {}'.format(str(candidate_path)))

            if isRunningInsideFlatpak():
                if not flatpak_host_file_exists(candidate_path):
                    continue
                dbg('Found program at flatpak host: {}'.format(str(candidate_path)))
                return MgExecutable(CmdType.DirectCmd, str(candidate_path))
            else:
                if not candidate_path.exists():
                    continue
                dbg('Found program at: {}'.format(str(candidate_path)))
                return MgExecutable(CmdType.DirectCmd, str(candidate_path))
            
        # not found on the path candidates

        result = MgExecutable()
        if cls.EXEC_NAME_FLATPAK:
            # look for program in flatpak list of program
            # ok, we have it !
            result = cls.find_flatpak_program()

        # could not find the wanted program
        return result


    @classmethod
    def find_flatpak_program(cls) -> MgExecutable:
        '''Detect a Flatpak app by ID and return a filled MgExecutable if found, else an empty MgExecutable.'''
        app_id = cls.EXEC_NAME_FLATPAK.strip()
        if not app_id:
            return MgExecutable()

        exec = MgExecutable(CmdType.DirectCmd, path='flatpak')
        cmd_args = ['info', '--show-ref', app_id]
        exec_status, exit_code, _output = RunProcess().exec_blocking(exec, cmd_args)

        if exec_status == ExecStatus.Ok and exit_code == 0:
            dbg(f'find_flatpak_program() - found flatpak app: {app_id}')
            return MgExecutable(CmdType.FlatpakProgram, name=app_id)

        dbg(f'find_flatpak_program() - flatpak app not found: {app_id}')
        return MgExecutable()


    @classmethod
    def shouldShow(cls) -> bool:
        '''Return whether to show the program in menu:
        - for first run, we show if the program is autodetected on the computer
        - for non first run, we show according to config
        '''
        if cls.config_read_entry(mg_config.SUFFIX_ACTIVATED) is None:
            # configuration entry does not exist, this is our first run
            if not cls.get_executable().is_empty():
                # program is not configured and but is autodetected
                showProgram = True
            else:
                # program is not configured and not autodetected
                showProgram = False
            cls.config_write_entry(mg_config.SUFFIX_ACTIVATED, showProgram)
        else:
            showProgram = cls.config_read_entry(mg_config.SUFFIX_ACTIVATED)
        return showProgram


    @classmethod
    def handle_process_return(cls, exec_status: ExecStatus, exit_code: int, output: str, allow_errors: bool, with_msg_box: bool = True) -> bool:
        '''Handle process execution errors

        allow_errors:
            True, could not start program (== wrong path) or bad exit code are ignored
            False, the error is reported with a message box or a message on stdout (see below)

        Crash and other errors are always reported, whatever the value of allow_errors

        with_msg_box: bool - if True, displays a message box when reporting errors. Else, just print an error on stdout

        return True if the execution is successful or error is within the allowed errors.
        '''
        def qmsgbox_critical(parent: Optional[QWidget], title: str, msg: str) -> None:
            if with_msg_box:
                QMessageBox.critical(parent, title, msg)
            else:
                print(msg)

        def qmsgbox_warning(parent: Optional[QWidget], title: str, msg: str) -> None:
            if with_msg_box:
                QMessageBox.warning(parent, title, msg)
            else:
                print(msg)

        if exec_status == ExecStatus.FailedToStart and not allow_errors:
            qmsgbox_critical(None,
                                 f'Could not start {cls.DISPLAY_NAME}',
                                 f'Error: Could not start {cls.DISPLAY_NAME}\n\nPlease adjust the execution information in the preference dialog')
            return False

        if exec_status == ExecStatus.Crashed:
            qmsgbox_critical(None,
                                 f'Execution error for {cls.DISPLAY_NAME}',
                                 f'Error: Execution of {cls.DISPLAY_NAME} crashed.\n\nPlease check the logs and adjust the execution information in the preference dialog')
            return False

        if exec_status == ExecStatus.OtherError:
            qmsgbox_critical(None,
                                 f'Execution error for {cls.DISPLAY_NAME}',
                                 f'Error: Execution of {cls.DISPLAY_NAME} failed.\n\nPlease check the logs and adjust the execution information in the preference dialog')
            return False

        if exit_code != 0 and not allow_errors:
            qmsgbox_warning(None, f'Execution error for {cls.DISPLAY_NAME}',
                                f'Error: {cls.DISPLAY_NAME} returned with exit code {exit_code}.\n\nOutput:\n{output}')
            return False

        # ok, execution was successful
        assert exec_status == ExecStatus.Ok, exec_status

        return True



    @classmethod
    def exec_non_blocking(cls, cmd_args: List[str], workdir: str = '',
                          allow_errors: bool = False,
                          callback: Optional[Callable[[int, str], Any]] = None,
                          output_callback: Union[None, Callable[[str], Any], SignalInstance] = None,
                          ) -> 'Optional[RunProcess]':
        '''Run the program with the arguments listed in cmd_args, in the working directory.

        If the execution is successful and the exit code is 0, callback is called with the exit code and the output of the command.
        The callback is also called if exit_code is not zero but allow_errors is True.

        If allow_errors is False and the process does not start or return with non zero exit code, an error message is displayed.
        If the process crashes or reports another kind of error, an error message is displayed.

        output_callback is called with the process output whenever a new output is available.
        '''
        exec = cls.get_executable()
        if exec.is_empty():
            QMessageBox.critical(None, f'Unable to execute {cls.DISPLAY_NAME}', f'Error: Unable to execute `{cls.DISPLAY_NAME}`\n'
                                + '\n\nPlease configure it in the preference dialog.\n')

        def cb_done(exec_status: ExecStatus, exit_code: int, output: str) -> None:
            if cls.handle_process_return(exec_status, exit_code, output, allow_errors):
                if callback is not None:
                    callback(exit_code, output)

        rp = RunProcess()
        if output_callback:
            rp.sigProcessOutput.connect(output_callback)
        rp.exec_async(exec=exec, cmd_args=cmd_args, cb_done=cb_done, working_dir=workdir,
                      emit_output=bool(output_callback))
        return rp



    @classmethod
    def exec_blocking(cls, cmd_args: List[str], workdir: str = '', allow_errors: bool = False,
                      callback: Optional[Callable[[int, str], Any]] = None,
                      ) -> str:
        '''Run the program with the arguments listed in cmd_args, in the working directory.
        Raises an exception if the command did not return with 0 status.
        '''
        exec = cls.get_executable()
        if exec.is_empty():
            QMessageBox.critical(None, f'Unable to execute {cls.DISPLAY_NAME}', f'Error: Unable to execute `{cls.DISPLAY_NAME}`\n'
                                 + '\n\nPlease configure it in the preference dialog.\n')


        exec_status, exit_code, output = RunProcess().exec_blocking(exec=exec, cmd_args=cmd_args, working_dir=workdir)
        if cls.handle_process_return(exec_status, exit_code, output, allow_errors):
            if callback is not None:
                callback(exit_code, output)

        return output


    @classmethod
    def doubleClickActions(cls) -> List[str]:
        '''Return the double click actions provided by this tool on the current platform'''
        if not cls.platform_supported() or not cls.shouldShow():
            return []

        return cls.DOUBLE_CLICK_ACTIONS


#######################################################
#       Git Stuff
#######################################################

class ExecGit(ExecTool):
    DISPLAY_NAME = 'Git'

    SUPPORTED_PLATFORMS = ['win32', 'linux', 'darwin']

    WIN32_PATH_CANDIDATES: List[Path] = [
        Path(os.environ.get("ProgramFiles", '')) / "Git" / "bin",
        Path(os.environ.get("ProgramFiles", '')) / "Git" / "cmd",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git" / "bin",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git" / "cmd",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git" / "bin",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git" / "cmd",
    ]

    LINUX_PATH_CANDIDATES = [
        Path('/usr/local/bin'),
        Path('/usr/bin'),
    ]

    DARWIN_PATH_CANDIDATES = [
        Path('/usr/local/bin'),
        Path('/usr/bin'),
    ]

    EXEC_NAME_LINUX = 'git'
    EXEC_NAME_DARWIN = 'git'
    EXEC_NAME_WIN32 = 'git.exe'
    EXEC_NAME_FLATPAK = ''

    INNOCUOUS_COMMAND = ['--version']

    CONFIG_ENTRY_BASE = 'CONFIG_GIT'

    @classmethod
    def checkFound(cls) -> bool:
        if cls.get_executable().is_empty():
            QMessageBox.warning(None, 'Could not execute git', 'Error: could not execute git\n'
                                '\nMultiGit needs git to work.\nPlease configure the location in the preference dialog.\n')
            return False

        return True


    @classmethod
    def exec_non_blocking(cls, cmd_args: List[str], workdir: str = '',
                          allow_errors: bool = False,
                          callback: Optional[Callable[[int, str], Any]] = None,
                          output_callback: Union[None, Callable[[str], Any], SignalInstance] = None,
                          ) -> 'Optional[RunProcess]':

        if MgAuthFailureMgr.shouldStopBecauseGitAuthFailureInProgress(cmd_args):
            exit_code = GIT_EXIT_CODE_STOPPED_BECAUSE_AUTH_FAILURE
            cmd_out = 'Multigit stopped git before execution because of too many previous git authentication failures.'
            dbg(cmd_out)
            if output_callback:
                if isinstance(output_callback, SignalInstance):
                    output_callback.emit(cmd_out)
                else:
                    output_callback(cmd_out)
            if callback:
                callback(exit_code, cmd_out)
            return None

        # catch git exit code to perform more actions
        def local_callback(exit_code: int, cmd_out: str) -> None:
            if hasGitAuthFailureMsg(cmd_out):
                MgAuthFailureMgr.gitAuthFailed()

            if  ('** *fatal error - add_item' in cmd_out or 'Stack trace:' in cmd_out) and exit_code == 0:
                # this crash happens sometimes with git process started very closely one to another with a fetch
                # that's why we use a delay between starting multiple git processes
                # usually, the error is not reported in git exit code, probably because it is not git-fetch
                # who is failing but a sub-program
                # so force exit code
                error(f'Git segfault detected, forcing exit code to {GIT_EXIT_CODE_SEGFAULT_OF_GIT_WITH_STACKTRACE}')
                exit_code = GIT_EXIT_CODE_SEGFAULT_OF_GIT_WITH_STACKTRACE

            if callback:
                callback(exit_code, cmd_out)


        return super().exec_non_blocking(cmd_args, workdir, allow_errors, local_callback, output_callback)


#######################################################
#       TortoiseGit Stuff
#######################################################

class ExecTortoiseGit(ExecTool):
    DISPLAY_NAME = 'TortoiseGit'

    SUPPORTED_PLATFORMS = ['win32']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles(x86)", '')) / "TortoiseGit"/"bin",
        Path(os.environ.get("PROGRAMW6432", '')) / "TortoiseGit"/"bin",
        Path(os.environ.get("ProgramFiles", '')) / "TortoiseGit"/"bin",
    ]

    EXEC_NAME_WIN32 = "TortoiseGitProc.exe"

    CONFIG_ENTRY_BASE = 'CONFIG_TORTOISEGIT'

    DOUBLE_CLICK_ACTIONS = [
        mg_const.DBC_TORTOISEGITSHOWLOG,
        mg_const.DBC_TORTOISEGITCOMMIT,
        mg_const.DBC_TORTOISEGITSWITCH,
        mg_const.DBC_TORTOISEGITBRANCH,
        mg_const.DBC_TORTOISEGITPUSH,
        mg_const.DBC_TORTOISEGITPULL,
        mg_const.DBC_TORTOISEGITFETCH,
        mg_const.DBC_TORTOISEGITDIFF,
    ]



#######################################################
#       SourceTree stuff
#######################################################

class ExecSourceTree(ExecTool):
    DISPLAY_NAME = 'SourceTree'

    SUPPORTED_PLATFORMS = ['win32']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Atlassian" / "SourceTree",
        Path(os.environ.get("PROGRAMW6432", '')) / "Atlassian" / "SourceTree",
        Path(os.environ.get("ProgramFiles", '')) / "Atlassian" / "SourceTree",
    ]

    EXEC_NAME_WIN32 = "SourceTree.exe"

    CONFIG_ENTRY_BASE = 'CONFIG_SOURCETREE'

    ACTION_RUN_SOURCETREE_TEXT = 'Run SourceTree'
    ACTION_RUN_SOURCETREE_ICON = ":/img/sourcetree.ico"
    ACTION_RUN_SOURCETREE_TOOLTIP = 'Open a SourceTree tab for each repository'

    DBC_RUNSOURCETREE = 'Run SourceTree'

    DOUBLE_CLICK_ACTIONS = [
        DBC_RUNSOURCETREE,
    ]

    @staticmethod
    def runDoubleClick(selectedRepos: List['MgRepoInfo']) -> None:
        dbg(f'ExecSourceTree.runDoubleClick({selectedRepos})')
        for repo in selectedRepos:
            ExecSourceTree.exec_non_blocking(['-t', str(repo.fullpath)])




#######################################################
#       SublimeMerge stuff
#######################################################

class ExecSublimeMerge(ExecTool):
    DISPLAY_NAME = 'SublimeMerge'

    SUPPORTED_PLATFORMS = ['win32', 'linux']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles", '')) / "Sublime Merge",
        Path(os.environ.get("PROGRAMW6432", '')) / "Sublime Merge",
    ]
    LINUX_PATH_CANDIDATES = [
        Path('/opt/sublime_merge'),
    ]

    EXEC_NAME_WIN32 = "sublime_merge.exe"
    EXEC_NAME_LINUX = "sublime_merge"
    EXEC_NAME_SNAP = 'sublime-merge'
    EXEC_NAME_FLATPAK = "com.sublimemerge.App"

    CONFIG_ENTRY_BASE = 'CONFIG_SUBLIMEMERGE'

    ACTION_RUN_SUBLIMEMERGE_TEXT = 'Run SublimeMerge'
    ACTION_RUN_SUBLIMEMERGE_ICON = ":/img/sublime_merge.ico"
    ACTION_RUN_SUBLIMEMERGE_TOOLTIP = 'Open a SublimeMerge tab for each repository'

    DBC_RUNSUBLIMEMERGE = 'Run SublimeMerge'

    DOUBLE_CLICK_ACTIONS = [
        DBC_RUNSUBLIMEMERGE,
    ]

    @staticmethod
    def runDoubleClick(selectedRepos: List['MgRepoInfo']) -> None:
        '''Run SublimeMerge on the current repos'''
        dbg(f'ExecSublimeMerge.runDoubleClick({selectedRepos})')
        for repo in selectedRepos:
            ExecSublimeMerge.exec_non_blocking([str(repo.fullpath)])


#######################################################
#       GitBash stuff
#######################################################

class ExecGitBash(ExecTool):
    DISPLAY_NAME = 'Git Bash'

    SUPPORTED_PLATFORMS = ['win32']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles", '')) / "Git",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git",
        ]

    INNOCUOUS_COMMAND = ['--version']

    EXEC_NAME_WIN32 = "git-bash.exe"

    CONFIG_ENTRY_BASE = 'CONFIG_GITBASH'

    ACTION_RUN_GITBASH_TEXT = 'Git bash here'
    ACTION_RUN_GITBASH_ICON = ":/img/git-bash.ico"
    ACTION_RUN_GITBASH_TOOLTIP = 'Open a git bash window for each repository'

    DBC_RUNGITBASH = 'Run git-bash'

    DOUBLE_CLICK_ACTIONS = [
        DBC_RUNGITBASH,
    ]


#######################################################
#       GitGui stuff
#######################################################

class ExecGitGui(ExecTool):
    DISPLAY_NAME = 'Git GUI'

    SUPPORTED_PLATFORMS = ['win32', 'linux']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles", '')) / "Git" / "cmd",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git" / "cmd",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git" / "cmd",
        ]

    LINUX_PATH_CANDIDATES = [
        Path('/usr/lib/git-core'),  # Ubuntu
    ]

    EXEC_NAME_WIN32 = "git-gui.exe"
    EXEC_NAME_LINUX = "git-gui"

    CONFIG_ENTRY_BASE = 'CONFIG_GITGUI'

    ACTION_RUN_GITGUI_TEXT = 'Run Git GUI'
    ACTION_RUN_GITGUI_TOOLTIP = 'Open a Git-gui window for each repository'

    DBC_RUNGITGUI = 'Run Git Gui'

    DOUBLE_CLICK_ACTIONS = [
        DBC_RUNGITGUI,
    ]

    @staticmethod
    def runDoubleClick(selectedRepos: List['MgRepoInfo']) -> None:
        dbg(f'ExecGitGui.runDoubleClick({selectedRepos})')
        for repo in selectedRepos:
            # allow errors needed because git-gui never returns 0 on Windows
            ExecGitGui.exec_non_blocking([], workdir=str(repo.fullpath), allow_errors=True)


#######################################################
#       Gitk stuff
#######################################################

class ExecGitK(ExecTool):
    DISPLAY_NAME = 'Gitk'

    SUPPORTED_PLATFORMS = ['win32', 'linux', 'darwin']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles", '')) / "Git" / "cmd",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git" / "cmd",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git" / "cmd",
    ]

    LINUX_PATH_CANDIDATES = [
        Path('/usr/bin'),  # Ubuntu
    ]

    DARWIN_PATH_CANDIDATES = [
        Path('/usr/bin'),  # darwin
        Path('/opt/homebrew/bin/')  #brew install
    ]

    EXEC_NAME_WIN32 = "gitk.exe"
    EXEC_NAME_LINUX = "gitk"
    EXEC_NAME_DARWIN = "gitk"

    CONFIG_ENTRY_BASE = 'CONFIG_GITK'

    ACTION_RUN_GITK_TEXT = 'Run GitK'
    ACTION_RUN_GITK_TOOLTIP = 'Open a GitK for each repository'

    DBC_RUNGITK = 'Run GitK'

    DOUBLE_CLICK_ACTIONS = [
        DBC_RUNGITK,
    ]

    @staticmethod
    def runDoubleClick(selectedRepos: List['MgRepoInfo']) -> None:
        dbg(f'ExecGitK.runDoubleClick({selectedRepos})')
        for repo in selectedRepos:
            # allow errors needed because gitk never returns 0 on Windows
            ExecGitK.exec_non_blocking([], workdir=str(repo.fullpath), allow_errors=True)


#######################################################
#       Open directory
#######################################################

class ExecExplorer(ExecTool):
    '''Note: this program is mandatory for MultiGit to work, as it is used to open directories in the file explorer.'''

    DISPLAY_NAME = 'Explorer'

    SUPPORTED_PLATFORMS = ['win32', 'linux', 'darwin']

    # no path candidates, it should be on the execution path
    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("SystemRoot", '')),
    ]
    LINUX_PATH_CANDIDATES = [
        Path("/usr/bin"),
    ]
    DARWIN_PATH_CANDIDATES = [
        Path("/usr/bin"),
    ]
    EXEC_NAME_WIN32 = 'explorer.exe'
    EXEC_NAME_LINUX = 'xdg-open'
    EXEC_NAME_DARWIN = 'open'

    GENERIC_PROGRAM = True

    # name of the configuration entry to store auto-detection behavior
    CONFIG_ENTRY_BASE = 'CONFIG_EXPLORER'


    @classmethod
    def checkFound(cls) -> bool:
        '''If the explorer program is not found, display an error dialog and return False.

        Else, simply return True
        '''
        if cls.get_executable() == '':
            QMessageBox.warning(None, 'Could not find the explorer program',
                                'Could not find a program to open directories. Please choose one in the File/Settings dialog.')
            return False

        return True


    @classmethod
    def exec_non_blocking(cls, cmd_args: List[str], workdir: str = '', allow_errors: bool = False,
                          callback: Optional[Callable[[int, str], Any]] = None,
                          output_callback: Union[None, Callable[[str], Any], SignalInstance] = None,
                          ) -> 'Optional[RunProcess]':
        '''Same as default exec_non_blocking but defaults to allow_errors for Windows'''
        override_allow_errors = allow_errors
        if sys.platform == 'win32':
            # on Windows, launching the explorer returns -1, so make sure we ignore it
            override_allow_errors = True
        return super().exec_non_blocking(cmd_args, workdir, override_allow_errors, callback, output_callback)


#######################################################
#
#       Low level process execution with RunProcess
#
#######################################################

# used when running tests, to avoid running an event loop and to run async calls in blocking mode
FORCE_ASYNC_TO_BLOCKING_CALLS = False


class RunProcess(QObject):
    '''Utility class to run any process synchronously or asynchronously.

    The interest of this class above QProcess:
    - can be called to run Flatpak, Snaps or regular commands
    - the debug log captures partial stdout/stderr which eases debugging
    - asynchronous execution is slightly easier than when dealing directly with QProcess
    - asynchronous execution can be forced to blocking execution, convenient for testing

    You can use the signal sigProcessOutput to track the progressive output of the process.

    '''

    process: Optional[QProcess]
    cb_done: Optional[ Callable[[ExecStatus, int, str], Any]]
    process_working_dir: Optional[str]
    sigProcessOutput = Signal(str)
    exec_status: ExecStatus

    def __init__(self) -> None:
        super().__init__(QApplication.instance())

        self.executable: Optional[MgExecutable] = None
        self.cmd_line: List[str] = []
        self.is_exec_blocking = False
        self.process_working_dir = None
        self.process = None
        self.cb_done = None
        self.exec_status = ExecStatus.Ok
        self.partial_stdout = ''
        self.emit_output = False


    def nice_cmdline(self) -> str:
        return  ' '.join(self.cmd_line)


    def create_process(self, exec: MgExecutable, cmd_args: List[str], working_dir: str = '',
                       emit_output: bool = False,
                       ) -> None:
        '''Creates a QProcess for running a command

        exec: the executable to run, with the information to run it properly (path for a direct command, snap name for a snap
         program, flatpak app id for a flatpak program
        cmd_args: arguments to execute.

        If running inside a flatpak container, the command is executed on the host with flatpak-spawn

        May block while a process is currently under execution
        '''
        dbg(f'create_process({exec} {cmd_args}, working_dir={working_dir})')
        cmd_type = exec.cmd_type

        assert not exec.is_empty(), f'Can not execute: {exec}'

        self.cmd_line = cmd_args

        if exec.cmd_type in [CmdType.DirectCmd]:
            self.cmd_line = [exec.path] + self.cmd_line

        if cmd_type == CmdType.FlatpakProgram:
            self.cmd_line = ['flatpak', 'run', exec.name] + self.cmd_line

        if cmd_type == CmdType.SnapProgram:
            self.cmd_line = [f'{SNAP_BIN_DIR}/{exec.name}'] + self.cmd_line

        if isRunningInsideFlatpak():
            self.cmd_line = FLATPAK_SPAWN + self.cmd_line

        dbg(f'create_process() cmd_line={self.cmd_line}')

        self.emit_output = emit_output
        self.process = QProcess(self)
        self.process.setProgram(self.cmd_line[0])
        self.process.setArguments(self.cmd_line[1:])
        if len(working_dir):
            self.process.setWorkingDirectory(working_dir)
        self.process.errorOccurred.connect(self.slot_error_occured)

        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)

        if self.emit_output:
            # noinspection PyUnresolvedReferences
            self.process.readyReadStandardOutput.connect(self.slotReadyReadStdout)

    def slotReadyReadStdout(self) -> None:
        '''Slot called when data is available from the process stdout channel'''
        assert self.process
        btext = bytes(self.process.readAllStandardOutput())
        self.partial_stdout += btext.decode('utf8', errors='replace')
        dbg('%s - partial git output:' % self.nice_cmdline())
        dbg(b'"%r"' % btext)
        if self.emit_output:
            self.sigProcessOutput.emit(self.partial_stdout)

        if hasGitAuthFailureMsg(self.partial_stdout):
            MgAuthFailureMgr.gitAuthFailed()


    def exec_blocking(self, exec: MgExecutable, cmd_args: List[str], working_dir: str = '') -> Tuple[ExecStatus, int, str]:
        '''Execute a program in blocking mode.

        args: the arguments to the program without the progam itself.

        Return the program exit code and the standard output of the command.
        '''
        self.is_exec_blocking = True
        self.create_process(exec, cmd_args, working_dir=working_dir)

        assert self.process
        dbg('Executing blocking: {}'.format(self.nice_cmdline()))
        self.process.start()

        if (self.process.state() not in (QProcess.ProcessState.Starting, QProcess.ProcessState.Running)
                or not self.process.waitForStarted(-1)):
            # could not start the process...
            dbg('exec_blocking() - could not start the process')

            # in case it was not caught earlier
            if self.exec_status == ExecStatus.Ok:
                self.exec_status = ExecStatus.FailedToStart
            return self.process_finished(EXIT_CODE_COULD_NOT_START_PROCESS, QProcess.ExitStatus.NormalExit)

        finished = self.process.waitForFinished(-1)
        if not finished:
            warn('Process returned before being finished...')
            raise AssertionError('process not yet finished...')

        # if an error occured, it was notified through slot_error_occured() and self.exec_status has been set
        return self.process_finished(self.process.exitCode(), self.process.exitStatus())


    def exec_async(self, exec: MgExecutable,
                   cmd_args: List[str],
                   cb_done: Optional[Callable[[ExecStatus, int, str], Any]],
                   force_blocking: bool = False,
                   working_dir: str = '',
                   emit_output: bool = False,
                   ) -> None:
        '''Execute a program asynchronously and calls cb_git_done() when the command completes.

        exec: the executable to run, with the information to run it properly (flatpak spawn, direct command, ...)
        cmd_args: the arguments to the program without the program itself.

        Calls: cb_done(exec_status, git_exit_code, git_output)

        if force_blocking is True, the call is made blocking and the callback is called
        when the process completes.

        If emit_output is True, the signal sigProcessOutput is emitted progressively
        as the process emits output.

        If output_callback is provided, it is connected to the output signal of the QProcess
        '''
        self.cb_done = cb_done
        if FORCE_ASYNC_TO_BLOCKING_CALLS or force_blocking:
            self.exec_blocking(exec, cmd_args, working_dir)
            return
        self.is_exec_blocking = False

        self.create_process(exec, cmd_args, working_dir=working_dir,
                            emit_output=emit_output)

        assert self.process

        self.process.finished.connect(self.process_finished)

        dbg('Executing async: {}'.format(self.nice_cmdline()))
        self.process.start()


    def slot_error_occured(self, error: QProcess.ProcessError) -> None:
        '''Slot called when an error occurs with the process'''
        dbg('RunProcess() error occurred for "%s": %s' % (self.nice_cmdline(), str(error)))
        if error == QProcess.ProcessError.FailedToStart:
            self.exec_status = ExecStatus.FailedToStart
            # in this case, we must call manually process_finished()
            if self.is_exec_blocking == False:
                # for async calls only. For blocking calls, we handle it later
                self.process_finished(EXIT_CODE_COULD_NOT_START_PROCESS, QProcess.ExitStatus.NormalExit)
        elif error == QProcess.ProcessError.Crashed:
            self.exec_status = ExecStatus.Crashed
        else:
            self.exec_status = ExecStatus.OtherError


    def clean(self) -> None:
        '''Clean the fields: process, cb_done, exec_status, partial_stdout'''
        self.process = None
        self.cb_done = None
        self.exec_status = ExecStatus.Ok
        self.partial_stdout = ''


    def process_cmd_out_finished(self) -> str:
        '''Retrieve the pending output of the process and return the complete process output'''
        assert self.process is not None
        btext = bytes(self.process.readAllStandardOutput())
        cmd_out = self.partial_stdout + btext.decode('utf8', errors='replace').replace('\r', '\n')
        self.partial_stdout = ''

        cmd_out_dbg = cmd_out if len(cmd_out) < mg_const.MAX_GIT_DBG_OUT_CHAR else \
            cmd_out[:mg_const.MAX_GIT_DBG_OUT_CHAR] + '\n<output truncated to {} characters>'.format(mg_const.MAX_GIT_DBG_OUT_CHAR)
        dbg('stdout: {}'.format(cmd_out_dbg))

        log_git_cmd(self.nice_cmdline())
        log_git_cmd('\t' + '\n\t'.join(cmd_out_dbg.split('\n')))

        return cmd_out


    def process_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> Tuple[ExecStatus, int, str]:
        '''Called by both blocking and async process execution, when execution is over.

        Calls the cb_done if any.
        '''
        dbg('Process finished for "%s" with exit status %d, exit code %d' % (self.nice_cmdline(), int(exit_status.value), exit_code))
        assert self.process

        cmd_out = self.process_cmd_out_finished()
        exec_status, process, cb_done = self.exec_status, self.process, self.cb_done
        self.clean()

        if process.exitStatus() == QProcess.ExitStatus.CrashExit and exec_status == ExecStatus.Ok:
            # in case the error was not caught earlier
            exec_status = ExecStatus.Crashed
            if exit_code == 0:
                exit_code = EXIT_CODE_CRASHED

        if cb_done is not None:
            dbg('Calling process done callback')
            cb_done(exec_status, exit_code, cmd_out)

        return exec_status, exit_code, cmd_out


    def abortProcessInProgress(self) -> None:
        '''Abort the running process.

        Does nothing if there is no process running
        '''
        if self.process:
            dbg('abortProcessInProgress() for %s, killing process ' % self.nice_cmdline())
            self.process.kill()
        else:
            dbg('abortProcessInProgress() for %s, no process to kill' % self.nice_cmdline())



RECYCLE_BIN=Path(r'\$Recycle.Bin')
GIT_MANDATORY_SUBDIRS = ['objects', 'refs']


def is_git_repo(git_dir: Path) -> bool:
    '''Return True if .git directory is actually a git repo.
    Checks for the presence of .git directory and other mandatory files.
    '''
    if git_dir.name != '.git':
        return False

    if git_dir.is_file():
        try:
            with open(git_dir, 'r', encoding='utf8') as f:
                content = f.read().strip()
                return content.startswith('gitdir:')
        except Exception as e:
            return False

    if sys.platform == 'win32':
        # we don't want to scan the recycle bin
        try:
            rec_bin = Path(git_dir.drive) / RECYCLE_BIN
            _ = git_dir.relative_to(rec_bin)
            # No exception raised, we are in the recycle bin
            # we don't want to return git repo from the recycle bin
            return False
        except ValueError:
            # good, git_dir is not in the Recycle Bin...
            pass

    for subd in GIT_MANDATORY_SUBDIRS:
        subd_path = git_dir / subd
        if not subd_path.exists() or not subd_path.is_dir():
            return False
    return True


def scan_git_dirs(base_path: str) -> Generator[str, str, None]:
    '''Return the list of Git directories (.git) within the given directory tree
    The traversal is breadth-first and it follows the symbolic links
    '''
    dbg(f'scan_git_dirs({base_path})')

    visited = set()

    path_to_visit = deque([base_path])
    while path_to_visit:
        dirpath = path_to_visit.popleft()

        resolved_path = str(Path(dirpath).resolve())
        if resolved_path in visited:
            # already visited, cycle created by symbolic links
            continue

        visited.add(resolved_path)

        try:
            dir_content = os.scandir(dirpath)
        except PermissionError:
            dbg(f'scan_git_dirs() - PermissionError when trying to access {dirpath}, skipping it')
            continue

        for entry in dir_content:
            try:
              if entry.name == '.git':
                  if is_git_repo(Path(entry.path)):
                      yield entry.path
                  continue 

              if not entry.is_dir(follow_symlinks=True):
                  continue

              if entry.name.startswith('.'):
                  # directries starting with . are often not relevant, don't scan them
                  continue

            except OSError:
                # we could not access the entry for some reason, it's ok,just continue scanning
                continue
           
            path_to_visit.append(entry.path)



def flatpak_host_file_exists(fpath: Path) -> bool:
    '''Check whether a given file exists on the flatpak host file system, by using sh to run a test command on the host.'''
    # assumption here: sh is on the path on the host. Very very likely
    # If it turns out to be a wrong assumption we can always organise a search for a shell or a python
    assert isRunningInsideFlatpak(), 'flatpak_host_file_exists() should only be called when running inside flatpak'
    USE_SH_TO_CHECK_THAT_FILE_EXISTS = ['sh', '-c', f'[ -e "{fpath}" ]']
    exec = MgExecutable(CmdType.DirectCmd, path=USE_SH_TO_CHECK_THAT_FILE_EXISTS[0])
    exec_status, exit_code, output = RunProcess().exec_blocking(exec, cmd_args=USE_SH_TO_CHECK_THAT_FILE_EXISTS[1:])
    return exec_status == ExecStatus.Ok and exit_code == 0
