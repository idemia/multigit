# Getting started

Multigit is a graphical tool for working with projects composed of multiple git repositories.

Your first step should be to open a base directory.


## Opening a base directory

The first time you launch it, you should open a `base directory` containing multiple git repositories. 
You can do this from the menu `File > Open base directory` or by clicking on the `Open directory` icon in 
the top-right corner.

Once you have selected a base directory, Multigit will scan it for git repositories and display them in the main window.
Note that Multigit supports nested git repositories.

The base directory is remembered between sessions.


## List of repositories

Once you have a base directory, you see the full list of its repositories. The 
interest of Multigit is that in one glance, you can see the state of all your repositories.

For each git repository, you can see: 

* The name of the repository, relative to the base directory
* The git HEAD: either the branch name, the tag name of the commit hash if you are in detached HEAD state
* The modified status: `OK` for no files modified, or number of modified files and/or files in conflict
* The push/pull status: when on a branch with a remote tracking
  * `Up-to-date` if you have nothing to pull or push
  * `2 to pull` if you are 2 commits behind the remote,
  * `3 to push` if you are 3 commits ahead of the remote
  * `1 to push, 2 to pull` if you are 1 commit ahead of the remote, and 2 commits behind

  When you are not on a branch with a remote tracking, this column stays empty.

* The commit short SHA1 of the current commit
* The remote URL of the repository

You can click on the column headers to sort it. It is a convenient way to put on top the repostiories where
you need to perform some actions, like comitting modified files, or pushing commits.

From the list of repositories, you can perform git operations, which are detailed later.

If you remove or add repositories on the filesystem, you must refresh the list with `View > Refresh local view` or with `F5` for Multigit to detect the changes.



## Bottom pane

When you select a repository, the bottom pane is updated with:

* The last commit information on that repository
* The diff of the modified files

It helps to track what changes you currently have and if they need committing.


## Choosing what you view

Some of the columns of the repository list are optional. You can choose whether to show SHA1 and remot URL, from the menu `View > Show > Show Columns` or by right-clicking on the column headers and choosing which item to show.

You can also decide to hide the bottom panels, from the menu `View > Show > Show last commit panel` and 
`Show modified files panel`.


## Refresh

Most of the time, Multigit refreshes the status of the repositories when needed and you seldom have the need to explicitly request a refresh.
You can do it for the repository list or for selected repositories with `View > Refresh local view` or with `F5`. Refreshing the local view will
pickup added and removed repositories.

When you switch to another application and return to the Multigit window, it refreshed the status of the currently selected repositories. This
usually sufficient to pickup changes done in the other application, and avoid the need to refresh manually.


## Tabs

Multigit supports multiple tabs, each with its own base directory. You can open a new tab with `View > New tab` or with the right click
menu on the tab header. Select then a new
base directory for that tab. You can switch between tabs with `Ctrl+Tab` and `Ctrl+Shift+Tab`. Other tabs operations
available are: rename a tab, close a tab and duplicate a tab. You can also reorder the tabs by dragging and dropping them at a new position.

Tab operations are available from the menu `View` and from the right-click menu on the tab header.

Tab organization and content is saved between sessions.


## Interacting with your repositories

The strength of Multigit is to let you find very quickly which repositories need some actions, and to perform these 
actions on several repositories at once. For example, you can select all the repositories with modified files (by sorting 
on the column `Status`), and commit them in one click. Or you can select all the repositories on a given branch (by sorting on the HEAD), 
and switch them to another branch in one click.

The possible operations are:

* Open an explorer on the repository with `View > Show in explorer`
* Common git operations: 
  * Commit the files
  * Revert modified files
  * Push commits
  * Push tags
  * Pull
  * Fetch
  * Tag
  * Create a branch
  * Switch to a branch
  * Checkout a tag
  * Delete a branch
  * Delete a tag
  * Run a custom git command
* Showing all git properties of a repository
* Launching a GUI on a repository

