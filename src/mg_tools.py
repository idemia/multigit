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


import functools, logging, pathlib, subprocess
from typing import Sequence, Union, Optional, Callable, Tuple, Any

from PySide2.QtCore import QObject, QProcess, Signal
from PySide2.QtWidgets import QMessageBox, QApplication

from src import mg_config
from src.mg_utils import hasGitAuthFailureMsg
from src.mg_const import GIT_PATH_CANDIDATES, TORTOISE_GIT_PATH_CANDIDATES, SOURCETREE_PATH_CANDIDATES, SUBLIMEMERGE_PATH_CANDIDATES, \
    MAX_GIT_DBG_OUT_CHAR, GITBASH_PATH_CANDIDATES, LOGGER_GIT_CMD
from src.mg_auth_failure_mgr import MgAuthFailureMgr

logger = logging.getLogger('mg_tools')
dbg = logger.debug
log_git_cmd = logging.getLogger(LOGGER_GIT_CMD).info

GIT_EXIT_CODE_SEGFAULT_OF_GIT_WITH_STACKTRACE = -1
GIT_EXIT_CODE_SEGFAULT_OF_GIT_NO_STACKTRACE = -2
GIT_EXIT_CODE_COULD_NOT_START_PROCESS = -3
GIT_EXIT_CODE_STOPPED_BECAUSE_AUTH_FAILURE = -4

def find_prog_exec(path_candidates: Sequence[Union[str, pathlib.Path]]) -> str:
    '''Scans locations path_candidates to see if the expected program exists. Return this location if found or an empty string.

    The path_candidates list must include the full path to the program, including the program name itself.

    Example:
        path_candidates: List[pathlib.Path] = [
            pathlib.Path(os.environ["ProgramFiles(x86)"])/"Git"/"bin"/ "git.exe",
            pathlib.Path(os.environ["ProgramFiles"])/"Git"/"bin"/ "git.exe",
        ]

        find_git_exec( path_candidates )
    '''
    dbg('find_prog_exec()')
    for possible_path in path_candidates:
        dbg('Looking at: {}'.format(possible_path))
        if not pathlib.Path(possible_path).exists():
            continue
        candidate = str(possible_path)
        # ok, we have it !
        dbg('Found program at: {}'.format(candidate))
        return candidate

    # could not find the wanted program
    return ''


#######################################################
#       Git Stuff
#######################################################

# this caches the function result, so the function is called only once
@functools.lru_cache(maxsize=1)
def autodetect_git_exec() -> str:
    '''Autodetect the git executable location according to a few heuristics and return the result.
    Returns an empty string when nothing found.
    '''
    try:
        cmd = 'git.exe'
        exit_code, output = RunProcess().exec_blocking([cmd, '--version'], allow_errors=True)
        # Git is on the path, use it
        if exit_code == 0:
            return cmd
    except FileNotFoundError:
        # Git is not on the default path, no big deal
        pass

    # Look for git in some standards locations
    cmd = find_prog_exec(GIT_PATH_CANDIDATES)
    # return the result even if we could not find anything
    return cmd


def get_git_exec() -> str:
    '''Find git executable according to configuration'''
    config = mg_config.get_config_instance()
    if config[mg_config.CONFIG_GIT_AUTODETECT] in (None, True):
        result = autodetect_git_exec()
    else:
        result = config[mg_config.CONFIG_GIT_MANUAL_PATH]
    return result

def git_exec(*args: str, gitdir: Union[str, pathlib.Path] = '', allow_errors: bool = False) -> str:
    '''Run git with the arguments passed in *args and return the stdout of the command.
    Raises an exception if the command did not return with 0 status.
    '''
    prog_git = get_git_exec()
    if prog_git is None or len(prog_git) == 0:
        raise FileNotFoundError('Can not execute git with empty executable!')
    if gitdir:
        args = tuple([ '-C', str(gitdir) ] + list(args))
    cmdline = [prog_git] + list(args)
    exitCode, output = RunProcess().exec_blocking(cmdline, allow_errors=allow_errors)
    if exitCode != 0 and not allow_errors:
        raise subprocess.CalledProcessError(cmd=[prog_git]+list(args), returncode=exitCode, output=output)
    return output


#######################################################
#       TortoiseGit Stuff
#######################################################

