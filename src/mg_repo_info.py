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


from typing import Dict, Tuple, Optional, List, Callable, Any, Sequence
import logging, re, csv, pathlib, os
from glob import glob, escape

from PySide2.QtCore import Signal, QObject, QCoreApplication
from PySide2.QtWidgets import QMessageBox

from src.mg_const import MSG_NO_COMMIT, MSG_REMOTE_TOPUSH_TOPULL, MSG_REMOTE_SYNCHRO_OK, MSG_REMOTE_TOPULL, \
    MSG_REMOTE_TOPUSH, MSG_REMOTE_BRANCH_GONE, MSG_LOCAL_BRANCH, SHORT_SHA1_NB_DIGITS, MSG_EMPTY_REPO
from src.mg_tools import RunProcess, ExecGit
from src.mg_utils import anonymise_git_url

logger = logging.getLogger('mg_repo_info')
dbg = logger.debug
warn = logger.warning

def dbg_var(var_name: str, var_value: str) -> None:
    logger.debug('{}="{}"'.format(var_name, var_value))

RECYCLE_BIN=pathlib.Path(r'\$Recycle.Bin')

def is_git_repo(repo: pathlib.Path) -> bool:
    '''Return True if directory is actually a git repo.
    Checks for the presence of .git directory and other mandatory files.
    '''
    git_dir = repo/'.git'
    try:
        rec_bin = pathlib.Path(git_dir.drive)/RECYCLE_BIN
        _ = git_dir.relative_to(rec_bin)
        # No exception raised, we are in the recycle bin
        # we don't want to return git repo from the recycle bin
        return False
    except ValueError:
        # good, git_dir is not in the Recycle Bin...
        pass

    for subd in [ 'hooks', 'info', 'objects', 'refs' ]:
        subd_path = git_dir/subd
        if not subd_path.exists() or not subd_path.is_dir():
            return False
    return True

re_ahead_behind = re.compile('(ahead (?P<ahead2>\\d+), behind (?P<behind2>\\d+))|(ahead (?P<ahead>\\d+))|(behind (?P<behind>\\d+))')
def match_ahead_behind(s: str) -> Tuple[int, int]:
    '''Match a string and return the number for ahead and the number for behind
    Possible matches: "ahead 33", "behind 22", "ahead 33, behind 22"
    '''
    mo = re_ahead_behind.match(s)
    if mo is None:
        warn('No re match for match_ahead_behind("%s")' % s)
        return 0, 0
    nb_ahead, nb_behind = 0, 0
    if mo.group('ahead'):
        nb_ahead = int(mo.group('ahead'))
    elif mo.group('ahead2'):
        nb_ahead = int(mo.group('ahead2'))
    if mo.group('behind'):
        nb_behind = int(mo.group('behind'))
    elif mo.group('behind2'):
        nb_behind = int(mo.group('behind2'))
    return nb_ahead, nb_behind

hexdigits = '0123456789abcdefABCDEF'
def is_not_sha1(ref: str) -> bool:
    '''Return True is this can not be a commit SHA1 and False if this may be a SHA1 or a tag with only numbers+A-F letters'''
    if ref.isdigit():
        # only digits, no way to guess between commit and tags
        return False

    if not ref.isalnum():
        # if contains '.' or '_', this is a tag name
        return True

    non_hex_chars = [c for c in ref if not c in hexdigits]
    if len(non_hex_chars):
        return True

    # we don't know
    return False


