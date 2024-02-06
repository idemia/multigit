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


from typing import Sequence, Union, Optional, Callable, Tuple, Any, List, Dict, Type

import functools, logging, subprocess, sys, os
from pathlib import Path

from PySide2.QtCore import QObject, QProcess, Signal
from PySide2.QtWidgets import QMessageBox, QApplication

from src import mg_config
from src.mg_utils import hasGitAuthFailureMsg
from src.mg_const import MAX_GIT_DBG_OUT_CHAR, LOGGER_GIT_CMD
from src.mg_auth_failure_mgr import MgAuthFailureMgr

logger = logging.getLogger('mg_tools')
dbg = logger.debug
warn = logger.warning
log_git_cmd = logging.getLogger(LOGGER_GIT_CMD).info

GIT_EXIT_CODE_SEGFAULT_OF_GIT_WITH_STACKTRACE = -1
GIT_EXIT_CODE_SEGFAULT_OF_GIT_NO_STACKTRACE = -2
GIT_EXIT_CODE_COULD_NOT_START_PROCESS = -3
GIT_EXIT_CODE_STOPPED_BECAUSE_AUTH_FAILURE = -4


class ExecTool:
    # List of platform (as returned by sys.platform()) where we can run this tool
    SUPPORTED_PLATFORMS: List[str]

    WIN32_PATH_CANDIDATES: List[Path]
    LINUX_PATH_CANDIDATES: List[Path]

    EXEC_NAME_LINUX: str
    EXEC_NAME_WIN32: str

    # if not None, this is a command which we can run to detect the program. Typically, this is ['--version']
    INNOCUOUS_COMMAND: Optional[List[str]] = None

    # name of the configuration entry to store auto-detection behavior
    CONFIG_ENTRY_AUTODETECT: str

    # name of the configuration entry to store the manual path to the program
    CONFIG_ENTRY_MANUAL_PATH: str

    # name of the configuration entry to store if the program is activated or not
    CONFIG_ENTRY_ACTIVATED: str

    SESSION_CACHE: Dict[Type['ExecTool'], str] = {
    }


    @classmethod
    def platform_supported(cls) -> bool:
        '''Return whether the current platform is supported'''
        return sys.platform in cls.SUPPORTED_PLATFORMS


    @classmethod
    def autodetect_executable(cls) -> str:
        '''Autodetect the executable location according to a few heuristics and return the result.
        Returns an empty string when nothing found.
        '''
        if not cls.platform_supported():
            return ''

        # check if we have it in cache
        if cls in cls.SESSION_CACHE:
            return cls.SESSION_CACHE[cls]

        if cls.INNOCUOUS_COMMAND:
            # first, try on the command-line
            try:
                exit_code, output = RunProcess().exec_blocking([cls.get_exec_name()] + cls.INNOCUOUS_COMMAND, allow_errors=True)
                if exit_code == 0:
                    # program is on the path, use it
                    cls.SESSION_CACHE[cls] = cls.get_exec_name()
                    return cls.get_exec_name()
            except FileNotFoundError:
                # program is not on the path
                pass


        # Look in some standards locations
        if sys.platform == 'win32':
            path_candidates = cls.WIN32_PATH_CANDIDATES
        elif sys.platform == 'linux':
            path_candidates = cls.LINUX_PATH_CANDIDATES
        else:
            raise ValueError('Unsupported platform')

        cmd = cls.find_prog_exec(path_candidates)

        # put it in cash for next time
        if cmd:
            cls.SESSION_CACHE[cls] = cmd

        # return the result even if we could not find anything
        return cmd


    @classmethod
    def get_executable(cls) -> str:
        '''Check if the configuration `autodetect` is True or None and in this case,
        auto-detects the program location. Else, simply return the value defined in `config_entry_manual_path`
        '''
        if not cls.platform_supported():
            return ''

        config = mg_config.get_config_instance()
        if config[cls.CONFIG_ENTRY_AUTODETECT] in (None, True):
            result = cls.autodetect_executable()
        else:
            result = config[cls.CONFIG_ENTRY_MANUAL_PATH]
        return result


    @classmethod
    def get_exec_name(cls) -> str:
        if sys.platform == 'win32':
            return cls.EXEC_NAME_WIN32
        elif sys.platform == 'linux':
            return cls.EXEC_NAME_LINUX
        else:
            raise ValueError('Platform not supported: ', sys.platform)


    @classmethod
    def find_prog_exec(cls, path_candidates: Sequence[Union[str, Path]]) -> str:
        '''Scans locations path_candidates to see if the expected program exists. Return the program at this location if found or an empty string.

        The path_candidates are a list of directory location where one can find exec_name

        Example:
            path_candidates: List[Path] = [
                Path(os.environ["ProgramFiles(x86)"])/"Git"/"bin",
                Path(os.environ["ProgramFiles"])/"Git"/"bin",
            ]

            find_prog_exec( path_candidates )
        '''
        dbg(f'find_prog_exec({cls}, {path_candidates})')
        exec_name = cls.get_exec_name()
        dbg(f'find_prog_exec() - exec_name={exec_name}')
        for possible_path in path_candidates:
            candidate_path = Path(possible_path) / exec_name
            dbg('Looking at: {}'.format(str(candidate_path)))
            if not candidate_path.exists():
                continue
            # ok, we have it !
            dbg('Found program at: {}'.format(str(candidate_path)))
            return str(candidate_path)

        # could not find the wanted program
        return ''


    @classmethod
    def shouldShow(cls) -> bool:
        '''Return whether to show the program in menu:
        - for first run, we show if the program is autodetected on the computer
        - for non first run, we show according to config
        '''
        if mg_config.get_config_instance().get(cls.CONFIG_ENTRY_ACTIVATED) is None:
            # configuration entry does not exist, this is our first run
            if cls.get_executable():
                # program is not configured and but is autodetected
                showProgram = True
            else:
                # program is not configured and not autodetected
                showProgram = False
            mg_config.get_config_instance()[cls.CONFIG_ENTRY_ACTIVATED] = showProgram
        else:
            showProgram = mg_config.get_config_instance().get(cls.CONFIG_ENTRY_ACTIVATED)
        return showProgram


    @classmethod
    def exec_non_blocking(cls, cmd_args: List[str], workdir: str = '', allow_errors: bool = False, callback: Optional[Callable[[], Any]] = None) -> None:
        '''Run the program with the arguments listed in cmd_args, in the working directory.
        Raises an exception if the command did not return with 0 status and allow_errors is False.
        '''
        prog_to_run = cls.get_executable()
        if prog_to_run == '':
            raise FileNotFoundError(f'Could not locate {cls.get_exec_name()}')

        cb_done = None
        if callback is not None:
            def cb_done(_exit_code: int, _output: str) -> None:
                assert callback
                callback()

        rp = RunProcess()
        cmdline = [prog_to_run] + cmd_args
        rp.exec_async(cmdline=cmdline, cb_done=cb_done, working_dir=workdir, allow_errors=allow_errors)


    @classmethod
    def exec_blocking(cls, cmd_args: Sequence[str], workdir: str = '', allow_errors: bool = False) -> str:
        '''Run the program with the arguments listed in cmd_args, in the working directory.
        Raises an exception if the command did not return with 0 status.
        '''
        prog_to_run = cls.get_executable()
        if prog_to_run == '':
            raise FileNotFoundError(f'Could not locate {cls.get_exec_name()}')

        cmdline = [prog_to_run] + list(cmd_args)
        exitCode, output = RunProcess().exec_blocking(cmdline, allow_errors=allow_errors, working_dir=workdir)
        if exitCode != 0 and not allow_errors:
            raise subprocess.CalledProcessError(cmd=cmdline, returncode=exitCode, output=output)
        return output



