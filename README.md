[![mypy checked](https://camo.githubusercontent.com/34b3a249cd6502d0a521ab2f42c8830b7cfd03fa/687474703a2f2f7777772e6d7970792d6c616e672e6f72672f7374617469632f6d7970795f62616467652e737667)](http://mypy-lang.org/)
[![Continuous Integration](https://github.com/idemia/multigit/actions/workflows/ci.yml/badge.svg)](https://github.com/idemia/multigit/actions/workflows/ci.yml)

Multigit
========

*by Philippe Fremy at IDEMIA (philippe.fremy at idemia.com)*

Multigit is a graphical tool for working with projects composed of multiple git repositories.

If you think that *submodules*, *subtree* or *Google repo* are not for you, you are probably at the
right place.

*Note: on PyPi, Multigit is registered as multigit_gx because there is another multigit software*

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
a project typically consists of 30 to 50 git repositories. In such environment, every simple git operation
becomes a complex task. Thank to Multigit, it becomes simple again. Any git operation like git fetching in the 
morning is run on all the repositories in one click. 
When time comes to commit changes and push them, having a graphical interface to
locate in the blink of an eye which repositories are modified and need a commit has been a life saver.


Multigit is developed within my employer IDEMIA. I would like to thank him again for allowing
me to open source it.

Status
------
Multigit is developed, tested and packaged for Windows. Testing and release on Linux is on the way.


Testing
-------

To run the tests, launch pytest from the main directory.

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








