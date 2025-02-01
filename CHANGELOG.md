MultiGit
========

*by Phlipppe Fremy <philippe.fremy@idemia.com>*

Introduction
------------

Multigit help users to manage many Git repositories simultaneously.

Version 1.6.1 (2025-02-01)
-----------------

Improvements

* Porting to Linux
* Add support for `gitk` and `git gui`
* Add CI for Linux and Windows on Github
* support cloning from url like: `fremy@host.xz:path/to/repo.git/`



Version 1.6.0 (2023-04-14)
-------------
First official release to the open source world!

Improvements:

* Using `Enter` on a repository triggers the same action as double-clicking it.
* Better about dialog, listing all open source components and licenses
* document multigit file format with a JSON schema


Bug fixes:

* Fix problem in branch/tag checkout
* it was impossible to create a branch with the name different only by case from another branch created in the past
* Do not hide the list of repositories when filtering in dialog switch/delete branch
* The settings dialog would not work when no config file exists
* When cloning nested repositories, ensure that nested clone starts even if top clone fails

Version 1.5 (2022-12-14)
-------------------------
New:

* Multigit uses multiple tabs
* Clone multigit file and Apply multigit file now follow dependency order of nested git repositories
* When checkouting a tag already on the current commit, force git to show the tag name
* In git switch branch, git delete branch, git checkout tag, show in a tooltip which repositories contain a branch/tag
* Show number of repositories and selected repositories in the status bar
* Add option to auto-fetch on startup
* Can choose repositories when using Git, custom command

Bug fixes:

* Ensure JSON multigit file is sorted when exporting
* No more "RunTimeError, C++ object already deleted"
* Deals better with corrupted configuration file
* Deals better with repositories deleted while showing the export to multigit dialog
* No more exceptions when multiple instances access the same log file
* avoids git complaining about branch with the same name as a directory by using argument '--' with checkout
* Better handling of scrolling in git execution window
* Better handling of abort requests
  

Version 1.4 (2022-06-03)
-------------------------
New:

* Multigit now exists in command-line: mgitcmd
* Branch without remote tracking branch: add tooltip for how to fix the situation
* Git push tags: choose which tag to push
* Git Revert: show the list of files being reverted
* Git Delete Branch: better control on which branch to delete (local vs remote)
* Git Delete Branch: can delete multiple branches
* Git authentication failure: warn user when git encounters too many authentication
  failures to avoid locking the user account.
* Installation: automatically uninstall previous version before installing a new one

Bug fixes:

* fix log not being written when configuration file is corrupted
* handles correctly path with characters ] and [
* better handling of git execution window
* do not allow cloning of ssh repositories with empty user name
* handle better the case where local branch can not be deleted because of unpushed commits
* fix *Git Switch Branch* to deal with multiple origins
* force Git to show the current tag when creating a new tag on an existing tag
* warn user before exporting unusable mgit files (empty url, local branches)


Version 1.3 (2022-01-27)
-------------------------

New funtionality

* Apply a multigit file to a directory
* When exporting to a multigit file, choice between exporting branches or a snapshot
* New column with remote URL (can be hidden)
* Configure visibility of SHA1 and URL column, of bottom tab Last Commit and Modified Files
* Git swtich can switch to branch and (new) to tag

Various bug fixes and small improvements:  

* fix username handling on clone url
* fix CSV and Multigit export for unicode branch names and repositories names
* fix sorting of repositories in clone/apply/export, make it case-insensitive
* switch branch, when branches are grouped by name, correctly display the selected branch name
* deal better with emtpy URL in multigit file
* branch filter is now case-insensitive


Version 1.2 (2021-12-20)
-------------------------
Main changes are:

* Menu to copy repository informations: url, branch name, tag, sha1
* Add buttons in main interface to switch base directory quickly
* When cloning over existing directories, tool can delete the directories or skip them


* Details of the changes
    * Bug correction
        * support branch names using unicode characters
        * Export to JSON and CSV is not done in alphabetical order 
        * Tool shows error message when a repository is deleted

    * Improvements
        * Better handling of existing directories when cloning
        * Add menu to copy SHA1, remote URL or full path
        * Open or switch base directory directly from main window
        * Better handling of existing directories when cloning
        * add ability to limit the maximum number of parallel git processes running
        * log git commands to a more readable file
        * log of git execution window can be copied to clipboard
        * Show the same menu in the menu bar and in the right-mouse click menu
        * Ask user to confirm when launching too many TortoiseGit actions
        * Git commit can recall previous commit messages
        * New column with SHA1
        * Add tooltip description to all menu items


Version 1.1.0 (2021-12-09)
--------------------------

* Bug correction
    * Git actions failed on large amount of repositories
    * Error on tracking remote repository for new created branch

* Improvements
    * progress bar when exporting to mulitgit file
    * Add tortoise git command to switch/checkout branch
    * Add Git switch branch command
    * Add Git delete branch command
    * Add Git commit command


Version 1.0.0 (2021-04-19)
--------------------------

* Project Configuration File
    * username removed from url
    * username used to clone is specified in UI
* Git programs need to be individually activated to be available
* Fix symlink management when opening directory and exporting project configuration file
* Fix git switch: replace git switch (not backward compatible) by git checkout


Version 0.8.0 (2021-04-09)
--------------------------
* Clone from configuration file
    * Improve cloning mecanism
    * fix if it is the first time (no last file)


Version 0.7.1 (2021-04-07)
---------------------------
* Fix TortoiseGit problem for repositories with space
* Speedup csv export by filling data asynchronously
* Fix export of empty repository
* Git execution window:
    * Improving handling of abort
    * Display progressive clone output  

Version 0.7.0 (2021-03-31)
--------------------------
* Bugfix: support for symlinks in working dir
* Create Project folder from multigit json configuration file (File menu)
    * List repositories 
    * Analyze the json file
    * Build the project in the specified directory
* Generate multigit json configuration file from opened directory (File menu)


Version 0.6.8 (2021-02-26)
--------------------------
* use a dedicated column and icon for showing that refresh is in progress
* refresh the selected repositories when switching back to window
* can run a custom git command
* git command execution: use fixed font and better indentation of results
* export CSV (warning, minor change of format)
    * can choose which fields to export
    * one column added to export the commit date
* bugfix: ESC during CSV export would crash
* columns "status" and "last remote synchro" are sorted using natural sort


Version 0.6.7 (2021-01-27)
--------------------------
* Show README and last changelog directly in the tool
* Refresh repository after closing Sublime Text or Source Tree
* Trigger the default action on a repo with enter
* limit size of log debug file
* shortcut F6 to fetch all
* bugfix: copy/paste icon from properties does not show up !
* fix bug: refresh all repo on F5 and not just the repo added
* fix bug: wrong repo opened by sublimemerge and sourcetree
* fix bug: exception when launching sublime merge and sourcetree
* refresh repository view automatically after execution of TortoiseGit or Git Bash
* fix bug: after launching TortoiseGit, an exception was sometimes raised, showing an exception dialog

Version 0.6.2 (2020-09-15)
---------------------------
* add git push --tags.
* mypy compliant 100%
* better handling of repos added and removed
* parallel execution of git jobs

Version 0.6 (2020-07-22)
-------------------------
* ability to create annotated tags.
* add Git Bash to the Git menu.
* add Tortoise Git Diff to menu.
* validation dialog before issuing git revert.
* export all repository status to a CSV file
* use colors for branch and tags.
* synchronise the view asynchronously
* remember last used repository upon startup
* small user interface improvements
* fixed a few bugs

Version 0.5 (2021-03-01)
-------------------------
* Fix execution from a directory with no access rights
* Configure action for double-click.
* Autocheck availability of TortoiseGit
* Disable TortoiseGit, SourceTree and SublimeMerge if not available
* Other small bug fixes

Version 0.4 (2020-01-07)
------------------------
* Can now launch some git commands directly on the repo: fetch, pull, push, revert, tag
* Add icons for Git and Tortoise Git operations
* Add copy button to properties
* add About dialog
* Add "show in explorer" functionality
* In repo properties, show all tags pointing to a given commit
* Show the synchro status with remote branche
* Add preference dialog to configure location of Git and TortoiseGit
* Deal better with the absence of Git or TortoiseGit

Version 0.3 (2019-11-27)
------------------------
* Add TortoiseGit actions on repositories
* Add a context menu
* Fix refresh action
* Add an icon
* limit size of the diff
* deal better with git diff generating invalid encodings
* colorize diff

Version 0.2 (2019-09-12)
-------------------------
* show last commit of the selected repo
* show diff status of modified files of the selected repo
* add property dialog
* avoid detection of non-git directories

Version 0.1 (2019-08-23)
-------------------------
* list all repos in a given directory, with their branch name and tags
