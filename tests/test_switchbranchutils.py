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
from typing import Union, Any, List

import unittest

from PySide2.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

from src.mg_repo_info import MgRepoInfo
from src.mg_utils import treeWidgetFlatIterator, treeWidgetDeepIterator
from src.mg_dialog_git_switch_delete_branch import analyseRepoBranchOrTagInfo, fillBranchTagInfo, \
    GroupingBy, buildRepoBranchInfo, stripOrigin, branchNameIsPresentInRemote, remoteBranchesForBranchName, applyFilterToTree


class TestGitSwitchBranchUtils(unittest.TestCase):

    def setUp(self):
        if QApplication.instance():
            self.app = QApplication.instance()
            return

        self.app = QApplication([])

    def tearDown(self):
        self.app = None

    def testAnanlyseRepoBranchInfo(self):
        self.assertEqual(analyseRepoBranchOrTagInfo([]), [])

        self.assertEqual( analyseRepoBranchOrTagInfo([
            ('repo1', ['l_br'], ['r_br'])
        ]), [
            ('l_br', 1, 'local', ['repo1']),
            ('r_br', 1, 'remote', ['repo1']),
        ])

        self.assertEqual( analyseRepoBranchOrTagInfo([
            ('repo1', ['l_br'], ['r_br']),
            ('repo2', ['l_br'], ['r_br']),
        ]), [
            ('l_br', 2, 'local', ['repo1', 'repo2']),
            ('r_br', 2, 'remote', ['repo1', 'repo2']),
        ])

        self.assertEqual( analyseRepoBranchOrTagInfo([
            ('repo1', ['master'], ['master']),
        ]), [
            ('master', 1, 'local and remote', ['repo1']),
        ])

        self.assertEqual( analyseRepoBranchOrTagInfo([
            ('repo1', ['master'], ['master']),
            ('repo2', ['master'], ['master']),
        ]), [
            ('master', 2, 'local and remote', ['repo1', 'repo2']),
        ])

        self.assertEqual( analyseRepoBranchOrTagInfo([
            ('repo1', ['l_br', 'master'], ['r_br', 'master']),
        ]), [
            ('l_br', 1, 'local', ['repo1']),
            ('r_br', 1, 'remote', ['repo1']),
            ('master', 1, 'local and remote', ['repo1']),
        ])

        self.assertEqual( analyseRepoBranchOrTagInfo([
            ('repo1', ['br1'], []),
            ('repo2', [], ['br1']),
        ]), [
            ('br1', 2, 'local and remote', ['repo1', 'repo2']),
        ])

        self.assertEqual( analyseRepoBranchOrTagInfo([
            ('repo1', ['br1'], []),
            ('repo2', ['br1'], ['br1']),
        ]), [
            ('br1', 2, 'local and remote', ['repo1', 'repo2']),
        ])

        self.assertEqual( analyseRepoBranchOrTagInfo([
            ('repo1', [], ['br1']),
            ('repo2', ['br1'], ['br1']),
        ]), [
            ('br1', 2, 'local and remote', ['repo1', 'repo2']),
        ])

        self.assertEqual(analyseRepoBranchOrTagInfo([
            ('repo1', [], ['br1']),
            ('repo2', ['br1'], ['br1']),
        ]), [
            ('br1', 2, 'local and remote', ['repo1', 'repo2']),
        ])


    def test_crash_during_switch_branch(self):

        class StubRepo: pass
        repo = StubRepo()
        repo.name = 'crash_during_switch_branch'
        repo.branches_local = [
            'dev',
            'feat/Grace_v4_demo',
            'feat/first_client_server_demo',
            'master',
        ]
        repo.branches_remote = [
            'origin/dev',
            'origin/feat/Grace_v4_demo',
            'origin/feat/new_GraceClient_exe_with_pyinstaller',
            'origin/int',
            'origin/master',
            'origin/rel/v0.5.0',
            'origin_FRSA_IP2/HEAD -> origin_FRSA_IP2/master',
            'origin_FRSA_IP2/feat/first_client_server_demo',
            'origin_FRSA_IP2/master',
            'origin_WW2/master',
        ]

        # collect branch names
        repoBranchInfo = buildRepoBranchInfo([repo])
        repoItemInfo = analyseRepoBranchOrTagInfo(repoBranchInfo)


    def test_buildRepoBranchInfo(self):
        class StubRepo: pass
        repo = StubRepo()
        repo.name = 'repo1'
        repo.branches_local = [
            'dev',
            'master',
        ]
        repo.branches_remote = [
            'origin/dev',
            'origin/master',
        ]

        # strips origin by default
        self.assertEqual(buildRepoBranchInfo([repo]),
                         [('repo1', ['dev', 'master'], ['dev', 'master'])]
                         )

        repo.branches_remote = [
            'origin/dev',
            'origin2/master',
        ]
        self.assertEqual(buildRepoBranchInfo([repo]),
                         [('repo1', ['dev', 'master'], ['dev', 'master'])]
                         )

        repo.branches_remote = [
            'origin/dev',
            'origin/master',
            'origin2/master',
        ]
        self.assertEqual(buildRepoBranchInfo([repo]),
                         [('repo1', ['dev', 'master'], ['dev', 'master'])]
                         )


    def test_stripOrigin(self):
        self.assertEqual(stripOrigin( [
            'origin/dev',
            'origin/master',
        ] ), [
            'dev',
            'master'
        ] )

        self.assertEqual(stripOrigin( [
            'origin/dev',
            'origin2/master',
        ] ), [
            'dev',
            'master'
        ] )

        self.assertEqual(stripOrigin( [
                'origin/dev',
                'origin/master',
                'origin2/master',
        ] ), [
            'dev',
            'master',
        ] )


    def test_BranchNameIsPresentInRemote(self):
        self.assertEqual(branchNameIsPresentInRemote('toto', ['origin/toto']), True)
        self.assertEqual(branchNameIsPresentInRemote('toto', ['origin/titi']), False)


    def test_remoteBranchesForBranchName(self):
        self.assertEqual(remoteBranchesForBranchName('toto', ['origin/toto']), ['origin/toto'])
        self.assertEqual(remoteBranchesForBranchName('titi', ['origin/toto']), [])
        self.assertEqual(remoteBranchesForBranchName('toto', ['origin/toto', 'origin2/toto']), ['origin/toto', 'origin2/toto'])


    def extractTreeStructure(self, treeWidget: QTreeWidget, visibleOnly: bool = False) -> Any:
        '''Return the content of the tree widget as a tree structure'''
        treeStructure = []

        def addChildren(item_or_tree: Union[QTreeWidgetItem, QTreeWidget], myTreeStruct: List[Any]):
            for childItem in treeWidgetFlatIterator(item_or_tree):
                if visibleOnly and childItem.isHidden():
                    continue
                myTreeStruct.append( (childItem.text(0).strip() or childItem.text(1).strip(), []) )
                addChildren( childItem, myTreeStruct[-1][1] )

        addChildren(treeWidget, treeStructure)

        return treeStructure

    def testFillBranchInfo(self):
        tree = QTreeWidget()
        fillBranchTagInfo([], tree, GroupingBy.NONE)
        self.assertEqual(tree.topLevelItemCount(), 0)
        tree.clear()

        branchList = [
            ('l_br', 1, 'local', ['repo1']),
            ('master', 1, 'local and remote', ['repo1']),
            ('r_br', 1, 'remote', ['repo1']),
        ]
        fillBranchTagInfo(branchList, tree, GroupingBy.NONE)
        self.assertEqual( self.extractTreeStructure(tree), [
            ('l_br', [('repo1', [])]),
            ('master', [('repo1', [])]),
            ('r_br', [('repo1', [])]),
        ])


        branchList = [
            ('feat/l_br1', 1, 'local', ['repo1']),
            ('feat/l_br2', 1, 'local', ['repo1']),
            ('feat/l_br2/titi', 1, 'local', ['repo1']),
            ('master', 1, 'local and remote', ['repo1']),
            ('xxx/r_br', 1, 'remote', ['repo1']),
        ]
        fillBranchTagInfo(branchList, tree, GroupingBy.NONE)
        self.assertEqual(self.extractTreeStructure(tree), [
            ('feat/l_br1', [('repo1', [])]),
            ('feat/l_br2', [('repo1', [])]),
            ('feat/l_br2/titi', [('repo1', [])]),
            ('master', [('repo1', [])]),
            ('xxx/r_br', [('repo1', [])]),
        ])

        branchList = [
            ('feat/l_br1', 1, 'local', ['repo1']),
            ('feat/l_br2', 1, 'local', ['repo1']),
            ('feat/l_br2/titi', 1, 'local', ['repo1']),
            ('master', 1, 'local and remote', ['repo1']),
            ('xxx/r_br', 1, 'remote', ['repo1']),
        ]
        fillBranchTagInfo(branchList, tree, GroupingBy.NAME)
        self.assertEqual(self.extractTreeStructure(tree), [
            ('feat', [
                ('l_br1', [('repo1', [])]),
                ('l_br2', [
                    ('repo1', []),
                    ('titi', [('repo1', [])]),
                ]),
             ]),
            ('master', [('repo1', [])]),
            ('xxx', [
                ('r_br', [('repo1', [])]),
            ]),
        ])


    def testItemIterator(self):
        tree = QTreeWidget()
        self.assertEqual(list(treeWidgetDeepIterator(tree)), [])


        branchList = [
            ('feat/l_br1', 1, 'local', ['repo1']),
            ('feat/l_br2', 1, 'local', ['repo1']),
            ('feat/l_br2/titi', 1, 'local', ['repo1']),
            ('master', 1, 'local and remote', ['repo1']),
            ('xxx/r_br', 1, 'remote', ['repo1']),
        ]
        fillBranchTagInfo(branchList, tree, GroupingBy.NAME)
        self.assertEqual(self.extractTreeStructure(tree), [
            ('feat', [
                ('l_br1', [
                    ('repo1', [])
                ]),
                ('l_br2', [
                    ('repo1', []),
                    ('titi', [
                        ('repo1', [])
                    ]),
                ]),
            ]),
            ('master', [('repo1', [])]),
            ('xxx', [
                ('r_br', [('repo1', [])]),
            ]),
        ])
        self.assertEqual(list(item.text(0) for item in treeWidgetDeepIterator(tree)), [
            'feat', 'l_br1', '', 'l_br2', '', 'titi', '', 'master', '', 'xxx', 'r_br', ''
        ])


    def testApplyFilterToTree(self):
        tree = QTreeWidget()
        branchList = [
            ('feat/l_br1', 1, 'local', ['repo1']),
            ('feat/l_br2', 1, 'local', ['repo1']),
            ('feat/l_br2/titi', 1, 'local', ['repo1']),
            ('master', 1, 'local and remote', ['repo1']),
            ('xxx/r_br', 1, 'remote', ['repo1']),
        ]
        fillBranchTagInfo(branchList, tree, GroupingBy.NAME)
        normalTreeStructure = [
                ('feat', [
                ('l_br1', [
                    ('repo1', [])
                ]),
                ('l_br2', [
                    ('repo1', []),
                    ('titi', [
                        ('repo1', [])
                    ]),
                ]),
            ]),
            ('master', [
                ('repo1', [])
            ]),
            ('xxx', [
                ('r_br', [
                    ('repo1', [])
                ]),
            ]),
        ]
        self.assertEqual(self.extractTreeStructure(tree, visibleOnly=True), normalTreeStructure)

        # hide everything
        applyFilterToTree(tree, 'yyyyyy')
        self.assertEqual(self.extractTreeStructure(tree, visibleOnly=True), [])

        # restore everything
        applyFilterToTree(tree, '')
        self.assertEqual(self.extractTreeStructure(tree, visibleOnly=True), normalTreeStructure)

        # more filtering
        applyFilterToTree(tree, 'br1')
        self.assertEqual(self.extractTreeStructure(tree, visibleOnly=True), [
            ('feat', [
                ('l_br1', [
                    ('repo1', [])
                ]),
            ])
        ])


        applyFilterToTree(tree, 'feat')
        self.assertEqual(self.extractTreeStructure(tree, visibleOnly=True), [
            ('feat', [
                ('l_br1', [
                    ('repo1', [])
                ]),
                ('l_br2', [
                    ('repo1', []),
                    ('titi', [('repo1', [])]),
                ]),
            ]),
        ])


        applyFilterToTree(tree, 'l_br')
        self.assertEqual(self.extractTreeStructure(tree, visibleOnly=True), [
            ('feat', [
                ('l_br1', [
                    ('repo1', [])
                ]),
                ('l_br2', [
                    ('repo1', []),
                    ('titi', [('repo1', [])]),
                ]),
            ]),
        ])

        applyFilterToTree(tree, 'titi')
        self.assertEqual(self.extractTreeStructure(tree, visibleOnly=True), [
            ('feat', [
                ('l_br2', [
                    ('titi', [('repo1', [])]),
                ]),
            ]),
        ])

        applyFilterToTree(tree, 'master')
        self.assertEqual(self.extractTreeStructure(tree, visibleOnly=True), [
            ('master', [
                ('repo1', [])
            ]),
        ])
