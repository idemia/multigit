scriptdir=$(dirname $(realpath $0))
basedir=$(realpath $(dirname $(realpath $0))/../../)

app_id=io.github.idemia.Multigit


(cd $scriptdir \
    && flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream $app_id.metainfo.xml \
    && echo "desktop-file-validate" && desktop-file-validate $app_id.desktop \
    && cd $scriptdir/../../../multigit-flatpak-build \
    && echo "Building flatpak" \
    && flatpak-builder --user --force-clean --install builddir $basedir/$app_id.yaml -v \
    && flatpak run $app_id --debug)

    # && echo "appstreamcli validate" && appstreamcli validate $app_id.metainfo.xml \
    #&& flatpak run --command=flathub-build org.flatpak.Builder --user --install builddir $app_id.yaml \