The operation is launched on the selected repositories. You can select one or more repositories with the usual 
Ctrl+click , Shift+click and Ctrl+A.

The operations which do not require user input (like pull, fetch, push, ...) are launched immediately, the other
operations show a dialog to choose the parameters of the operation (which also let you adjust the repositories target).

Fetching repositories is such a common operation that Multigit provides a shortcut for fetching all repositories in the current tab
or fetching all repositories of all opened tabls. Check the first entries in the menu `Git` and the associated shortcuts. It is also
possible to fetch all repositories upon startup, check the settings dialog for that.

Every operation is accessble from the window top menu or from the right-click menu on the repository list.

The list of git operations is limited to what is commonly used, and don't provide all the possible flags, on purpose. Multigit
is not meant to be a full git client, but a tool to quickly perform the most common operations on multiple repositories at once.
If you feel that an important operation should be present though, please open an issue to request it. In the meantime, you can use the `Custom git command` operation to run any git command on the selected repositories.

Multigit also lets you run a git GUI on the selected repositories, which you can use to perform more complex operations. The list
of git GUIs is limited and can *not* be extended by the user as of today. This will evolve in the future to let the user add any GUI they want. In
the meantime, if you want your favorite git GUI to be available in Multigit, please open an issue to request it.

Multigit normally detects the git GUIs installed on your system. If it is not detected, you can configure it in the `File > Edit settings > External programs` menu. 


## Double-clicking

You can configure Multigit to perform a certain action when double-clicking on a repository. Most people like to launch their favorite git GUI.
Configuring the double-click action is done in the `File > Edit settings > Double-click` menu.


## Git repository selection in dialogs

For git operations which need more user parameters, Multigit launches a dialog to choose these parameters. These dialog always 
show the number and list of targeted repositories, and includes a button `Adjust repository list` to change this list.

The `Adjust repository list` dialog is composed of three parts:

* the bottom panel with the list of targeted repositories
* the top panel with the list of non-selected repositories
* the middle panel with the buttons to move repositories from one list to the other

You can use the buttons from the middle panel to add or remove repositories from the target list.

On the top panel, you can filter the list of non-selected repositories by typing a text in the filter field. The filter is applied on all
the columns.

This dialog gives you flexibility in refining the repository selection.


## Operation execution dialog

Git operations launched with Multigit are executed in parallel and visible in an execution dialog. The dialog shows one entry per repository,
in a tree view. The detailed of the operation is not visible by default, but you can expand the entry to see the different operations run 
on that repository. If you expand further, the actual git command and its output becomes visible.

An icon indicates the status of the operation on each repository:

* a dotted circle when the operations are running
* A green check mark when all operations have succeeded
* A question mark when a user interaction is needed 
* A red cross if at least one operation failed

If one operation fails in a repository, Multigit adds a question inside the
repository entry on what to do next:

* `Retry` to retry the failed operation. Useful when the failure is due to a temporary issue
* `Continue` to continue the next operations in the sequence
* `Abort` to stop all the next operations on that repository

An operation failing on one repository does not impact the operations running on the other repositories.

The right-click menu on a repository lets you copy the details of the operations on the clipboard. The `Copy log` button at the bottom lets you copy the full logs of all repositories to the clipboard.


## Copying git information

Multigit provides a menu to copy the most common needed git information to the clipboard: 

* repository path
* relative path to the base directory
* branch or tag name
* commit SHA1 (short or long)
* remote URL

This menu is available from the right-click menu on the repository list, and from the window top menu `View > Copy` submenu. 

You can also request the display of all git information with the `Git properties` operation, from the `Git` menu.


## Importing / Exporting repositories state

When working in a multi-repository project, sharing your exact project state becomes more challenging and more important task. Fortunately, 
Multigit makes this an easy process.


## Exporting the project state to a multigit file

Using the menu `File > Export to multigit file`, you can export the state of all repositories in the current tab to a multigit file. The
export dialog lets choose between exporting as a *project* or as a *snapshot*.