@functools.lru_cache(maxsize=1)
def autodetect_tortoise_git_exec() -> str:
    '''Autodetect the TotoiseGitProc executable location according to a few heuristics and return the result.
    Returns an empty string when nothing found.
    '''
    # Look in some standards locations
    cmd = find_prog_exec(TORTOISE_GIT_PATH_CANDIDATES)
    # return the result even if we could not find anything
    return cmd

def get_tortoisegit_exec() -> str:
    '''Find TortoiseGitProc executable according to configuration'''
    config = mg_config.get_config_instance()
    if config[mg_config.CONFIG_TORTOISEGIT_AUTODETECT] in (None, True):
        result = autodetect_tortoise_git_exec()
    else:
        result = config[mg_config.CONFIG_TORTOISEGIT_MANUAL_PATH]
    return result

def tortoisegit_exec(*args: str, callback: Optional[Callable[[], Any]] = None) -> None:
    '''Run TortoiseGitProc with the arguments passed in *args.
    Raises an exception if the command did not return with 0 status.
    '''
    prog_tortoisegit = get_tortoisegit_exec()
    if prog_tortoisegit == '':
        raise FileNotFoundError('Could not locate TortoiseGitProc.exe')
    cb_tgit_done: Optional[Callable[[int, str], None]]
    if callback is not None:
        def cb_tgit_done(_git_exit_code: int, _git_output: str) -> None:
            assert callback
            callback()
    else:
        cb_tgit_done = None
    rp = RunProcess()
    cmdline = [prog_tortoisegit] + list(args)
    # some TortoiseGit commands return -1 on Cancel
    rp.exec_async(cmdline=cmdline, cb_done=cb_tgit_done, allow_errors=True)


def shouldShowTortoiseGit() -> bool:
    '''Return whether to show the TortoiseGit menu according to configuration'''
    if mg_config.get_config_instance().get(mg_config.CONFIG_TORTOISEGIT_ACTIVATED) is None:
        # configuration entry does not exist, this is our first run
        if get_tortoisegit_exec() == '':
            # tortoise git is not configured and not autodetected
            showTortoiseGit = False
        else:
            # tortoise git is not configured and but is autodetected
            # since this is our default tool, always show it when detected
            showTortoiseGit = True
        mg_config.get_config_instance()[mg_config.CONFIG_TORTOISEGIT_ACTIVATED] = showTortoiseGit
    else:
        showTortoiseGit = mg_config.get_config_instance().get(mg_config.CONFIG_TORTOISEGIT_ACTIVATED)
    return showTortoiseGit


#######################################################
#       SourceTree stuff
#######################################################

@functools.lru_cache(maxsize=1)
def autodetect_sourcetree_exec() -> str:
    '''Autodetect the SourceTree executable location according to a few heuristics and return the result.
    Returns an empty string when nothing found.
    '''

    # Look in some standards locations
    cmd = find_prog_exec(SOURCETREE_PATH_CANDIDATES)
    # return the result even if we could not find anything
    return cmd

def get_sourcetree_exec() -> str:
    '''Find SourceTree executable according to configuration'''
    config = mg_config.get_config_instance()
    if config[mg_config.CONFIG_SOURCETREE_AUTODETECT] in (None, True):
        result = autodetect_sourcetree_exec()
    else:
        result = config[mg_config.CONFIG_SOURCETREE_MANUAL_PATH]
    return result

def sourcetree_exec(*args: str, callback: Optional[Callable[[], Any]] = None) -> None:
    '''Run SourceTree the arguments passed in *args.
    Raises an exception if the command did not return with 0 status.
    '''
    prog_sourcetree = get_sourcetree_exec()
    if prog_sourcetree == '':
        raise FileNotFoundError('Could not locate SourceTree.exe')
    cb_git_done = None
    if callback is not None:
        def cb_git_done(_git_exit_code: int, _git_output: str) -> None:
            assert callback
            callback()
    rp = RunProcess()
    cmdline = [prog_sourcetree] + list(args)
    rp.exec_async(cmdline=cmdline, cb_done=cb_git_done)


#######################################################
#       SublimeMerge stuff
#######################################################

@functools.lru_cache(maxsize=1)
def autodetect_sublimemerge_exec() -> str:
    '''Autodetect the SublimeMerge executable location according to a few heuristics and return the result.
    Returns an empty string when nothing found.
    '''

    # Look in some standards locations
    cmd = find_prog_exec(SUBLIMEMERGE_PATH_CANDIDATES)
    # return the result even if we could not find anything
    return cmd