#######################################################
#       Git Stuff
#######################################################

class ExecGit(ExecTool):
    SUPPORTED_PLATFORMS = ['win32', 'linux']

    WIN32_PATH_CANDIDATES: List[Path] = [
        Path(os.environ.get("ProgramFiles", '')) / "Git" / "bin",
        Path(os.environ.get("ProgramFiles", '')) / "Git" / "cmd",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git" / "bin",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git" / "cmd",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git" / "bin",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git" / "cmd",
    ]

    LINUX_PATH_CANDIDATES = [
        Path('/usr/bin'),
        Path('/usr/local/bin'),
    ]

    EXEC_NAME_LINUX = 'git'
    EXEC_NAME_WIN32 = 'git.exe'

    INNOCUOUS_COMMAND = ['--version']

    CONFIG_ENTRY_AUTODETECT = mg_config.CONFIG_GIT_AUTODETECT
    CONFIG_ENTRY_MANUAL_PATH = mg_config.CONFIG_GIT_MANUAL_PATH

    @classmethod
    def checkFound(cls) -> bool:
        '''If the explorer program is not found, display an error dialog and return False.

        Else, simply return True
        '''
        if cls.get_executable() == '':
            QMessageBox.warning(None, 'Could not execute git', 'Error: could not execute git\n'
                                '\nMultiGit needs git to work.\nPlease configure the location in the preference dialog.\n')
            return False

        return True


