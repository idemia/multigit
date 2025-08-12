# Generated from CHANGELOG.md on 2025-02-05 22:32:00.447749


content_html = '''
<h1 align="center">MultiGit</h1>

<p><em>by Phlipppe Fremy <a href="&#109;&#x61;i&#x6c;&#116;&#x6f;&#58;&#112;&#x68;&#x69;&#x6c;&#105;&#x70;&#112;&#x65;&#46;&#x66;&#114;&#x65;&#x6d;&#121;&#x40;&#105;d&#x65;&#x6d;&#105;&#97;&#46;&#x63;&#111;&#109;">&#112;&#x68;&#x69;&#x6c;&#105;&#x70;&#112;&#x65;&#46;&#x66;&#114;&#x65;&#x6d;&#121;&#x40;&#105;d&#x65;&#x6d;&#105;&#97;&#46;&#x63;&#111;&#109;</a></em></p>

<h2>Introduction</h2>

<p>Multigit help users to manage many Git repositories simultaneously.</p>

<h2>Version 1.7.1 (2025-02-05)</h2>

<p>Improvements</p>

<ul>
<li>Porting to Qt6 / PySide6 for better support on recent linux</li>
</ul>

<h2>Version 1.6.1 (2025-02-01)</h2>

<p>Improvements</p>

<ul>
<li>Porting to Linux</li>
<li>Add support for <code><span style="background-color:#f5f5f5;">gitk</span></code> and <code><span style="background-color:#f5f5f5;">git gui</span></code></li>
<li>Add CI for Linux and Windows on Github</li>
<li>support cloning from url like: <code><span style="background-color:#f5f5f5;">fremy@host.xz:path/to/repo.git/</span></code></li>
</ul>

<h2>Version 1.6.0 (2023-04-14)</h2>

<p>First official release to the open source world!</p>

<p>Improvements:</p>

<ul>
<li>Using <code><span style="background-color:#f5f5f5;">Enter</span></code> on a repository triggers the same action as double-clicking it.</li>
<li>Better about dialog, listing all open source components and licenses</li>
<li>document multigit file format with a JSON schema</li>
</ul>

<p>Bug fixes:</p>

<ul>
<li>Fix problem in branch/tag checkout</li>
<li>it was impossible to create a branch with the name different only by case from another branch created in the past</li>
<li>Do not hide the list of repositories when filtering in dialog switch/delete branch</li>
<li>The settings dialog would not work when no config file exists</li>
<li>When cloning nested repositories, ensure that nested clone starts even if top clone fails</li>
</ul>

<h2>Version 1.5 (2022-12-14)</h2>

<p>New:</p>

<ul>
<li>Multigit uses multiple tabs</li>
<li>Clone multigit file and Apply multigit file now follow dependency order of nested git repositories</li>
<li>When checkouting a tag already on the current commit, force git to show the tag name</li>
<li>In git switch branch, git delete branch, git checkout tag, show in a tooltip which repositories contain a branch/tag</li>
<li>Show number of repositories and selected repositories in the status bar</li>
<li>Add option to auto-fetch on startup</li>
<li>Can choose repositories when using Git, custom command</li>
</ul>

<p>Bug fixes:</p>

<ul>
<li>Ensure JSON multigit file is sorted when exporting</li>
<li>No more "RunTimeError, C++ object already deleted"</li>
<li>Deals better with corrupted configuration file</li>
<li>Deals better with repositories deleted while showing the export to multigit dialog</li>
<li>No more exceptions when multiple instances access the same log file</li>
<li>avoids git complaining about branch with the same name as a directory by using argument '--' with checkout</li>
<li>Better handling of scrolling in git execution window</li>
<li>Better handling of abort requests</li>
</ul>

<h2>Version 1.4 (2022-06-03)</h2>

<p>New:</p>

<ul>
<li>Multigit now exists in command-line: mgitcmd</li>
<li>Branch without remote tracking branch: add tooltip for how to fix the situation</li>
<li>Git push tags: choose which tag to push</li>
<li>Git Revert: show the list of files being reverted</li>
<li>Git Delete Branch: better control on which branch to delete (local vs remote)</li>
<li>Git Delete Branch: can delete multiple branches</li>
<li>Git authentication failure: warn user when git encounters too many authentication
failures to avoid locking the user account.</li>
<li>Installation: automatically uninstall previous version before installing a new one</li>
</ul>

<p>Bug fixes:</p>

<ul>
<li>fix log not being written when configuration file is corrupted</li>
<li>handles correctly path with characters ] and [</li>
<li>better handling of git execution window</li>
<li>do not allow cloning of ssh repositories with empty user name</li>
<li>handle better the case where local branch can not be deleted because of unpushed commits</li>
<li>fix <em>Git Switch Branch</em> to deal with multiple origins</li>
<li>force Git to show the current tag when creating a new tag on an existing tag</li>
<li>warn user before exporting unusable mgit files (empty url, local branches)</li>
</ul>

<h2>Version 1.3 (2022-01-27)</h2>

<p>New funtionality</p>

<ul>
<li>Apply a multigit file to a directory</li>
<li>When exporting to a multigit file, choice between exporting branches or a snapshot</li>
<li>New column with remote URL (can be hidden)</li>
<li>Configure visibility of SHA1 and URL column, of bottom tab Last Commit and Modified Files</li>
<li>Git swtich can switch to branch and (new) to tag</li>
</ul>

<p>Various bug fixes and small improvements:  </p>

<ul>
<li>fix username handling on clone url</li>
<li>fix CSV and Multigit export for unicode branch names and repositories names</li>
<li>fix sorting of repositories in clone/apply/export, make it case-insensitive</li>
<li>switch branch, when branches are grouped by name, correctly display the selected branch name</li>
<li>deal better with emtpy URL in multigit file</li>
<li>branch filter is now case-insensitive</li>
</ul>

<h2>Version 1.2 (2021-12-20)</h2>

<p>Main changes are:</p>

<ul>
<li>Menu to copy repository informations: url, branch name, tag, sha1</li>
<li>Add buttons in main interface to switch base directory quickly</li>
<li><p>When cloning over existing directories, tool can delete the directories or skip them</p></li>
<li><p>Details of the changes</p>

<ul>
<li><p>Bug correction</p>

<ul>
<li>support branch names using unicode characters</li>
<li>Export to JSON and CSV is not done in alphabetical order </li>
<li>Tool shows error message when a repository is deleted</li>
</ul></li>
<li><p>Improvements</p>

<ul>
<li>Better handling of existing directories when cloning</li>
<li>Add menu to copy SHA1, remote URL or full path</li>
<li>Open or switch base directory directly from main window</li>
<li>Better handling of existing directories when cloning</li>
<li>add ability to limit the maximum number of parallel git processes running</li>
<li>log git commands to a more readable file</li>
<li>log of git execution window can be copied to clipboard</li>
<li>Show the same menu in the menu bar and in the right-mouse click menu</li>
<li>Ask user to confirm when launching too many TortoiseGit actions</li>
<li>Git commit can recall previous commit messages</li>
<li>New column with SHA1</li>
<li>Add tooltip description to all menu items</li>
</ul></li>
</ul></li>
</ul>

<h2>Version 1.1.0 (2021-12-09)</h2>

<ul>
<li><p>Bug correction</p>

<ul>
<li>Git actions failed on large amount of repositories</li>
<li>Error on tracking remote repository for new created branch</li>
</ul></li>
<li><p>Improvements</p>

<ul>
<li>progress bar when exporting to mulitgit file</li>
<li>Add tortoise git command to switch/checkout branch</li>
<li>Add Git switch branch command</li>
<li>Add Git delete branch command</li>
<li>Add Git commit command</li>
</ul></li>
</ul>

<h2>Version 1.0.0 (2021-04-19)</h2>

<ul>
<li>Project Configuration File
<ul>
<li>username removed from url</li>
<li>username used to clone is specified in UI</li>
</ul></li>
<li>Git programs need to be individually activated to be available</li>
<li>Fix symlink management when opening directory and exporting project configuration file</li>
<li>Fix git switch: replace git switch (not backward compatible) by git checkout</li>
</ul>

<h2>Version 0.8.0 (2021-04-09)</h2>

<ul>
<li>Clone from configuration file
<ul>
<li>Improve cloning mecanism</li>
<li>fix if it is the first time (no last file)</li>
</ul></li>
</ul>

<h2>Version 0.7.1 (2021-04-07)</h2>

<ul>
<li>Fix TortoiseGit problem for repositories with space</li>
<li>Speedup csv export by filling data asynchronously</li>
<li>Fix export of empty repository</li>
<li>Git execution window:
<ul>
<li>Improving handling of abort</li>
<li>Display progressive clone output  </li>
</ul></li>
</ul>

<h2>Version 0.7.0 (2021-03-31)</h2>

<ul>
<li>Bugfix: support for symlinks in working dir</li>
<li>Create Project folder from multigit json configuration file (File menu)
<ul>
<li>List repositories </li>
<li>Analyze the json file</li>
<li>Build the project in the specified directory</li>
</ul></li>
<li>Generate multigit json configuration file from opened directory (File menu)</li>
</ul>

<h2>Version 0.6.8 (2021-02-26)</h2>

<ul>
<li>use a dedicated column and icon for showing that refresh is in progress</li>
<li>refresh the selected repositories when switching back to window</li>
<li>can run a custom git command</li>
<li>git command execution: use fixed font and better indentation of results</li>
<li>export CSV (warning, minor change of format)
<ul>
<li>can choose which fields to export</li>
<li>one column added to export the commit date</li>
</ul></li>
<li>bugfix: ESC during CSV export would crash</li>
<li>columns "status" and "last remote synchro" are sorted using natural sort</li>
</ul>

<h2>Version 0.6.7 (2021-01-27)</h2>

<ul>
<li>Show README and last changelog directly in the tool</li>
<li>Refresh repository after closing Sublime Text or Source Tree</li>
<li>Trigger the default action on a repo with enter</li>
<li>limit size of log debug file</li>
<li>shortcut F6 to fetch all</li>
<li>bugfix: copy/paste icon from properties does not show up !</li>
<li>fix bug: refresh all repo on F5 and not just the repo added</li>
<li>fix bug: wrong repo opened by sublimemerge and sourcetree</li>
<li>fix bug: exception when launching sublime merge and sourcetree</li>
<li>refresh repository view automatically after execution of TortoiseGit or Git Bash</li>
<li>fix bug: after launching TortoiseGit, an exception was sometimes raised, showing an exception dialog</li>
</ul>

<h2>Version 0.6.2 (2020-09-15)</h2>

<ul>
<li>add git push --tags.</li>
<li>mypy compliant 100%</li>
<li>better handling of repos added and removed</li>
<li>parallel execution of git jobs</li>
</ul>

<h2>Version 0.6 (2020-07-22)</h2>

<ul>
<li>ability to create annotated tags.</li>
<li>add Git Bash to the Git menu.</li>
<li>add Tortoise Git Diff to menu.</li>
<li>validation dialog before issuing git revert.</li>
<li>export all repository status to a CSV file</li>
<li>use colors for branch and tags.</li>
<li>synchronise the view asynchronously</li>
<li>remember last used repository upon startup</li>
<li>small user interface improvements</li>
<li>fixed a few bugs</li>
</ul>

<h2>Version 0.5 (2021-03-01)</h2>

<ul>
<li>Fix execution from a directory with no access rights</li>
<li>Configure action for double-click.</li>
<li>Autocheck availability of TortoiseGit</li>
<li>Disable TortoiseGit, SourceTree and SublimeMerge if not available</li>
<li>Other small bug fixes</li>
</ul>

<h2>Version 0.4 (2020-01-07)</h2>

<ul>
<li>Can now launch some git commands directly on the repo: fetch, pull, push, revert, tag</li>
<li>Add icons for Git and Tortoise Git operations</li>
<li>Add copy button to properties</li>
<li>add About dialog</li>
<li>Add "show in explorer" functionality</li>
<li>In repo properties, show all tags pointing to a given commit</li>
<li>Show the synchro status with remote branche</li>
<li>Add preference dialog to configure location of Git and TortoiseGit</li>
<li>Deal better with the absence of Git or TortoiseGit</li>
</ul>

<h2>Version 0.3 (2019-11-27)</h2>

<ul>
<li>Add TortoiseGit actions on repositories</li>
<li>Add a context menu</li>
<li>Fix refresh action</li>
<li>Add an icon</li>
<li>limit size of the diff</li>
<li>deal better with git diff generating invalid encodings</li>
<li>colorize diff</li>
</ul>

<h2>Version 0.2 (2019-09-12)</h2>

<ul>
<li>show last commit of the selected repo</li>
<li>show diff status of modified files of the selected repo</li>
<li>add property dialog</li>
<li>avoid detection of non-git directories</li>
</ul>

<h2>Version 0.1 (2019-08-23)</h2>

<ul>
<li>list all repos in a given directory, with their branch name and tags</li>
</ul>

'''
