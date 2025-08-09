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


from typing import List, Callable, Any, Optional, ClassVar, cast, Union

import functools
import logging
import enum
import pathlib
import shutil

from PySide6.QtCore import Signal, QObject, Qt, QThread
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QTreeWidgetItem, QApplication

from src.mg_tools import RunProcess, ExecGit
from src.mg_repo_info import MgRepoInfo
from src.mg_utils import handle_cr_in_text, ignoreCppObjectDeletedError, tryHardDeletingDirList

logger = logging.getLogger('mg_exec_task')
dbg = logger.debug
warning = logger.warning
error = logger.error

MAX_LINES_PER_ITEM = 1
QTREE_WIDGET_ITEM_BUTTONBAR_TYPE = cast(int, QTreeWidgetItem.ItemType.UserType)+1

class PreConditionState(enum.Enum):
    NotFulfilled = enum.auto()
    FulFilled = enum.auto()
    Errored = enum.auto()


class TaskState(enum.Enum):
    NotStarted = enum.auto()
    Started = enum.auto()
    Successful = enum.auto()
    Errored = enum.auto()


PreConditionFunc = Callable[[], PreConditionState]


class IconSet(enum.Enum):
    Empty = enum.auto()
    InProgress = enum.auto()
    Aborted = enum.auto()
    Success = enum.auto()
    UserOk = enum.auto()
    Failed = enum.auto()
    Question = enum.auto()
    Retry = enum.auto()
    Warning = enum.auto()
    Comment = enum.auto()


ICON_FNAME_DICT = {
    IconSet.InProgress   : ':img/icons8-loader-96.png',
    IconSet.Aborted      : ':img/icons8-stop-sign-96.png',
    IconSet.Failed       : ':img/icons8-cancel-96.png',
    IconSet.Success      : ':img/icons8-checked-96.png',
    IconSet.Warning      : ':img/icons8-general-warning-sign-96.png',
    IconSet.Question     : ':img/icons8-question-mark-96.png',
    IconSet.UserOk       : ':img/icons8-checkmark-96.png',
    IconSet.Retry        : ':img/icons8-reset-96.png',
    IconSet.Comment      : ':img/icons8-buble-conversation-96.png',
}


@functools.lru_cache(maxsize=None)
def getIcon(icon: IconSet) -> QIcon:
    '''Return an icon corresponding to string provided. Caches the result so that QIcon() is called
    only once per icon to generate.
    '''
    if icon == IconSet.Empty:
        emptyPixmap = QPixmap(16, 16)
        emptyPixmap.fill(Qt.GlobalColor.transparent)
        return QIcon(emptyPixmap)

    return QIcon(ICON_FNAME_DICT[icon])



class MgExecTask(QObject):
    '''Generic task class, inherited by specialized task class

    Child classes should:
    - implement the _run() method
    - call task_done() when the execution is finished.
    '''

    sig_task_done: ClassVar[Signal] = Signal(bool, str, IconSet)
    sig_partial_output: ClassVar[Signal] = Signal(str)

    def __init__(self, desc: str, repo: MgRepoInfo, ignore_failure: bool = False, icon_success_hint: IconSet = IconSet.Success):
        super().__init__()
        self.desc = desc
        self.repo = repo
        self.task_state = TaskState.NotStarted
        self.cmd_line = ''
        self.ignore_failure = ignore_failure
        self.icon_success_hint = icon_success_hint


    def __str__(self) -> str:
        return f'MgExecTask<repo={(self.repo.name if self.repo else "")}, cmd={self.cmd_line}, state={str(self.task_state)}>'


    def is_task_done(self) -> bool:
        '''Return true if task is in states Successful or Errored'''
        return self.task_state in (TaskState.Successful, TaskState.Errored)


    def is_task_started(self) -> bool:
        '''Return true if task is in states Successful or Errored'''
        return self.task_state in (TaskState.Started, TaskState.Successful, TaskState.Errored)


    def is_task_successful(self) -> bool:
        return self.task_state == TaskState.Successful


    def is_task_errored(self) -> bool:
        return self.task_state == TaskState.Errored


    def run(self) -> None:
        '''Run the task. The precondition has been check by the caller prior to calling run()'''
        dbg(f'MgExecTask.run() - {str(self)}')
        if self.task_state == TaskState.Started:
            error('MgExecTask.run() - trying to start an already started task')
            return

        if self.task_state in (TaskState.Successful, TaskState.Errored):
            # we are restarting a finished task
            self.task_state = TaskState.NotStarted

        self.task_state = TaskState.Started
        self._do_run()
        return


    def _do_run(self) -> None:
        '''Called to start the task. To be reimplemented.

        The call should not be blocking: please use threads or processes for that
        '''
        raise NotImplementedError('Not implemented!')


    def task_done(self, success: bool, output: str) -> None:
        '''To be called when the run() task has completed. Emits the signal sig_task_done when completed'''
        self.task_state = TaskState.Successful if success else TaskState.Errored
        dbg(f'MgExecTask.task_done(success={success}) - {str(self)}')
        if not success and self.ignore_failure:
            dbg('MgExecTask.task_done() - ignoring failure requested, so reporting success')
            success = True
        self.sig_task_done.emit(success, output, self.icon_success_hint)


    def abort(self) -> None:
        '''Cancel the task in progress, sets the error state and emit the done signal'''
        dbg(f'MgExecTask.abort() - {str(self)}')
        if self.task_state == TaskState.NotStarted:
            self.task_state = TaskState.Errored
            self.task_done(False, 'Aborted before started.')

        if self.task_state == TaskState.Started:
            # this will call the task_done() automatically
            self._do_abort()
            return

        # if task is already in state Errored or Successful, nothing to do for aborting
        return


    def _do_abort(self) -> None:
        '''Abort the current task and call self.task_done() appropriately'''
        raise NotImplementedError('Must be implemented')


