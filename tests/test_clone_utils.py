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


from typing import List, Tuple

import unittest

from src.mg_clone_execution import addPreconditionToEnsureCloneOrderLogic, \
    build_taskgroup_dep_graph, addPreconditionsToTaskGroup
from src.mg_exec_task_item import MgExecTaskGroup
from src.mg_repo_info import MgRepoInfo


class TestCloneGraphOrdering(unittest.TestCase):

    def buildTaskGroups(self) -> Tuple[List[str], List[MgExecTaskGroup]]:
        repoNames = [
            'dev',
            'dev/subdev1',
            'dev/subdev1/subdev1_sub1',
            'dev/subdev1/subdev1_sub2',
            'dev/subdev2',
            'dev/subdev2/toto/subdev2_sub1',
            'test',
            'test/extern/subtest1',
            'doc/whats/up',
        ]


        taskGroups: List[MgExecTaskGroup] = [
            MgExecTaskGroup(name, MgRepoInfo(name, name))
            for name in repoNames
        ]

        return repoNames, taskGroups



    def test_cloneGraphOrdering(self):
        repoNames, taskGroups = self.buildTaskGroups()
        taskGroups = addPreconditionToEnsureCloneOrderLogic(taskGroups)

        # check that ordering is the same
        self.assertEqual([tg.desc for tg in taskGroups], repoNames)

    def test_cloneGraphStructureFlexibleSplitter(self):
        repoNames = [
            'titi/toto',
            'tata\\tutu',
        ]

        taskGroups: List[MgExecTaskGroup] = [
            MgExecTaskGroup(name, MgRepoInfo(name, name))
            for name in repoNames
        ]
        topNode = build_taskgroup_dep_graph(taskGroups)

        self.assertEqual(topNode.children[0].name, 'titi')
        self.assertEqual(topNode.children[0].children[0].name, 'toto')

        self.assertEqual(topNode.children[1].name, 'tata')
        self.assertEqual(topNode.children[1].children[0].name, 'tutu')


    def test_cloneGraphStructure(self):
        repoNames, taskGroups = self.buildTaskGroups()
        topNode = build_taskgroup_dep_graph(taskGroups)

        self.assertEqual(topNode.children[0].name, 'dev')
        self.assertEqual(topNode.children[0].taskGroup.desc, 'dev')
        self.assertEqual(topNode.children[1].name, 'test')
        self.assertEqual(topNode.children[1].taskGroup.desc, 'test')
        self.assertEqual(topNode.children[2].name, 'doc')
        self.assertEqual(topNode.children[2].taskGroup, None)
        self.assertEqual(len(topNode.children), 3)

        node = topNode.children[0]
        self.assertEqual(node.children[0].name, 'subdev1')
        self.assertEqual(node.children[0].taskGroup.desc, 'dev/subdev1')
        self.assertEqual(node.children[1].name, 'subdev2')
        self.assertEqual(node.children[1].taskGroup.desc, 'dev/subdev2')
        self.assertEqual(len(node.children), 2)

        node = topNode.children[0].children[0]
        self.assertEqual(node.children[0].name, 'subdev1_sub1')
        self.assertEqual(node.children[0].taskGroup.desc, 'dev/subdev1/subdev1_sub1')
        self.assertEqual(node.children[1].name, 'subdev1_sub2')
        self.assertEqual(node.children[1].taskGroup.desc, 'dev/subdev1/subdev1_sub2')
        self.assertEqual(len(node.children), 2)

        node = topNode.children[0].children[1]
        self.assertEqual(node.children[0].name, 'toto')
        self.assertEqual(node.children[0].taskGroup, None)
        self.assertEqual(len(node.children), 1)

        node = topNode.children[0].children[1].children[0]
        self.assertEqual(node.children[0].name, 'subdev2_sub1')
        self.assertEqual(node.children[0].taskGroup.desc, 'dev/subdev2/toto/subdev2_sub1')
        self.assertEqual(len(node.children), 1)

        node = topNode.children[1]
        self.assertEqual(node.children[0].name, 'extern')
        self.assertEqual(node.children[0].taskGroup, None)
        self.assertEqual(len(node.children), 1)

        node = topNode.children[1].children[0]
        self.assertEqual(node.children[0].name, 'subtest1')
        self.assertEqual(node.children[0].taskGroup.desc, 'test/extern/subtest1')
        self.assertEqual(len(node.children), 1)

        node = topNode.children[2]
        self.assertEqual(node.children[0].name, 'whats')
        self.assertEqual(node.children[0].taskGroup, None)
        self.assertEqual(len(node.children), 1)

        node = topNode.children[2].children[0]
        self.assertEqual(node.children[0].name, 'up')
        self.assertEqual(node.children[0].taskGroup.desc, 'doc/whats/up')
        self.assertEqual(len(node.children), 1)


    def test_cloneGraphPreconditions(self):
        repoNames, taskGroups = self.buildTaskGroups()
        topNode = build_taskgroup_dep_graph(taskGroups)
        addPreconditionsToTaskGroup(topNode)

        # check each precondition

        self.assertEqual(taskGroups[0].desc, 'dev')
        self.assertEqual(taskGroups[0].pre_condition, None)

        self.assertEqual(taskGroups[1].desc, 'dev/subdev1')
        self.assertEqual(taskGroups[1].pre_condition.task_group, taskGroups[0])

        self.assertEqual(taskGroups[2].desc, 'dev/subdev1/subdev1_sub1')
        self.assertEqual(taskGroups[2].pre_condition.task_group, taskGroups[1])

        self.assertEqual(taskGroups[3].desc, 'dev/subdev1/subdev1_sub2')
        self.assertEqual(taskGroups[3].pre_condition.task_group, taskGroups[1])

        self.assertEqual(taskGroups[4].desc, 'dev/subdev2')
        self.assertEqual(taskGroups[4].pre_condition.task_group, taskGroups[0])

        self.assertEqual(taskGroups[5].desc, 'dev/subdev2/toto/subdev2_sub1')
        self.assertEqual(taskGroups[5].pre_condition.task_group, taskGroups[4])

        self.assertEqual(taskGroups[6].desc, 'test')
        self.assertEqual(taskGroups[6].pre_condition, None)

        self.assertEqual(taskGroups[7].desc, 'test/extern/subtest1')
        self.assertEqual(taskGroups[7].pre_condition.task_group, taskGroups[6])

        self.assertEqual(taskGroups[8].desc, 'doc/whats/up')
        self.assertEqual(taskGroups[8].pre_condition, None)

        # TaskGroups:
        # - 'dev'
        # - 'dev/subdev1'
        # - 'dev/subdev1/subdev1_sub1'
        # - 'dev/subdev1/subdev1_sub2'
        # - 'dev/subdev2'
        # - 'dev/subdev2/toto/subdev2_sub1'
        # - 'test'
        # - 'test/extern/subtest1'
        # - 'doc/whats/up'


