pushd %~dp0\..

@FOR /F "delims=" %%a in ('python -c "from src.mg_const import VERSION; print(VERSION)"') do SET VERSION=%%a
@echo Packaging MultiGit v%VERSION%

python generate_html_whatsnew.py

@set ZIP7="C:\Program Files\7-Zip\7z.exe"
@rmdir /s /q dist\multigit 2>NUL
@del /s /q  dist\multigit-%VERSION%.zip 2>NUL
pyinstaller.exe -y packaging\multigit.spec || exit /b 1
pyinstaller.exe -y packaging\mgitcmd.spec || exit /b 1
copy /y dist\mgitcmd\mgitcmd.exe dist\multigit
copy /y README.md dist\multigit
copy /y LICENSE.txt dist\multigit
copy /y CONTRIBUTING.md dist\multigit
copy /y CHANGELOG.md dist\multigit
copy /y FULL_LICENSING_INFORMATION.md dist\multigit
pyi-set_version packaging\multigit_version_info.txt dist\MultiGit\MultiGit.exe
pyi-set_version packaging\multigit_version_info.txt dist\MultiGit\mgitcmd.exe
del /q /y dist\mgitcmd
del /s /q  dist\*.log
echo DONE
popd
pause



