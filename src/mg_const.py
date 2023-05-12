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


from typing import List, Optional
import pathlib, os, platform, enum

############################################
#   Product Constants
############################################

VERSION = '1.6.0'

MAX_DIFF_LINES = 1000
MAX_GIT_DBG_OUT_CHAR = 5000

COL_UPDATE = 0
COL_REPO_NAME = 1
COL_HEAD = 2
COL_STATUS = 3
COL_REMOTE_SYNCHRO = 4
COL_SHA1 = 5
COL_URL = 6
COL_NB = 7
COL_TITLES = ['', 'Git Repo Path', 'Head', 'Status', 'Last Remote Synchro', 'SHA1', 'URL']

SHORT_SHA1_NB_DIGITS = 7

GIT_PATH_CANDIDATES: List[pathlib.Path] = [
    pathlib.Path(os.environ["ProgramFiles(x86)"])/"Git"/"bin"/ "git.exe",
    pathlib.Path(os.environ["ProgramFiles(x86)"])/"Git"/"cmd"/ "git.exe",
    pathlib.Path(os.environ["PROGRAMW6432"])/"Git"/"bin"/ "git.exe",
    pathlib.Path(os.environ["PROGRAMW6432"])/"Git"/"cmd"/ "git.exe",
    ]
GIT_EXEC = 'git.exe'

TORTOISE_GIT_PATH_CANDIDATES: List[pathlib.Path] = [
    pathlib.Path(os.environ["ProgramFiles(x86)"])/"TortoiseGit"/"bin"/ "TortoiseGitProc.exe",
    pathlib.Path(os.environ["PROGRAMW6432"])/"TortoiseGit"/"bin"/ "TortoiseGitProc.exe",
]
SOURCETREE_PATH_CANDIDATES: List[pathlib.Path] = [
    pathlib.Path(os.environ["ProgramFiles(x86)"])/"Atlassian"/"SourceTree"/ "SourceTree.exe",
]

SUBLIMEMERGE_PATH_CANDIDATES: List[pathlib.Path] = [
    pathlib.Path(os.environ["PROGRAMW6432"])/"Sublime Merge"/"sublime_merge.exe",
]

GITBASH_PATH_CANDIDATES: List[pathlib.Path] = [
    pathlib.Path(os.environ["PROGRAMW6432"])/"Git"/"git-bash.exe",
    pathlib.Path(os.environ["ProgramFiles(x86)"]) /"Git"/"git-bash.exe",
]
APPDATA_USER_MULTIGIT = pathlib.Path(os.environ['USERPROFILE']) / 'AppData/Local/MultiGit/'

# This is filled when initializing the application
PATH_LOG_NORMAL: Optional[pathlib.Path]
PATH_LOG_DEBUG: Optional[pathlib.Path]
PATH_LOG_GIT_CMD: Optional[pathlib.Path]
LOGGER_GIT_CMD = 'git_cmd'

GIT_AUTH_FAILURE_MARKER='fatal: Authentication failed'

############################################
#   UI Messages
############################################

MSG_BIG_DIFF = 'Diff is too big to be displayed in total.'
MSG_NO_COMMIT= 'No commit yet...'
MSG_EMPTY_REPO = '<empty repo>'

# remote_synchro messages
MSG_REMOTE_SYNCHRO_OK = 'Up-to-date'
MSG_REMOTE_TOPUSH     = '%d to push'
MSG_REMOTE_TOPULL     = '%d to pull'
MSG_REMOTE_TOPUSH_TOPULL = '%d to push, %d to pull'
MSG_REMOTE_BRANCH_GONE = 'remote branch deleted'
MSG_LOCAL_BRANCH = 'No remote tracking'
MSG_LOCAL_BRANCH_TOOLTIP = 'Set remote tracking branch by using Multigit -> git -> push .'

DISPLAY_IN_ITALIC_MSG = [ MSG_REMOTE_BRANCH_GONE, MSG_LOCAL_BRANCH ]
DISPLAY_IN_BOLD_MSG   = [ 'to push', 'to pull', MSG_REMOTE_BRANCH_GONE ]

try:
    from PySide2.QtCore import qVersion
    pyqt_version_info = '* Qt for Python v%s\n' % qVersion()
    pyqt_version_info = pyqt_version_info.strip('\n')
except ImportError:
    pyqt_version_info = ''

MSG_ABOUT_MULTIGIT = """MultiGit v%s

MultiGit manages multiple Git Repositories with one interface.

MultiGit is developed by Philippe Fremy <philippe.fremy@idemia.com> and Florent Oulieres <florent.oulieres@idemia.com>
Please contact us for any requests or bugs.

MultiGit is based on the following software:
* Python v%s
%s
* Git
* PyInstaller v5.0

Icons provided freely by icons8 (see https://icons8.com )
""" % (VERSION, platform.python_version(), pyqt_version_info)

MSG_GIT_EXEC_STARTING_EXEC  = 'Git batch execution %d of %d'
MSG_GIT_EXEC_FAILED  = 'Git execution crashed or was interrupted'
MSG_GIT_EXEC_BAD_EXIT_STATUS = 'Git exited with error code %d'
MSG_GIT_EXEC_OK = 'Git executed successfully'
MSG_GIT_EXEC_ALL_OK = 'Successful execution of %d git %s'
MSG_GIT_EXEC_1_OK = 'Successful execution of git %s'
MSG_GIT_SOME_FAILED = 'Failed execution of git %s, %d errors out of %d'


class DoubleClickActions(enum.Enum):
    '''All possible actions for double-click on a repo. Some actions are intentionally not
    included in this list because they are too invasive to be put on a double-click:
    * git revert, git tag, git delete branch, git push tags
    * tortoise git revert, tortoise git tag
    '''

    GitCommit          = 'Git Commit'
    GitCreateBranch    = 'Git Create Branch'
    GitSwitchBranch    = 'Git Switch Branch'
    GitPush            = 'Git Push'
    GitPull            = 'Git Pull'
    GitFetch           = 'Git Fetch'

    TortoiseGitShowLog = 'TortoiseGit ShowLog'
    TortoiseGitCommit  = 'TortoiseGit Commit'
    TortoiseGitSwitch  = 'TortoiseGit Switch'
    TortoiseGitBranch  = 'TortoiseGit Branch'
    TortoiseGitPush    = 'TortoiseGit Push'
    TortoiseGitPull    = 'TortoiseGit Pull'
    TortoiseGitFetch   = 'TortoiseGit Fetch'
    TortoiseGitDiff    = 'TortoiseGit Diff'

    RunSourceTree      = 'Run SourceTree'
    RunSublimeMerge    = 'Run SublimeMerge'
    RepositoryProperties = 'Repository Properties'
    ShowInExplorer     = 'Show in Explorer'
    DoNothing          = 'Do nothing'
