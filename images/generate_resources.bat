pushd %~dp0
pyside2-rcc.exe multigit_resources.qrc -o ..\src\multigit_resources_rc.py
popd
pause
