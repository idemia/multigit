import sys
from pathlib import Path

import pytest

from src.mg_tools import scan_git_dirs_flatpak, extract_valid_git_directories, FLATPAK_SPAWN
from tests.test_repoinfo import git_init_repo, TempGitDirReady

def test_extract_valid_git_directories():
    assert list(extract_valid_git_directories('''
.git
.git/refs
.git/objects
    ''')) == ['.git']

    assert list(extract_valid_git_directories('''
toto/.git
toto/.git/refs
toto/.git/objects
    ''')) == ['toto/.git']

    # out of order
    assert list(extract_valid_git_directories('''
toto/.git/refs
toto/.git
toto/.git/objects
    ''')) == ['toto/.git']

    # out of order
    assert list(extract_valid_git_directories('''
toto/.git/refs
toto/.git/objects
toto/.git
    ''')) == ['toto/.git']

    # out of order
    assert list(extract_valid_git_directories('''
toto/.git/objects
toto/.git
toto/.git/refs
    ''')) == ['toto/.git']

    # non git directories
    assert list(extract_valid_git_directories('''
objects
.git
refs
toto/.git
toto/.git/objects
titi/.git/refs
titi/.git
    ''')) == []



class TestScanGitDirsFlatpak(TempGitDirReady):

    @classmethod
    def setUpClass(cls) -> None:
        TempGitDirReady.setUpClass()

        # trick to test the code under linux without flatpak
        cls.old_flatpak_spawn = FLATPAK_SPAWN[:]
        del FLATPAK_SPAWN[1]
        del FLATPAK_SPAWN[0]

    @classmethod
    def tearDownClass(cls) -> None:
        TempGitDirReady.tearDownClass()
        # restore default value
        FLATPAK_SPAWN.extend(cls.old_flatpak_spawn)

    def test_scan_git_dirs_flatpak(self):
        if sys.platform != 'linux':
            self.skipTest('Test runs only on Linux')

        git1 = self.gitdir / 'git1'
        git_init_repo(git1)

        git2 = self.gitdir / 'toto/git2'
        git_init_repo(git2)

        git3 = self.gitdir / 'titi/.git'
        git3.mkdir(parents=True)

        git4 = self.gitdir / 'tutu/.git'
        git4.mkdir(parents=True)
        (git4 / 'refs').mkdir(parents=True)

        assert list(scan_git_dirs_flatpak(str(self.gitdir))) == [
            str(git1/'.git'), str(git2/'.git')
        ]