class MgExecTaskCollectRemoteUrl(MgExecTask):
    '''Task for running a function'''
    def __init__(self,
                 desc: str,
                 repo: MgRepoInfo,
                 ) -> None:
        '''Run a function on the repo
        '''
        super().__init__(desc=desc, repo=repo)
        self.cmd_line = 'git remote --verbose'


    def _do_run(self) -> None:
        self.repo.ensure_url(cb_url=self.url_collected)


    def url_collected(self, _url: str) -> None:
        if self.repo.url:
            output = 'Collected url: ' + self.repo.url
            self.task_done(True, output)
        else:
            self.task_done(False, 'Fail to collect url')


class ThreadRunningPythonCode(QThread):
    '''A convenient class for running python code

    Please fill self.output and self.success to express the status of the finished task
    '''

    def __init__(self, desc: str, func: Callable[..., Any]) -> None:
        '''
        Prepare the calling function for the thread.

        `func` is the called with the instance of ThreadRunningPythonCode + the other arguments

        The output of the function execution should be added with add_output() and the final
        result if failing should be set explicitely with the attribute success . By default
        success is True.

            Exmaple:

                def myfunc(thread) -> None:
                    ...
                    thread.add_output('Some output from exeucing the code')
                    if error:
                        thread.success = False


        '''
        super().__init__()
        self.desc = desc
        self.func = func
        self.output_lines: List[str] = []
        self.success = True


    def run(self) -> None:
        dbg(f'ThreadRunningPythonCode.run() - {self.desc}')
        self.func(self)


    def add_output(self, msg: str) -> None:
        '''Fill output with one more line. The line must contain the endline'''
        self.output_lines.append(msg)


    def get_output(self) -> str:
        return ''.join(self.output_lines)



class MgTaskExecPythonCode(MgExecTask):
    def __init__(self, desc: str, repo: MgRepoInfo, func: Callable[..., Any]) -> None:
        MgExecTask.__init__(self, desc, repo, ignore_failure=True)
        self.runner = ThreadRunningPythonCode(desc, func)
        self.runner.finished.connect(self.thread_task_done)


    def _do_run(self) -> None:
        '''Start the thread with the python funtion to execute'''
        dbg(f'MgTaskExecPythonCode._do_run() - {self.desc}')
        self.runner.start()


    def thread_task_done(self) -> None:
        '''Slot called when the thread is finished running'''
        dbg(f'MgTaskExecPythonCode.thread_task_done() - {self.desc}')
        self.task_done(self.runner.success, self.runner.get_output())


class MgTaskDelDirectory(MgTaskExecPythonCode):
    '''Task for deleting a directory'''

    def __init__(self,
                 desc: str,
                 repo: MgRepoInfo,
                 dir_path: Union[str, pathlib.Path],
                 ) -> None:
        super().__init__(desc, repo, self.delDirectory)
        self.dir_path = pathlib.Path(dir_path)
        self.dir_path.resolve()
        self.cmd_line = f'Deleting {self.dir_path}'


    def delDirectory(self, thread: ThreadRunningPythonCode) -> None:
        '''Called from within the thread'''
        dbg(f'Deleting directory files from {self.dir_path}')
        result = tryHardDeletingDirList([str(self.dir_path)])
        if len(result):
            if result[-1] != '\n':
                result += '\n'
            thread.add_output(result)
            thread.success = False



