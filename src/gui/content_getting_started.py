# Generated from getting_started.md on 2026-04-19 09:58:48.789788


content_html = '''
<h1 align="center">Getting started</h1>

<p>Multigit is a graphical tool for working with projects composed of multiple git repositories.</p>

<p>Your first step should be to open a base directory.</p>

<h2>Opening a base directory</h2>

<p>The first time you launch it, you should open a <code><span style="background-color:#f5f5f5;">base directory</span></code> containing multiple git repositories. 
You can do this from the menu <code><span style="background-color:#f5f5f5;">File &gt; Open base directory</span></code> or by clicking on the <code><span style="background-color:#f5f5f5;">Open directory</span></code> icon in 
the top-right corner.</p>

<p>Once you have selected a base directory, Multigit will scan it for git repositories and display them in the main window.
Note that Multigit supports nested git repositories.</p>

<p>The base directory is remembered between sessions.</p>

<h2>List of repositories</h2>

<p>Once you have a base directory, you see the full list of its repositories. The 
interest of Multigit is that in one glance, you can see the state of all your repositories.</p>

<p>For each git repository, you can see: </p>

<ul>
<li>The name of the repository, relative to the base directory</li>
<li>The git HEAD: either the branch name, the tag name of the commit hash if you are in detached HEAD state</li>
<li>The modified status: <code><span style="background-color:#f5f5f5;">OK</span></code> for no files modified, or number of modified files and/or files in conflict</li>
<li><p>The push/pull status: when on a branch with a remote tracking</p>

<ul>
<li><code><span style="background-color:#f5f5f5;">Up-to-date</span></code> if you have nothing to pull or push</li>
<li><code><span style="background-color:#f5f5f5;">2 to pull</span></code> if you are 2 commits behind the remote,</li>
<li><code><span style="background-color:#f5f5f5;">3 to push</span></code> if you are 3 commits ahead of the remote</li>
<li><code><span style="background-color:#f5f5f5;">1 to push, 2 to pull</span></code> if you are 1 commit ahead of the remote, and 2 commits behind</li>
</ul>

<p>When you are not on a branch with a remote tracking, this column stays empty.</p></li>
<li><p>The commit short SHA1 of the current commit</p></li>
<li>The remote URL of the repository</li>
</ul>

<p>You can click on the column headers to sort it. It is a convenient way to put on top the repostiories where
you need to perform some actions, like comitting modified files, or pushing commits.</p>

<p>From the list of repositories, you can perform git operations, which are detailed later.</p>

<p>If you remove or add repositories on the filesystem, you must refresh the list with <code><span style="background-color:#f5f5f5;">View &gt; Refresh local view</span></code> or with <code><span style="background-color:#f5f5f5;">F5</span></code> for Multigit to detect the changes.</p>

<h2>Bottom pane</h2>

<p>When you select a repository, the bottom pane is updated with:</p>

<ul>
<li>The last commit information on that repository</li>
<li>The diff of the modified files</li>
</ul>

<p>It helps to track what changes you currently have and if they need committing.</p>

<h2>Choosing what you view</h2>

<p>Some of the columns of the repository list are optional. You can choose whether to show SHA1 and remot URL, from the menu <code><span style="background-color:#f5f5f5;">View &gt; Show &gt; Show Columns</span></code> or by right-clicking on the column headers and choosing which item to show.</p>

<p>You can also decide to hide the bottom panels, from the menu <code><span style="background-color:#f5f5f5;">View &gt; Show &gt; Show last commit panel</span></code> and 
<code><span style="background-color:#f5f5f5;">Show modified files panel</span></code>.</p>

<h2>Refresh</h2>

<p>Most of the time, Multigit refreshes the status of the repositories when needed and you seldom have the need to explicitly request a refresh.
You can do it for the repository list or for selected repositories with <code><span style="background-color:#f5f5f5;">View &gt; Refresh local view</span></code> or with <code><span style="background-color:#f5f5f5;">F5</span></code>. Refreshing the local view will
pickup added and removed repositories.</p>

<p>When you switch to another application and return to the Multigit window, it refreshed the status of the currently selected repositories. This
usually sufficient to pickup changes done in the other application, and avoid the need to refresh manually.</p>

<h2>Tabs</h2>

<p>Multigit supports multiple tabs, each with its own base directory. You can open a new tab with <code><span style="background-color:#f5f5f5;">View &gt; New tab</span></code> or with the right click
menu on the tab header. Select then a new
base directory for that tab. You can switch between tabs with <code><span style="background-color:#f5f5f5;">Ctrl+Tab</span></code> and <code><span style="background-color:#f5f5f5;">Ctrl+Shift+Tab</span></code>. Other tabs operations
available are: rename a tab, close a tab and duplicate a tab. You can also reorder the tabs by dragging and dropping them at a new position.</p>

<p>Tab operations are available from the menu <code><span style="background-color:#f5f5f5;">View</span></code> and from the right-click menu on the tab header.</p>

<p>Tab organization and content is saved between sessions.</p>

<h2>Interacting with your repositories</h2>

<p>The strength of Multigit is to let you find very quickly which repositories need some actions, and to perform these 
actions on several repositories at once. For example, you can select all the repositories with modified files (by sorting 
on the column <code><span style="background-color:#f5f5f5;">Status</span></code>), and commit them in one click. Or you can select all the repositories on a given branch (by sorting on the HEAD), 
and switch them to another branch in one click.</p>

<p>The possible operations are:</p>

<ul>
<li>Open an explorer on the repository with <code><span style="background-color:#f5f5f5;">View &gt; Show in explorer</span></code></li>
<li>Common git operations: 
<ul>
<li>Commit the files</li>
<li>Revert modified files</li>
<li>Push commits</li>
<li>Push tags</li>
<li>Pull</li>
<li>Fetch</li>
<li>Tag</li>
<li>Create a branch</li>
<li>Switch to a branch</li>
<li>Checkout a tag</li>
<li>Delete a branch</li>
<li>Delete a tag</li>
<li>Run a custom git command</li>
</ul></li>
<li>Showing all git properties of a repository</li>
<li>Launching a GUI on a repository</li>
</ul>

<p>The operation is launched on the selected repositories. You can select one or more repositories with the usual 
Ctrl+click , Shift+click and Ctrl+A.</p>

<p>The operations which do not require user input (like pull, fetch, push, ...) are launched immediately, the other
operations show a dialog to choose the parameters of the operation (which also let you adjust the repositories target).</p>

<p>Fetching repositories is such a common operation that Multigit provides a shortcut for fetching all repositories in the current tab
or fetching all repositories of all opened tabls. Check the first entries in the menu <code><span style="background-color:#f5f5f5;">Git</span></code> and the associated shortcuts. It is also
possible to fetch all repositories upon startup, check the settings dialog for that.</p>

<p>Every operation is accessble from the window top menu or from the right-click menu on the repository list.</p>

<p>The list of git operations is limited to what is commonly used, and don't provide all the possible flags, on purpose. Multigit
is not meant to be a full git client, but a tool to quickly perform the most common operations on multiple repositories at once.
If you feel that an important operation should be present though, please open an issue to request it. In the meantime, you can use the <code><span style="background-color:#f5f5f5;">Custom git command</span></code> operation to run any git command on the selected repositories.</p>

<p>Multigit also lets you run a git GUI on the selected repositories, which you can use to perform more complex operations. The list
of git GUIs is limited and can <em>not</em> be extended by the user as of today. This will evolve in the future to let the user add any GUI they want. In
the meantime, if you want your favorite git GUI to be available in Multigit, please open an issue to request it.</p>

<p>Multigit normally detects the git GUIs installed on your system. If it is not detected, you can configure it in the <code><span style="background-color:#f5f5f5;">File &gt; Edit settings &gt; External programs</span></code> menu. </p>

<h2>Double-clicking</h2>

<p>You can configure Multigit to perform a certain action when double-clicking on a repository. Most people like to launch their favorite git GUI.
Configuring the double-click action is done in the <code><span style="background-color:#f5f5f5;">File &gt; Edit settings &gt; Double-click</span></code> menu.</p>

<h2>Git repository selection in dialogs</h2>

<p>For git operations which need more user parameters, Multigit launches a dialog to choose these parameters. These dialog always 
show the number and list of targeted repositories, and includes a button <code><span style="background-color:#f5f5f5;">Adjust repository list</span></code> to change this list.</p>

<p>The <code><span style="background-color:#f5f5f5;">Adjust repository list</span></code> dialog is composed of three parts:</p>

<ul>
<li>the bottom panel with the list of targeted repositories</li>
<li>the top panel with the list of non-selected repositories</li>
<li>the middle panel with the buttons to move repositories from one list to the other</li>
</ul>

<p>You can use the buttons from the middle panel to add or remove repositories from the target list.</p>

<p>On the top panel, you can filter the list of non-selected repositories by typing a text in the filter field. The filter is applied on all
the columns.</p>

<p>This dialog gives you flexibility in refining the repository selection.</p>

<h2>Operation execution dialog</h2>

<p>Git operations launched with Multigit are executed in parallel and visible in an execution dialog. The dialog shows one entry per repository,
in a tree view. The detailed of the operation is not visible by default, but you can expand the entry to see the different operations run 
on that repository. If you expand further, the actual git command and its output becomes visible.</p>

<p>An icon indicates the status of the operation on each repository:</p>

<ul>
<li>a dotted circle when the operations are running</li>
<li>A green check mark when all operations have succeeded</li>
<li>A question mark when a user interaction is needed </li>
<li>A red cross if at least one operation failed</li>
</ul>

<p>If one operation fails in a repository, Multigit adds a question inside the
repository entry on what to do next:</p>

<ul>
<li><code><span style="background-color:#f5f5f5;">Retry</span></code> to retry the failed operation. Useful when the failure is due to a temporary issue</li>
<li><code><span style="background-color:#f5f5f5;">Continue</span></code> to continue the next operations in the sequence</li>
<li><code><span style="background-color:#f5f5f5;">Abort</span></code> to stop all the next operations on that repository</li>
</ul>

<p>An operation failing on one repository does not impact the operations running on the other repositories.</p>

<p>The right-click menu on a repository lets you copy the details of the operations on the clipboard. The <code><span style="background-color:#f5f5f5;">Copy log</span></code> button at the bottom lets you copy the full logs of all repositories to the clipboard.</p>

<h2>Copying git information</h2>

<p>Multigit provides a menu to copy the most common needed git information to the clipboard: </p>

<ul>
<li>repository path</li>
<li>relative path to the base directory</li>
<li>branch or tag name</li>
<li>commit SHA1 (short or long)</li>
<li>remote URL</li>
</ul>

<p>This menu is available from the right-click menu on the repository list, and from the window top menu <code><span style="background-color:#f5f5f5;">View &gt; Copy</span></code> submenu. </p>

<p>You can also request the display of all git information with the <code><span style="background-color:#f5f5f5;">Git properties</span></code> operation, from the <code><span style="background-color:#f5f5f5;">Git</span></code> menu.</p>

<h2>Importing / Exporting repositories state</h2>

<p>When working in a multi-repository project, sharing your exact project state becomes more challenging and more important task. Fortunately, 
Multigit makes this an easy process.</p>

<h2>Exporting the project state to a multigit file</h2>

<p>Using the menu <code><span style="background-color:#f5f5f5;">File &gt; Export to multigit file</span></code>, you can export the state of all repositories in the current tab to a multigit file. The
export dialog lets choose between exporting as a <em>project</em> or as a <em>snapshot</em>.</p>

<p>The <em>project mode</em>  lists all repositories, their remote url and their tags or branches. This is suitable for sharing
with somebody who needs to clone the repositories for the first time, and will work on some of the repositories, contribute to some branches.</p>

<p>The <em>snapshot mode</em> lists all repositories, their remote url and the exact commit each repository is on. This allows somebody
else to reproduce the exact same state for each repository, in detached HEAD mode. It is suitable for copying a specific state, usually
to reproduce a specific problem.</p>

<p>In both cases, the exported file a JSON file with the <code><span style="background-color:#f5f5f5;">.mgit</span></code> extension, containing all your repositories. The next paragraphs 
explain how to use it</p>

<h2>Cloning from a multigit file</h2>

<p>When joining a multi-repository project, your first step is to clone all the repositories, positionned on the right branches and tags. 
This is where you need a multigit file, exported as a <em>project</em> . Use the menu <code><span style="background-color:#f5f5f5;">File &gt; Clone from multigit file</span></code> to do this.</p>

<p>After choosing the multigit file and the destination directory, you can see in the bottom panel the list of repositories which are going
to be created and their exact destination and states.</p>

<p>Before actually cloning, you have two more informations to provide: the username and the clone behavior for existing directories. 
The username to use in the remote URL may work, or may need to be 
adjusted, especially if you are cloning with <code><span style="background-color:#f5f5f5;">ssh</span></code> protocol. You provide this information in the middle-left side part of the dialog.</p>

<p>The other information to provide is how to deal with existing directories. Git let's you clone only to non-existing directories. If you
have existing directories, this will prevent git from cloning successfully. Multigit can help though, by choosing what to do when facing an 
existing directory prior to cloning.</p>

<p>Note that if you have existing set of repositories and you want to reproduce your colleague state, cloning from a multigit file is not the 
right operation. It would delete all your work. What are looking for is the next section: <em>Applying a multigit file on existing repositories</em>.</p>

<p>The default behavior for cloning on existing directories is the safe one: let git fails on an existing directory, and the user 
shall manage the failure, or remove the existing 
directory himself before for example retrying the clone operation (this is possible to do during the execution of the clone operation). Multigit
also lets choose <code><span style="background-color:#f5f5f5;">skip directory</span></code>, meaning that this particular repository will not be cloned. The last option, <code><span style="background-color:#f5f5f5;">delete directory</span></code> must be used
carefully: Multigit will erase the directory before cloning. You may lose your existing work if used unwisely.</p>

<p>Whatever your choice, before executing the clone operation, Multigit will check if there are actual existing directories. If that's the
case, it will ask you to validate in a dialog, with the exact list of impacted repositories and an explicit description of your choice (fail, skip or delete).</p>

<p>Note that when you have nested repositories, Multigit reorders the clone operations to make sure that the nested repositories are not blocking
the cloning of the parent repository.</p>

<h2>Exporting to CSV</h2>

<p>You can also export all your repositories states to a CSV file. Just use <code><span style="background-color:#f5f5f5;">File &gt; Export to CSV</span></code>.  It will contain one line per 
repository, and one column per information: repository path, branch name, commit SHA1, url, ...</p>

<h2>Applying a multigit file on existing repositories</h2>

<p>When you want to reproduce an exact repository state from a multigit file, you use the menu <code><span style="background-color:#f5f5f5;">File &gt; Apply a multigit file</span></code> . This will go
over your repositories one by one and adjust the HEAD to the exact branch or tag described in the Multigit file. </p>

<p>The dialog works mostly like the clone dialog, with about the same options.</p>

<p>When applying a multigit file, if a repository is listed
in the multigit file but missing in your base directory, it will be cloned. </p>

<p>If a repository exists on the filesystem but is not listed in the
multigit file, Multigit lets you choose between deleting the directory on the filesystem (a risky operation) or keeping it. Be careful with
your answer to this question, or you may lose your work.</p>

<h2>Dealing with lots of repositories</h2>

<p>When you are dealing with an important number of repositories (like more than fifty), Multigit can become unresponsive on the first launch
or after a complex operation. This is due to the important number of git processes launched in parallel to collect all the repository
information. </p>

<p>To improve this situation, you can limit the maximum number of parallel git tasks running. In the <code><span style="background-color:#f5f5f5;">File &gt; Settings</span></code> dialog,
edit the number of parallel running git processes from <code><span style="background-color:#f5f5f5;">unlimited</span></code> to  a reasonable amount, like 10.</p>

<p>The second thing you can do is reduce the number of columns displayed by Multigit: SHA1 column and URL column are optional, and they do trigger
one git process each to be updated. Hiding them should help.</p>

<p>Multigit will improve with this situation in the future.</p>

<h1 align="center">Conclusion</h1>

<p>I hope this little documentation helped you get a grip on Multigit. Don't hesitate to report positive feedback and issues on 
the Github page</p>

'''
