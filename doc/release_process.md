
# Release process

* Update version in 
   * src/mg_const.py
   * CHANGELOG.md
   * packaging/windows/Multigit.iss
   * packaging/windows/multigit_version_info.txt
   * packaging/chocolatey/multigit.nuspec
   * packaging/flatpak/org.multigit.Multigit.metainfo.xml
   * packaging/flatpak/org.multigit.Multigit.yaml

* run: python generate_html_whatsnew.py


## Create Python package
* run: hatch build
  * creates
    * dist/multigit_gx-....tar.gz
    * dist/multigit_gx-....whl
    
* run: hatch publish
  * this pushes the package to pypi.org so be sure to push rc before pushing an official package
 

## Create Windows installer and Chocolatey package
* run: packaging\windows\package_exe.bat
  * This builds the executables for Windows with pyinstaller
  
* run: packaging\windows\package_installer.bat
  * This builds a full Windows installer with InnoSetup

* run: python packaging\chocolatey\package_chocolatey.py
  * This stages the Chocolatey package in `build\chocolatey\package`
  * If `choco` is installed, it also creates `dist\multigit.<version>.nupkg`
  * Test locally with `choco install --yes multigit --source dist`
  * Push the result with: `choco push dist\multigit.1.7.1.nupkg  --source https://push.chocolatey.org/`

 
## Publish the release on GitHub
 
* login to github with idemia account
  * go to: https://github.com/idemia/multigit/releases
  * click "Draft new Release"