class MgTaskMoveDirectory(MgExecTask):
    '''Task for moving a directory'''

    def __init__(self,
                 desc: str,
                 repo: MgRepoInfo,
                 src_path: Union[str, pathlib.Path],
                 dest_path: Union[str, pathlib.Path],
                 skip_git_admin_dir: bool = True
                 ) -> None:
        '''Move a directory to another location

        if skip_git_admind_dir is True (default), the `.git` directory will be ignored
        '''
        super().__init__(desc, repo)
        self.src_path = pathlib.Path(src_path)
        self.src_path.resolve()
        self.dest_path = pathlib.Path(dest_path)
        self.dest_path.resolve()
        self.skip_git_admin_dir = skip_git_admin_dir
        self.cmd = ['robocopy', '/move', '/s', '/e', str(self.src_path), str(self.dest_path)]
        if self.skip_git_admin_dir:
            self.cmd.extend(['/xd', '.git'])
        self.cmd_line = ' '.join(self.cmd)
        self.run_process: Optional[RunProcess] = None


    def _do_run(self) -> None:
        dbg('MgExecTaskMoveDirectory._do_run() - %s' % self.cmd)

        self.run_process = RunProcess()
        self.run_process.sigProcessOutput.connect(self.sig_partial_output)
        # We allow error in git because we have our own way of handling it
        self.run_process.exec_async(self.cmd,
                                    self.move_task_done,
                                    allow_errors=True,  # to avoid dialog
                                    emit_output=True)


    def move_task_done(self, exit_code: int, stdout: str) -> None:
        dbg(f'MgExecTaskMoveDirectory.move_task_done(exit_code={exit_code}) - "{self}"')

        # for exit code analysis, see https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy
        success = True
        if exit_code >= 8:
            if len(stdout) != 0:
                stdout += '\n'
            stdout += 'Robocopy did not complete successfully.'
            if self.ignore_failure:
                stdout += '\nIgnoring failure'
            else:
                success = False

        self.run_process = None
        self.task_done(success, stdout)


    def _do_abort(self) -> None:
        '''Abort the current task and call self.task_done() appropriately'''
        assert self.task_state == TaskState.Started
        if self.run_process is not None:
            # process was indeed started
            # kill the process in progress, this will call slotGitDone()
            self.run_process.abortProcessInProgress()
            self.run_process = None
        else:
            warning('MgExecTaskMoveDirectory._do_abort() with self.run_process == None, should not happen!')
            self.task_done(False, '')


class MgTaskComment(MgExecTask):
    '''Display a comment'''

    def __init__(self,
                 comment: str,
                 repo: MgRepoInfo,
                 more_comment: str = '',
                 ) -> None:
        '''Display a comment
        '''
        super().__init__(comment, repo)
        self.more_comment = more_comment
        self.run_process: Optional[RunProcess] = None
        self.icon_success_hint = IconSet.Comment


    def _do_run(self) -> None:
        dbg('MgExecTaskComment._do_run() - %s' % self.desc)
        self.task_done(True, self.more_comment)


    def _do_abort(self) -> None:
        '''Abort the current task and call self.task_done() appropriately'''
        assert self.task_state == TaskState.Started
        self.task_done(True, self.more_comment)



class MgExecTaskGit(MgExecTask):
    '''Task for running a git command'''

    def __init__(self,
                 desc: str,
                 repo: MgRepoInfo,
                 git_args: List[str],
                 ignore_failure: bool = False,
                 run_inside_git_repo: bool = True,
                 ) -> None:
        '''Run a git command specified in git_args.

        if run_inside_git_repo is True (default), the git command is run with "-C path_of_the_repo" to behave like
        it was run inside the git repos.

        Some commands don't need this, like 'clone' or 'ls-remote'
        '''
        if not desc:
            # desc is empty, fill it with the command-line
            desc = 'git ' + ' '.join(git_args)
        super().__init__(desc=desc, repo=repo, ignore_failure=ignore_failure)
        self.git_args = git_args
        self.cmd_line = 'git ' + ' '.join(git_args)
        self.run_process: Optional[RunProcess] = None
        self.run_inside_git_repo = run_inside_git_repo


    def _do_run(self) -> None:
        prog_git = ExecGit.get_executable()
        if prog_git is None or len(prog_git) == 0:
            raise FileNotFoundError('Can not execute git with empty executable!')

        if self.run_inside_git_repo:
            if self.repo is None:
                raise ValueError('Missing mandatory argument repo in _do_run()')
            git_args_repo_path = ['-C', self.repo.fullpath]
        else:
            # when cloning, we don't want to specify the directory in which to run the command
            git_args_repo_path = []

        git_cmd = [prog_git] + git_args_repo_path + list(self.git_args)
        dbg('MgExecTaskGit.run() - %s' % git_cmd)

        self.run_process = RunProcess()
        self.run_process.sigProcessOutput.connect(self.sig_partial_output)
        # We allow error in git because we have our own way of handling it
        self.run_process.exec_async(git_cmd, self.git_task_done, allow_errors=True,
                                    emit_output=True)


    def git_task_done(self, git_exit_code: int, git_stdout: str) -> None:
        dbg(f'MgExecTaskGit.git_task_done(git_exit_code={git_exit_code}) - "{self}"')

        if git_exit_code != 0:
            if len(git_stdout) != 0:
                git_stdout += '\n'
            git_stdout += 'Git did not complete successfully.'
            if self.ignore_failure:
                git_stdout += '\nIgnoring non relevant git error'

        self.run_process = None
        self.task_done(git_exit_code == 0, git_stdout)


    def _do_abort(self) -> None:
        '''Abort the current task and call self.task_done() appropriately'''
        assert self.task_state == TaskState.Started
        if self.run_process is not None:
            # process was indeed started
            # kill the process in progress, this will call slotGitDone()
            self.run_process.abortProcessInProgress()
            self.run_process = None
        else:
            warning('MgExecTaskGit._do_abort() with self.run_process == None, should not happen!')
            self.task_done(False, '')


