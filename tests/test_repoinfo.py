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


from typing import Union, Any
import unittest, tempfile, datetime, collections, pathlib, os, stat, shutil
from logging import warning

import os

from multigit import init_logging
import src.mg_tools
from src.mg_tools import git_exec
from src.mg_const import MSG_EMPTY_REPO, MSG_NO_COMMIT, MSG_LOCAL_BRANCH, MSG_REMOTE_SYNCHRO_OK, SHORT_SHA1_NB_DIGITS
from src.mg_repo_info import MgRepoInfo, MultiRepo

# More tests to write
# * detached head from a remote branch
#   + deleting the remote branch
# * clone remote branch + delete the remote branch

AUTHOR_NAME = 'philou'
AUTHOR_EMAIL = 'phil_tests@github'

os.environ['GIT_AUTHOR_NAME'] = AUTHOR_NAME
os.environ['GIT_AUTHOR_EMAIL'] = AUTHOR_EMAIL

LONG_TESTS = True

init_logging(run_from_tests=True, debug_activated=False) # set to True, True when you want debug on stdout

RepoInfoTuple = collections.namedtuple('RepoInfoTuple',
                   ["name", "head", "branch", "tag", "remote_branch", "status", "fullpath",
                    "last_commit", "remote_synchro", "tags", "branches_local", "branches_remote"],
                       defaults=["", "", "", "", "", "", "", "", "", None, (), ()])

def rmtree_failsafe(p: Union[str, pathlib.Path]) -> None:
    # print('rmtree_failsafe(%s)' % p)
    try:
        dirlist = list(os.scandir(p))
    except PermissionError:
        # nothing we can do with this directory
        return

    local_error = []

    def rmtree_onerror(_function: Any, path: Any, _excinfo: Any) -> None:
        try:
            # deletion errors are usually because a file is readonly
            os.chmod(path, stat.S_IWRITE)
            os.unlink(path)
        except Exception as exc:
            # exception again !
            local_error.append('''On path %s
    %s''' % (str(path), str(exc)))
            warning(local_error[-1])

    shutil.rmtree(p, onerror=rmtree_onerror)

    if len(local_error) > 2:
        local_error = local_error[:2] + ['And more errors...\n']

    return '\n'.join(local_error)


def to_named_tuple(ric: MgRepoInfo) -> RepoInfoTuple:
        return RepoInfoTuple(
            name=ric.name,
            fullpath=ric.fullpath,
            branch=ric.branch,
            head=ric.head,
            tag=ric.tag,
            remote_branch=ric.remote_branch,
            status=ric.status,
            last_commit=ric.last_commit,
            remote_synchro=ric.remote_synchro,
            tags=ric.tags,
            branches_remote=tuple(ric.branches_remote),
            branches_local=tuple(ric.branches_local),
        )


def git_init_repo(repo: str) -> None:
    '''Init the repository and creates commit config'''
    git_exec('init', '-b', 'main', repo)

def git_commit(repo: str, msg: str, allow_errors: bool = False) -> str:
    '''Commit the repo with the message passed in argument and return the SHA1 of the commit.'''
    out = git_exec('-C', repo, 'commit', '-m', msg, allow_errors=allow_errors)
    sha1 = out.split(']')[0].split(' ')[-1]
    return sha1


def add_content(repo: Union[str, pathlib.Path], fname: str, content: str = '') -> str:
    '''create or append to a file and commit it. Return the sha1 of the commit'''
    olddir = os.getcwd()
    os.chdir(repo)
    if not content:
        content = generate_content()
    if not content.endswith('\n'):
        content += '\n'

    with open(fname,'a') as f:
        f.write(content)
    git_exec('add', fname)
    sha1 = git_commit('.', '"extend %s"' % fname)
    os.chdir(olddir)
    return sha1


content_idx = 0
def generate_content():
    '''Return the text "line X" increasing on each call'''
    global content_idx
    content_idx += 1
    return 'line %d\n' % content_idx


#######################################################
#           Tests for RepoInfo
#######################################################

