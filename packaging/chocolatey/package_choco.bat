pushd %~dp0\..\..

@FOR /F "delims=" %%a in ('python -c "from src.mg_const import VERSION; print(VERSION)"') do SET VERSION=%%a
@echo Creating chocolatey package for MultiGit v%VERSION%

copy /y "Setup\Multigit OpenSource "%VERSION%".exe" packaging\chocolate\tools
copy /y FULL_LICENSING_INFORMATION.md move packaging\chocolatey\tools\LICENSE.txt
cd packaging\chocolatey
choco pack multigit.nuspec

popd
pause