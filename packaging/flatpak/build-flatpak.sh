scriptdir=$(dirname $(realpath $0))

app_id=io.github.idemia.Multigit

(cd $scriptdir 
	&& flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream $app_id.metainfo.xml \
	&& desktop-file-validate $app_id.desktop \
	&& cd $scriptdir/../.. \
	&& flatpak-builder --force-clean builddir /home/philippe/work/multigit/io.github.idemia.Multigit.yaml \
	&& flatpak-builder --user --force-clean --install builddir io.github.idemia.Multigit.yaml -v \
	&& flatpak run io.github.idemia.Multigit --debug)
	
