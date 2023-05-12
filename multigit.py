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


import platform
import sys, logging, datetime, tempfile, pathlib
import logging.handlers
import traceback as tb_module
from typing import Type, Optional
from types import TracebackType

from concurrent_log_handler import ConcurrentRotatingFileHandler

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2 import QtGui

import src.multigit_resources_rc        # uses side-effects to make resources available
from src.mg_window import MgMainWindow
from src import mg_const

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
Please report the problem to philippe.fremy@idemia.com and florent.oulieres@idemia.com
Please include the file log_multigit_debug.log which you can find in the menu About / Show Multigit log files .
''' % exc_msg )

    # do nothing else, it's enough already



# mandatory to avoid Python crashing on exceptions raised inside slots
app: Optional[ QApplication ] = None

def main_gui() -> None:
    global app
    app = QApplication([])
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/img/multigit-logo-256.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon.addPixmap(QtGui.QPixmap(":/img/multigit-logo-16.png"),  QtGui.QIcon.Normal, QtGui.QIcon.Off)
    app.setWindowIcon(icon)
    w = MgMainWindow(sys.argv)
    w.setWindowIcon(icon)
    w.show()

    app.exec_()

def is_writeable(fname: pathlib.Path) -> bool:
    '''Return true if file may be written'''
    try:
        with open(fname, 'a+') as _:
            pass
        return True
    except PermissionError:
        return False

def init_logging(debug_activated: bool = False, run_from_tests: bool = False) -> None:
    '''run_from_tests: when activated, a different logging filename is used
    debug_activated: when True, a lot more informaiton is written to a debug log file.
                     The feature is activated when the tool is launched with --debug
    '''
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

    # Make sure we are actually logging to a file which can be written
    try:
        if not mg_const.APPDATA_USER_MULTIGIT.exists():
            mg_const.APPDATA_USER_MULTIGIT.mkdir(parents=True)
        path_log_normal = mg_const.APPDATA_USER_MULTIGIT / fname_log_normal
        path_log_debug = mg_const.APPDATA_USER_MULTIGIT / fname_log_debug
        path_log_git_cmd = mg_const.APPDATA_USER_MULTIGIT / fname_log_git_cmd

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

    formatter = logging.Formatter('%(asctime)s %(name)15s:%(levelname)7s %(message)s')
    formatter.default_time_format = '%H:%M:%S'

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


    if path_log_normal:
        fhandler_info = ConcurrentRotatingFileHandler(str(path_log_normal), encoding='utf8', maxBytes=10_000_000, backupCount=5)
        fhandler_info.setLevel( logging.INFO )
        fhandler_info.setFormatter(formatter)
        logger.addHandler(fhandler_info)
        # ensure that git_cmd records are not propagated to root handlers
        fhandler_info.addFilter(lambda record: int(record.name != mg_const.LOGGER_GIT_CMD))

    if (path_log_debug and debug_activated):
        fhandler_dbg = ConcurrentRotatingFileHandler(str(path_log_debug), encoding='utf8', maxBytes=10_000_000, backupCount=5)
        fhandler_dbg.setLevel( logging.DEBUG )
        fhandler_dbg.setFormatter(formatter)
        logger.addHandler(fhandler_dbg)
        # ensure that git_cmd records are not propagated to root handlers
        fhandler_dbg.addFilter(lambda record: int(record.name != mg_const.LOGGER_GIT_CMD))

    if path_log_git_cmd:
        fhandler_git_cmd = ConcurrentRotatingFileHandler(str(path_log_git_cmd), encoding='utf8', maxBytes=10_000_000, backupCount=5)
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


if __name__ == '__main__':
    if '--version' in sys.argv:
        print('Multigit v%s' % mg_const.VERSION)
        print('Based on:')
        print('- python v%s' % platform.python_version())
        try:
            from PySide2.QtCore import qVersion
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
        from PySide2.QtCore import qVersion
        qt_version = 'v%s' % qVersion()
    except ImportError:
        qt_version = 'unknown'
    logging.info( 'Using Python v%s and Qt for Python %s' % (platform.python_version(), qt_version))
    main_gui()
    logging.info( 'Exit.' )