#######################################################
#       TortoiseGit Stuff
#######################################################

class ExecTortoiseGit(ExecTool):
    SUPPORTED_PLATFORMS = ['win32']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles(x86)", '')) / "TortoiseGit"/"bin",
        Path(os.environ.get("PROGRAMW6432", '')) / "TortoiseGit"/"bin",
        Path(os.environ.get("ProgramFiles", '')) / "TortoiseGit"/"bin",
    ]

    EXEC_NAME_WIN32 = "TortoiseGitProc.exe"

    CONFIG_ENTRY_AUTODETECT = mg_config.CONFIG_TORTOISEGIT_AUTODETECT
    CONFIG_ENTRY_MANUAL_PATH = mg_config.CONFIG_TORTOISEGIT_MANUAL_PATH
    CONFIG_ENTRY_ACTIVATED = mg_config.CONFIG_TORTOISEGIT_ACTIVATED


#######################################################
#       SourceTree stuff
#######################################################

class ExecSourceTree(ExecTool):
    SUPPORTED_PLATFORMS = ['win32']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Atlassian" / "SourceTree",
        Path(os.environ.get("PROGRAMW6432", '')) / "Atlassian" / "SourceTree",
        Path(os.environ.get("ProgramFiles", '')) / "Atlassian" / "SourceTree",
    ]

    EXEC_NAME_WIN32 = "SourceTree.exe"

    CONFIG_ENTRY_AUTODETECT = mg_config.CONFIG_SOURCETREE_AUTODETECT
    CONFIG_ENTRY_MANUAL_PATH = mg_config.CONFIG_SOURCETREE_MANUAL_PATH
    CONFIG_ENTRY_ACTIVATED = mg_config.CONFIG_SOURCETREE_ACTIVATED


#######################################################
#       SublimeMerge stuff
#######################################################

class ExecSublimeMerge(ExecTool):
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

    CONFIG_ENTRY_AUTODETECT = mg_config.CONFIG_SUBLIMEMERGE_AUTODETECT
    CONFIG_ENTRY_MANUAL_PATH = mg_config.CONFIG_SUBLIMEMERGE_MANUAL_PATH
    CONFIG_ENTRY_ACTIVATED = mg_config.CONFIG_SUBLIMEMERGE_ACTIVATED


#######################################################
#       GitBash stuff
#######################################################

class ExecGitBash(ExecTool):
    SUPPORTED_PLATFORMS = ['win32']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles", '')) / "Git",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git",
        ]

    INNOCUOUS_COMMAND = ['--version']

    EXEC_NAME_WIN32 = "git-bash.exe"

    CONFIG_ENTRY_AUTODETECT = mg_config.CONFIG_GITBASH_AUTODETECT
    CONFIG_ENTRY_MANUAL_PATH = mg_config.CONFIG_GITBASH_MANUAL_PATH
    CONFIG_ENTRY_ACTIVATED = mg_config.CONFIG_GITBASH_ACTIVATED


#######################################################
#       GitGui stuff
#######################################################

class ExecGitGui(ExecTool):
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

    CONFIG_ENTRY_AUTODETECT = mg_config.CONFIG_GITGUI_AUTODETECT
    CONFIG_ENTRY_MANUAL_PATH = mg_config.CONFIG_GITGUI_MANUAL_PATH
    CONFIG_ENTRY_ACTIVATED = mg_config.CONFIG_GITGUI_ACTIVATED


#######################################################
#       Gitk stuff
#######################################################

