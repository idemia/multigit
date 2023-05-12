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


from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.mg_window import MgMainWindow
    from src.mg_repo_tree import MgRepoTree
    from src.mg_dialog_clone_from_mgit import MgDialogCloneFromMgitFile


class MgPluginManager:

    def __init__(self) -> None:
        self.idemiaPlugin = None

    def registerIdemiaPlugin(self, idemiaPlugin: Any) -> None:
        self.idemiaPlugin = idemiaPlugin

    def setupTopMenu(self, window: 'MgMainWindow') -> None:
        '''Called during init of the actions and menus of the top window'''
        if not self.idemiaPlugin:
            return

        self.idemiaPlugin.setupTopMenu(window)

    def setupRepoRmbMenu(self, repoTree: 'MgRepoTree') -> None:
        '''Called when each MgRepoTree prepares his RMB menu'''
        if not self.idemiaPlugin:
            return

        self.idemiaPlugin.setupRepoRmbMenu(repoTree)


    def setupCloneDialog(self, cloneDialog: 'MgDialogCloneFromMgitFile') -> None:
        '''Called when preparing the clone Dialog'''
        if not self.idemiaPlugin:
            return

        self.idemiaPlugin.setupCloneDialog(cloneDialog)


pluginMgrInstance = MgPluginManager()

try:
    from idemia import idemia_plugin        # type: ignore[import]
    pluginMgrInstance.registerIdemiaPlugin(idemia_plugin.MgIdemiaPlugin())
except ImportError as exc:
    if not 'idemia' in str(exc):
        # this is an import error, but not for the idemia plugin
        # we should report it !
        raise



