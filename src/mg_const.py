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


from typing import Optional

import pathlib, platform

############################################
#   Product Constants
############################################

VERSION = '1.7.1'

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
COL_TITLES = ['', 'Git Repo Path', 'Head', 'Status', 'Synchro current branch', 'SHA1', 'URL']

SHORT_SHA1_NB_DIGITS = 7

# This is filled when initializing the application
PATH_LOG_NORMAL: Optional[pathlib.Path]
PATH_LOG_DEBUG: Optional[pathlib.Path]
PATH_LOG_GIT_CMD: Optional[pathlib.Path]
LOGGER_GIT_CMD = 'git_cmd'

GIT_AUTH_FAILURE_MARKER='fatal: Authentication failed'

DISPLAY_FETCH_ON_STARTUP_COUNTDOWN_INIT = 5

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
MSG_REMOTE_NA = 'N.A.'

DISPLAY_IN_ITALIC_MSG = [ MSG_REMOTE_BRANCH_GONE, MSG_LOCAL_BRANCH ]
DISPLAY_IN_BOLD_MSG   = [ 'to push', 'to pull', MSG_REMOTE_BRANCH_GONE ]

try:
    from PySide6.QtCore import qVersion
    pyqt_version_info = '* Qt for Python v%s\n' % qVersion()
    pyqt_version_info = pyqt_version_info.strip('\n')
except ImportError:
    pyqt_version_info = ''

MSG_ABOUT_MULTIGIT = """MultiGit OpenSource v%s

MultiGit manages multiple Git Repositories with one interface.

MultiGit is developed by Philippe Fremy <philippe.fremy@idemia.com> .

Please use Github repository page for any feedback: https://github.com/idemia/multigit/

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

MSG_TOOLTIP_UPDATE = 'git information refresh in progress'
MSG_TOOLTIP_STATUS = 'Display whether files are modified'
MSG_TOOLTIP_REMOTE_SYNCHRO = 'Delta vs origin'



############################################
#   Double click actions
############################################

### All possible double-click actions
DBC_GITCOMMIT          = 'Git Commit'
DBC_GITCREATEBRANCH    = 'Git Create Branch'
DBC_GITSWITCHBRANCH    = 'Git Switch Branch'
DBC_GITPUSH            = 'Git Push'
DBC_GITPULL            = 'Git Pull'
DBC_GITFETCH           = 'Git Fetch'
DBC_REPOSITORYPROPERTIES = 'Repository Properties'
DBC_SHOWINEXPLORER     = 'Show in Explorer'
DBC_DONOTHING          = 'Do nothing'
DBC_TORTOISEGITSHOWLOG = 'TortoiseGit ShowLog'
DBC_TORTOISEGITSWITCH  = 'TortoiseGit Switch'
DBC_TORTOISEGITBRANCH  = 'TortoiseGit Branch'
DBC_TORTOISEGITCOMMIT  = 'TortoiseGit Commit'
DBC_TORTOISEGITDIFF    = 'TortoiseGit Diff'
DBC_TORTOISEGITPUSH    = 'TortoiseGit Push'
DBC_TORTOISEGITPULL    = 'TortoiseGit Pull'
DBC_TORTOISEGITFETCH   = 'TortoiseGit Fetch'
DBC_RUNSOURCETREE      = 'Run SourceTree'
DBC_RUNSUBLIMEMERGE    = 'Run SublimeMerge'
DBC_RUNGITGUI          = 'Run Git Gui'
DBC_RUNGITK            = 'Run GitK'
DBC_RUNGITBASH         = 'Run git-bash'