class ExecGitK(ExecTool):
    SUPPORTED_PLATFORMS = ['win32', 'linux']

    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("ProgramFiles", '')) / "Git" / "cmd",
        Path(os.environ.get("ProgramFiles(x86)", '')) / "Git" / "cmd",
        Path(os.environ.get("PROGRAMW6432", '')) / "Git" / "cmd",
    ]

    LINUX_PATH_CANDIDATES = [
        Path('/usr/bin'),  # Ubuntu
    ]

    EXEC_NAME_WIN32 = "gitk.exe"
    EXEC_NAME_LINUX = "gitk"

    CONFIG_ENTRY_AUTODETECT = mg_config.CONFIG_GITK_AUTODETECT
    CONFIG_ENTRY_MANUAL_PATH = mg_config.CONFIG_GITK_MANUAL_PATH
    CONFIG_ENTRY_ACTIVATED = mg_config.CONFIG_GITK_ACTIVATED


#######################################################
#       Open directory
#######################################################

class ExecExplorer(ExecTool):
    SUPPORTED_PLATFORMS = ['win32', 'linux']

    # no path candidates, it should be on the execution path
    WIN32_PATH_CANDIDATES = [
        Path(os.environ.get("SystemRoot", '')),
    ]
    LINUX_PATH_CANDIDATES = [
        Path("/usr/bin"),
    ]

    EXEC_NAME_WIN32 = 'explorer.exe'
    EXEC_NAME_LINUX = 'xdg-open'

    # name of the configuration entry to store auto-detection behavior
    CONFIG_ENTRY_AUTODETECT = mg_config.CONFIG_EXPLORER_AUTODETECT

    # name of the configuration entry to store the manual path to the program
    CONFIG_ENTRY_MANUAL_PATH = mg_config.CONFIG_EXPLORER_MANUAL_PATH

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
    def exec_non_blocking(cls, cmd_args: List[str], workdir: str = '', allow_errors: Optional[bool] = None, callback: Optional[Callable[[], Any]] = None) -> None:
        '''Same as default exec_non_blocking but defaults to allow_errors for Windows'''
        if allow_errors == None:
            if sys.platform == 'win32':
                # on Windows, launching the explorer returns -1
                override_allow_errors = True
            else:
                override_allow_errors = False
        return super().exec_non_blocking(cmd_args, workdir, override_allow_errors, callback)


#######################################################
#       GitProcess class
#######################################################

FORCE_ASYNC_TO_BLOCKING_CALLS = False

