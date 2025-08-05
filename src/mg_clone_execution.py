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


from typing import TYPE_CHECKING, List, Optional, cast, Set
import logging, os, subprocess, time
import enum
import tempfile

from PySide6.QtWidgets import QMessageBox

if TYPE_CHECKING:
    from src.mg_window import MgMainWindow
    from src.mg_json_mgit_parser import ProjectStructure

from src.mg_repo_info import MgRepoInfo
from src.mg_exec_window import MgExecWindow
from src.mg_exec_task_item import MgExecTaskGroup, after_other_taskgroup_is_started_and_dir_exists, MgTaskMoveDirectory, MgTaskDelDirectory
from src.mg_utils import tryHardDeletingDirList

logger = logging.getLogger('mg_clone_from_dialog')
dbg = logger.debug
warn = logger.warning


class CloneExistDirBehavior(enum.Enum):
    skipClone = enum.auto()
    deleteDirectory = enum.auto()
    gitFails = enum.auto()


def cloneFromDialog(structureToClone: 'ProjectStructure', window: 'MgMainWindow', existingDirBehavior: CloneExistDirBehavior,) -> None:
    '''Triggered by clone from Multigit file, clone from Sage file'''
    dbg('cloneFromDialog')
    # user clicked on OK, display the folder in the main window
    # performing clone

    taskGroups: List[MgExecTaskGroup] = []
    reposToClone = structureToClone.repos[:]
    reposToClone.sort(key=lambda r: r.destination)

    skipDir  = []
    toDelDir = []
    alreadyExists = []
    destinationSet: Set[str] = set([])
    duplicatedDests: Set[str] = set([])

    # First pass, inspect the actions to perform
    for jsonFileRepo in reposToClone:
        if jsonFileRepo.url == '':
            # the user was informed about this, skip the repo
            continue

        if os.path.exists(jsonFileRepo.dest_fullpath):
            # ohoh, directory exists, let see what user want us to do:
            if existingDirBehavior == CloneExistDirBehavior.skipClone:
                skipDir.append(jsonFileRepo.dest_fullpath)
                # the best way to skip is to do nothing
                continue

            if existingDirBehavior == CloneExistDirBehavior.deleteDirectory:
                toDelDir.append(jsonFileRepo.dest_fullpath)

            if existingDirBehavior == CloneExistDirBehavior.gitFails:
                # this is the default behavior, so do nothing
                alreadyExists.append(jsonFileRepo.dest_fullpath)


        if jsonFileRepo.dest_fullpath in destinationSet:
            duplicatedDests.add(jsonFileRepo.dest_fullpath)
        destinationSet.add(jsonFileRepo.dest_fullpath)


    if len(alreadyExists):
        msg = 'The following repositories already exists:\n'
        msg += '- ' + '\n- '.join(alreadyExists) + '\n\n'
        msg += 'Continue will trigger a git error for these repositories, please consider Deleting them.'
        msgBox = QMessageBox(window)
        msgBox.setWindowTitle('Confirm clone on existing')
        msgBox.setText(msg)
        continueButton = msgBox.addButton('Continue', QMessageBox.ButtonRole.AcceptRole)
        delButton = msgBox.addButton('Delete directories', QMessageBox.ButtonRole.AcceptRole)
        abortButton = msgBox.addButton(QMessageBox.StandardButton.Abort)
        msgBox.exec()
        buttonSelected = msgBox.clickedButton()

        if buttonSelected == abortButton:
            # user changed its mind ...
            return

        elif buttonSelected == delButton:
            # mark the directories to be deleted
            toDelDir = alreadyExists


    if len(skipDir):
        msg = 'The following repositories already exists and will NOT be cloned (skip behavior):\n'
        msg += '- ' + '\n- '.join(skipDir) + '\n'
        buttonSelectedWarning = QMessageBox.warning(window, 'Confirm skip of repositories', msg, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort)
        if buttonSelectedWarning == QMessageBox.StandardButton.Abort:
            # user changed its mind ...
            return

    if len(toDelDir):
        # alreadyExists is set when user chose no special action in the clone dialog, but
        # choose to delete in the second dialog
        if not alreadyExists:
            # the user has not yet validated the list of repos
            msg = 'The following repositories already exists and will be DELETED (delete behavior):\n'
            msg += '- ' + '\n- '.join(toDelDir) + '\n'
            buttonSelectedWarning = QMessageBox.warning(window, 'Confirm deletion of repositories', msg, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort)
            if buttonSelectedWarning == QMessageBox.StandardButton.Abort:
                # user changed its mind ...
                return

    for jsonFileRepo in reposToClone:
        if jsonFileRepo.url == '':
            # the user was informed about this, skip the repo
            continue

        repoInfo = MgRepoInfo(jsonFileRepo.destination, jsonFileRepo.dest_fullpath, jsonFileRepo.destination)
        taskGroup = MgExecTaskGroup(f'Cloning {repoInfo.name}', repoInfo)

        if jsonFileRepo.dest_fullpath in toDelDir:
            taskGroup.tasks.append(MgTaskDelDirectory(f'Delete directory prior to cloning `{jsonFileRepo.dest_fullpath}`',
                                                      repoInfo,
                                                      jsonFileRepo.dest_fullpath,
                                                      )
                                   )


        if jsonFileRepo.dest_fullpath not in duplicatedDests:
            taskGroup.appendGitTask(f'git clone {repoInfo.name}',
                                    ['clone', '--progress', jsonFileRepo.url, jsonFileRepo.dest_fullpath],
                                    run_inside_git_repo=False,
                                    )

            if len(jsonFileRepo.head):
                # use checkout and not switch because HEAD may point to a branch, tag or commit SHA1
                taskGroup.appendGitTask( f'git checkout {jsonFileRepo.head}', ['checkout', jsonFileRepo.head, '--' ] )
            # if head is empty, the repo is probably empty, so do nothing

        else:
            tempDestPath = tempfile.mkdtemp(prefix=repoInfo.name + '_')
            taskGroup.appendGitTask(f'git clone to temp directory (because the target directory contains multiple git repositories)',
                                    ['clone', '--progress', jsonFileRepo.url, tempDestPath],
                                    run_inside_git_repo=False,
                                    )
            if len(jsonFileRepo.head):
                # use checkout and not switch because HEAD may point to a branch, tag or commit SHA1
                taskGroup.appendGitTask( f'git checkout {jsonFileRepo.head}',
                                         ['-C', tempDestPath, 'checkout', jsonFileRepo.head, '--' ],
                                         run_inside_git_repo=False )
            # if head is empty, the repo is probably empty, so do nothing


            taskGroup.tasks.append(MgTaskMoveDirectory(f'Move clone to final directory `{jsonFileRepo.dest_fullpath}`',
                                                        repoInfo,
                                                        tempDestPath,
                                                       jsonFileRepo.dest_fullpath,
                                                       skip_git_admin_dir=True)
                                       )

            taskGroup.tasks.append(MgTaskDelDirectory(f'Delete temp directory `{tempDestPath}`',
                                                       repoInfo,
                                                       tempDestPath,
                                                      )
                                   )


        taskGroups.append( taskGroup )


    # Ensure that clone will work with nested subdirectories
    taskGroups = addPreconditionToEnsureCloneOrderLogic(taskGroups)

    # Give some time between two clones to make sure a clone is fully started
    # before the next one starts, because the next one may create some subdirectories
    # which would then prevent the first clone.
    gitExecWindow = MgExecWindow(window, 0.5)
    gitExecWindow.execTaskGroups('Clone project repositories', taskGroups)

    # show the newly created path in MultiGit
    gitExecWindow.finished.connect( lambda result: window.openDir(str(structureToClone.base_path)) )


