scriptdir=$(dirname $(realpath $0))

(cd $scriptdir && appstreamcli validate io.github.idemia.Multigit.metainfo.xml \
	&& desktop-file-validate io.github.idemia.Multigit.desktop \
	&& cd $scriptdir/../.. \
	&& flatpak-builder --force-clean builddir /home/philippe/work/multigit/io.github.idemia.Multigit.yaml \
	&& flatpak-builder --user --force-clean --install builddir io.github.idemia.Multigit.yaml -v \
	&& flatpak run io.github.idemia.Multigit --debug)
	