app = None
old_FORCE_ASYNC_TO_BLOCKING_CALLS = False
def setUpModule() -> None:
    '''Make all git calls blocking during the duration of the test'''
    global old_FORCE_ASYNC_TO_BLOCKING_CALLS
    old_FORCE_ASYNC_TO_BLOCKING_CALLS = src.mg_tools.FORCE_ASYNC_TO_BLOCKING_CALLS
    src.mg_tools.FORCE_ASYNC_TO_BLOCKING_CALLS = True


def tearDownModule() -> None:
    '''Restore previous state after all tests execution'''
    src.mg_tools.FORCE_ASYNC_TO_BLOCKING_CALLS = old_FORCE_ASYNC_TO_BLOCKING_CALLS


# noinspection PyArgumentList,PyBroadException
class TestRepoInfo(unittest.TestCase):
    '''This test creates git repositories in TEMP/test_multigit/YYYYMMDD_HHMMSS

    The tests are serialized. We tried to make them independant but it was too messy
    and too long to recreate independant states.

    A repository is put into various states (empty, one commit, modified, ...) and
    a test function is run for each of these tests:
    * run_test_on_empty_git()
    * run_test_on_main()
    * run_test_on_main_modified_files()
    * run_test_on_main_with_one_tag()
    * run_test_on_tag()
    * run_test_on_tag2_with_tag3(self.dir1, 'tag2', 'tag3')
    * run_test_on_commit()
    * run_test_on_tag_like_sha1()
    * run_test_on_other_branch()
    * run_test_on_other_branch_merged_main()


    if LONG_TEST is set to True, an additional set of longer tests is run, involving clones:
    * run_clone_test_on_empty_git(self.dir1, self.dir3)
    * run_clone_test_on_origin_main_2_commits()
    * run_clone_test_on_origin_main_more_commits(self.dir1, self.dir3)

    '''

    @classmethod
    def setUpClass(cls: 'TestRepoInfo') -> None:
        cls.tempdir_setUp()

    @classmethod
    def tearDownClass(cls: 'TestRepoInfo') -> None:
        cls.tempdir_tearDown()

    @classmethod
    def tempdir_setUp(cls: 'TestRepoInfo') -> None:
        cls.tempdir = pathlib.Path(tempfile.gettempdir()) / 'test_multigit'
        cls.tempdir.mkdir(exist_ok=True)
        cls.gitdir = cls.tempdir / datetime.datetime.now().isoformat().replace(':', '_').split('.')[0]
        cls.gitdir.mkdir()
        print('Creating test git directory: %s' % cls.gitdir)


    @classmethod
    def tempdir_tearDown(cls: 'TestRepoInfo') -> None:
        if not os.path.exists(cls.tempdir):
            return
        # try to remove our own stuff
        rmtree_failsafe(cls.gitdir)

        # try to remove leftofers from previous tests as well
        rmtree_failsafe(cls.tempdir)

    def test_repo_info_fill_branch(self) -> None:
        ri = MgRepoInfo('toto', '.', '.')
        self.assertEqual(ri.branches_remote, [])
        self.assertEqual(ri.branches_local, [])
        self.assertEqual(ri.branches_filled, False)

        ri.cb_fill_branches_done('toto', 0, '''
  dev
  feat/f-1
* feat/f-2
  main
  remotes/origin/HEAD -> origin/fix/toto
  remotes/origin/b2
  remotes/origin/dev
  remotes/origin/feat/Clone_1
  remotes/origin/feat/GF_2
        
''')
        self.assertEqual(ri.branches_local, ['dev', 'feat/f-1', 'feat/f-2', 'main'])
        self.assertEqual(ri.branches_remote, [
            'origin/b2',
            'origin/dev',
            'origin/feat/Clone_1',
            'origin/feat/GF_2',
            ])
        self.assertEqual(ri.branches_filled, True)

        # when head is detached, we have an extra line of information
        ri = MgRepoInfo('toto', '.', '.')
        ri.cb_fill_branches_done('toto', 0, ''' * (HEAD detached at tag1)
  main
''')
        self.assertEqual(ri.branches_local, ['main'])
        self.assertEqual(ri.branches_remote, [])



    def test_repo_info(self) -> None:
        self.dir1 = pathlib.Path(self.gitdir) / 'dir1'
        self.dir1.mkdir()
        os.chdir(self.dir1)
        git_init_repo('.')

        self.run_test_on_empty_git(self.dir1)

        if LONG_TESTS:
            self.dir3 = pathlib.Path(self.gitdir) / 'dir3'
            self.dir3.mkdir()
            self.run_clone_test_on_empty_git(self.dir1, self.dir3)

        # add one file, one commit, no tag
        sha1 = add_content(self.dir1, 'file1')
        self.run_test_on_main(self.dir1, 'file1', sha1)

        # add 2nd commit
        # checkout is still on main
        sha1 = add_content(self.dir1, 'file2')
        self.run_test_on_main(self.dir1, 'file2', sha1)

        if LONG_TESTS:
            self.run_clone_test_on_origin_main_2_commits(self.dir1, self.dir3)

        self.run_test_on_main_modified_files(self.dir1, sha1)

        # tag the file
        git_exec('tag', 'tag1')
        self.run_test_on_main_with_one_tag(self.dir1, 'tag1')

        # checkout tag1
        git_exec('checkout', 'tag1')
        self.run_test_on_tag(self.dir1, 'tag1')

        if LONG_TESTS:
            # checkout main, add 3rd commit, checkout tag1
            git_exec('checkout', 'main')
            _sha1 = add_content(self.dir1, 'tata')

            self.run_clone_test_on_origin_main_more_commits(self.dir1, self.dir3)

            # clone a directory while it is pointing to a tag
            git_exec('checkout', 'tag1')
            ric = MgRepoInfo(str(self.dir1), '')
            ric.fill_last_commit()
            tag_sha1 = ric.commit_sha1

            self.dir4 = pathlib.Path(self.gitdir) / 'dir4'
            self.dir4.mkdir()
            self.run_clone_test_on_tag(self.dir1, 'tag1', self.dir4, tag_sha1)

        # checkout main, tag the file twice, checkout one tag
        git_exec('checkout', 'main')
        _sha1 = add_content(self.dir1, 'tata')
        git_exec('tag', 'tag2')
        git_exec('tag', 'tag3')
        git_exec('checkout', 'tag2')
        self.run_test_on_tag2_with_tag3(self.dir1, 'tag2', 'tag3')

        # checkout main, add 4th commit, add 5th commit
        # checkout 4th commit
        git_exec('checkout', 'main')
        sha1_4 = add_content(self.dir1, 'titi')
        sha1_5 = add_content(self.dir1, 'titi')
        git_exec('checkout', sha1_5)
        self.run_test_on_commit(self.dir1, sha1_5)

        if LONG_TESTS:
            # add tag looking like a sha1
            tag_like_sha1 = '112233AABB'
            git_exec('tag', tag_like_sha1)
            git_exec('checkout', sha1_4) # we change the current commit to fetch the information about tags
            git_exec('checkout', tag_like_sha1)
            self.run_test_on_tag_like_sha1(self.dir1, tag_like_sha1)

        # create branch branch1, add 2 commits
        git_exec('checkout', '-b', 'branch1')
        add_content(self.dir1, 'toto')
        sha1 = add_content(self.dir1, 'toto')
        self.run_test_on_other_branch(self.dir1, 'branch1', sha1)

        # merge main into branch1
        git_exec('merge', 'main')
        self.run_test_on_other_branch_merged_main(self.dir1, 'branch1')

        # create branch2, fill it with content, merge it to main and delete it
        git_exec('checkout', '-b', 'branch2')
        add_content(self.dir1, 'toto')
        git_exec('checkout', 'main')
        git_exec('merge', 'branch2')
        git_exec('branch', '-d', 'branch2')
        self.run_test_on_main_after_branch2_deleted(self.dir1, 'main')


    def run_test_on_empty_git(self, dir1):
        print('    - run_test_on_empty_git')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())

        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
             RepoInfoTuple(name=n,
                           head=MSG_EMPTY_REPO,
                           branch=MSG_EMPTY_REPO,
                           fullpath=fp,
                           status='OK',
                           last_commit=MSG_NO_COMMIT,
                           tags='',
                       ))
        self.assertEqual(ric.commit_sha1, '')

        # check ensure_last_commit() effect
        self.assertEqual(ric.last_commit, MSG_NO_COMMIT)
        ric.ensure_last_commit()
        self.assertEqual(ric.last_commit, MSG_NO_COMMIT)

        self.assertEqual(ric.branches_filled, False)
        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, [])


        # check ensure_all_filled() does not fail
        ric = MgRepoInfo(n, fp)
        ric.ensure_all_filled()

        # check how modified files are reported
        with open(p/'tutu','a') as f:
            f.write('blurb' + '\n')

        self.assertEqual(to_named_tuple(ric.refresh()),
             RepoInfoTuple(name=n,
                           head=MSG_EMPTY_REPO,
                           branch=MSG_EMPTY_REPO,
                           fullpath=fp,
                           status='OK',
                           last_commit=MSG_NO_COMMIT,
                           tags=''
                        ))
        self.assertEqual(ric.commit_sha1, '')

        git_exec('add', 'tutu', gitdir=p)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head=MSG_EMPTY_REPO,
                                       branch=MSG_EMPTY_REPO,
                                       fullpath=fp,
                                       status='1 modified file',
                                       last_commit=MSG_NO_COMMIT,
                                       tags=''
                                       ))
        self.assertEqual(ric.commit_sha1, '')

        git_exec('rm', '-f', 'tutu', gitdir=p)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head=MSG_EMPTY_REPO,
                                       branch=MSG_EMPTY_REPO,
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=MSG_NO_COMMIT,
                                       tags=''
                                       ))
        self.assertEqual(ric.commit_sha1, '')
        self.assertEqual((p/'tutu').exists(), False)
        return


    def run_test_on_main(self, dir1, fname, commit_sha1: str):
        print('    - run_test_on_main')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())

        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
             RepoInfoTuple(name=n,
                           head='branch main',
                           branch='main',
                           remote_synchro = MSG_LOCAL_BRANCH,
                           fullpath=fp,
                           status='OK',
                           last_commit='',
                           tags=None,
                    ))
        self.assertEqual(ric.commit_sha1, None)
        ric.ensure_last_commit()
        self.assertTrue(ric.last_commit.startswith('commit %s' % commit_sha1))
        self.assertTrue(('extend %s' % fname) in ric.last_commit)
        self.assertTrue('Author:' in ric.last_commit)
        self.assertTrue('Date:' in ric.last_commit)

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, ['main'])


    def run_test_on_main_modified_files(self, dir1, _sha1: str):
        print('    - run_test_on_main_modified_files')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())

        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n, head='branch main', branch='main',
                                       remote_synchro = MSG_LOCAL_BRANCH, fullpath=fp,
                                       status='OK',
                                       ))

        with open(p / 'file1', 'a') as f:
            f.write(generate_content())

        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n, head='branch main', branch='main',
                                       remote_synchro=MSG_LOCAL_BRANCH, fullpath=fp,
                                       status='1 modified file'
                                       ))

        with open(p / 'file3', 'a') as f:
            f.write(generate_content())
        git_exec('add', 'file3', gitdir=p)

        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n, head='branch main', branch='main',
                                       remote_synchro=MSG_LOCAL_BRANCH, fullpath=fp,
                                       status='2 modified files'
                                       ))

        (p/'file2').unlink()
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n, head='branch main', branch='main',
                                       remote_synchro=MSG_LOCAL_BRANCH, fullpath=fp,
                                       status='3 modified files'
                                       ))

        git_exec('add', 'file1', gitdir=p)
        git_exec('rm', 'file2', gitdir=p)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n, head='branch main', branch='main',
                                       remote_synchro=MSG_LOCAL_BRANCH, fullpath=fp,
                                       status='3 modified files'
                                       ))

        git_commit(fp, 'check on modified files done')

        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n, head='branch main', branch='main',
                                       remote_synchro = MSG_LOCAL_BRANCH, fullpath=fp,
                                       status='OK',
                                       ))

    def run_test_on_main_with_one_tag(self, dir1, tag1: str):
        print('    - run_test_on_main_with_one_tag')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())
        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head='branch main',
                                       branch='main',
                                       remote_synchro = MSG_LOCAL_BRANCH,
                                       fullpath=fp,
                                       status='OK',
                                       last_commit='',
                                       tags=None,
                                       ))
        ric.ensure_tags()
        self.assertEqual(ric.tags, tag1)
        ric.ensure_all_filled() # check that no exception is raised

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, ['main'])



    def run_test_on_tag(self, dir1, tag1: str):
        print('    - run_test_on_tag')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())
        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        ric.refresh()
        self.assertEqual(to_named_tuple(ric),
                         RepoInfoTuple(name=n,
                                       head='tag %s' % tag1,
                                       tag=tag1,
                                       branch='',
                                       remote_synchro='',
                                       fullpath=fp,
                                       status='OK',
                                       last_commit='',
                                       tags=None,
                                       ))
        ric.ensure_tags()
        self.assertEqual(ric.tags, tag1)
        ric.ensure_all_filled() # check that no exception is raised

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, ['main'])



    def run_test_on_tag2_with_tag3(self, dir1, tag2: str, tag3: str):
        print('    - run_test_on_tag2_with_tag3')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())
        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head='tag tag2',
                                       tag='tag2',
                                       branch='',
                                       remote_synchro='',
                                       fullpath=fp,
                                       status='OK',
                                       last_commit='',
                                       tags=None,
                                       ))
        ric.ensure_tags()
        self.assertEqual(ric.tags, '%s %s' % (tag2, tag3))
        ric.ensure_all_filled() # check that no exception is raised

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, ['main'])



    def run_test_on_commit(self, dir1, commit_sha1):
        print('    - run_test_on_commit')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())
        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        ric.refresh()
        self.assertEqual(to_named_tuple(ric),
                         RepoInfoTuple(name=n,
                                       head='commit %s' % commit_sha1,
                                       tag='',
                                       branch='',
                                       remote_synchro='',
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=ric.last_commit,
                                       tags=None,
                                       ))
        self.assertTrue(ric.last_commit.startswith('commit %s' % commit_sha1))
        ric.ensure_tags()
        self.assertEqual(ric.tags, '')
        ric.ensure_all_filled()  # check that no exception is raised

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, ['main'])



    def run_test_on_tag_like_sha1(self, dir1, tag1: str):
        print('    - run_test_on_tag_like_sha1')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())
        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        ric.refresh()
        self.assertEqual(to_named_tuple(ric),
                         RepoInfoTuple(name=n,
                                       head='tag %s' % tag1,
                                       tag=tag1,
                                       branch='',
                                       remote_synchro='',
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=ric.last_commit,
                                       tags=None,
                                       ))
        ric.ensure_all_filled()  # check that no exception is raised

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_local, ['main'])
        self.assertEqual(ric.branches_remote, [])



    def run_test_on_other_branch(self, dir1, branch, _sha1):
        print('    - run_test_on_other_branch')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())
        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        ric.refresh()
        self.assertEqual(to_named_tuple(ric),
                         RepoInfoTuple(name=n,
                                       head='branch %s' % branch,
                                       tag='',
                                       branch=branch,
                                       remote_synchro=MSG_LOCAL_BRANCH,
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=ric.last_commit,
                                       tags=None,
                                       ))
        ric.ensure_all_filled()  # check that no exception is raised

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, ['branch1', 'main'])



    def run_test_on_other_branch_merged_main(self, dir1, branch):
        print('    - run_test_on_other_branch_merged_main')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())
        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        ric.refresh()
        self.assertEqual(to_named_tuple(ric),
                         RepoInfoTuple(name=n,
                                       head='branch %s' % branch,
                                       tag='',
                                       branch=branch,
                                       remote_synchro=MSG_LOCAL_BRANCH,
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=ric.last_commit,
                                       tags=None,
                                       ))
        ric.ensure_all_filled()  # check that no exception is raised

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, ['branch1', 'main'])


    def run_test_on_main_after_branch2_deleted(self, dir1, branch):
        print('    - run_test_on_main_after_branch2_deleted')
        n, p, fp = str(dir1), dir1, str(dir1.resolve())
        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        ric.refresh()
        self.assertEqual(to_named_tuple(ric),
                         RepoInfoTuple(name=n,
                                       head='branch %s' % branch,
                                       tag='',
                                       branch=branch,
                                       remote_synchro=MSG_LOCAL_BRANCH,
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=ric.last_commit,
                                       tags=None,
                                       ))
        ric.ensure_all_filled()  # check that no exception is raised

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, ['branch1', 'main'])



    def test_find_git_repos(self) -> None:
        self.dir2 = pathlib.Path(self.gitdir) / 'dir2'
        self.dir2.mkdir()
        os.chdir(self.dir2)
        git_init_repo('.')

        git_dir = self.gitdir
        os.chdir(git_dir)
        (git_dir/'tmp_a/.git').mkdir(parents=True)
        mr = MultiRepo(str(git_dir))
        repo_list = mr.find_git_repos()
        self.assertEqual(set(repo_list), {'dir2'})

        # nothing added, or removed
        added_repo, rm_repo = mr.find_git_repos_added_removed()
        self.assertEqual((added_repo, rm_repo), ([], []))

        # fake that 'dir2' is a new repo added and that 'removed' was removed
        removed_ric = MgRepoInfo('removed', str(git_dir / 'removed'))
        mr.repo_dict['removed'] = removed_ric
        mr.repo_names.append('removed')
        mr.repo_list.append(removed_ric)

        del mr.repo_dict['dir2']
        del mr.repo_names[0]
        del mr.repo_list[0]

        added_repo, rm_repo = mr.find_git_repos_added_removed()
        self.assertEqual(len(added_repo), 1)
        self.assertEqual(added_repo[0].name, 'dir2')
        self.assertEqual(rm_repo,    [mr.repo_dict['removed']])

        rmtree_failsafe(self.dir2)

    def test_find_git_repos_with_strange_names(self) -> None:
        strange_dir1 = pathlib.Path(self.gitdir) / 'strange_dir[with_bracket]'
        strange_dir1.mkdir()
        os.chdir(strange_dir1)
        git_init_repo(str(strange_dir1))

        strange_dir2 = pathlib.Path(strange_dir1) / 'strange_subdir[with_bracket]'
        strange_dir2.mkdir()
        git_init_repo(str(strange_dir2))

        os.chdir(self.gitdir)
        mr = MultiRepo(str(self.gitdir))
        repo_list = mr.find_git_repos()
        self.assertEqual(set(repo_list), {
            'strange_dir[with_bracket]', 
            'strange_dir[with_bracket]\\strange_subdir[with_bracket]'
        })

        os.chdir(strange_dir1)
        mr = MultiRepo(str(strange_dir1))
        repo_list = mr.find_git_repos()
        self.assertEqual(set(repo_list), {
            '.',
            'strange_subdir[with_bracket]'
        } )

        rmtree_failsafe(strange_dir1)


    def run_clone_test_on_empty_git(self, dir1: pathlib.Path, dir3: pathlib.Path):
        print('    - run_clone_test_on_empty_git')

        n, p, fp = str(dir3), dir3, str(dir3.resolve())
        git_exec('clone', str(dir1), fp)

        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head=MSG_EMPTY_REPO,
                                       branch=MSG_EMPTY_REPO,
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=MSG_NO_COMMIT,
                                       tags='',
                                       ))
        self.assertEqual(ric.commit_sha1, '')
        ric.ensure_all_filled()  # check ensure_all_filled() does not fail

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, [])
        self.assertEqual(ric.branches_local, [])



    def run_clone_test_on_origin_main_2_commits(self, _dir1, dir3):
        print('    - run_clone_test_on_origin_main_2_commits')

        n, p, fp = str(dir3), dir3, str(dir3.resolve())

        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head=MSG_EMPTY_REPO,
                                       branch=MSG_EMPTY_REPO,
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=MSG_NO_COMMIT,
                                       tags='',
                                       ))

        git_exec('fetch', gitdir=dir3)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head=MSG_EMPTY_REPO,
                                       branch=MSG_EMPTY_REPO,
                                       fullpath=fp,
                                       status='OK',
                                       last_commit=MSG_NO_COMMIT,
                                       tags='',
                                       ))

        git_exec('pull', gitdir=dir3)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head='branch main',
                                       branch='main',
                                       fullpath=fp,
                                       status='OK',
                                       remote_synchro=MSG_REMOTE_SYNCHRO_OK,
                                       remote_branch='origin/main',
                                       last_commit='',
                                       tags=None,
                                       ))

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_local, ['main'])
        self.assertEqual(ric.branches_remote, ['origin/main'])



    def run_clone_test_on_origin_main_more_commits(self, dir1, dir3):
        print('    - run_clone_test_on_origin_main_more_commits')

        n, p, fp = str(dir3), dir3, str(dir3.resolve())

        # check refesh() effect
        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head='branch main',
                                       branch='main',
                                       fullpath=fp,
                                       status='OK',
                                       remote_synchro=MSG_REMOTE_SYNCHRO_OK,
                                       remote_branch='origin/main',
                                       last_commit='',
                                       tags=None,
                                       ))
        git_exec('fetch', gitdir=dir3)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head='branch main',
                                       branch='main',
                                       fullpath=fp,
                                       status='OK',
                                       remote_synchro='2 to pull',
                                       remote_branch='origin/main',
                                       last_commit='',
                                       tags=None,
                                       ))

        add_content(fp, 'blabla')
        git_commit(fp, 'add blabla', allow_errors=True) # when creating the commit, git returns 1 because the branches are diverging
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head='branch main',
                                       branch='main',
                                       fullpath=fp,
                                       status='OK',
                                       remote_synchro='1 to push, 2 to pull',
                                       remote_branch='origin/main',
                                       last_commit='',
                                       tags=None,
                                       ))

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_local, ['main'])
        self.assertEqual(ric.branches_remote, ['origin/main'])



    def run_clone_test_on_tag(self, dir1, tag, dir4, tag_sha1):
        # clone on a repo pointing on a tag
        print('    - run_clone_test_on_tag')

        n, p, fp = str(dir4), dir4, str(dir4.resolve())
        # clone on the tag, we are in detached state now
        git_exec('clone', str(dir1), str(dir4))

        # check refesh() effect
        # the current status is that the fact that we are detached on a specific tag has not been
        # identified by git
        ric = MgRepoInfo(n, fp)
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head='commit %s' % tag_sha1[:SHORT_SHA1_NB_DIGITS],
                                       branch='',
                                       tag='',
                                       fullpath=fp,
                                       status='OK',
                                       remote_synchro='',
                                       remote_branch='',
                                       last_commit=ric.last_commit,
                                       tags=None,
                                       ))


        sha1 = add_content(fp, 'blabla')
        self.assertEqual(to_named_tuple(ric.refresh()),
                         RepoInfoTuple(name=n,
                                       head='commit %s' % sha1,
                                       branch='',
                                       tag='',
                                       fullpath=fp,
                                       status='OK',
                                       remote_synchro='',
                                       remote_branch='',
                                       last_commit=ric.last_commit,
                                       tags=None,
                                       ))

        ric.ensure_branches_filled()
        self.assertEqual(ric.branches_filled, True)
        self.assertEqual(ric.branches_remote, ['origin/main'])
        self.assertEqual(ric.branches_local, [])