class TaskNode:
    def __init__(self, parent: Optional['TaskNode'], name: str, taskGroup: Optional[MgExecTaskGroup]) -> None:
        self.parent = parent
        self.name = name
        self.taskGroup = taskGroup
        self.children: List['TaskNode'] = []


    def addChild(self, parts: List[str], taskGroup: MgExecTaskGroup ) -> 'TaskNode':
        '''Add a child in the graph, in the right node'''
        if len(parts) == 0:
            # we are ready to set the task group
            self.taskGroup = taskGroup
            return self

        for child in self.children:
            if child.name == parts[0]:
                # we have found our children !
                break
        else:
            # we have found no children, create one
            child = TaskNode(self, parts[0], None)
            self.children.append(child)

        # continue the search
        return child.addChild(parts[1:], taskGroup)


def build_taskgroup_dep_graph(taskGroups: List[MgExecTaskGroup]) -> TaskNode:
    '''Build a dependency graph with the nodes and return the top node of the graph'''
    topNode = TaskNode(None, '', None)

    for taskGroup in taskGroups:
        splitter = '/'
        if not splitter in taskGroup.repo.name and '\\' in taskGroup.repo.name:
            splitter = '\\'
        topNode.addChild( taskGroup.repo.name.split(splitter), taskGroup )

    return topNode


def findParentTaskGroup(node: TaskNode) -> Optional[TaskNode]:
    '''Walk the parent of this tasknode until another tasknode is found and return it.

    If no tasknode is found, return None'''
    while node.parent is not None:
        if node.parent.taskGroup is not None:
            return node.parent

        node = node.parent

    return None


def addPreconditionsToTaskGroup(node: TaskNode) -> None:
    '''Using the graph, modify the taskGroup objects in place by adding preconditions
    when one taskGroup depends on another one.'''

    if node.taskGroup is not None:
        # add precondition for this node
        parentTaskGroupNode = findParentTaskGroup(node)

        if parentTaskGroupNode is not None:
            assert parentTaskGroupNode.taskGroup is not None
            node.taskGroup.pre_condition = after_other_taskgroup_is_started_and_dir_exists(parentTaskGroupNode.taskGroup)

    # add preconditions for this nodes children
    for n in node.children:
        addPreconditionsToTaskGroup(n)



def addPreconditionToEnsureCloneOrderLogic(taskGroups: List[MgExecTaskGroup]) -> List[MgExecTaskGroup]:
    '''Generate preconditions so that a subdirectory of a git repo is cloned after the git parent git repo.

    The taskGroup inside the list are modifed in place, with a new precondition.

    Example, with the structure:
    dev/ (git repo)
      + subdev1 (git repo)
        + subdev1_sub1 (git repo)
        + subdev1_sub2 (git repo)
      + subdev2 (git repo)
        + toto
           + subdev2_sub1 (git repo)

    It will generate the following pre-conditions:
    - subdev1 is cloned after dev/ clone has started
    - subdev1_sub1 is cloned after subdev1/ clone has started
    - subdev1_sub2 is cloned after subdev1/ clone has started
    - subdev2 is cloned after dev/ clone has started
    - subdev2_sub1 is cloned after subdev2/ clone has started
    '''
    topNode = build_taskgroup_dep_graph(taskGroups)

    addPreconditionsToTaskGroup(topNode)

    return taskGroups

# TODO
# - rename Structure  to JsonFileStructure
# - rename Repository to JsonFileRepo
# - rename Repository to JsonFilePostCloneCommand