class MgExecTaskGroup:
    '''A taskgroup contains several tasks to be run in order on a given repository'''

    def __init__(self,
                 desc: str,
                 repo: MgRepoInfo,
                 tasks: Optional[List[MgExecTask]] = None,
                 pre_condition: Optional[PreConditionFunc] = None,
                 ):
        self.desc = desc
        self.repo = repo
        self.tasks = tasks or []
        self.pre_condition = pre_condition
        self.aborted = False


    def __str__(self) -> str:
        return f'<TaskGroup desc={self.desc} repo={self.repo} len(tasks)={len(self.tasks)}>'


    def appendTask(self, task: MgExecTask) -> None:
        '''Append one task to the list of task for this group'''
        self.tasks.append(task)


    def appendTasks(self, taskList: List[MgExecTask]) -> None:
        '''Append multiple tasks to the list of task for this group'''
        self.tasks.extend(taskList)


    def appendGitTask(self, desc: str, git_args: List[str], run_inside_git_repo: bool = True) -> None:
        '''Shortcut for adding a git task'''
        git_task = MgExecTaskGit(desc, self.repo, git_args, run_inside_git_repo=run_inside_git_repo)
        self.tasks.append(git_task)


    def is_precondition_fulfilled(self) -> PreConditionState:
        '''Return whether the precondition for starting this task are fulfilled. The possibilities are:
        - FulFilled: no precondition, or precondition is fulfilled
        - NotFulFilled: the precondition is not yet fulfilled, proceed with other tasks and come back later
        - Errorred: the preccondition is in error and will never be fulfilled.
        '''
        if self.pre_condition is None:
            return PreConditionState.FulFilled

        return self.pre_condition()


    def is_finished(self) -> bool:
        '''Return True if all tasks of this taskgroup are finished or if the taskgroup is aborted.'''
        if self.is_aborted():
            return True

        return all(task.is_task_done() for task in self.tasks)


    def is_successful(self) -> bool:
        '''Return True if all subtasks are finished and successful'''
        if self.is_aborted():
            return False

        return all(task.is_task_successful() for task in self.tasks)


    def is_errored(self) -> bool:
        '''Return True if any subtasks is errored'''
        if self.is_aborted():
            return True

        return any(task.is_task_errored() for task in self.tasks)


    def is_started(self) -> bool:
        '''Return True if any of the tasks of this taskgroup is started'''
        return any(task.is_task_started() for task in self.tasks)


    def is_aborted(self) -> bool:
        '''Return True if:
        * the taskgroup is not in pause. Else, it is not an abortion, just a temporary pause
        * one of the tasks is in state error
        * following tasks are not started
        * previous tasks are all successful
        '''
        return self.aborted


    def abort(self) -> None:
        '''Mark current task group as aborted'''
        self.aborted = True


    def __len__(self) -> int:
        return len(self.tasks)



def after_other_taskgroup_is_finished(task_group: MgExecTaskGroup) -> PreConditionFunc:
    '''Return a function that checks if a given taskgroup has finished (successful or error)'''
    def is_taskgroup_finished() -> PreConditionState:
        if task_group is None:
            return PreConditionState.Errored

        if task_group.is_finished():
            return PreConditionState.FulFilled

        return PreConditionState.NotFulfilled

    # mark the dependency in the function, it's convenient for verification
    is_taskgroup_finished.task_group = task_group   # type: ignore[attr-defined] # mypy does not know about this attribute

    return is_taskgroup_finished


