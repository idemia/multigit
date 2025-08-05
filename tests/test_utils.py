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


import unittest, os

from src.mg_utils import htmlize_diff, handle_cr_in_text, set_username_on_git_url, add_suffix_if_missing, extractInt, \
    hasGitAuthFailureMsg, isGitCommandRequiringAuth, anonymise_git_url
from src.mg_config import MgConfig
from src.mg_const import MSG_BIG_DIFF
from src.mg_repo_info import match_ahead_behind, is_not_sha1, MgRepoInfo


#######################################################
#           Tests for various utilities
#######################################################


class TestUtilityFunctions(unittest.TestCase):

    def test_anonymise_git_url(self):
        test_data = [
            ("ssh://fremy@some.server.com:29418/some/path/to/repo.git",
             "ssh://username@some.server.com:29418/some/path/to/repo.git"),
            ("ssh://some.server.com:29418/some/path/to/repo.git",
             "ssh://username@some.server.com:29418/some/path/to/repo.git"),
            ("https://fremy@some.server.com:29418/some/path/to/repo.git",
             "https://some.server.com:29418/some/path/to/repo.git"),
            ("https://some.server.com:29418/some/path/to/repo.git",
             "https://some.server.com:29418/some/path/to/repo.git"),
            (r"c:\cloned\from\filesystem",
             r"c:\cloned\from\filesystem",),
            ("file://C:/work/Multigit/Sandbox/",
             "file://C:/work/Multigit/Sandbox/"),

            # ssh equivalent, see man git-clone, sections url
            ('fremy@host.xz:path/to/repo.git/',
             'username@host.xz:path/to/repo.git/'),
        ]

        for before, after in test_data:
            with self.subTest(before) as _:
                self.assertEqual( anonymise_git_url(before), after)


    def test_set_username_to_git_url(self):

        test_data = [
            ("ssh://fremy@some.server.com:29418/some/path/to/repo.git",
                "ssh://totoro@some.server.com:29418/some/path/to/repo.git"),
            ("ssh://some.server.com:29418/some/path/to/repo.git",
                "ssh://totoro@some.server.com:29418/some/path/to/repo.git"),
            ("https://fremy@some.server.com:29418/some/path/to/repo.git",
                "https://totoro@some.server.com:29418/some/path/to/repo.git"),
            ("https://some.server.com:29418/some/path/to/repo.git",
                "https://totoro@some.server.com:29418/some/path/to/repo.git"),
            ("http://fremy@some.server.com:29418/some/path/to/repo.git",
                "http://totoro@some.server.com:29418/some/path/to/repo.git"),
            ("http://some.server.com:29418/some/path/to/repo.git",
                "http://totoro@some.server.com:29418/some/path/to/repo.git"),
            (r"c:\cloned\from\filesystem",
                r"c:\cloned\from\filesystem",),
            (r"cloned\from\filesystem",
             r"cloned\from\filesystem",),
            (r"cloned/from/filesystem",
             r"cloned/from/filesystem",),
            (r"/cloned/from/filesystem",
             r"/cloned/from/filesystem",),
            ("file://C:/work/Multigit/Sandbox/",
                 "file://C:/work/Multigit/Sandbox/"),
        ]

        for before, after in test_data:
            with self.subTest(before) as _:
                self.assertEqual( set_username_on_git_url('totoro', before), after)

        self.assertEqual( set_username_on_git_url('', "ssh://fremy@some.server.com:29418/some/path/to/repo.git"),
                          "ssh://some.server.com:29418/some/path/to/repo.git")
        self.assertEqual( set_username_on_git_url('', "ssh://some.server.com:29418/some/path/to/repo.git"),
             "ssh://some.server.com:29418/some/path/to/repo.git")


    def test_strip_protocol_from_git_url(self):

        test_data = [
            ("ssh://fremy@some.server.com:29418/some/path/to/repo.git",
             "some.server.com:29418/some/path/to/repo.git"),
            ("ssh://some.server.com:29418/some/path/to/repo.git",
             "some.server.com:29418/some/path/to/repo.git"),
            ("https://fremy@some.server.com:29418/some/path/to/repo.git",
             "some.server.com:29418/some/path/to/repo.git"),
            ("https://some.server.com:29418/some/path/to/repo.git",
             "some.server.com:29418/some/path/to/repo.git"),
            ("http://fremy@some.server.com:29418/some/path/to/repo.git",
             "some.server.com:29418/some/path/to/repo.git"),
            ("http://some.server.com:29418/some/path/to/repo.git",
             "some.server.com:29418/some/path/to/repo.git"),
            (r"c:\cloned\from\filesystem",
             r"c:\cloned\from\filesystem",),
            (r"c:\cloned\from\filesystem",
             r"c:\cloned\from\filesystem",),
            ("file://fremy@C:/work/Multigit/Sandbox/",
             "C:/work/Multigit/Sandbox/"),
            ("file://C:/work/Multigit/Sandbox/",
             "C:/work/Multigit/Sandbox/"),
            (None,''),
            ('', ''),
        ]

        for before, after in test_data:
            with self.subTest(before) as _:
                self.assertEqual( strip_protocol_from_url(before), after)


    def test_anonymise_git_url(self):

        test_data = [
            ("ssh://fremy@some.server.com:29418/some/path/to/repo.git",
             "ssh://username@some.server.com:29418/some/path/to/repo.git"),
            ("ssh://some.server.com:29418/some/path/to/repo.git",
             "ssh://username@some.server.com:29418/some/path/to/repo.git"),
            ("https://fremy@some.server.com:29418/some/path/to/repo.git",
             "https://some.server.com:29418/some/path/to/repo.git"),
            ("https://some.server.com:29418/some/path/to/repo.git",
             "https://some.server.com:29418/some/path/to/repo.git"),
            ("http://fremy@some.server.com:29418/some/path/to/repo.git",
             "http://some.server.com:29418/some/path/to/repo.git"),
            ("http://some.server.com:29418/some/path/to/repo.git",
             "http://some.server.com:29418/some/path/to/repo.git"),
            (r"c:\cloned\from\filesystem",
             r"c:\cloned\from\filesystem",),
            (r"c:\cloned\from\filesystem",
             r"c:\cloned\from\filesystem",),
            ("file://C:/work/Multigit/Sandbox/",
             "file://C:/work/Multigit/Sandbox/"),
        ]

        for before, after in test_data:
            with self.subTest(before) as _:
                self.assertEqual( anonymise_git_url(before), after)


    def test_handle_cr_in_text(self):
        self.assertEqual( handle_cr_in_text('abc\n'),               'abc\n')
        self.assertEqual( handle_cr_in_text('abc\ndef\r'),          'abc\ndef')
        self.assertEqual( handle_cr_in_text('abc\ndef\rDEF\r'),     'abc\nDEF')
        self.assertEqual( handle_cr_in_text('abc\ndef\rDEF\r123\n'),'abc\n123\n')


    def test_match_ahead_behind(self):
        self.assertEqual(match_ahead_behind('ahead 33'), (33, 0))
        self.assertEqual(match_ahead_behind('behind 22'), (0, 22))
        self.assertEqual(match_ahead_behind('ahead 33, behind 22'), (33, 22))

    def test_is_not_sha1(self):
        self.assertEqual(is_not_sha1('11'), False)
        self.assertEqual(is_not_sha1('11af'), False)
        self.assertEqual(is_not_sha1('11.af'), True)
        self.assertEqual(is_not_sha1('11.22'), True)
        self.assertEqual(is_not_sha1('11_af'), True)

    def test_re_mod_files(self):
        mo = MgRepoInfo.re_status_mod_files.match('A  toto')
        assert mo
        self.assertEqual(mo.group(2), 'toto')
        mo = MgRepoInfo.re_status_mod_files.match(' D toto')
        assert mo
        self.assertEqual(mo.group(2), 'toto')
        mo = MgRepoInfo.re_status_mod_files.match(' D toto')
        assert mo
        self.assertEqual(mo.group(2), 'toto')
        mo = MgRepoInfo.re_status_mod_files.match('AD "toto titi"')
        assert mo
        self.assertEqual(mo.group(2), '"toto titi"')
        mo = MgRepoInfo.re_status_mod_files.match('AD toto')
        assert mo
        self.assertEqual(mo.group(2), 'toto')
        mo = MgRepoInfo.re_status_mod_files.match(' toto')
        self.assertEqual(mo, None)

        mo = MgRepoInfo.re_status_mod_files.match('A  toto -> titi')
        assert mo
        self.assertEqual(mo.group(2), 'toto -> titi')
        mo = MgRepoInfo.re_status_mod_files.match('AD toto -> titi')
        assert mo
        self.assertEqual(mo.group(2), 'toto -> titi')


        # conflict
        mo = MgRepoInfo.re_status_mod_files.match('AA  toto')
        assert mo
        mo = MgRepoInfo.re_status_mod_files.match('DD  toto')
        assert mo
        mo = MgRepoInfo.re_status_mod_files.match('UA  toto')
        assert mo
        mo = MgRepoInfo.re_status_mod_files.match('DU  toto')
        assert mo
        mo = MgRepoInfo.re_status_mod_files.match('UU  toto')
        assert mo

    def test_re_conflict_files(self):

        # not a conflict
        mo = MgRepoInfo.re_status_conflict_files.match('A  toto')
        assert not mo

        mo = MgRepoInfo.re_status_conflict_files.match('D  toto')
        assert not mo

        mo = MgRepoInfo.re_status_conflict_files.match('AD  toto')
        assert not mo

        # conflict
        mo = MgRepoInfo.re_status_conflict_files.match('AA  toto')
        assert mo
        mo = MgRepoInfo.re_status_conflict_files.match('DD  toto')
        assert mo
        mo = MgRepoInfo.re_status_conflict_files.match('UA  toto')
        assert mo
        mo = MgRepoInfo.re_status_conflict_files.match('DU  toto')
        assert mo
        mo = MgRepoInfo.re_status_conflict_files.match('UU  toto')
        assert mo



    def test_add_suffix_if_missing(self):
        self.assertEqual(add_suffix_if_missing('toto', '.mgit'), 'toto.mgit')
        self.assertEqual(add_suffix_if_missing('toto.mgit', '.mgit'), 'toto.mgit')


    def test_extract_int(self):
        self.assertEqual(extractInt(''), 0)
        self.assertEqual(extractInt('123'), 123)
        self.assertEqual(extractInt('123xxx45'), 123)
        self.assertEqual(extractInt('001xxx45'), 1)
        self.assertEqual(extractInt('xxx45'), 0)
        self.assertEqual(extractInt('xxx45', intAtBeginning=False), 45)
        self.assertEqual(extractInt('001xxx45', intAtBeginning=True), 1)


    def test_hasGitAuthFailureMsg(self):
        gitlog = '''warning: ----------------- SECURITY WARNING ----------------
warning: | TLS certificate verification has been disabled! |
warning: ---------------------------------------------------
warning: HTTPS connections may not be secure. See https://aka.ms/gcmcore-tlsverify for more information.
fatal: Authentication failed for 'https://xxx.yyy.com/toto/Sandbox.git/'
bla bla bla
'''
        self.assertEqual(hasGitAuthFailureMsg(gitlog), True)
        gitlog2 = '''xxfatal: Authentication failed for 'https://xxx.yyy.com/toto/Sandbox.git/' 
    '''
        self.assertEqual(hasGitAuthFailureMsg(gitlog2), False)


    def test_isGitCommandRequiringAuth(self):
        self.assertEqual(isGitCommandRequiringAuth(['git', 'push', '--verbose']), True)
        self.assertEqual(isGitCommandRequiringAuth(['git', 'pull']), True)
        self.assertEqual(isGitCommandRequiringAuth(['git', 'fetch', '--progress']), True)

        for cmdline in [
            ['git.exe', '--version'],
            ['git.exe', '-C', r'C:\work\Multigit\Dev', 'log', '-1'],
            ['git.exe', '-C', r'C:\work\Multigit\Dev', 'remote', '--verbose'],
            ['git.exe', '-C', r'C:\work\Multigit\Dev', 'status', '--porcelain', '--branch'],
            ['git.exe', '-C', r'C:\work\Multigit\Sandbox_http', 'diff', '-u', '--patience', '--stat'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\submodule2', 'checkout', 'master'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo1', 'merge', 'dev'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo1', 'status', '--porcelain', '--branch'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo1', 'tag', '--list', '--sort',
             'creatordate'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo2', 'branch'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo2', 'checkout', 'dev'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo2', 'checkout', 'int'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo1', 'tag', 'int_112234', '-F', r'C:\Users\g582619\AppData\Local\Temp\tmp_b_uwll1']
        ]:
            with self.subTest(' '.join(cmdline)):
                self.assertEqual(isGitCommandRequiringAuth(cmdline), False)

        for cmdline in [
            ['git.exe', '-C', r'C:\work\Multigit\Sandbox_http', 'fetch', '--verbose', '--prune'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo1', 'fetch', '--prune'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo1', 'pull'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo1', 'push', '-u', '--progress', 'origin', 'int:int'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo1', 'push', 'origin', 'int_112234'],
            ['git.exe', '-C', r'C:\work\Multigit\tmp\toto2\subdir1\subdir1_repo2', 'fetch', '--prune'],
            ['git.exe', 'clone', '--progress file://C:/work/Multigit/Sandbox/', r'C:\work\Multigit\tmp\submodule2'],
            ['git.exe', 'clone', '--progress file://C:/work/Multigit/Sandbox/', r'C:\work\Multigit\tmp\submodule2'],
        ]:
            with self.subTest(' '.join(cmdline)):
                self.assertEqual(isGitCommandRequiringAuth(cmdline), True)


    def test_mg_config(self):
        try:
            mgc = MgConfig('my_config.cfg')
            mgc['toto'] = { 1:2, 3:4 }
            mgc['titi'] = [ 1, 2, 3, 4]
            mgc['tutu'] = 'coucou'

            assert mgc['toto'] == { 1:2, 3:4 }
            assert mgc['titi'] == [1,2,3,4]
            assert mgc['tutu'] == 'coucou'

            assert mgc['key_not_present'] is  None

            mgc.save()

            mgc = MgConfig('my_config.cfg')
            mgc.load()

            assert mgc['toto'] == { 1:2, 3:4 }
            assert mgc['titi'] == [1,2,3,4]
            assert mgc['tutu'] == 'coucou'

        finally:
            if os.path.exists('my_config.cfg'):
                os.unlink('my_config.cfg')

    def test_htmlize_diff(self):
        sin = ''' test/test_gui.py    | 16 ++++++++++++++++
 test/test_sxtool.py |  6 +-----
 2 files changed, 17 insertions(+), 5 deletions(-)

diff --git a/test/test_gui.py b/test/test_gui.py
index 8125a27..3e51db7 100644
--- a/test/test_gui.py
+++ b/test/test_gui.py
@@ -11,6 +11,22 @@ from PyQt5.QtTest import QTest

 from src.main_form import MainForm
+
+from src.const import CONST_33
+
@@ this is a description @@
this line is plain
- this line is removed
+ this line is added
'''

        sout_ref='''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap;font-family:'Courier New'; font-size:8pt; font-weight:600; 
        font-style:normal; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; 
        -qt-block-indent:0; text-indent:0px; }
</style></head>
<body style="font-family:'Courier New'; font-size:8pt; font-weight:400; font-style:normal">
 test/test_gui.py    | 16 <span style="background-color:#ccffcc;">++++++++++++++++</span><br/>
 test/test_sxtool.py |  6 <span style="background-color:#ccffcc;">+</span><span style="background-color:#ffdddd;">-----</span><br/>
 2 files changed, 17 insertions(+), 5 deletions(-)<br/>
<br/>
<span style="background-color:#ffff7f ">diff --git a/test/test_gui.py b/test/test_gui.py</span><br/>
<span style="background-color:#ffff7f ">index 8125a27..3e51db7 100644</span><br/>
<span style="background-color:#ffff7f ">--- a/test/test_gui.py</span><br/>
<span style="background-color:#ffff7f ">+++ b/test/test_gui.py</span><br/>
<span style="background-color:#aaffff;">@@ -11,6 +11,22 @@</span> from PyQt5.QtTest import QTest<br/>
<br/>
 from src.main_form import MainForm<br/>
<span style="background-color:#ccffcc;">+</span><br/>
<span style="background-color:#ccffcc;">+from src.const import CONST_33</span><br/>
<span style="background-color:#ccffcc;">+</span><br/>
<span style="background-color:#aaffff;">@@ this is a description @@</span><br/>
this line is plain<br/>
<span style="background-color:#ffdddd;">- this line is removed</span><br/>
<span style="background-color:#ccffcc;">+ this line is added</span><br/>
<br/>
</body></html>'''

        sout = htmlize_diff(sin)
        if sout != sout_ref:
            for l, lref in zip(sout.split('\n'), sout_ref.split('\n')):
                if l == lref:
                    print('={}\\n'.format(l))
                else:
                    print('-{}\\n'.format(l))
                    print('+{}\\n'.format(lref))
        self.assertEqual(sout, sout_ref)

    def test_htmlize_diff_maxlines(self):
        sin = ''' test/test_gui.py    | 16 ++++++++++++++++
 test/test_sxtool.py |  6 +-----
 2 files changed, 17 insertions(+), 5 deletions(-)

diff --git a/test/test_gui.py b/test/test_gui.py
index 8125a27..3e51db7 100644
--- a/test/test_gui.py
+++ b/test/test_gui.py
@@ -11,6 +11,22 @@ from PyQt5.QtTest import QTest
'''

        sout_ref='''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap;font-family:'Courier New'; font-size:8pt; font-weight:600; 
        font-style:normal; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; 
        -qt-block-indent:0; text-indent:0px; }
</style></head>
<body style="font-family:'Courier New'; font-size:8pt; font-weight:400; font-style:normal">
 test/test_gui.py    | 16 <span style="background-color:#ccffcc;">++++++++++++++++</span><br/>
 test/test_sxtool.py |  6 <span style="background-color:#ccffcc;">+</span><span style="background-color:#ffdddd;">-----</span><br/>
 2 files changed, 17 insertions(+), 5 deletions(-)<br/>
<br/>
[...]<br/>
%s<br/>
</body></html>''' % MSG_BIG_DIFF

        sout = htmlize_diff(sin, 4)
        if sout != sout_ref:
            for l, lref in zip(sout.split('\n'), sout_ref.split('\n')):
                if l == lref:
                    print('={}\\n'.format(l))
                else:
                    print('-{}\\n'.format(l))
                    print('+{}\\n'.format(lref))
        self.assertEqual(sout, sout_ref)

        sin = ''

        sout_ref='''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap;font-family:'Courier New'; font-size:8pt; font-weight:600; 
        font-style:normal; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; 
        -qt-block-indent:0; text-indent:0px; }
</style></head>
<body style="font-family:'Courier New'; font-size:8pt; font-weight:400; font-style:normal">
<br/>
</body></html>'''

        sout = htmlize_diff(sin, 1000)
        self.assertEqual(sout, sout_ref)
