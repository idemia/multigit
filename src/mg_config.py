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


from typing import List, TypeVar, Sequence, Optional, Any, Dict

import os, ast, sys
from pathlib import Path
from pprint import pformat
import logging, traceback
import datetime, shutil

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMessageBox, QApplication
from PySide2.QtGui import QColor

# keys for the configuration file
CONFIG_MAINWINDOW_GEOMETRY = 'MAINWINDOW_GEOMETRY'
CONFIG_LAST_OPENED = 'LAST_OPENED'
CONFIG_TABS_OPENED = 'CONFIG_TABS_OPENED'
CONFIG_TABS_CURRENT = 'CONFIG_TABS_CURRENT'
CONFIG_SPLITTER_STATE = 'SPLITTER_STATE'
CONFIG_SPLITTER_STATE_V2 = 'SPLITTER_STATE_V2'
CONFIG_GIT_AUTODETECT = 'CONFIG_GIT_AUTODETECT'
CONFIG_GIT_MANUAL_PATH = 'CONFIG_GIT_MANUAL_PATH'
CONFIG_TORTOISEGIT_AUTODETECT = 'CONFIG_TORTOISEGIT_AUTODETECT'
CONFIG_TORTOISEGIT_MANUAL_PATH = 'CONFIG_TORTOISEGIT_MANUAL_PATH'
CONFIG_TORTOISEGIT_ACTIVATED = 'CONFIG_TORTOISEGIT_ACTIVATED'
CONFIG_SOURCETREE_AUTODETECT = 'CONFIG_SOURCETREE_AUTODETECT'
CONFIG_SOURCETREE_MANUAL_PATH = 'CONFIG_SOURCETREE_MANUAL_PATH'
CONFIG_SOURCETREE_ACTIVATED = 'CONFIG_SOURCETREE_ACTIVATED'
CONFIG_SUBLIMEMERGE_AUTODETECT = 'CONFIG_SUBLIMEMERGE_AUTODETECT'
CONFIG_SUBLIMEMERGE_MANUAL_PATH = 'CONFIG_SUBLIMEMERGE_MANUAL_PATH'
CONFIG_SUBLIMEMERGE_ACTIVATED = 'CONFIG_SUBLIMEMERGE_ACTIVATED'
CONFIG_GITBASH_AUTODETECT = 'CONFIG_GITBASH_AUTODETECT'
CONFIG_GITBASH_MANUAL_PATH = 'CONFIG_GITBASH_MANUAL_PATH'
CONFIG_TAG_HISTORY = 'CONFIG_TAG_HISTORY'
CONFIG_GIT_CMD_HISTORY = 'CONFIG_GIT_CMD_HISTORY'
CONFIG_GIT_BRANCH_HISTORY = 'CONFIG_GIT_BRANCH_HISTORY'
CONFIG_DOUBLE_CLICK_ACTION = 'CONFIG_DOUBLE_CLICK_ACTION'
CONFIG_HEAD_COLOR_BRANCH = 'CONFIG_HEAD_COLOR_BRANCH'
CONFIG_HEAD_COLOR_TAG = 'CONFIG_HEAD_COlOR_TAG'
CONFIG_LAST_SHOWN_WHATISNEW = 'CONFIG_LAST_SHOWN_WHATISNEW'
CONFIG_LAST_MGIT_FILE = 'CONFIG_LAST_PROJECT_FILE'
CONFIG_LAST_PROJECT_DIR = 'CONFIG_LAST_PROJECT_DIR'
CONFIG_NB_GIT_PROC = 'CONFIG_NB_GIT_PROC'
CONFIG_LOG_DEBUG = 'CONFIG_LOG_DEBUG'
CONFIG_GIT_COMMIT_HISTORY = 'CONFIG_GIT_COMMIT_HISTORY'
CONFIG_VIEW_TAB_LAST_COMMIT = 'CONFIG_VIEW_TAB_LAST_COMMIT'
CONFIG_VIEW_TAB_MOD_FILES = 'CONFIG_VIEW_TAB_MOD_FILES'
CONFIG_VIEW_COL_SHA1 = 'CONFIG_VIEW_COL_SHA1'
CONFIG_VIEW_COL_URL = 'CONFIG_VIEW_COL_URL'
CONFIG_CLONE_USERNAME = 'CONFIG_CONFIG_CLONE_USERNAME'
CONFIG_FETCH_ON_STARTUP = 'CONFIG_FETCH_ON_STARTUP'

DEFAULT_CHECK_UPDATE_FREQUENCY = 30 # check every month

# Format is: 0xAARRGGBB with AA = alpha, RR = red, GG = green, BB = blue
DEFAULT_CONFIG_HEAD_COLOR_BRANCH = QColor(Qt.blue).rgb()
DEFAULT_CONFIG_HEAD_COLOR_TAG = QColor(Qt.darkCyan).rgb()

logger = logging.getLogger('mg_config')
dbg = logger.debug

__CONFIG_INSTANCE = None


def get_config_instance() -> 'MgConfig':
    '''Return an instance of the configuration of Multigit, with the default configuration path'''
    global __CONFIG_INSTANCE

    if sys.platform == 'win32':
        DEFAULT_CONFIG_PATH = Path(os.environ['USERPROFILE']) / 'AppData/Local/MultiGit/multigit.config'

    if __CONFIG_INSTANCE is None:
        __CONFIG_INSTANCE = MgConfig(str(DEFAULT_CONFIG_PATH))
        __CONFIG_INSTANCE.load()
    return __CONFIG_INSTANCE