def after_other_taskgroup_is_started_and_dir_exists(task_group: MgExecTaskGroup) -> PreConditionFunc:
    '''Return a function that return True if a given taskgroup:
     - is started and the repo directory has been created.
     - OR is aborted
     - OR is finished
     '''
    def is_taskgroup_started_and_dir_exists() -> PreConditionState:
        if task_group is None:
            return PreConditionState.Errored

        if task_group.is_finished():
            # we consider that an aborted or finished dependency is an OK to continue
            return PreConditionState.FulFilled

        if not task_group.is_started():
            return PreConditionState.NotFulfilled

        if not pathlib.Path(task_group.repo.fullpath).exists():
            return PreConditionState.NotFulfilled

        return PreConditionState.FulFilled

    # mark the dependency in the function, it's convenient for verification
    is_taskgroup_started_and_dir_exists.task_group = task_group   # type: ignore[attr-defined] # mypy does not know about this attribute

    return is_taskgroup_started_and_dir_exists


class UserActionOnGitError(enum.IntFlag):
    NOTHING     = 0x00
    ABORT       = 0x01
    CONTINUE    = 0x02
    RETRY       = 0x04
    OK          = 0x08


class MgExecItemBase(QTreeWidgetItem):
    '''The interface common for MgExecItemOneCmd and MgExecItemMultiCmd'''

    def __init__(self, desc: str, cbExecDone: Callable[[bool], Any]) -> None:
        super().__init__()
        self.cbExecDone = cbExecDone
        self.ignoreUpdates = False
        self.setText(0, desc)
        self.fixedFont = QFont("Consolas")
        self.refresh_when_completed = True

    def run(self) -> None:
        raise NotImplementedError()

    def abortItem(self) -> None:
        raise NotImplementedError()

    @ignoreCppObjectDeletedError
    def autoAdjustColumnSize(self) -> None:
        '''Adjust automatically the column size to the largest item'''
        for i in range(self.treeWidget().columnCount()):
            self.treeWidget().resizeColumnToContents(i)
        QApplication.processEvents()


class MgExecItemOneCmd(MgExecItemBase):
    '''An item tree running a single execution task.

    Calls cbExecDone() when the job is completed.
    '''

    def __init__(self, task: MgExecTask,
                 cbExecDone: Callable[[bool], Any],
                 ) -> None:
        super(MgExecItemOneCmd, self).__init__(task.desc, cbExecDone)
        self.task = task
        self.task.sig_task_done.connect(self.slotTaskDone)
        self.task.sig_partial_output.connect(self.slotProgressiveOutput)
        self.setIcon(0, getIcon(IconSet.Empty))
        self.gitContentItem: Optional[QTreeWidgetItem] = None
        self.abortRequested = False


    @ignoreCppObjectDeletedError
    def run(self) -> None:
        dbg(f'MgExecItemOneCmd.run() - {self}')
        # setting icon must be done before calling run(), because run() may actually complete
        # the task and call self.slotTaskDone() which will set the icon to success
        self.setIcon(0, getIcon(IconSet.InProgress))
        self.task.run()
        self.setContentItem('')


    @ignoreCppObjectDeletedError
    def setContentItem(self, task_output: str) -> None:
        '''Set the content of a task output

        Each line of the output creates a new QTreeWidgetItem showing this line only
        (because Qt5 scroll behavior is atrocious else).

        This gets around Qt limitation where it is
        impossible to show on screen an item with more lines than the screen height
        can show

        This method may be called multiple times, always with the full output. It will update
        the existing items of the previous lines have changed, remove extra line if the content
        has diminished, add items for new lines being added.
        '''
        output = ''
        if self.task.cmd_line:
            output += f"> {self.task.cmd_line}\n"
        output += task_output
        output = handle_cr_in_text(output)
        out_lines = output.split('\n')

        # strip out empty lines at the end
        while out_lines and out_lines[-1] == '':
            del out_lines[-1]

        out_idx = 0

        # update the existing items
        for child_idx in range(self.childCount()):
            # do we have a text for this child ? If not, get out
            if out_idx >= len(out_lines):
                break

            child = self.child(child_idx)
            if child.text(0) != out_lines[out_idx]:
                child.setText(0, out_lines[out_idx])
            out_idx += 1

        # if we have less lines of text than during the previous update, remove the extra
        while out_idx > self.childCount():
            self.takeChild( self.childCount()-1 )
            self.gitContentItem = self.child(self.childCount()-1)

        # fill content with new items
        while out_idx < len(out_lines):
            self.gitContentItem = QTreeWidgetItem()
            self.gitContentItem.setFont(0, self.fixedFont)
            self.gitContentItem.setIcon(0, getIcon(IconSet.Empty))
            self.addChild(self.gitContentItem)
            self.gitContentItem.setText(0, out_lines[out_idx])
            out_idx += 1


    @ignoreCppObjectDeletedError
    def slotProgressiveOutput(self, output: str) -> None:
        item = self.gitContentItem
        while item:
            item = item.parent()
        self.setContentItem(output)


    @ignoreCppObjectDeletedError
    def slotTaskDone(self, success: bool, task_stdout: str, icon_success_hint: IconSet) -> None:
        dbg(f'MgExecItemOneCmd.slotTaskDone(success={success}) - {str(self.task)}')

        if self.abortRequested:
            self.setIcon(0, getIcon(IconSet.Aborted))
            self.setExpanded(False)
            if not success:
                task_stdout += '\nAborted!'
        elif success:
            self.setIcon(0, getIcon(icon_success_hint))
        else:
            self.setIcon(0, getIcon(IconSet.Failed))
            self.setExpanded(True)

        self.setContentItem(task_stdout)

        # if task was aborted but is still successful, we notify success ?
        self.cbExecDone(success)

        if success and self.refresh_when_completed:
            # We are in a single-git command context
            # if the command is not successful, the state of the repo has not changed, there is no need to refresh
            if self.task.repo:
                self.task.repo.refresh()

        # new text might need column adjustment
        self.autoAdjustColumnSize()


    def abortItem(self) -> None:
        dbg(f'MgExecItemOneCmd.abortItem() - {str(self.task)}')
        # mark abortRequested so that we use the correct icon when completing the job
        self.abortRequested = True
        if self.task.is_task_done():
            # nothing to do, process is already finished
            return

        # this will call slotTaskDone() with a failure status, even if the task was not started
        self.task.abort()


    def isTaskDone(self) -> bool:
        '''Return True if the underlying task was completed, successfully or not'''
        return self.task.is_task_done()


    def isTaskStarted(self) -> bool:
        '''Return True if the underlying task was started'''
        return self.task.is_task_started()


    def clearRepoConnections(self) -> None:
        self.ignoreUpdates = True
        try:
            self.task.sig_task_done.disconnect(self.slotTaskDone)
        except RuntimeError:
            # happens sometimes
            pass

        try:
            self.task.sig_partial_output.disconnect(self.slotProgressiveOutput)
        except RuntimeError:
            # happens sometimes
            pass



