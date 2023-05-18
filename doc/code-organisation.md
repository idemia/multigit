Code organisation
=================

Directories
-----------
* doc: general documentation
* src: all the code source of MultiGit Open Source
* src/gui: all the .ui files used by designer, and the generated .py files
           They are converted into .py files using:
               ./generate_ui.bat
* images: all the images used by MultiGit in various formats.
          They are converted into Qt resource file using:
              ./generate_resource.bat


Files:
------
* README.md: description of the software and of each release changes
* multigit.py: the launcher for multigit graphical version
* mgitcmd.py: the launcher for multigit command-line version
* test_multigit.py: test file for running tests on MultiGit (there are not so many...)
* mypy.ini: file defining the settings for running Type Annotations

(source code)
* src/*.py : all the code
* src/gui/*.ui : the Qt Designer files
* src/gui/ui_*.py : the files generated by Qt pyuic from the designer file
* src/gui/*.py  : python files generated from CHANGELOG.md and FULL_LICENSING_INFORMATION.md
* src/gui/generate_ui.bat :
      Batch file to build all the python file from Qt Designer UI files.
      Note that it optimizes by only regenerating what is needed (Makefile style) and that
      it adds very minimal type annotations to the generated files.

(file generation)
* generate_ui.bat: calls the src/gui/generate_ui.bat to generate all python files from ui files
* images/generate_resource.bat: calls the images/generate_resources.bat to generate the resource file
                         multigit_resource_rc.py from the images/multigit_resources.qrc
* generate_html_whatsnew.py: converts the README.md into src/gui/content_whatisnew.py so
                             that the README content can be shown by MultiGit
                             This is typically done during the release process

(packageing related stuff)
* packaging/multigit.spec: file used by pyinstaller to generate the .exe
                 This file is modified from the default spec file to remove some unneeded DLL
* packaing/Multigit.iss: used by InnoSetup to generate the installer
* packaing/package_exe.bat: generate a .exe using pyinstaller in dist/multigit/
* packaing/package_installer.bat: generate an installer from the content of dist/multigit



Coding styleguide
=================
* PEP8 is a good idea but not mandatory, except for the items listed next
* classes names use CamelCase and start with Mg.
        Example: MgDialogSelectRepo
* function names start with lower case and use either camelCase or snake case:
        Example: exportToMgit(), update_label()
* all functions are type-annotated. See mypy documentation for a better understanding of type annotations.
  The project should pass fine with running: mypy .
* files containing dialogs are named: mg_dialog_something.py
* classes implementing dialogs are named MgDialogSomething
* constants generic for the software are stored in the mg_const.py . This includes:
    * version of the product
    * some important ui messages
* imports:
    * imports are grouped by category
    * First group of import are typing related import, using "from typing import ..."
      Example: from typing import List
    * Second group of import are python library related import, possibly grouped on one line.
        Example: import os, sys, subprocess
    * Third group of import are PyQt library related import. We import directly and explicitely the class
      we use:
        Example:
            from PySide2.QtWidgets import QMainWindow, QPushButton
            from PySide2.QtCore import Qt
    * Fourth and last group, the import from multigit, all related  to the base directory.
        Example:
            from src.gui.ui_select_repos import Ui_SelectRepos
            from src.mg_repo_tree_item import MgRepoTreeItem


Code insights
=============

Call graph for different situations:
------------------------------------
Goal is to check that we use always one code path for completing/aborting tasks.

* MgExecTask:
    * is_task_done(): return self.task_state in (TaskState.Successful, TaskState.Errored)
    * is_task_started(): return self.task_state in (TaskState.Started, TaskState.Successful, TaskState.Errored)
  
* MgExecTaskGroup:
    * self.tasks: List[MgExecTask]
    * is_started(): one of the tasks returns True to is_started()
    * is_finished(): all tasks returns True to is_task_done()

* MgExecItemOneCmd
    * self.task:  MgExecTask
    * self.task.sig_task_done() -> slotTaskDone() -> self.cb_exec_done()
    * job completes successfully -> slotTaskDone(True)
    * job completes with error -> slotTaskDone(False)
    * job is aborted after end -> nothing, slotTaskDone(True/False) was already called
    * job is aborted before end -> self.abortRequested=True + task.abort()  -> slotTaskDone(False)


* MgExecItemMultiCmd
    * self.taskGroup: MgExecTaskGroup
    * isDone(): return self.nbCmdDone == len(self.taskGroup) or self.abortRequested
    * slotOneCmdDone()
        * all job complete successfully -> allCmdDone() -> MgExecWindow.oneMoreJobDone(True)
        * one job fails -> nbError += 1 
            * askQuestionAfterCmdFailed() + question
                * user aborts or abortRequested
                    * allCmdDone() ->  MgExecWindow.oneMoreJobDone(False)
                * user retries
                    * nbError -= 1, nbJobsDone -= 1
                    * runOneCmdLine()
                        * success -> slotallCmdDone() -> MgExecWindow.oneMoreJobDone(True)
                        * failure -> back to slotOneCmdDone()
                * user continue
                    * runOneCmdLine()
                        * slotOneCmdDone()
                            * success -> slotallCmdDone() -> MgExecWindow.oneMoreJobDone(False) because there was still one error
                            * failure -> back to slotOneCmdDone() above
                * user ok
                    * allCmdDone() ->  MgExecWindow.oneMoreJobDone(False)
    * abortItem()
        * self.abortRequested = True
        * if question pending (if buttonBar is not None)
            * abort the question like a user would do: self.handleQuestionResult(UserActionOnGitError.ABORT)
                * allCmdDone() ->  MgExecWindow.oneMoreJobDone(False)
        * if all jobs done
            * we don't care that abort was requested, everything is already finished
            * self.abortRequested = False
            * return
        * if self.isStarted == False, no job started -> allCmdDone() ->  MgExecWindow.oneMoreJobDone(False)
        * some job was started, and we are aborting
            * abort the job in progress 
                * -> one job in the middle fails -> see above
                * -> job succeeds before it is aborted -> slotOneCmdDone()


Testing:
========
Test coverage is limited to MgRepoInfo mostly.

- run unit-test with:

    python test_multigit.py
  
- run type-annotations test with:

    mypy .

Manual tests
============

GitExecWindow:
- run git tag -> execTaskGroup()
- run git fetch -> execOneGitCommand()