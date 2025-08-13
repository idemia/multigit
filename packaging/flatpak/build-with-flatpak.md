

# to regenerate python signed requirements
/flatpak-pip-generator --requirements-file ../../reqs/requirements-release.txt org.multigit.Multigit.yaml 



Build multigit:
===============

* General rule

	$ flatpak-builder <build-dir> <manifest>


* For us:
	$ cd packaging/flatpak
	$ rm -rf builddir && flatpak-builder --user --install builddir org.multigit.Multigit.yaml



Run multigit
============

$ flatpak run org.multigit.Multigit 



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

	$ flatpak-builder --run build-dir org.multigit.Multigit.yaml sh

Inspect portal permissions:

	$ flatpak permission-show org.multigit.Multigit

All apps running inside sandboxes:

	$ flatpak ps


Session bus traffic can be audited by passing --log-session-bus to flatpak run:

	$ flatpak run --log-session-bus <application-id>