class MgButtonBarErrorHandling(QWidget):
    '''Widget used to display a message and 3 buttons to capture user
    action after a failing git command'''

    sigUserChoiceDone: ClassVar[Signal] = Signal(int)

    def __init__(self, parent: QWidget, buttonToShow: UserActionOnGitError) -> None:
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.buttonAbort =    QPushButton('Abort', self)
        self.buttonAbort.setToolTip('Abort sequence of tasks')
        self.buttonContinue = QPushButton('Continue', self)
        self.buttonContinue.setToolTip('Ignore the current error and continue the sequence of tasks')
        self.buttonRetry =    QPushButton('Retry', self)
        self.buttonRetry.setToolTip('Retry the last task')
        self.buttonOk =    QPushButton('Finish', self)
        self.buttonOk.setToolTip('Finish the dialog')
        self.labelQuestion = QLabel('An error occured, what do you want to do next ?')
        self.userChoice: Optional[UserActionOnGitError] = None

        buttonLayout = QHBoxLayout()
        if buttonToShow & UserActionOnGitError.ABORT:
            buttonLayout.addWidget(self.buttonAbort)
        else:
            self.buttonAbort.hide()
        if buttonToShow & UserActionOnGitError.CONTINUE:
            buttonLayout.addWidget(self.buttonContinue)
        else:
            self.buttonContinue.hide()
        if buttonToShow & UserActionOnGitError.RETRY:
            buttonLayout.addWidget(self.buttonRetry)
        else:
            self.buttonRetry.hide()

        if buttonToShow & UserActionOnGitError.OK:
            buttonLayout.addWidget(self.buttonOk)
        else:
            buttonLayout.addWidget(QWidget(self))
            self.buttonOk.hide()

        widgetLayout = QVBoxLayout(self)
        widgetLayout.addWidget(self.labelQuestion)
        widgetLayout.addLayout(buttonLayout)

        self.buttonAbort.clicked.connect(lambda: self.slotUserChoiceDone(UserActionOnGitError.ABORT))
        self.buttonContinue.clicked.connect(lambda: self.slotUserChoiceDone(UserActionOnGitError.CONTINUE))
        self.buttonRetry.clicked.connect(lambda: self.slotUserChoiceDone(UserActionOnGitError.RETRY))
        self.buttonOk.clicked.connect(lambda: self.slotUserChoiceDone(UserActionOnGitError.OK))


    def slotUserChoiceDone(self, userChoice: UserActionOnGitError) -> None:
        '''Called when the user presses one of the buttons'''
        self.sigUserChoiceDone.emit(userChoice)


