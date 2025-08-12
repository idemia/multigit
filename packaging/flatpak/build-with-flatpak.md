

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

Runs a shell inside the sandbox:

	$ flatpak-builder --run build-dir org.multigit.Multigit.yaml sh

Inspect portal permissions:

	$ flatpak permission-show org.multigit.Multigit

All apps running inside sandboxes:

	$ flatpak ps


Session bus traffic can be audited by passing --log-session-bus to flatpak run:

	$ flatpak run --log-session-bus <application-id>
