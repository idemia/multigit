

Multigit accesses the filesystem in several occasions.

* xdg directories:
    * reading and writing configuration file
    * creating configuration directory for saving configuration file and log files
    * writing log files
* Files chosen by user:
    * loading multigit file
    * export multigit file
    * export to CSV file
* General filesystem access
    * Checking if a directory exists prior to performing a clone
    * checking if a directory exists to perform a clone in a subdirectory
    * removing directories (after user validation) to allow cloning (and check that the directory no longer exists)
    * scanning recursively the directory content to identify git repositories (check if file exists and is a directory)
    * Checking if an executable exists to list it as Git frontend (done using flatpak spawn)
* Executables (launched through flatpak spawn)
    * git
    * git-gui
    * gitk
    * SublimeMerge
    * Explorer (defaults to xdg-open)
    * rsync on linux, robocopy on Windows: to move directories when 2 git repositories overlap
    * flatpak info (to check if a flatpak program is installed)
    * flatpak run for git frontends (to check if a flatpak program is installed)
    * /snap/bin/program for running git frontends available as snaps