class MultiRepo:
    '''Public fields:
    - base_path: base path for finding all contained git repositories
    - repo_dict: dictionnary mapping repo names to MgRepoInfo
    - repo_names: sorted list of repository names.
    '''
    # base_dir an base_path represent the same information in two format: the base directory
    base_path: pathlib.Path
    base_dir: str

    # to iterate over all repo names in sorted order
    repo_names: List[str]

    # to itereate  over all repos objects in sorted order
    repo_list: List['MgRepoInfo']

    # to find a repo given its name
    repo_dict: Dict[str, 'MgRepoInfo']

    def __init__(self, base_dir: str = ''):
        self.base_path = pathlib.Path(base_dir)
        dbg('MultiRepo with dir: %s, %d' % (self.base_path, self.base_path.is_dir()))
        self.base_dir = base_dir
        self.repo_dict = {}
        self.repo_list = []
        self.repo_names = []

    def isEmpty(self) -> bool:
        '''Return whether this instance has been filled or is just empty'''
        return self.base_dir == ''

    def __repr__(self) -> str:
        s = 'MultiRepo< %s >' % self.base_dir
        s += '\n\t' + '\n\t'.join( '%s: %s' % (k, v) for k,v in self.repo_dict.items())
        return s

    def __getitem__(self, item: str) -> 'MgRepoInfo':
        '''Return the MgRepoInfo object from a given repo name'''
        return self.repo_dict[item]

    def __len__(self) -> int:
        '''Return the number of repos'''
        return len(self.repo_names)

    def find_git_repos(self) -> List[str]:
        '''Return a list of git repos contained in base_dir, including base_dir itself, sorted by name'''
        self.repo_dict = {}
        self.repo_list = []
        self.repo_names = []
        self.base_path = pathlib.Path(self.base_dir)
        # Use glob.glob(recursive=True) to follow symlinks whereas Path.glob() doesn't.
        # RND_P_5RNDIT_05-85: ensure base path does not contain magic chars like []*?
        for d in glob(escape(str(self.base_path)) + '/**/.git', recursive=True):
            repo = pathlib.Path(d).parent
            if is_git_repo(repo):
                repo_name = str(repo.relative_to(self.base_path))
                self.repo_names.append(repo_name)

                repo_path = str(repo.resolve())
                repo_info = MgRepoInfo(repo_name, repo_path, repo_name)
                self.repo_dict[repo_name] = repo_info
                self.repo_list.append(repo_info)
                repo_info.repo_deleted.connect(self.slotRepoDeleted)

        self.repo_names.sort(key=lambda name: name.lower())
        self.repo_list.sort(key=lambda repo: repo.name.lower())
        dbg('Repo list:\n%s' % self.repo_names)
        return self.repo_names


    def slotRepoDeleted(self, repo_name: str) -> None:
        '''Called when one of the repo is deleted'''
        dbg('MultiRepo.slotRepoDeleted(%s)' % repo_name)
        if not repo_name in self.repo_dict:
            dbg('repo already deleted!')
            return

        repo = self.repo_dict[repo_name]
        del self.repo_names[self.repo_names.index(repo_name)]
        del self.repo_list[self.repo_list.index(repo)]
        del self.repo_dict[repo_name]


    def find_git_repos_added_removed(self) -> Tuple[List['MgRepoInfo'], List['MgRepoInfo']]:
        '''Return a tuple of:
        - new repos created since the initial scan
        - repos removed since the initial scan

        The content of MultiRepo is adjusted accordingly
        '''
        new_repo_names = []
        self.base_path = pathlib.Path(self.base_dir)
        # Use glob.glob(recursive=True) to follow symlinks whereas Path.glob() doesn't.
        # RND_P_5RNDIT_05-85: ensure base path does not contain magic chars like []*?
        for d in glob(escape(str(self.base_path)) + '/**/.git', recursive=True):
            repo = pathlib.Path(d).parent
            if is_git_repo(repo):
                repo_name = str(repo.relative_to(self.base_path))
                new_repo_names.append(repo_name)

        added_repo_names = set(new_repo_names) - set(self.repo_names)
        rm_repo_names = set(self.repo_names) - set(new_repo_names)
        added_repo = []
        for repo_name in added_repo_names:
            repo_path = str((self.base_path / repo_name).resolve())
            repo_info = MgRepoInfo(repo_name, repo_path, repo_name)
            added_repo.append(repo_info)

        rm_repo = [ self.repo_dict[repo_name] for repo_name in rm_repo_names ]
        return added_repo, rm_repo


    def adjust_git_repos(self, added_repos: List['MgRepoInfo'], rm_repo: List['MgRepoInfo']) -> None:
        '''Adjust the internal list of repos according to the repos added and removed.'''
        for repo in rm_repo:
            del self.repo_names[self.repo_names.index(repo.name)]
            del self.repo_dict[repo.name]
            del self.repo_list[ self.repo_list.index(repo) ]

        for repo in added_repos:
            self.repo_dict[repo.name] = repo
            self.repo_list.append(repo)
            self.repo_names.append(repo.name)
            # don't forget that we want to know when the repo is deleted!
            repo.repo_deleted.connect(self.slotRepoDeleted)

        self.repo_names.sort(key=lambda name: name.lower())
        self.repo_list.sort(key=lambda repo: repo.name.lower())
        dbg('New repo list:\n%s' % self.repo_names)


    def exportCsv(self, fname: str, fieldsRequested: Optional[Dict[str, bool]] = None) -> None:
        '''Export the view on the repo to the CSV'''
        with open(fname, 'w', newline='', errors='replace') as csvf:
            writer = csv.writer(csvf, delimiter=';')
            writer.writerow( ['Path', 'HEAD', 'current branch', 'current tag', 'commit sha1', 'url', 'date'] )

            for repo in sorted(self.repo_list, key=lambda repo: repo.relpath):
                QCoreApplication.processEvents()  # give a chance to asynchronous jobs to complete
                # fetching the information but normally, it was fetched in advance
                repo.ensure_head_and_url_and_commit_date(blocking=True)

                repo_url = anonymise_git_url(repo.url or '')

                if fieldsRequested is None:
                    writer.writerow( [repo.name, repo.head, repo.branch, repo.tag, repo.commit_sha1, repo.commit_date, repo_url] )
                else:
                    content = []
                    content.append(repo.name if fieldsRequested['path'] else '')
                    content.append(repo.head if fieldsRequested['head'] else '')
                    content.append(repo.branch if fieldsRequested['branch'] else '')
                    content.append(repo.tag if fieldsRequested['tag'] else '')
                    content.append((repo.commit_sha1 or '') if fieldsRequested['commit_sha1'] else '')
                    content.append((repo_url or '') if fieldsRequested['url'] else '')
                    content.append((repo.commit_date or '') if fieldsRequested['commit_date'] else '')
                    writer.writerow( content )


