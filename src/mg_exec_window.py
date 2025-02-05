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


from typing import Sequence, cast, Any, Tuple, List
import logging, time

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QDialog, QTreeWidgetItem, QDialogButtonBox, QWidget, QApplication, QPushButton

from src.gui.ui_git_exec_window import Ui_GitExecDialog
import src.mg_config as mgc
from src.mg_repo_info import MgRepoInfo
from src.mg_auth_failure_mgr import MgAuthFailureMgr
from src.mg_exec_task_item import MgExecTaskGit, MgExecTask, MgExecItemBase, MgExecItemOneCmd, MgExecItemMultiCmd, MgExecTaskGroup, after_other_taskgroup_is_finished, PreConditionState

logger = logging.getLogger('mg_git_exec_window')
dbg = logger.debug
warning = logger.warning
error = logger.error


# If you get git stack-traces / crash looking like:
# 0 [main] sh (88240) C:\Program Files\Git\usr\bin\sh.exe: *** fatal error - add_item ("\??\C:\Program Files\Git", "/", ...) failed, errno 1
# Increase this time
#
# Also, a delay is needed to avoid that when user changed his password and the stored password is no longer valid
# we don't want too many git process to be started before the first processes fail and a proper action is proposed
# to the user.
DELTA_BETWEEN_CONCURRENT_GIT_RUN = 0.10

INDENT_TEXT = '    '
def collectColumnText(depth: int, item: QTreeWidgetItem) -> List[str]:
    '''Collect text of item and all child, with an indentation'''
    result = [ INDENT_TEXT * depth + text for text in item.text(0).split('\n') ]
    for itemChildIdx in range(item.childCount()):
        result.extend( collectColumnText(depth + 1, item.child(itemChildIdx) ) )
    return result


