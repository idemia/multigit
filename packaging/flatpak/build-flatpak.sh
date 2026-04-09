scriptdir=$(dirname $(realpath $0))

(cd $scriptdir && appstreamcli validate org.multigit.Multigit.metainfo.xml \
	&& desktop-file-validate org.multigit.Multigit.desktop \
	&& cd $scriptdir/../.. \
	&& flatpak-builder --force-clean builddir /home/philippe/work/multigit/org.multigit.Multigit.yaml \
	&& flatpak-builder --user --force-clean --install builddir org.multigit.Multigit.yaml -v \
	&& flatpak run org.multigit.Multigit --debug)
	
