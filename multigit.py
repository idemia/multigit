#!/usr/bin/env python

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

import os
import platform
import sys, logging, datetime, tempfile, pathlib
import logging.handlers
import traceback as tb_module
from typing import Type, Optional
from types import TracebackType

from concurrent_log_handler import ConcurrentRotatingFileHandler

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6 import QtGui

if __package__:
    # when running inside a package, src/* is not on the path, only multigit_gx is.
    # we must add it explicitely
    path = os.path.dirname(__file__)
    sys.path.insert(0, path)

import src.multigit_resources_rc        # uses side-effects to make resources available
from src.mg_window import MgMainWindow
from src import mg_const
from src.mg_tools import isRunningInsideFlatpak

# by default Qt abort on Python exceptions so we need to provide
# our own hook that does the job
def handle_exception(type_: Type[BaseException], value: BaseException, traceback: Optional[TracebackType]) -> None:
    # note: the argument names have to have the same name as in the stdlib
    # else mypy will complain.
    if issubclass(type_, KeyboardInterrupt) and traceback is not None:
        sys.__excepthook__(type_, value, traceback)
        return

    # yeah ... logging also raises exceptions sometimes...
    # noinspection PyBroadException
    try:
        logging.error("Uncaught exception", exc_info=(type_, value, traceback))
    except Exception:
        pass

    if app:
        exc_msg = ''.join( tb_module.format_exception(type_, value, traceback) )
        # noinspection PyTypeChecker
        QMessageBox.critical(None, 'Fatal error',
'''A fatal error occured:
%s\n
Please report the problem on opening an issue on https://github.com/idemia/multigit/ .
Please include the file log_multigit_debug.log which you can find in the menu About / Show Multigit log files .
''' % exc_msg )

    # do nothing else, it's enough already



# mandatory to avoid Python crashing on exceptions raised inside slots
app: Optional[ QApplication ] = None

