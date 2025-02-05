set DIR_IMAGEMAGICK=c:\software\ImageMagick-7.1.0\
%DIR_IMAGEMAGICK%\convert.exe multigit-logo.png -alpha off -colors 256 -resize 256x256 multigit-logo-256.png
%DIR_IMAGEMAGICK%\convert.exe multigit-logo.png -alpha off -colors 256 -resize 64x64   multigit-logo-64.png
%DIR_IMAGEMAGICK%\convert.exe multigit-logo.png -alpha off -colors 256 -resize 48x48   multigit-logo-48.png
%DIR_IMAGEMAGICK%\convert.exe multigit-logo.png -alpha off -colors 256 -resize 32x32   multigit-logo-32.png
%DIR_IMAGEMAGICK%\convert.exe multigit-logo-small.png -alpha off -colors 256 -resize 16x16   multigit-logo-16.png
%DIR_IMAGEMAGICK%\convert.exe multigit-logo-256.png multigit-logo-64.png multigit-logo-48.png multigit-logo-32.png multigit-logo-16.png -colors 256 -alpha off multigit-logo.ico  
pyside6-rcc.exe multigit_resources.qrc -o ..\src\multigit_resources_rc.py
pause