The *project mode*  lists all repositories, their remote url and their tags or branches. This is suitable for sharing
with somebody who needs to clone the repositories for the first time, and will work on some of the repositories, contribute to some branches.

The *snapshot mode* lists all repositories, their remote url and the exact commit each repository is on. This allows somebody
else to reproduce the exact same state for each repository, in detached HEAD mode. It is suitable for copying a specific state, usually
to reproduce a specific problem.

In both cases, the exported file a JSON file with the `.mgit` extension, containing all your repositories. The next paragraphs 
explain how to use it


## Cloning from a multigit file

When joining a multi-repository project, your first step is to clone all the repositories, positionned on the right branches and tags. 
This is where you need a multigit file, exported as a *project* . Use the menu `File > Clone from multigit file` to do this.

After choosing the multigit file and the destination directory, you can see in the bottom panel the list of repositories which are going
to be created and their exact destination and states.

Before actually cloning, you have two more informations to provide: the username and the clone behavior for existing directories. 
The username to use in the remote URL may work, or may need to be 
adjusted, especially if you are cloning with `ssh` protocol. You provide this information in the middle-left side part of the dialog.

The other information to provide is how to deal with existing directories. Git let's you clone only to non-existing directories. If you
have existing directories, this will prevent git from cloning successfully. Multigit can help though, by choosing what to do when facing an 
existing directory prior to cloning.

Note that if you have existing set of repositories and you want to reproduce your colleague state, cloning from a multigit file is not the 
right operation. It would delete all your work. What are looking for is the next section: *Applying a multigit file on existing repositories*.

The default behavior for cloning on existing directories is the safe one: let git fails on an existing directory, and the user 
shall manage the failure, or remove the existing 
directory himself before for example retrying the clone operation (this is possible to do during the execution of the clone operation). Multigit
also lets choose `skip directory`, meaning that this particular repository will not be cloned. The last option, `delete directory` must be used
carefully: Multigit will erase the directory before cloning. You may lose your existing work if used unwisely.

Whatever your choice, before executing the clone operation, Multigit will check if there are actual existing directories. If that's the
case, it will ask you to validate in a dialog, with the exact list of impacted repositories and an explicit description of your choice (fail, skip or delete).

Note that when you have nested repositories, Multigit reorders the clone operations to make sure that the nested repositories are not blocking
the cloning of the parent repository.


## Exporting to CSV

You can also export all your repositories states to a CSV file. Just use `File > Export to CSV`.  It will contain one line per 
repository, and one column per information: repository path, branch name, commit SHA1, url, ...


## Applying a multigit file on existing repositories

When you want to reproduce an exact repository state from a multigit file, you use the menu `File > Apply a multigit file` . This will go
over your repositories one by one and adjust the HEAD to the exact branch or tag described in the Multigit file. 

The dialog works mostly like the clone dialog, with about the same options.

When applying a multigit file, if a repository is listed
in the multigit file but missing in your base directory, it will be cloned. 

If a repository exists on the filesystem but is not listed in the
multigit file, Multigit lets you choose between deleting the directory on the filesystem (a risky operation) or keeping it. Be careful with
your answer to this question, or you may lose your work.


## Dealing with lots of repositories

When you are dealing with an important number of repositories (like more than fifty), Multigit can become unresponsive on the first launch
or after a complex operation. This is due to the important number of git processes launched in parallel to collect all the repository
information. 

To improve this situation, you can limit the maximum number of parallel git tasks running. In the `File > Settings` dialog,
edit the number of parallel running git processes from `unlimited` to  a reasonable amount, like 10.

The second thing you can do is reduce the number of columns displayed by Multigit: SHA1 column and URL column are optional, and they do trigger
one git process each to be updated. Hiding them should help.

Multigit will improve with this situation in the future.


# Conclusion

I hope this little documentation helped you get a grip on Multigit. Don't hesitate to report positive feedback and issues on 
the Github page