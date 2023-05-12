[link to mypy]

Multigit
========

*by Philippe Fremy at IDEMIA*

Multigit simplifies working with multiple git repositories at the same time.

Typically, it lets you:
* fetch or pull on all repositories at the same time
* identify visually which repositories are modified or need an update (push or pull)
* create a new branch in a subset of repositories
* switch to a branch existing only in some repositories (but you don't remember which one)
* perform a commit on multiple repositories at the same time, and push it
* launch your preferred git frontend on an interesting repository
* export your repositories state to a file, for reproducing it on a colleagues computer
* and more...

The need arose from my work environment, where
a project typically consists of 30 to 50 git repositories. In such environment, every simple git operation
becomes a complex task. With Multigit, it is simple again. Any git operation like git fetching in the 
morning is run on all the repositories in one click. 
When time comes to commit changes and push them, having a graphical interface to
locate in the blink of an eye which repositories are modified and need a commit has been a life saver.


Multigit is developed within my employer IDEMIA. I would like to thank him again for allowing
me to open source it.

Status
------
Multigit is developed, tested and packaged for Windows. Testing and release on Linux is on the way.


License
-------
Multigit is released under the Apache 2.0 license.

Multigit depends on several other open source projects:
* Python
* PySide/Qt for Python
* Concurrent Log Handler
* PyInstaller

See the file FULL_LICENSING_INFORMATION.md for details.


Contributions
-------------
Contributions are welcome: bug reports, improvements, pull requests. They must be under the Apache 2.0 license.

Multigit is still developed internally at IDEMIA. I will regularly land on the open source version the 
improvements.

See the file CONTRIBUTING.md for details .


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