def main_gui() -> None:
    global app
    app = QApplication([])
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/img/multigit-logo-256.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    icon.addPixmap(QtGui.QPixmap(":/img/multigit-logo-16.png"),  QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    app.setWindowIcon(icon)
    w = MgMainWindow(sys.argv)
    w.setWindowIcon(icon)
    w.show()

    app.exec()

def is_writeable(fname: pathlib.Path) -> bool:
    '''Return true if file may be written'''
    try:
        with open(fname, 'a+') as _:
            pass
        return True
    except PermissionError:
        return False


def configure_logpath(debug_activated: bool = False, run_from_tests: bool = False) -> None:
    '''Creates the log path in mg_const according to platform and ability to write to directory'''

    if run_from_tests:
        fname_log_normal = 'log_tests_multigit.log'
        fname_log_debug = 'log_tests_multigit_debug.log'
        fname_log_git_cmd = 'log_tests_git_cmd.log'
    else:
        fname_log_normal = 'log_multigit.log'
        fname_log_debug  = 'log_multigit_debug.log'
        fname_log_git_cmd = 'log_git_cmd.log'

    path_log_normal: Optional[pathlib.Path]
    path_log_debug: Optional[pathlib.Path]
    path_log_git_cmd: Optional[pathlib.Path]

    if sys.platform == 'win32':
        multigit_log_dir = pathlib.Path(os.environ['USERPROFILE']) / 'AppData/Local/MultiGit/'
    else:
        # See https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
        xdg_config_home: str
        if os.environ.get('XDG_CONFIG_HOME', ''):
            xdg_config_home = os.environ['XDG_CONFIG_HOME']
        else:
            xdg_config_home = os.path.expanduser('~/.config')

        multigit_log_dir = pathlib.Path(xdg_config_home) / 'Multigit'

    # Make sure we are actually logging to a file which can be written
    try:
        if not multigit_log_dir.exists():
            multigit_log_dir.mkdir(parents=True)
        path_log_normal = multigit_log_dir / fname_log_normal
        path_log_debug = multigit_log_dir / fname_log_debug
        path_log_git_cmd = multigit_log_dir / fname_log_git_cmd

        if not is_writeable(path_log_normal) and is_writeable(path_log_debug):
            raise PermissionError('Can not create log file in location %s' % path_log_normal)
    except PermissionError:
        # is raised either by the mkdir() or the is_writeable() check
        # try yet another location
        temp_dir = pathlib.Path(tempfile.gettempdir())
        path_log_normal = temp_dir / fname_log_normal
        path_log_debug = temp_dir / fname_log_debug
        path_log_git_cmd = temp_dir / fname_log_git_cmd

        if not is_writeable(path_log_normal) and is_writeable(path_log_debug):
            # Desesperate case, do not create logs
            path_log_normal = None
            path_log_debug = None
            path_log_git_cmd = None

    mg_const.PATH_LOG_NORMAL = path_log_normal
    mg_const.PATH_LOG_DEBUG = path_log_debug
    mg_const.PATH_LOG_GIT_CMD = path_log_git_cmd

def init_logging(debug_activated: bool = False, run_from_tests: bool = False) -> None:
    '''run_from_tests: when activated, a different logging filename is used
    debug_activated: when True, a lot more informaiton is written to a debug log file.
                     The feature is activated when the tool is launched with --debug
        '''
    configure_logpath(debug_activated, run_from_tests)

    formatter = logging.Formatter('%(asctime)s %(name)15s:%(levelname)7s %(message)s')

    logger = logging.getLogger()

    # root log receives logging from all the tool
    # root log distributes log to:
    #   log file normal handler:
    #       filtered on level >= info
    #       exclude logger git command
    #   log file debug  handler: filtered on level debug
    #       filtered on level >= debug
    #       exclude logger git command
    #   stderr:
    #       filtered on level >= debug if in debug mode, >= info else
    #       exclude logger git command

    # configuration allows logging of debug messages
    if debug_activated:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


    if mg_const.PATH_LOG_NORMAL:
        fhandler_info = ConcurrentRotatingFileHandler(str(mg_const.PATH_LOG_NORMAL), encoding='utf8', maxBytes=10_000_000, backupCount=5)
        fhandler_info.setLevel( logging.INFO )
        fhandler_info.setFormatter(formatter)
        logger.addHandler(fhandler_info)
        # ensure that git_cmd records are not propagated to root handlers
        fhandler_info.addFilter(lambda record: record.name != mg_const.LOGGER_GIT_CMD)

    if (mg_const.PATH_LOG_DEBUG and debug_activated):
        fhandler_dbg = ConcurrentRotatingFileHandler(str(mg_const.PATH_LOG_DEBUG), encoding='utf8', maxBytes=10_000_000, backupCount=5)
        fhandler_dbg.setLevel( logging.DEBUG )
        fhandler_dbg.setFormatter(formatter)
        logger.addHandler(fhandler_dbg)
        # ensure that git_cmd records are not propagated to root handlers
        fhandler_dbg.addFilter(lambda record: record.name != mg_const.LOGGER_GIT_CMD)

    if mg_const.PATH_LOG_GIT_CMD:
        fhandler_git_cmd = ConcurrentRotatingFileHandler(str(mg_const.PATH_LOG_GIT_CMD), encoding='utf8', maxBytes=10_000_000, backupCount=5)
        fhandler_git_cmd.setLevel( logging.DEBUG )
        fhandler_git_cmd.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        logger_git_cmd = logging.getLogger(mg_const.LOGGER_GIT_CMD)
        logger_git_cmd.addHandler(fhandler_git_cmd)


    shandler_err = logging.StreamHandler(sys.stderr)
    if debug_activated:
        shandler_err.setLevel( logging.DEBUG )
    else:
        shandler_err.setLevel( logging.INFO )
    logger.addHandler(shandler_err)
    shandler_err.setFormatter(formatter)

    logging.info('log paths: ')
    logging.info(mg_const.PATH_LOG_DEBUG)
    logging.info(mg_const.PATH_LOG_NORMAL)


def main() -> None:
    if '--version' in sys.argv:
        print('Multigit v%s' % mg_const.VERSION)
        print('Based on:')
        print('- python v%s' % platform.python_version())
        try:
            from PySide6.QtCore import qVersion
            print('- Qt for Python v' + qVersion())
        except ImportError:
            print('- Qt for Python version not available')
        sys.exit(0)

    # to avoid crashes when Python exceptions are raised inside Qt slots
    sys.excepthook = handle_exception
    # sys.argv.append('--debug')
    debug_activated = False
    if '--debug' in sys.argv:
        debug_activated = True
        del sys.argv[sys.argv.index('--debug')]
    init_logging(debug_activated=debug_activated, run_from_tests=False)
    logging.info( 'Starting multigit v%s on %s' % (mg_const.VERSION, datetime.datetime.now().isoformat(sep=' ', timespec='seconds') ))
    try:
        from PySide6.QtCore import qVersion
        qt_version = 'v%s' % qVersion()
    except ImportError:
        qt_version = 'unknown'
    logging.info( 'Using Python v%s and Qt for Python %s' % (platform.python_version(), qt_version))
    if isRunningInsideFlatpak():
        logging.debug('Running inside flatpak container')
    main_gui()
    logging.info( 'Exit.' )


if __name__ == '__main__':
    main()