class MgConfig:
    '''MultiGit configuration management'''

    def __init__(self, config_path: str):
        '''Set the configuration filename.
        '''
        self.config_dict: Dict[str, Any] = {}
        self.lru_dict: Dict[str, LRUList] = {}
        self.config_path = Path(config_path)
        self.do_not_save = False

    def load(self) -> None:
        '''Load configuration from the config location'''
        if not self.config_path.exists():
            # start from an empty configuration
            self.config_dict = {}
            return

        with open(self.config_path, 'r', encoding='utf8') as f:
            config_content = f.read()

        try:
            self.config_dict = ast.literal_eval(config_content)
            return
        except Exception as exc:
            self.do_not_save = True

        # we know that configuration loading failed
        logger.error(traceback.format_exc())
        self.config_dict = {}

        msg1 = 'Could not read configuration file'
        msg2 = ('Warning: unable to understand content of configuration file:\n%s\n\n' % self.config_path +
                'Configuration file will not be updated.\n'
                'Please report this to philippe.fremy@idemia.com\n'
                )

        logger.error(msg1)
        logger.error(msg2)

        # if QApplication exists, let's display a warning message
        if QApplication.instance():
            QMessageBox.warning(None, msg1, msg2 )

        invalidFileName = self.config_path.parent / \
                          ('multigit-invalid-config-file-%s.config' % datetime.datetime.now().isoformat().replace(':', '.'))

        msg2 = f'The invalid configuration file has been renamed to:\n{invalidFileName}\nPlease include this file when reporting the problem to philippe.fremy@idemia.com'
        try:
            shutil.move(str(self.config_path), invalidFileName)
            logger.error(msg2)
            if QApplication.instance():
                QMessageBox.warning(None, msg1, msg2)

            # corrupted config file is gone, let's create a new one
            self.do_not_save = False

        except OSError:
            try:
                shutil.copy(self.config_path, invalidFileName)
                logger.error(msg2)
                if QApplication.instance():
                    QMessageBox.warning(None, msg1, msg2)

                # corrupted config file is gone, let's create a new one
                self.do_not_save = False

            except OSError:
                logger.error('Unable to move or copy the faulty file')
                # we could not even copy the file, make sure it is not overwritten
                # by not allowing to save configuration
                pass

                msg2 = (f'To fix the configuration file, you can either open the configuration file and fix the syntax error.'
                       + f'Or you can simply erase the file, MultiGit will create a new empty configuration.\n'
                       + f'\nThe configuration file is :\n{self.config_path}'
                        )
                if QApplication.instance():
                    QMessageBox.warning(None, msg1, msg2)


    def save(self) -> None:
        '''Save configuration into the config location'''
        dbg('Saving config to %s' % self.config_path)
        if not self.config_path.parent.exists():
            self.config_path.parent.mkdir(parents=True)

        if self.do_not_save:
            # we don't want to write a config which we failed to read first, so skip silently
            return

        with open(self.config_path, 'w', encoding='utf8') as f:
            f.write(pformat(self.config_dict, indent=4, width=200))

    def __getitem__(self, config_key: str) -> Any:
        '''Return the content of the configuration key or None if the key does not exist.'''
        return self.config_dict.get(config_key)

    def get(self, config_key: str, default_value: Any = None) -> Any:
        '''Return the content of the configuration key or None if the key does not exist.'''
        return self.config_dict.get(config_key, default_value)

    def __setitem__(self, key: str, value: Any) -> None:
        '''Set a configuration key with a value'''
        if isinstance(value, Path):
            value = str(value)
        self.config_dict[key] = value


    def _lruCreateOrGet(self, config_key: str) -> 'LRUList':
        '''Create a LRU list for a given configuration entry on-demand, or return
        an existing one if it already exists'''
        if not config_key in self.lru_dict:
            value = self.get(config_key) or []
            self.lru_dict[config_key] = LRUList(value)
        return self.lru_dict[config_key]


    def lruGetFirst(self, config_key: str) -> Any:
        '''Return the last lru element of config key config_key'''
        return self._lruCreateOrGet(config_key).getFirst()


    def lruSetRecent(self, config_key: str, value: Any) -> None:
        '''Update the LRU entry for config_key with the given value'''
        lru = self._lruCreateOrGet(config_key)
        lru.setRecent(value)
        self.config_dict[config_key] = lru.asList()


    def lruAsList(self, config_key: str) -> List[Any]:
        '''Return the full content of the LRU entry config_key as a list'''
        return self._lruCreateOrGet(config_key).asList()


T = TypeVar('T')


class LRUList:
    def __init__(self, l: Sequence[T], maxSize: int = 20) -> None:
        self.maxSize = maxSize
        self._l: List[T] = []
        for v in reversed(l):
            # add them in reverse order, guarantee that no double are presents
            self.setRecent(v)

    def getFirst(self) -> Optional[T]:
        '''Return the first item of the LRU list, without modifying it.
        Returns None if the list is empty.'''
        if len(self._l):
            return self._l[0]
        else:
            return None

    def setRecent(self, v: T) -> None:
        # normally, there is zero or one copy
        assert (self._l.count(v) < 2)

        # remove previous instance if any
        if v in self._l:
            self._l.remove(v)

        self._l.insert(0, v)

        # ensure max size
        while len(self._l) > self.maxSize:
            self._l.pop()

    def asList(self) -> List[T]:
        return self._l[:]