# noinspection PyAttributeOutsideInit
class MgExecWindow(QDialog):
    '''Window for the execution of one or several git commands'''

    def __init__(self, parent: QWidget, delta_between_concurrent_git_run: float = DELTA_BETWEEN_CONCURRENT_GIT_RUN) -> None:
        super().__init__(parent)
        self.setModal(False)
        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.ui = Ui_GitExecDialog()
        self.ui.setupUi(self)
        self.ui.treeGitJobs.itemExpanded.connect(self.autoAdjustColumnSize)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Discard).clicked.connect( self.slotAbort )
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Discard).setText('Abort')
        self.buttonCopyLog = QPushButton('Copy git log to clipboard', self.ui.buttonBox)
        self.ui.buttonBox.addButton(self.buttonCopyLog, QDialogButtonBox.ButtonRole.ActionRole)
        self.ui.textEditSummary.hide()
        self.buttonCopyLog.clicked.connect( self.slotCopyLog )
        self.delta_between_concurrent_git_run = delta_between_concurrent_git_run
        self.clear()
        MgAuthFailureMgr.newSession()

    def clear(self) -> None:
        self.abort_requested = False
        self.ui.treeGitJobs.clear()
        self.nb_errors = 0
        self.nb_jobs = 0
        self.nb_jobs_running = 0
        self.nb_jobs_done = 0
        self.last_started_job_time = 0.0
        self.first_started_job_time = 0.0
        self.duration = 0.0
        self.askQuestionUponFailure = True


    def execOneGitCommand(self, desc: str, cmdline: List[str], repos: Sequence[MgRepoInfo],
                          display_window: bool = True) -> None:
        '''Execute the same git command on each repo of the list of repos.

        cmdline: command-line to execute on the repo, provided as a list of string.
                 The git command should not be part of it.
        '''
        return self.execSeqOfGitCommand(desc, [cmdline], repos, display_window)


    def execSeqOfGitCommand(self, desc: str, cmdlineSeq: List[List[str]], repos: Sequence[MgRepoInfo],
                            display_window: bool = True) -> None:
        '''Run the sequence of git commands on each repo listed in repos

        desc: a string used to describe the command under execution
        cmdlineSeq: list of command-lines for git as a list of string for the git command.
                    The git command should not be part of it.
        repos: a sequence of MgRepoInfo to run the command on

        This will:
        - show the window
        - execute the command on each repo in background, updating the window live
        - display errors in red
        - once command is completed, refresh the item in the view
        - update the progress bar
        - show a final status
        '''
        self.execEachRepoWithHisSeqOfGitCommand(desc, [(repo.name, repo, cmdlineSeq) for repo in repos], display_window)


    def execEachRepoWithHisSeqOfGitCommand(self, globalDesc: str,
                                           cmdlinePerRepo: List[Tuple[str, MgRepoInfo, List[List[str]]]],
                                           display_window: bool = True) -> None:
        '''For each repo, execute a different sequence of git command.

        globalDesc: a global description string
        cmdLinePerRepo: a Tuple containing the following elements:
            * a description string of the command to run
            * the repo on which to run the git command
            * the sequence git command to execute, as a list of list of string, excluding the git executable itself

        Example:
            execEachRepoWithHisSeqOfGitCommand('Cloning Repositories', [
                ('cloning multigit from GitHub',
                 repoInfo,
                 [
                    ['clone', 'https://github.com/Multigit', 'c:\\work\\MultiGit' ],
                    ['checkout', 'master'],
                 ]
                ),
                ('cloning multigit plugins',
                 repoInfo,
                 [
                    ['clone', 'https://git.oberthur.com/Multigit-plugin', 'c:\\work\\MultiGit-plugin'],
                    ['checkout', 'master'],
                 ]
                ),
                ...
            ])
        '''
        taskGroups = [
            MgExecTaskGroup(repo.name, repo, [cast(MgExecTask, MgExecTaskGit('', repo, cmdLine)) for cmdLine in cmdlineSeq])
            for (desc, repo, cmdlineSeq) in cmdlinePerRepo
        ]
        # tasksPerRepo[0][2][0].pre_condition = precond_other_task_finished(tasksPerRepo[-1][2][0])
        self.execTaskGroups(globalDesc, taskGroups, display_window)


    def execTaskGroups(self, globalDesc: str,
                       taskGroups: List[MgExecTaskGroup],
                       display_window: bool = True
                       ) -> None:
        '''Execute each task group under a global description'''
        dbg(f'execTaskGroups({globalDesc}, {taskGroups}, {display_window})')
        if display_window is True:
            self.show()
        self.nb_jobs += len(taskGroups)
        self.abort_requested = False

        tli = QTreeWidgetItem([globalDesc])
        self.ui.treeGitJobs.addTopLevelItem( tli )
        tli.setExpanded(True)

        jobitem: MgExecItemBase
        for taskGroup in taskGroups:
            # multiple jobs to run, even if there is only one item
            jobitem = MgExecItemMultiCmd(taskGroup, self.oneMoreJobDone, self.askQuestionUponFailure)
            tli.addChild( jobitem )

        # 1/3 for starting the job
        # +2/3 for job completion
        # we set a goal to 1 when there are zero jobs
        self.ui.progressBar.setMaximum(max(self.nb_jobs*3, 1))
        self.autoAdjustColumnSize()

        self.duration = 0.0
        self.first_started_job_time = time.time()
        self.updateProgress()

        self.last_started_job_time = time.time() - self.delta_between_concurrent_git_run - 0.1 # note: force the delta to run the first job
        self.startNewJobs()


    def startNewJobs(self) -> None:
        dbg('startNewJobs')
        if self.abort_requested:
            dbg('startNewJobs() - Avoid starting new jobs because abort was requested')
            return

        nb_jobs_started = 0
        nb_jobs_blocked_by_precondition = 0
        max_git_process = mgc.get_config_instance().get(mgc.CONFIG_NB_GIT_PROC, 0)
        for jobItem in self.getAllJobItems():
            if max_git_process and self.nb_jobs_running == max_git_process:
                dbg('startNewJobs() - max number of process reached')
                # we have reach our maximum
                return

            dbg('startNewJobs() - looking at job to start: %s' % jobItem)
            if not jobItem.isStarted:
                if jobItem.taskGroup.is_precondition_fulfilled() == PreConditionState.NotFulfilled :
                    dbg(f'startNewjobs() - condition not fullfilled for {jobItem.taskGroup}, choosing the next one')
                    nb_jobs_blocked_by_precondition += 1
                    continue

                if jobItem.taskGroup.is_precondition_fulfilled() == PreConditionState.Errored :
                    dbg(f'startNewjobs() - condition already in error for {jobItem.taskGroup}, aborting the item')
                    jobItem.abortItem()
                    continue

                # condition is fulfilled, we can start

                # leave some time between each run of process, else you get a git crash
                # this is a git/cygwin concurrency issue so limit the concurrency here
                # also, it is better visually.
                cur_time = time.time()
                while cur_time - self.last_started_job_time < self.delta_between_concurrent_git_run:
                    QApplication.processEvents()
                    cur_time = time.time()

                # note: the processEvent() call may catch another job finishing, triggering
                #       a call to startNewJobs() in parallel to the currently running one.
                #       This in-between call may start the job which we are currently looking at.
                #       So be sure to check again that the job is not started.

                if not jobItem.isStarted:
                    dbg('startNewJobs() - actually starting: %s' % jobItem)
                    self.last_started_job_time = cur_time
                    self.nb_jobs_running += 1
                    nb_jobs_started += 1
                    jobItem.run()
                else:
                    # job was started in the interim
                    dbg('startNewJobs() - job started while we were waiting: {}'.format(jobItem))
                    dbg('startNewJobs() - proceed to the next job')

        if nb_jobs_blocked_by_precondition > 0 and not self.abort_requested \
                and (not max_git_process or self.nb_jobs_running < max_git_process):
            # we have room to start new jobs, but we did not do it, certainly because of non fulfilled
            # preconditions. In this case, let's give some delay for the preconditions and call back this
            # method again.
            # If we don't to this, we rely on job completion to call startNewJobs(), but some precondition
            # can fulfill before any job completion.
            dbg('startNewJobs() - give a chance to start jobs again in one second')
            QTimer.singleShot(1000, self.startNewJobs)
            return


    def getAllJobItems(self) -> List[MgExecItemMultiCmd]:
        '''Return a list of all MgExecItemMultiCmd'''
        all_job_items: List[MgExecItemMultiCmd] = []
        for tliIdx in range(self.ui.treeGitJobs.topLevelItemCount()):
            tli = self.ui.treeGitJobs.topLevelItem(tliIdx)
            assert tli is not None
            for childIdx in range(tli.childCount()):
                jobItem = cast(MgExecItemMultiCmd, tli.child(childIdx))
                assert isinstance(jobItem, MgExecItemMultiCmd)
                all_job_items.append(jobItem)
        return all_job_items


    def updateProgress(self) -> None:
        if self.nb_errors > 0:
            msg = '%d of %d completed, with %d errors' % (self.nb_jobs_done, self.nb_jobs, self.nb_errors)
        else:
            msg = '%d of %d completed' % (self.nb_jobs_done, self.nb_jobs)
        if self.nb_jobs_done == self.nb_jobs and self.duration != 0.0:
            msg += ' in %0.1f seconds' % self.duration
        self.ui.labelTasks.setText(msg)
        if self.nb_jobs == 0:
            # when running with no jobs, we fake the 100% immediatly
            self.ui.progressBar.setValue(1)
        else:
            self.ui.progressBar.setValue(self.nb_jobs + self.nb_jobs_done*2)
        completed = (self.nb_jobs_done == self.nb_jobs)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Discard).setEnabled(not completed)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(completed)


    def oneMoreJobDone(self, success: bool) -> None:
        '''Called when one job is completed, with the success status'''
        dbg(f'oneMoreJobDone(success={success})')
        self.nb_jobs_done += 1
        self.nb_jobs_running -= 1
        if self.nb_jobs_done == self.nb_jobs:
            # we are done !
            self.duration = time.time() - self.first_started_job_time
        if not success:
            self.nb_errors += 1
        dbg('Running %d, done %d, errors %d, remaining %d' % (self.nb_jobs_running, self.nb_jobs_done,
            self.nb_errors, self.nb_jobs-self.nb_jobs_done))
        self.updateProgress()
        self.autoAdjustColumnSize()

        if not self.abort_requested and self.nb_jobs_done < self.nb_jobs:
            # we have not started all our jobs (probably because of the MAX_PROCESS limitation),
            # start the remaining ones
            dbg(f'Starting new jobs for {self.nb_jobs - self.nb_jobs_done} jobs remaining')
            self.startNewJobs()


    def slotAbort(self) -> None:
        '''Triggered when abort is requested'''
        dbg('Aborting...')
        self.abort_requested = True
        for topLevelIdx in range(self.ui.treeGitJobs.topLevelItemCount()-1, -1, -1):
            topLevel = self.ui.treeGitJobs.topLevelItem(topLevelIdx)
            assert topLevel is not None
            # note: we must abort in the reverse order, else one abort is going to trigger the next job
            #       which is not aborted yet at the item level
            for i in reversed(range(topLevel.childCount())):
                childItem = topLevel.child(i)
                if isinstance(childItem, MgExecItemBase):
                    childItem.abortItem()


    def slotCopyLog(self) -> None:
        '''Copy the log of the window to the clipboard'''
        fullLog = []        # type: List[str]
        for topLevelIdx in range(0, self.ui.treeGitJobs.topLevelItemCount()):
            item = self.ui.treeGitJobs.topLevelItem(topLevelIdx)
            assert item is not None
            fullLog.extend( collectColumnText(0, item) )

        QGuiApplication.clipboard().setText('\n'.join(fullLog))


    def autoAdjustColumnSize(self) -> None:
        '''Adjust automatically the column size to the largest item'''
        for i in range(self.ui.treeGitJobs.columnCount()):
            self.ui.treeGitJobs.resizeColumnToContents(i)
        QApplication.processEvents()


    def done(self, v: Any) -> None:
        '''Called by the OK button when closing the dialog'''
        dbg('done()')
        self.clear()
        super().done(v)


    def waitForJobCompletion(self) -> None:
        '''Wait until all running jobs have completed'''
        while self.nb_jobs_done < self.nb_jobs:
            QApplication.processEvents()


# TODO: ensure that passing multiple commands per repo gets a proper title