def get_sublimemerge_exec() -> str:
    '''Find SublimeMerge executable according to configuration'''
    config = mg_config.get_config_instance()
    if config[mg_config.CONFIG_SUBLIMEMERGE_AUTODETECT] in (None, True):
        result = autodetect_sublimemerge_exec()
    else:
        result = config[mg_config.CONFIG_SUBLIMEMERGE_MANUAL_PATH]
    return result

def sublimemerge_exec(*args: str, callback: Optional[Callable[[], Any]] = None) -> None:
    '''Run SublimeMerge the arguments passed in *args.
    Raises an exception if the command did not return with 0 status.
    Call optional callback if provided when the operation is done
    '''
    prog_sublimemerge = get_sublimemerge_exec()
    if prog_sublimemerge == '':
        raise FileNotFoundError('Could not locate SublimeMerge.exe')
    cb_git_done = None
    if callback is not None:
        def cb_git_done(_git_exit_code: int, _git_output: str) -> None:
            assert callback
            callback()
    rp = RunProcess()
    cmdline = [prog_sublimemerge] + list(args)
    rp.exec_async(cmdline=cmdline, cb_done=cb_git_done)


def shouldShowSourceTree() -> bool:
    '''Return whether to show sourcetree menu'''
    return bool(mg_config.get_config_instance().get(mg_config.CONFIG_SOURCETREE_ACTIVATED))


#######################################################
#       GitBash stuff
#######################################################

@functools.lru_cache(maxsize=1)
def autodetect_gitbash_exec() -> str:
    '''Autodetect the git-bash executable location according to a few heuristics and return the result.
    Returns an empty string when nothing found.
    '''
    # Look in some standards locations
    cmd = find_prog_exec(GITBASH_PATH_CANDIDATES)

    if cmd == '':
        # git-bash was not found, try directly in the command-line
        try:
            try_cmd = 'git-bash.exe'
            _, output = RunProcess().exec_blocking([try_cmd, '--version'], allow_errors=True)
            # Git-bash is on the path, use it
            return try_cmd
        except FileNotFoundError:
            # Git is not on the default path, no big deal
            pass

    # return the result even if we could not find anything
    return cmd

def get_gitbash_exec() -> str:
    '''Find git-bash executable according to configuration'''
    config = mg_config.get_config_instance()
    if config[mg_config.CONFIG_GITBASH_AUTODETECT] in (None, True):
        result = autodetect_gitbash_exec()
    else:
        result = config[mg_config.CONFIG_GITBASH_MANUAL_PATH]
    return result


def gitbash_exec(gitdir: str, callback: Optional[Callable[[], Any]] = None) -> None:
    '''Run git-bash on the directory passed in argument.
    Raises an exception if the command did not return with 0 status.
    '''
    prog_gitbash = get_gitbash_exec()
    if prog_gitbash == '':
        raise FileNotFoundError('Could not locate SourceTree.exe')

    cb_done = None
    if callback is not None:
        def cb_done(_git_exit_code: int, _git_output: str) -> None:
            assert callback
            callback()

    rp = RunProcess()
    cmdline = [prog_gitbash]
    rp.exec_async(cmdline=cmdline, cb_done=cb_done, working_dir=gitdir)


def shouldShowSublimeMerge() -> bool:
    return bool(mg_config.get_config_instance().get(mg_config.CONFIG_SUBLIMEMERGE_ACTIVATED))


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
        self.process.setProcessChannelMode(QProcess.MergedChannels)

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
            cmd_out = self.process_finished(self.last_exit_code, QProcess.NormalExit)
            return self.last_exit_code, cmd_out

        assert self.process
        dbg('Executing blocking: {}'.format(self.nice_cmdline()))
        self.process.start()

        if self.process.state() not in (QProcess.Starting, QProcess.Running):
            # could not start the process...
            cmd_out = self.process_finished(GIT_EXIT_CODE_COULD_NOT_START_PROCESS, QProcess.FailedToStart)
        else:
            finished = self.process.waitForFinished(-1)
            if not finished:
                logger.warning('Process returned before being finished...')
                raise AssertionError('process not yet finished...')

            cmd_out = self.process_finished(self.process.exitCode(), self.process.exitStatus())

        return self.last_exit_code, cmd_out


    def exec_async(self, cmdline: Sequence[str],
                   cb_done: Optional[Callable[[int, str], Any]],
                   force_blocking: bool = False, allow_errors: bool = False,
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
            self.process_finished(self.last_exit_code, QProcess.NormalExit)
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



