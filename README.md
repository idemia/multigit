[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Continuous Integration](https://github.com/bluebird75/multigit/actions/workflows/ci.yml/badge.svg)](https://github.com/bluebird75/multigit/actions/workflows/ci.yml)


Multigit
========

*by Philippe Fremy at IDEMIA (philippe.fremy at idemia.com)*

Multigit is a graphical tool for working with projects composed of multiple git repositories.

If you think that *submodules*, *subtree* or *Google repo* are not for you, you are probably at the
right place.

*Note: on PyPi, Multigit is registered as multigit_gx because there is already a multigit software*

Typically, it lets you:
* fetch or pull on many repositories at the same time
* identify visually which repositories are modified or need an update (push or pull)
* create a new branch in a subset of repositories
* switch to a branch existing only in some repositories (but you don't remember which one)
* perform a commit on multiple repositories at the same time, and push it
* launch your preferred git frontend on an interesting repository
* export your repositories state to a file, for reproducing it on a colleagues computer
* and more...

The need arose from my work environment, where
a project typically consists of thirty to fifty git repositories. In such environment, every simple git operation
becomes a complex task. Thank to Multigit, it becomes simple again. Any git operation like git fetching in the 
morning is run on all the repositories in one click. When time comes to commit changes and push them, having a 
graphical interface to locate in the blink of an eye which repositories are modified and need a commit has been a life saver.

Multigit is Open source and developed in Github. It has been developed intially within my employer IDEMIA. I would like 
to thank them again for allowing me to open source it. 


Status
------
Multigit has been used widely for several years within IDEMIA, it's mature and stable.

Platform support:
* Windows: rock-stable, primary development platform, used everyday
* Linux: stable, but small user base so far
* MacOs X: None yet, contribution welcome.


Installation
------------
Multigit is installation is possible through different formats:

* Graphical Installer (Windows): just run `setup_multigit-v1.6.1.exe` and look for Multigit in your Applications
* Portable Application (Windows): just unzip `multigit_portable-v1.6.1.zip` and execute `multigit.exe`
* PyPI package (Windows and Linux): the recommended way is to use `pipx` to install it:

    $ python -m pip install pipx
    $ pipx install multigit_gx
  
    $ # launch it with:
    $ multigit
    
* (future) chocolatey package
* (future) snap



License
-------
Multigit is released under the Apache 2.0 license.

Multigit depends on several other open source projects:
* Python
* PySide/Qt for Python
* Concurrent Log Handler
* PyInstaller

See the file `FULL_LICENSING_INFORMATION.md` for details.


Contributions
-------------
Contributions are welcome: bug reports, improvements, pull requests. They must be under the Apache 2.0 license.

Multigit is developed both as an open source version and internally at IDEMIA. I will make sure that the Open Source
versions thrives. The plan is to share improvements done internally at IDEMIA to the Open Source version on a regular
basis.

See the file `CONTRIBUTING.md` for details .

If you want to exchange with the author, do not hesitate to contact me: philippe.fremy at idemia.com


History and Alternatives
-------------------------
When I started to search how to solve the *run one operation on multiple git repositories* problem, the only tool
I found was Google's `repo` . But it did not fit my requirements:

* It is command-line based but I wanted a graphical tool
* It requires to learn a new set of commands to operate, whereas I wanted to keep the git process and knowledge.

I also looked at `git submodules` but for the same reason, I did not like this solution: not graphical, complexifies
the workflow and requires learning a new set of commands.

So, Multigit was born. Internally at IDEMIA, people love it for how it made their life simpler in environments
with 40 git repositories, without a learning curve for a new tool. Just use your git knowledge.

Since the development of Multigit, other tool with similar functionality have emerged (some of them also named
Multigit). However, from my last inspection, they are all command-line tools. Multigit is the only one providing
a graphical interface.