class RunProcess(QObject):
    '''Utility class to run a git or another process synchronously or asynchronously.

    One RunProcess() only shall be created for a repository and it will ensure that only one git command
    is running at the same time on the repository.

    This class also uses the GitProcessPool to limit the number of total git processes running in parallel.

    Typical usage:
    ==============

    # aysnchronous git execution
    rp = RunProcess('some_repo')
    rp.exec_async(callback_git_operation_finished, ['-C', 'some_repo', 'fetch'])

    rp.exec_async(callback_git_operation_finished, ['-C', 'some_repo', 'fetch'], force_blocking=True)
    rp.exec_async(callback_git_operation_finished, ['-C', 'some_repo', 'fetch'], allow_errors=True)

    # synchronous git execution
    rp = RunProcess('some_repo')
    git_exit_code, cmd_out = rp.exec_blocking(None, ['-C', 'some_repo', 'fetch'])

    # asynchronous execution of another program
    rp = RunProcess(None)
    rp.process_working_dir = gitdir
    rp.cmd = prog_gitbash
    rp.exec_async(args=[], cb_done=cb_done)

    The interest of this class above QProcess:
    - limit one git execution over a given repository
    - detects some git execution errors corner cases
    - shows a dialog box if git executable can not be found
    - shows a dialog box if the executable returned an error (configurable with allow_errors)
    - asynchronous execution is slightly easier than when dealing directly with QProcess
    - the debug log captures partial stdout/stderr which eases debugging

    You can use the signal sigProcessOutput to track the progressive output of the process.

    '''

    process: Optional[QProcess]
    cb_done: Optional[ Callable[[int, str], Any]]
    process_working_dir: Optional[str]
    sigProcessOutput = Signal(str)

    def __init__(self) -> None:
        super().__init__(QApplication.instance())

        self.cmdline: Sequence[str] = []
        self.process_working_dir = None
        self.process = None
        self.cb_done = None
        self.partial_stdout = ''
        self.last_exit_code = 0
        self.allow_errors = False
        self.emit_output = False


    def nice_cmdline(self) -> str:
        return ' '.join(self.cmdline)


    def create_process(self, cmdline: Sequence[str], working_dir: str = '',
                       allow_errors: bool = False, emit_output: bool = False) -> None:
        '''Creates a QProcess for running a git command

        cmdline: argument to git to execute.

        May block while a git process is currently under execution
        '''
        self.cmdline = cmdline
        self.emit_output = emit_output
        self.process = QProcess(self)
        self.process.setProgram(cmdline[0])
        self.process.setArguments(cmdline[1:])
        if len(working_dir):
            self.process.setWorkingDirectory(working_dir)
        self.allow_errors = allow_errors

        self.last_exit_code = 0
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)

        if self.emit_output:
            # noinspection PyUnresolvedReferences
            self.process.readyReadStandardOutput.connect(self.slotReadyReadStdout)


    def slotReadyReadStdout(self) -> None:
        '''Slot called when data is available from the process stdout channel'''
        assert self.process
        btext = bytes(self.process.readAllStandardOutput())
        self.partial_stdout += btext.decode('utf8', errors='replace')
        logger.debug('%s - partial git output:' % self.nice_cmdline())
        logger.debug(b'"%r"' % btext)
        if self.emit_output:
            self.sigProcessOutput.emit(self.partial_stdout)

        if hasGitAuthFailureMsg(self.partial_stdout):
            MgAuthFailureMgr.gitAuthFailed(self.nice_cmdline())


    def exec_blocking(self, cmdline: Sequence[str], allow_errors: bool = False, working_dir: str = '') -> Tuple[int, str]:
        '''Execute a git command in blocking mode.

        args: the arguments to git.

        Return the git exit code and the standard output of the command.

        If allow_errors is False (the default) a message box reports the git error. If it is True, nothing
        is done. In both cases, the git exit code is returned.
        '''
        self.create_process(cmdline, working_dir=working_dir, allow_errors=allow_errors)

        if MgAuthFailureMgr.shouldStopBecauseAuthFailureInProgress(cmdline):
            self.last_exit_code = GIT_EXIT_CODE_STOPPED_BECAUSE_AUTH_FAILURE
            self.partial_stdout = 'Stopped before execution because too many authentication failures.'
            dbg('Execution canceled because of too many authentication failures: {}'.format(self.nice_cmdline()))
            cmd_out = self.process_finished(self.last_exit_code, QProcess.ExitStatus.NormalExit)
            return self.last_exit_code, cmd_out

        assert self.process
        dbg('Executing blocking: {}'.format(self.nice_cmdline()))
        self.process.start()

        if self.process.state() not in (QProcess.Starting, QProcess.Running):
            # could not start the process...
            cmd_out = self.process_finished(GIT_EXIT_CODE_COULD_NOT_START_PROCESS, QProcess.ExitStatus.CrashExit)
        else:
            finished = self.process.waitForFinished(-1)
            if not finished:
                logger.warning('Process returned before being finished...')
                raise AssertionError('process not yet finished...')

            cmd_out = self.process_finished(self.process.exitCode(), self.process.exitStatus())

        return self.last_exit_code, cmd_out


    def exec_async(self, cmdline: Sequence[str],
                   cb_done: Optional[Callable[[int, str], Any]],
                   force_blocking: bool = False,
                   allow_errors: bool = False,
                   working_dir: str = '',
                   emit_output: bool = False) -> None:
        '''Execute a git command asynchronously and calls cb_git_done() when the command completes.

        cmdline: the full command-line including the program. When running over a repo, the first argument
                 of the command is replaced by the actual path to git, extracted from the config.

        Calls: cb_git_done(git_exit_code, git_output)

        if force_blocking is True, the call is made blocking and the callback is called
        when the git process completes.

        If allow_errors is False (the default) a message box reports the git error. If it is True, nothing
        is done. In both cases, the git exit code is passed to the callback.

        If emit_output is True, the signal sigProcessOutput is emitted progressively
        as the process emits output.
        '''
        self.cb_done = cb_done
        if FORCE_ASYNC_TO_BLOCKING_CALLS or force_blocking:
            self.exec_blocking(cmdline, allow_errors, working_dir)
            return

        self.create_process(cmdline, working_dir=working_dir, allow_errors=allow_errors,
                            emit_output=emit_output)

        assert self.process

        if MgAuthFailureMgr.shouldStopBecauseAuthFailureInProgress(cmdline):
            self.last_exit_code = GIT_EXIT_CODE_STOPPED_BECAUSE_AUTH_FAILURE
            self.partial_stdout = 'Stopped before execution because too many authentication failures.'
            dbg('Execution canceled because of too many authentication failures: {}'.format(self.nice_cmdline()))
            QApplication.processEvents()
            self.process_finished(self.last_exit_code, QProcess.ExitStatus.NormalExit)
            return

        # noinspection PyUnresolvedReferences
        self.process.finished.connect(self.process_finished)

        dbg('Executing async: {}'.format(self.nice_cmdline()))
        self.process.start()


    def process_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> str:
        '''Called by both blocking and async process execution, when execution is over.

        Calls the cb_done if any.
        '''
        dbg('Process finished for "%s" with exit status %d, exit code %d' % (self.nice_cmdline(), int(exit_status), exit_code))
        assert self.process
        cmd_out: str
        btext = bytes(self.process.readAllStandardOutput())
        cmd_out = self.partial_stdout + btext.decode('utf8', errors='replace').replace('\r', '\n')
        self.partial_stdout = ''
        cmd_out_dbg = cmd_out if len(cmd_out) < MAX_GIT_DBG_OUT_CHAR else \
            cmd_out[:MAX_GIT_DBG_OUT_CHAR] + '\n<output truncated to {} characters>'.format(MAX_GIT_DBG_OUT_CHAR)
        logger.debug('stdout: {}'.format(cmd_out_dbg))

        log_git_cmd(self.nice_cmdline())
        log_git_cmd('\t' + '\n\t'.join(cmd_out_dbg.split('\n')))

        # keep a local copy before final cleanup
        process = self.process
        cb_done = self.cb_done
        self.process = None
        self.cb_done = None

        if hasGitAuthFailureMsg(cmd_out_dbg):
            MgAuthFailureMgr.gitAuthFailed(self.nice_cmdline())

        self.last_exit_code = exit_code
        if  '** *fatal error - add_item' in cmd_out or 'Stack trace:' in cmd_out and self.last_exit_code == 0:
            # this happens sometimes with git process started very closely one to another with a fetch
            # that's why we use a delay between starting multiple git processes
            # usually, the error is not reported in git exit code, probably because it is not git-fetch
            # who is failing but a sub-program
            # so force exit code
            logger.error('Git segfault detected, forcing exit code to -1 for: %s' % self.nice_cmdline())
            self.last_exit_code = GIT_EXIT_CODE_SEGFAULT_OF_GIT_WITH_STACKTRACE

        elif process.exitStatus() != QProcess.NormalExit and self.last_exit_code == 0:
            logger.error('Git segfault detected, forcing exit code to -2 for: %s' % self.nice_cmdline())
            self.last_exit_code = GIT_EXIT_CODE_SEGFAULT_OF_GIT_NO_STACKTRACE

        if self.last_exit_code != 0 and not self.allow_errors:
            # noinspection PyTypeChecker
            if QApplication.instance():
                QMessageBox.warning(None, 'Error when running process',
                                    'Bad exit code %d, see command below:\n\n%s' % ( self.last_exit_code, self.nice_cmdline()))
            else:
                raise ValueError('Bad exit code %d for command: %s' % (self.last_exit_code, self.nice_cmdline()))

        # to avoid recursion, don't leave any pending callbacks
        if cb_done:
            logger.debug('Calling process done callback')
            cb_done(self.last_exit_code, cmd_out)

        return cmd_out


    def abortProcessInProgress(self) -> None:
        '''Abort the running git process.

        Does nothing if there is no process running
        '''
        if self.process:
            dbg('abortProcessInProgress() for %s, killing process ' % self.nice_cmdline())
            self.process.kill()
        else:
            dbg('abortProcessInProgress() for %s, no process to kill' % self.nice_cmdline())



