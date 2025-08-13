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


import unittest, tempfile, os, json

from src.mg_json_mgit_parser import exportToMgit, ProjectStructure
from src.mg_repo_info import MgRepoInfo

class TestMgitImportExport(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        os_handle, cls.mgitFname = tempfile.mkstemp(suffix='.mgit', prefix='test_mgit_', text=True)
        os.close(os_handle)
        # we only need the filename
        print('\nUsing temp filename: %s\n' % cls.mgitFname)


    def testEmptyExportImport(self):
        exportToMgit(self.mgitFname, '', [])
        proj = ProjectStructure()
        proj.fill_from_json_file(self.mgitFname, '.')
        self.assertEqual(proj.description, '')
        self.assertEqual(proj.repos, [])


    def testExportImportRepos(self):
        repo1 = MgRepoInfo('repo1', 'repo1', 'repo1')
        repo1.url = 'file://server/repo1.git'
        repo2 = MgRepoInfo('repo2', 'repo2', 'repo2')
        repo2.url = 'file://server/repo2.git'
        exportToMgit(self.mgitFname, 'some description', [repo2, repo1])

        with open(self.mgitFname) as f:
            d = json.load(f)

        # check that repos are sorted upon export
        self.assertEqual(d['repositories'][0]['destination'], 'repo1')


        proj = ProjectStructure()
        proj.fill_from_json_file(self.mgitFname, '.')

        self.assertEqual(proj.description, 'some description')
        self.assertEqual(len(proj.repos), 2)
        self.assertEqual(proj.repos[0].destination, 'repo1')
        self.assertEqual(proj.repos[1].destination, 'repo2')


    def testExportImportReposSnapshotMode(self):
        repo1 = MgRepoInfo('repo1', 'repo1', 'repo1')
        repo1.url = 'file://server/repo1.git'
        repo1.head = 'branch toto'
        repo1.commit_sha1 = '1111'

        repo2 = MgRepoInfo('Repo2', 'Repo2', 'Repo2')
        repo2.url = 'file://server/repo2.git'
        repo2.head = 'tag titi'
        repo2.commit_sha1 = '2222'

        repo3 = MgRepoInfo('repo3', 'repo3', 'repo3')
        repo3.url = 'file://server/repo3.git'
        repo3.head = 'commit 3333'
        repo3.commit_sha1 = '3333'

        exportToMgit(self.mgitFname, 'some description', [repo2, repo1, repo3], snapshotMode=False)

        proj = ProjectStructure()
        proj.fill_from_json_file(self.mgitFname, '.')

        self.assertEqual(proj.description, 'some description')
        self.assertEqual(len(proj.repos), 3)

        self.assertEqual(proj.repos[0].destination, 'repo1')
        self.assertEqual(proj.repos[0].head_type, 'branch')
        self.assertEqual(proj.repos[0].head, 'toto')

        self.assertEqual(proj.repos[1].destination, 'Repo2')
        self.assertEqual(proj.repos[1].head_type, 'tag')
        self.assertEqual(proj.repos[1].head, 'titi')

        self.assertEqual(proj.repos[2].destination, 'repo3')
        self.assertEqual(proj.repos[2].head_type, 'commit')
        self.assertEqual(proj.repos[2].head, '3333')


        exportToMgit(self.mgitFname, 'some description', [repo2, repo1, repo3], snapshotMode=True)

        proj = ProjectStructure()
        proj.fill_from_json_file(self.mgitFname, '.')

        self.assertEqual(proj.description, 'some description')
        self.assertEqual(len(proj.repos), 3)

        self.assertEqual(proj.repos[0].destination, 'repo1')
        self.assertEqual(proj.repos[0].head_type, 'commit')
        self.assertEqual(proj.repos[0].head, '1111')

        self.assertEqual(proj.repos[1].destination, 'Repo2')
        self.assertEqual(proj.repos[1].head_type, 'commit')
        self.assertEqual(proj.repos[1].head, '2222')

        self.assertEqual(proj.repos[2].destination, 'repo3')
        self.assertEqual(proj.repos[2].head_type, 'commit')
        self.assertEqual(proj.repos[2].head, '3333')


    def testEmptyExportImport(self):
        exportToMgit(self.mgitFname, '', [])
        proj = ProjectStructure()
        proj.fill_from_json_file(self.mgitFname, '.')
        self.assertEqual(proj.description, '')
        self.assertEqual(proj.repos, [])