class MgExecItemMultiCmd(MgExecItemBase):
    '''An item tree for running multiple commands'''

    def __init__(self, taskGroup: MgExecTaskGroup, cbExecDone: Callable[[bool], Any], askQuestionUponFailure: bool = True) -> None:
        '''A MgExecItemMultiCmd item.

        Calls cbExecDone() when the git execution is finished.
        '''
        super(MgExecItemMultiCmd, self).__init__(taskGroup.desc, cbExecDone)
        assert len(taskGroup) > 0
        self.taskGroup = taskGroup
        self.taskIdx = -1
        self.abortRequested = False
        self.askQuestionUponFailure = askQuestionUponFailure
        self.nbCmdDone = 0
        self.nbError = 0
        self.isStarted = False
        self.buttonBar: Optional[MgButtonBarErrorHandling] = None
        self.buttonBarItem: Optional[QTreeWidgetItem] = None
        self.setText(0, taskGroup.repo.name)
        # pre-fill with an icon to avoid the text sliding when creating the icon
        self.setIcon(0, getIcon(IconSet.Empty))
        self.setExpanded(False)


    def __str__(self) -> str:
        return f'<MgExecItemMultiCmd<taskGroup={self.taskGroup} nbCmdDone={self.nbCmdDone} nbError={self.nbError}>'

    @property
    def isDone(self) -> bool:
        '''Return true if all sub-tasks are completed or if the user aborted globally the tasks'''
        return self.nbCmdDone == len(self.taskGroup) or self.abortRequested


    @ignoreCppObjectDeletedError
    def run(self) -> None:
        dbg(f'MgExecItemMultiCmd.run() - {self}')
        self.isStarted = True
        self.setIcon(0, getIcon(IconSet.InProgress))
        self.runOneCmdline()


    def runOneCmdline(self, retrying: bool = False) -> None:
        '''Run one more task in the task list.

        When retrying a previous task, set retrying to True. This avoids setting up a double signal-slot connection.
        '''
        dbg(f'MgExecItemMultiCmd.runOneCmdline() - {self}')
        if retrying:
            lastTaskItem = cast(MgExecItemOneCmd, self.child(self.childCount()-2))
            lastTask = self.taskGroup.tasks[self.taskIdx]
            assert lastTaskItem.task == lastTask
            # this avoids calling back self.slotOneCmdDone() again
            lastTask.sig_task_done.disconnect(lastTaskItem.slotTaskDone)

            # pretend that the last job was not completed
            self.nbCmdDone -= 1
            self.nbError -= 1
            self.taskIdx -= 1

        assert not self.isDone, "nbCmdDone=%d, len(tasks)=%d" % (self.nbCmdDone, len(self.taskGroup))  # more tasks to run
        self.taskIdx += 1
        task = self.taskGroup.tasks[self.taskIdx]
        jobitem = MgExecItemOneCmd(task, self.slotOneCmdDone)
        jobitem.refresh_when_completed = False
        self.addChild(jobitem)
        jobitem.run()


    def slotOneCmdDone(self, success: bool) -> None:
        '''Called when one of the job item has completed. We are ready to possibly start the next one'''

        self.nbCmdDone += 1
        if not success:
            self.nbError += 1
        dbg(f'MgExecItemMultiCmd.slotOneCmdDone({success}) - {self}')

        try:
            # just to trigger access to C++ object
            self.text(0)
        except RuntimeError:
            # dialog has been closed, we no longer care to update it
            warning('slotOneCmdDone() - C++ object deleted event')
            # no need to update it graphically anymore
            self.ignoreUpdates = True

        if self.ignoreUpdates:
            dbg('MgExecitemMultiCmd.slotOneCmdDone() - ignore updates and aborting early')
            self.taskGroup.repo.refresh()
            return


        if not success and not self.abortRequested:
            # last command fail, show it in the icon, ask a question
            self.setIcon(0, getIcon(IconSet.Failed))

            if not self.askQuestionUponFailure:
                # return before opening the item and handling the question
                self.allCmdDone()
                return

            self.setExpanded(True)
            self.askQuestionAfterCmdFailed()
            return

        if not self.isDone:
            # more jobs to run !
            self.runOneCmdline()
            return

        self.allCmdDone()


    def allCmdDone(self, setIconForResult: bool = True) -> None:
        '''Tasks to perform when all jobs are done'''
        dbg(f'MgExecItemMultiCmd.allCmdDone() - {self}')
        # no need to do more, everything was already done for notifying of job being finished

        # mark all commands as done
        self.nbCmdDone = len(self.taskGroup)

        # we are done with all jobs
        if self.abortRequested:
            self.setIcon(0, getIcon(IconSet.Aborted))
        elif self.nbError == 0:
            self.setIcon(0, getIcon(IconSet.Success))
        else:
            self.setIcon(0, getIcon(IconSet.Failed))

        self.cbExecDone(self.nbError == 0 and not self.abortRequested)

        # url does not need to be refreshed that often...
        self.taskGroup.repo.refresh()


    def askQuestionAfterCmdFailed(self) -> None:
        '''Called when one task has failed, which is not the final task'''
        if self.abortRequested:
            dbg(f'MgExecItemMultiCmd.askQuestionAfterCmdFailed() - do nothing after abort requested')
            return

        self.buttonBarItem = QTreeWidgetItem(type=QTREE_WIDGET_ITEM_BUTTONBAR_TYPE)
        self.addChild(self.buttonBarItem)
        flags = UserActionOnGitError.NOTHING
        if not self.isDone:
            flags |= UserActionOnGitError.CONTINUE
            flags |= UserActionOnGitError.ABORT
            flags |= UserActionOnGitError.RETRY
        else:
            flags |= UserActionOnGitError.ABORT
            flags |= UserActionOnGitError.RETRY
            flags |= UserActionOnGitError.OK
        self.buttonBar = MgButtonBarErrorHandling(self.treeWidget(), flags)
        self.buttonBar.sigUserChoiceDone.connect(self.handleQuestionResult)
        self.treeWidget().setItemWidget(self.buttonBarItem, 0, self.buttonBar)
        self.buttonBarItem.setIcon(0, getIcon(IconSet.Question))


    def handleQuestionResult(self, result: UserActionOnGitError) -> None:
        dbg(f'MgExecItemMultiCmd.handleQuestionResult({result}) - {self}')
        # hide the buttons
        assert self.buttonBarItem is not None
        self.treeWidget().setItemWidget(self.buttonBarItem, 0, None)
        self.buttonBar = None
        lastTaskItem = cast(MgExecItemOneCmd, self.child(self.childCount()-2))
        lastTaskItem.setExpanded(False)

        if result == UserActionOnGitError.ABORT or self.abortRequested:
            self.taskGroup.abort()
            self.buttonBarItem.setIcon(0, getIcon(IconSet.Aborted))
            self.buttonBarItem.setText(0, 'Aborting job')
            self.allCmdDone()
            return

        if result == UserActionOnGitError.CONTINUE:
            self.buttonBarItem.setText(0, 'Continuing job')
            # mark with a transparent check, to show that we validate but something was strange
            self.buttonBarItem.setIcon(0, getIcon(IconSet.UserOk))
            # resume execution of the set of tasks
            self.runOneCmdline()
            return

        if result == UserActionOnGitError.RETRY:
            self.buttonBarItem.setText(0, 'Retrying last command')
            self.buttonBarItem.setIcon(0, getIcon(IconSet.Retry))
            self.runOneCmdline(retrying=True)
            return

        if result == UserActionOnGitError.OK:
            self.buttonBarItem.setText(0, 'OK')
            self.buttonBarItem.setHidden(True)
            self.allCmdDone()
            return

        # handle retry as well
        assert False, 'should not be reached'


    def abortItem(self) -> None:
        dbg(f'MgExecItemMultiCmd.abortItem() - {self}')

        self.taskGroup.abort()
        self.abortRequested = True

        if self.buttonBar:
            # we are currently asking a question to the user, use the abort path to get everything completed
            self.handleQuestionResult(UserActionOnGitError.ABORT)
            return

        if self.nbCmdDone == len(self.taskGroup):
            # all jobs were done, either successfully or failed, there is really nothing to do.
            # if there was an error, it is not due to abort request, so it is reported as failure normally
            # we hide the fact that abort was requested because it no longer matters, everything was completed before
            self.abortRequested = False
            return

        # not all jobs were completed, meaning either we have never started any jobs,
        # or we have there is one (and only one) job in progress

        if not self.isStarted:
            # no jobs started at all
            self.allCmdDone()
            return


        # find the job in progress and abort it
        for idx in range(self.childCount()):
            childItem = self.child(idx)
            if childItem.type() == QTREE_WIDGET_ITEM_BUTTONBAR_TYPE:
                continue
            assert isinstance(childItem, MgExecItemOneCmd)
            if childItem.isTaskStarted() and not childItem.isTaskDone():
                # we have found the task in progress
                childItem.abortItem()
                # this will call slotOneCmdDone() with success or failure, nothing more to do
                return

        # self.allCmdDone() will be called indirectly when the running finished, successfully or with error
        raise ValueError('Should not be reached!')


    def clearRepoConnections(self) -> None:
        self.ignoreUpdates = True
        for childIdx in range(self.childCount()):
            child = self.child(childIdx)
            if child.type() != QTREE_WIDGET_ITEM_BUTTONBAR_TYPE:
                cast(MgExecItemOneCmd, child).clearRepoConnections()