class MgRepoInfo(QObject):
    '''Class managing the access to a repository.

    When the class is created, it does not fetch any information.

    Use:
    - fill_repo_info() to fill the base information about a repository
    - fill_repo_url() to also fill the url part
    - fill_last_commit() to fill the last commit part.
    '''

    # Internal conventions:
    # last_commit: empty when not filled, not empty when filled => always a string

    name: str                   # name of the repo == relative path to the base directory
    relpath: str                # the relative path of this repo to the base dir, usually same as name
    fullpath: str               # the full path to the repository, used for running git commands
    url: Optional[str]          # None when not filled yet, string (possibly empty) when filled
    status: str                 # emtpy string when not filled, string when filled. Description of the modified files
    tag: str                    # current tag we are on, if any. Empty string when not pointing on a tag
    branch: str                 # current branch we are on, if any. Emtpy string when not on a branch, "<empty repo>" is also a valid value
    head: str                   # description of what head points: "branch XXX", "tag XXX", "commit XXX", "<empty repo>"
    last_commit: str            # message of the last commit
    commit_date: Optional[str]  # date of the last commit
    commit_sha1: Optional[str]  # sha1 of the last commit, None if not set
    diff: Optional[str]         # diff of the last commit if any
    diff_summary: Optional[str] # list of modified files in the diff
    remote_branch: str          # remote-branch of any, or empty string
    remote_synchro: str         # informative message about sync with remote branch:
                                    # "xx to push, yy to pull"
                                    # "remote branch gone"
                                    # "NA for local branch"
                                    # "up-to-date"
    branches_local: List[str]   # list of all local branches on this repo
    branches_remote: List[str]  # list of all remote branches on this repo
    branches_filled: bool       # True when the attributes branches_* have been filled
    tags: Optional[str]         # all the tags pointing at this commit. None when not filled, comma separated list of tags
    all_tags: List[str]   # all tags existing on this repo
    all_tags_filled: bool           # set when all tags of the repo
    files_sha1: List[Tuple[str, str]]  # List of (files, sha1)
    files_sha1_filled: bool           # set when files sha1 of the repo is filled
    is_deleted: bool                # set to True when emitting the signal repo_deleted

    tag_or_commit: Optional[str]    # internal field, used in log -1
    force_blocking_git: bool        # internal field, used in ensure_all_filled()

    # signals to emit
    repo_update_in_progress = Signal(str)
    repo_info_available = Signal(str)
    repo_deleted = Signal(str)


    def __repr__(self) -> str:
        s = 'MgRepoInfo< %s >' % self.name
        return s


    def __init__(self, name: str, fullpath: str, relpath: str = '') -> None:
        super().__init__()

        self.name = name
        self.relpath = relpath
        self.force_blocking_git = False

        self.cb_repo_info_available: Optional[Callable[[str], Any]] = None

        # full path to our repo
        self.fullpath = fullpath

        self._clear_all()

    def _clear_all(self, clearUrl: bool = True) -> None:
        dbg(f'clear_all(clearUrl={clearUrl}) - {self.name}')
        self._clear_basic_info()
        if clearUrl:
            self.url = None
        self.last_commit = ''
        self.diff = None
        self.diff_summary = None
        self.commit_sha1 = None
        self.tag_or_commit = None
        self.commit_date = None
        self.branches_filled = False
        self.branches_local = []
        self.branches_remote = []
        self.is_deleted = False


    def abortBecauseRepoDeleted(self) -> bool:
        '''Called to check if repo has been deleted.
        Emits the appropriate signal and return True if repo was deleted.
        This is to be called each time git returns an error code'''
        if not os.path.exists(self.fullpath)  \
            or not os.path.exists(os.path.join(self.fullpath, '.git')):
            self.is_deleted = True
            self.repo_deleted.emit(self.relpath)
            return True

        return False


    def _clear_basic_info(self) -> None:
        '''Clear the basic information on a repo, displayed in the main window: head, branch, tag, status, remote_branch, tags'''
        dbg('clear_basic_info() - %s' % self.name)
        self.branch = ''
        self.tag = ''
        self.head = ''
        self.remote_branch = ''
        self.status = ''
        self.remote_synchro = ''
        self.tags = None
        self.all_tags = []
        self.all_tags_filled = False
        self.files_sha1 = []
        self.files_sha1_filled = False


    def deepRefresh(self) -> 'MgRepoInfo':
        '''Reread all relevant information from git repositories, erasing remote url '''
        dbg('deepRefresh() - %s' % self.name)
        return self._refresh(True)


    def refresh(self) -> 'MgRepoInfo':
        '''Reread all relevant information from git repositories, keeping remote url'''
        dbg('refresh() - %s' % self.name)
        return self._refresh(False)


    def _refresh(self, clearUrl: bool) -> 'MgRepoInfo':
        '''Reread all relevant information from git repositories, and keep or clear url depending on parameter'''
        dbg(f'_refresh(clearUrl={clearUrl}) - %s' % self.name)
        self._clear_all(clearUrl)
        self.fill_repo_info()
        return self


    def nice_status(self) -> str:
        '''Nicer status line, longer to display'''
        s = self.status
        return s


    def repo_info_is_available(self) -> None:
        '''Called when basic information has been filled (result of calling fill_repo_info()).

        Actions:
        * calls the callback self.cb_repo_info_available if set, and reset it to None
        * emit the signal repo_info_available
        '''
        if self.cb_repo_info_available is not None:
            # set self.cb_repo_info_available to None first, to avoid recursive calls
            cb_repo_info_available = self.cb_repo_info_available
            self.cb_repo_info_available = None
            cb_repo_info_available(self.name)

        self.repo_info_available.emit(self.name)


    def ensure_all_filled(self) -> 'MgRepoInfo':
        '''Ensure that all information of the repo, including URL is filled.

        To be called when displaying properties for example
        '''
        dbg('ensure_all_filled() - %s' % self.name)

        old_force_blocking_git = self.force_blocking_git
        try:
            # force the calls to blocking to make sure information is available after this call
            # opening properties is still not asynchronous
            self.force_blocking_git = True

            if self.status == '':
                # not filled yet
                self.fill_repo_info()

            self.ensure_url()
            self.ensure_last_commit()
            self.ensure_tags()
            self.ensure_diff_summary()
            self.ensure_diff()
            self.ensure_commit_date()
        finally:
            self.force_blocking_git = old_force_blocking_git
        return self


    def ensure_head_and_url_and_commit_date(self, blocking: bool = False) -> None:
        '''Ensure that the fields 'head' and 'url' and 'commit_date' are filled.
        If blocking is True, the call is blocking. Else, an asynchronous call is made'''
        old_force_blocking_git = self.force_blocking_git
        try:
            # force the calls to blocking to make sure information is available after this call
            # opening properties is still not asynchronous
            self.force_blocking_git = blocking

            if self.head == '':
                self.fill_repo_info()
            self.ensure_url()
            self.ensure_commit_date()
        finally:
            self.force_blocking_git = old_force_blocking_git


    def ensure_head_and_url(self, blocking: bool = False, cb_info_and_url_avail: Optional[Callable[[str], Any]] = None) -> None:
        '''Ensure that the fields 'head' and 'url' are filled.
        If blocking is True, the call is blocking. Else, an asynchronous call is made'''
        old_force_blocking_git = self.force_blocking_git
        try:
            # force the calls to blocking to make sure information is available after this call
            # opening properties is still not asynchronous
            self.force_blocking_git = blocking

            def local_cb_url(_url: str) -> None:
                if cb_info_and_url_avail is not None:
                    cb_info_and_url_avail(self.name)

            def local_cb_fill_repo_info(_repo_name: str) -> None:
                # called when repository information is available
                self.ensure_url(local_cb_url)

            # basic information is missing
            if self.head == '':
                self.fill_repo_info(local_cb_fill_repo_info)
                return

            self.ensure_url(local_cb_url)

        finally:
            self.force_blocking_git = old_force_blocking_git


    def ensure_url(self, cb_url: Optional[Callable[[str], Any]] = None) -> None:
        '''Ensure that url field is correctly filled. If provided callback is called synchronously or asynchronously
        with the URL'''
        if self.url is not None:
            if cb_url:
                cb_url(self.url)
            return

        self.fill_repo_url(cb_url)


    def ensure_last_commit(self, cb_last_commit: Optional[Callable[[str, str], Any]] = None) -> None:
        '''Ensure that the last_commit field gets filled

        Calls cb_last_commit() when the last_commit information is available. This
        is either immediate or pending the git command execution.

        The call to cb_last_commit is done with: cb_last_commit(<repo_name>, <last_commit_content>)
        '''
        dbg('ensure_last_commit() - %s' % self.name)
        if self.last_commit:
            if cb_last_commit:
                cb_last_commit(self.name, self.last_commit)
            return

        self.fill_last_commit(cb_last_commit)


    def fill_last_commit(self, cb_last_commit: Optional[Callable[[str, str], Any]] = None) -> None:
        '''Force the filling of the fields:
         - last_commit
         - commit_date (side-effect)
         - commit_sha1 (side-effect)
         '''

        # local function to allow calling the callback
        def local_fill_last_commit_git_log_done(repo_name: str, git_exit_code: int, git_output: str) -> None:
            self.cb_fill_repo_info_log_done(repo_name, git_exit_code, git_output)
            if cb_last_commit:
                cb_last_commit(repo_name, self.last_commit)

        # errors possible for empty repository
        self.git_exec_async_here(['log', '-1'], local_fill_last_commit_git_log_done, allow_errors=True)


    def ensure_diff(self, cb_fill_diff: Optional[Callable[[str, str], Any]] = None) -> None:
        '''Ensure that diff information is filled'''
        dbg('ensure_diff() - %s' % self.name)
        if self.diff is not None:
            if cb_fill_diff:
                cb_fill_diff(self.name, self.diff)
            return

        def local_cb_fill_diff_done(repo_name: str, exit_code: int, diff_out: str) -> None:
            if exit_code != 0:
                if self.abortBecauseRepoDeleted():
                    return
                self.show_error_message_bad_git_exit_code(exit_code, diff_out)
            self.diff = diff_out
            if cb_fill_diff:
                cb_fill_diff(repo_name, self.diff)

        # errors possible when repo is deleted
        self.git_exec_async_here(['diff', '-u', '--patience', '--stat'], local_cb_fill_diff_done, allow_errors=True)


    def ensure_diff_summary(self, cb_fill_diff_summary: Optional[Callable[[str, str], Any]] = None, blocking: bool = False) -> None:
        '''Ensure that diff summary is filled'''
        dbg('ensure_diff_summary() - %s' % self.name)
        if self.diff_summary is not None:
            if cb_fill_diff_summary:
                cb_fill_diff_summary(self.name, self.diff_summary)
            return

        old_force_blocking_git = self.force_blocking_git
        try:
            # force the calls to blocking to make sure information is available after this call
            # opening properties is still not asynchronous
            self.force_blocking_git = blocking

            def local_cb_git_diff_stat_done(repo_name: str, exit_code: int, diff_out: str) -> None:
                if exit_code != 0:
                    if self.abortBecauseRepoDeleted():
                        return
                    self.show_error_message_bad_git_exit_code(exit_code, diff_out)
                    return

                self.diff_summary = diff_out
                if cb_fill_diff_summary:
                    cb_fill_diff_summary(repo_name, self.diff_summary)

            # errors possible when repo is deleted
            self.git_exec_async_here(['diff', '--stat'], local_cb_git_diff_stat_done, allow_errors=True)
        finally:
            self.force_blocking_git = old_force_blocking_git


    def ensure_commit_date(self) -> None:
        '''Ensure that field commit_date is filled'''
        if self.commit_date is None:
            self.fill_last_commit()   # fill fill self.last_date as a side-effect


    def ensure_tags(self) -> None:
        '''Ensure that fields are filled: tags'''
        dbg('ensure_tags() - %s' % self.name)
        if self.tags is None:
            self.fill_tags()


    def ensure_sha1(self, cb_commit_sha1: Optional[Callable[[str], Any]] = None, blocking: bool = False) -> None:
        '''Ensure that the sha1 information is available. If blocking is True,
        the function will return only after the sha1 is available.'''

        if self.commit_sha1 is not None:
            # we already have it
            if cb_commit_sha1:
                cb_commit_sha1(self.commit_sha1)
            return

        old_force_blocking_git = self.force_blocking_git
        try:
            # force the calls to blocking to make sure information is available after this call
            # opening properties is still not asynchronous
            self.force_blocking_git = blocking

            local_cb_last_commit: Optional[Callable[[str, str], None]]
            if cb_commit_sha1:
                def local_cb_last_commit(_repoName: str, _lastCommit: str) -> None:
                    # see https://github.com/python/mypy/issues/10993 for why type: ignore is necessary
                    cb_commit_sha1(self.commit_sha1 or '')  # type: ignore
            else:
                local_cb_last_commit = None

            # request sha1 with log -1
            self.fill_last_commit(local_cb_last_commit)

        finally:
            self.force_blocking_git = old_force_blocking_git


    def fill_tags(self) -> None:
        '''Fill the following fields: tags (blocking)'''
        dbg('fill_tags() - %s' % self.name)
        if self.last_commit == MSG_NO_COMMIT:
            # no commits means no tags...
            self.tags = ''
            return
        self.tags = ' '.join(self.git_exec_blocking_here('tag', '--points-at', 'HEAD').strip().split('\n'))


    def fill_repo_url(self, cb_url: Optional[Callable[[str], Any]] = None) -> None:
        '''Fill the URL part of the repo: field url and calls the callback if any when done'''
        dbg('fill_repo_url() - %s' % self.name)

        if cb_url:
            def local_cb_fill_git_remote_done(repo_name: str, git_exit_code: int, remote_out: str) -> None:
                self.cb_fill_git_remote_done(repo_name, git_exit_code, remote_out)
                # necessary to make mypy happy, see https://github.com/python/mypy/issues/10993
                cb_url(self.url or '')  # type: ignore
        else:
            local_cb_fill_git_remote_done = self.cb_fill_git_remote_done

        # errors possible when repo is deleted
        self.git_exec_async_here(['remote', '--verbose'], local_cb_fill_git_remote_done, allow_errors=True)


    def cb_fill_git_remote_done(self, repo_name: str, git_exit_code: int, remote_out: str) -> None:
        self.url = ''
        '''Output looks like:       
        origin  https://toto@titi.org/toto/multigit.git (fetch)
        origin  https://toto@titi.org/toto/multigit.git (push)

        or nothing if no remote has been set
        or more lines if there are multiple remotes
        '''
        if git_exit_code != 0:
            if not self.abortBecauseRepoDeleted():
                self.show_error_message_bad_git_exit_code(git_exit_code, remote_out)
            return

        # We give priority to origin and (fetch)
        remote_out_lines = [ l.split(maxsplit=1) for l in remote_out.split('\n') if len(l) ]
        if len(remote_out_lines) == 0:
            return
        origin_url = [ url for (name, url) in remote_out_lines if 'origin' == name]
        if len(origin_url) == 0:
            # no origin, uncommon!
            # but there are other lines to interpret, try them
            origin_url = [url for (name, url) in remote_out_lines]
        url_method = [ l.rsplit(' ', maxsplit=1) for l in origin_url ]
        fetch_url = [ url for url,method in url_method if method == '(fetch)' ]
        assert len(fetch_url) > 0
        self.url = fetch_url[0]


    def fill_repo_info(self, cb_repo_info_available: Optional[Callable[[str], Any]] = None) -> None:
        '''Fill the following fields:
        - status
        - head
        - branch
        - tag
        - remote_synchro

        May also fill:
        - diff
        - last_commit
        - commit_date
        - commit_sha1
        - tags
        '''
        dbg('fill_repo_info() - %s' % self.name)
        self._clear_basic_info()
        self.cb_repo_info_available = cb_repo_info_available
        self.repo_update_in_progress.emit(self.name)
        # errors possible when repo is deleted
        self.git_exec_async_here(['status', '--porcelain', '--branch'], self.cb_fill_repo_info_status_done,
                                 allow_errors=True)


    re_status_mod_files = re.compile('([MDRCUA ][MDRCUA]|[MDRCUA][MDRCUA ]) (.+)')


    def cb_fill_repo_info_status_done(self, _repo_name: str, git_exit_code: int, status_out: str) -> None:
        '''Called after git status'''
        dbg('fill_repo_info_status_done() - %s, exit_code=%d' % (self.name, git_exit_code))
        if git_exit_code != 0:
            if not self.abortBecauseRepoDeleted():
                self.show_error_message_bad_git_exit_code(git_exit_code, status_out)
            return

        '''git status output:
        "## No commits yet on master
            -> no commit yet
        "## Initial commit on master" 
            -> ???
        "## <branch name>" 
            -> on a branch, no remote
        "## <branch name>...<remote branch name>" 
            -> on a branch, with remote, up-to-date
        "## <branch name>...<remote branch name> [behind N]" 
            -> on a branch, with remote, not uptodate
        "## <branch name>...<remote branch name> [ahead N]" 
            -> on a branch, with remote, not uptodate
        "## HEAD (no branch)" 
            -> detached head

        "?? filename"
            -> untracked files

        " M <fname with or without quotes>"
        " D <fname>"
        " R <fname>"
        " C <fname>"
        " U <fname>"
            -> modified file name
        " A <fname> -> <fname>"
            -> renamed file name
        '''
        status_out_lines = status_out.split('\n')
        mod_files = [ self.re_status_mod_files.match(l).group(2)  # type: ignore # mypy does not understand theat the None value is excluded from the list
                        for l in status_out_lines 
                        if self.re_status_mod_files.match(l) 
        ]
        
        if len(mod_files) == 1:
            self.status = '{} modified file'.format(len(mod_files))
        elif len(mod_files) > 1:
            self.status = '{} modified files'.format(len(mod_files))
        else:
            self.status = 'OK'
            self.diff = ''

        if '## HEAD (no branch)' in status_out:
            # HEAD is detached
            self.git_exec_async_here(['branch'], self.cb_fill_repo_info_branch_done)
            return

        # HEAD is not detached, we are on a branch or on an empty repo

        if '## No commits yet on' in status_out or \
            '## Initial commit on' in status_out:
            # repo is only initialized, no commit, no branch yet:
            #   output: "## No commits yet on master"
            # or repo is cloned from an empty repo:
            #   output: "## No commits yet on master...origin/master [gone]"
            self.branch = MSG_EMPTY_REPO
            self.head = MSG_EMPTY_REPO
            self.tags = ''
            self.commit_sha1 = ''
            self.commit_date = ''
            self.last_commit = MSG_NO_COMMIT
            self.remote_synchro = ''
            self.repo_info_is_available()
            return

        # HEAD is not detached, we are on a branch, we can fetch its name from status
        # we can also fetch the remote name, and the status vs remote branch (ahead, behind)
        status_out_header = [l for l in status_out_lines if l.startswith('##') ][0]
        if '...' in status_out_header:
            # branch + remote-tracking branch
            self.branch, remote_branch_and_remote_status = status_out_header[3:].split('...')
            if '[' in remote_branch_and_remote_status:
                # ahead / behind info is present
                self.remote_branch, remote_status = remote_branch_and_remote_status.split(' [')
                remote_status = remote_status.strip(']')
                # remote_status is either: "ahead 33", "behind 2", "ahead 2, behind 3"
                nb_ahead, nb_behind = match_ahead_behind(remote_status)
                if nb_ahead > 0 and nb_behind > 0:
                    self.remote_synchro = MSG_REMOTE_TOPUSH_TOPULL % (nb_ahead, nb_behind)
                elif nb_ahead > 0:
                    self.remote_synchro = MSG_REMOTE_TOPUSH % nb_ahead
                elif nb_behind > 0:
                    self.remote_synchro = MSG_REMOTE_TOPULL % nb_behind
                elif remote_status == 'gone':
                    # possible cases:
                    # - cloning an empty repo
                    #     output: '## No commits yet on master...origin/master [gone]
                    #     => this is already handled at the beginninig of this function, when looking for
                    #        the string "No commits yet on master". So no need to handle it here
                    # - cloning from a branch, then the remote branch is deleted
                    #     output:  ## master...origin/master [gone]

                    # happens when the tracking branch is gone, or when cloning an empty repo
                    # and then comitting to it
                    self.remote_synchro = MSG_REMOTE_BRANCH_GONE
                else:
                    assert False, "neither ahead nor behind are positive: ahead = %d, behind = %d" % (nb_ahead, nb_behind)
            else:
                self.remote_branch = remote_branch_and_remote_status
                self.remote_synchro = MSG_REMOTE_SYNCHRO_OK

            self.head = 'branch %s' % self.branch
        else:
            self.branch = status_out_header[3:]
            self.head = 'branch %s' % self.branch
            self.remote_synchro = MSG_LOCAL_BRANCH

        self.repo_info_is_available()
        return


    def cb_fill_repo_info_branch_done(self, _repo_name: str, git_exit_code: int, branch_out: str) -> None:
        '''Called after "git branch" to fetch the status of the local and remote branch more precisely'''
        dbg('fill_repo_info_branch_done() - %s' % self.name)
        if git_exit_code != 0:
            # error already notified to user by previous callback
            self.abortBecauseRepoDeleted()
            return

        '''git branch output:
        * (no branch)        
            -> no information provided on where the head is detached
        * (HEAD detached at XXX)
            -> tag-name or commit sha, as used directly by checkout
        * (HEAD detached from XXX)
            -> detached head, then some commits occured
        * master
            -> on branch master
          other_branch
            -> other branch also exists
        '''
        branch_out_lines = branch_out.split('\n')

        # if we need to call "git log -1", we need a local function callback to emit the signal repo_info_available
        def local_fill_repo_info_log_done(repo_name: str, git_exit_code: int, git_log_out: str) -> None:
            self.cb_fill_repo_info_log_done(repo_name, git_exit_code, git_log_out)
            self.repo_info_is_available()

        if '* (HEAD detached at' in branch_out:
            # branch output: * (HEAD detached at XXX) => tag-name or commit, used directly by checkout
            tag_line = [l for l in branch_out_lines if 'HEAD detached' in l]
            self.tag_or_commit = tag_line[0][20:-1]
            if is_not_sha1(self.tag_or_commit):
                # this is a tag
                self.tag = self.tag_or_commit
                self.head = 'tag %s' % self.tag
            else:
                # we can not tell if we are on a commit SHA1 or a tag
                # check using the commit sha1
                self.git_exec_async_here(['log', '-1'], local_fill_repo_info_log_done, allow_errors=True)
                return

            self.repo_info_is_available()
            return

        if '* (HEAD detached from' in branch_out or '(no branch)' in branch_out:
            # branch output: * (HEAD detached from XXX) => checkout + commit has occured
            # branch output: * (no branch) => no information provided on where we are detached
            # use git-log to fetch the commit
            self.git_exec_async_here(['log', '-1'], local_fill_repo_info_log_done, allow_errors=True)
            return

        # we know there is one branch there
        br_line = [l for l in branch_out.split('\n') if '*' in l]
        self.branch = br_line[0][2:]
        self.head = 'branch %s' % self.branch
        self.repo_info_is_available()
        return


    def cb_fill_repo_info_log_done(self, _repo_name: str, git_exit_code: int, git_log_out: str) -> None:
        '''Called after "git log -1" to parse the result'''
        dbg('fill_repo_info_log_done() - %s' % self.name)
        # git returns an error on empty repo, don't bother. Else log -1 should always work
        if git_exit_code != 0:
            if 'does not have any commits yet' in git_log_out:
                self.last_commit = MSG_NO_COMMIT
                self.commit_date = ''
                self.commit_sha1 = ''
            else:
                if self.abortBecauseRepoDeleted():
                    return

                nice_git_cmd = '> "git" "-C" "%s" "log" "-1"' % self.fullpath
                # noinspection PyTypeChecker
                msg = nice_git_cmd + '\n' + git_log_out

                self.show_error_message_bad_git_exit_code(git_exit_code, msg)
            return

        self.last_commit = git_log_out
        log_out_lines = git_log_out.split('\n')

        for l in log_out_lines:
            if l.startswith('Date:'):
                self.commit_date = l[6:].strip()
                break
        else:
            warn('Could not locate the Date line inside the log -1 response')

        self.commit_sha1 = log_out_lines[0].split(' ')[1].strip()
        if self.tag_or_commit:
            # we had the message "detached at XXX" and we try to figure out
            # if XXX is a commit or a tag
            if self.tag_or_commit in self.commit_sha1:
                # this was a commit
                self.head = 'commit %s' % self.tag_or_commit[:SHORT_SHA1_NB_DIGITS]
            else:
                # this was a tag
                self.head = 'tag %s' % self.tag_or_commit
                self.tag = self.tag_or_commit
            self.tag_or_commit = None

        elif self.head == '':
            # head is not set yet, we were on a detached head with no information
            self.head = 'commit %s' % self.commit_sha1[:SHORT_SHA1_NB_DIGITS]
        else:
            # we are just parsing the output of log -1, nothing special to do here
            pass


    def ensure_branches_filled(self, cb_branches_filled_done: Optional[Callable[[str], None]] = None, blocking: bool = False) -> None:
        '''Ensure that fields branch_local and branch_remote are filled.

        If provided, the callback function is called with the name of the repository'''
        dbg('ensure_branches_filled() - %s' % self.name)
        if self.branches_filled:
            if cb_branches_filled_done:
                cb_branches_filled_done(self.name)
            return

        old_force_blocking_git = self.force_blocking_git
        try:
            # force the calls to blocking to make sure information is available after this call
            # opening properties is still not asynchronous
            self.force_blocking_git = blocking
            self.fill_branches(cb_branches_filled_done)
        finally:
            self.force_blocking_git = old_force_blocking_git



    def ensure_all_tags_filled(self, cb_all_tags_filled_done: Optional[Callable[[str], None]] = None, blocking: bool = False) -> None:
        '''Ensure that fields branch_local and branch_remote are filled.

        If provided, the callback function is called with the name of the repository'''
        dbg('ensure_all_tags_filled() - %s' % self.name)
        if self.all_tags_filled:
            if cb_all_tags_filled_done:
                cb_all_tags_filled_done(self.name)
            return

        old_force_blocking_git = self.force_blocking_git
        try:
            # force the calls to blocking to make sure information is available after this call
            # opening properties is still not asynchronous
            self.force_blocking_git = blocking
            self.fill_all_tags(cb_all_tags_filled_done)

        finally:
            self.force_blocking_git = old_force_blocking_git




    def fill_branches(self, cb_branches_filled_done: Optional[Callable[[str], None]] = None) -> None:
        '''Fills fields branch_local and branch_remote are filled.

        If provided, the callback function is called with the name of the repository'''

        def local_cb_fill_branches_done(repo_name: str, git_exit_code: int, git_output: str) -> None:
            self.cb_fill_branches_done(repo_name, git_exit_code, git_output)
            if cb_branches_filled_done:
                cb_branches_filled_done(repo_name)

        # errors possible when repo is deleted
        self.git_exec_async_here(['branch', '--all'], local_cb_fill_branches_done, allow_errors=True)


    def cb_fill_branches_done(self, _repo_name: str, git_exit_code: int, git_output: str) -> None:
        '''Called when [git branch --all] completes'''

        '''Example of output:
  dev
  feat/GF_feature_finish
* feat/improv-misc
  master
  remotes/origin/HEAD -> origin/fix/toto
  remotes/origin/b2
  remotes/origin/dev
  remotes/origin/feat/Clone_from_Project_Configuration_file
  remotes/origin/feat/GF_feature_finish
  
 
        Other example: 
* (HEAD detached at tag1)
  master
        '''

        if git_exit_code != 0:
            if not self.abortBecauseRepoDeleted():
                self.show_error_message_bad_git_exit_code(git_exit_code, git_output)
            return

        self.branches_local = []
        self.branches_remote = []
        for v in git_output.split('\n'):
            v = v.strip()
            if not len(v):
                continue
            if v.startswith('* ('):
                # this is not a branch, just an informative message
                continue
            if v.startswith('* '):
                v = v[2:]
            if ' -> ' in v:
                v = v.split(' -> ')[0].strip()

            if not v.startswith('remotes/'):
                self.branches_local.append(v)
            elif v != 'remotes/origin/HEAD':
                # we skip the HEAD branch for remotes, it is not useful for git usage
                self.branches_remote.append(v[8:])

        self.branches_filled = True


    def fill_all_tags(self, cb_all_tags_filled_done: Optional[Callable[[str], None]] = None) -> None:
        '''Fill the following fields: all_tags'''
        dbg('fill_all_tags() - %s' % self.name)
        if self.last_commit == MSG_NO_COMMIT:
            # no commits means no tags...
            self.all_tags = []
            if cb_all_tags_filled_done:
                cb_all_tags_filled_done(self.name)
            return

        def local_cb_fill_all_tags_done(repo_name: str, git_exit_code: int, git_output: str) -> None:
            self.cb_fill_all_tags_done(repo_name, git_exit_code, git_output)
            if cb_all_tags_filled_done:
                cb_all_tags_filled_done(repo_name)

        self.git_exec_async_here(['tag', '--list', '--sort', 'creatordate'], local_cb_fill_all_tags_done, allow_errors=True)


    def cb_fill_all_tags_done(self, _repo_name: str, git_exit_code: int, git_output: str) -> None:
        if git_exit_code != 0:
            if not self.abortBecauseRepoDeleted():
                self.show_error_message_bad_git_exit_code(git_exit_code, git_output)
            return

        self.all_tags = []
        for v in git_output.split('\n'):
            v = v.strip()
            if not len(v):
                continue

            self.all_tags.append(v)

        self.all_tags_filled = True


    def has_commits_to_push(self) -> bool:
        '''Check if remote synchro has commits to push.

        This is used to check for some git operations invalid when there are commits to push'''
        return 'to push' in self.remote_synchro


    def ensure_files_sha1_filled(self, cb_fill_files_sha1_done: Optional[Callable[[str], None]] = None, blocking: bool = False) -> None:
        '''Ensure that fields files_sha1 is filled.

        If provided, the callback function is called with the name of the repository'''
        dbg('ensure_files_sha1_filled() - %s' % self.name)
        if self.files_sha1_filled:
            if cb_fill_files_sha1_done:
                cb_fill_files_sha1_done(self.name)
            return

        old_force_blocking_git = self.force_blocking_git
        try:
            # force the calls to blocking to make sure information is available after this call
            # opening properties is still not asynchronous
            self.force_blocking_git = blocking
            self.fill_files_sha1(cb_fill_files_sha1_done)

        finally:
            self.force_blocking_git = old_force_blocking_git


    def fill_files_sha1(self, cb_fill_files_sha1_done: Optional[Callable[[str], None]] = None) -> None:
        '''Fill the URL part of the repo: field url and calls the callback if any when done'''
        dbg('fill_files_sha1() - %s' % self.name)

        def local_cb_fill_files_sha1_done(repo_name: str, git_exit_code: int, remote_out: str) -> None:
            self.cb_fill_files_sha1_done(repo_name, git_exit_code, remote_out)
            if cb_fill_files_sha1_done:
                cb_fill_files_sha1_done(self.name)

        # errors possible when repo is deleted
        self.git_exec_async_here(['ls-files', '-s'], local_cb_fill_files_sha1_done, allow_errors=True)


    def cb_fill_files_sha1_done(self, _repo_name: str, git_exit_code: int, git_output: str) -> None:
        if git_exit_code != 0:
            if not self.abortBecauseRepoDeleted():
                self.show_error_message_bad_git_exit_code(git_exit_code, git_output)
            return

        self.files_sha1 = []
        for line in git_output.split('\n'):
            line = line.strip('\t \n')
            if not len(line):
                continue

            _0, sha1, _2, fname, *_3 = line.replace('\t', ' ').split(' ')
            self.files_sha1.append((fname, sha1))

        self.files_sha1.sort()
        self.files_sha1_filled = True



    ##############################################################################
    #
    #          Generic interactions with git
    #
    ##############################################################################


    def git_exec_blocking_here(self, *args: str) -> str:
        '''Execute a git command in the context of the current repo.
        Blocks until the command is complete and returns the command output.

        May raise subprocess.CalledProcessError() if git does not exit with 0
        '''
        prog_git = ExecGit.get_executable()
        if prog_git is None or len(prog_git) == 0:
            raise FileNotFoundError('Can not execute git with empty executable!')
        git_cmd = [prog_git, '-C', self.fullpath] + list(args)
        git_exit_code, cmd_out = RunProcess().exec_blocking(git_cmd)
        return cmd_out


    def git_exec_async_here(self, args: Sequence[str], cb_git_done: Optional[Callable[[str, int, str], Any]],
                            allow_errors: bool = False) -> None:
        '''Execute git on the current repo with a callback for when the command is over.

        Note that if self.force_blocking_git is True, the call will be turned into
        a blocking call instead of an async call. The callback is called in both situations.

        if allow_errors is False, a message box is displayed if git returns an exit code different than 0. If you
        have your own handling of git errors, set allow_errors to True.
        '''
        prog_git = ExecGit.get_executable()
        if prog_git is None or len(prog_git) == 0:
            raise FileNotFoundError('Can not execute git with empty executable!')
        git_cmd = [prog_git, '-C', self.fullpath] + list(args)

        cb_process_done = None
        if cb_git_done:
            # adapt the callback by including the repo name
            def cb_process_done(git_exit_code: int, git_output: str) -> None:
                assert cb_git_done  # to help mypy not raise an error
                cb_git_done(self.name, git_exit_code, git_output)

        # our pool process does not handle force blocking, launch directly
        RunProcess().exec_async(git_cmd, cb_process_done, force_blocking=self.force_blocking_git, allow_errors=allow_errors)


    def show_error_message_bad_git_exit_code(self, git_exit_code: int, git_output: str) -> None:
        QMessageBox.warning(None, 'Error when running git',
                            f'Git bad exit code {git_exit_code}.\n\nError message:\n{git_output}')


