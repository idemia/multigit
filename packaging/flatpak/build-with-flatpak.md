

# to regenerate python signed requirements
/flatpak-pip-generator --requirements-file ../../reqs/requirements-release.txt io.github.idemia.Multigit.yaml 



Build multigit:
===============

Notes specific to Flatpak
-------------------------

- Do not use a distro package manager such as `apt` inside the Flatpak build.
  Flatpak builds run against the declared runtime/SDK and manifest modules, not
  against host distribution packages.
- If a system library is missing in Flatpak, add it through the manifest or use
  a runtime that already provides it.
- This manifest forces `QT_QPA_PLATFORM=xcb` for the packaged application.

* General rule

	$ flatpak-builder <build-dir> <manifest>


* For us:
	$ cd packaging/flatpak
	$ rm -rf builddir && flatpak-builder --user --install builddir io.github.idemia.Multigit.yaml



Run multigit
============

$ flatpak run io.github.idemia.Multigit 



Debug build process
===================

Build process
-------------

- Download all sources
- Initialize the application directory with `flatpak build-init`
- Build and install each module with `flatpak build`
- Clean up the final build tree by removing unwanted files and e.g. stripping binaries
- Finish the application directory with flatpak `build-finish`


Tips
----

Runs a shell inside the sandbox:

	$ flatpak-builder --run build-dir io.github.idemia.Multigit.yaml sh

Inspect portal permissions:

	$ flatpak permission-show io.github.idemia.Multigit

All apps running inside sandboxes:

	$ flatpak ps


Session bus traffic can be audited by passing --log-session-bus to flatpak run:

	$ flatpak run --log-session-bus <application-id>
