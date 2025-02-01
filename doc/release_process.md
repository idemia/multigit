
# Release process

* Update version in 
   * src/mg_const.py
   * CHANGELOG.md
   * packaging/multigit.iss
   * packaging/multigit_version_info.txt

* run: python generate_html_whatsnew.py

* run: hatch build
  * creates
    * dist/multigit_gx-....tar.gz
    * dist/multigit_gx-....whl
    
* run: hatch publish
  * this pushes the package to pypi.org so be sure to push rc before pushing an official package
  
* run: packaging\package_exe.bat
  * This builds the executables for Windows with pyinstaller
  
* run: packaging\package_installer.bat
  * This builds a full Windows installer with InnoSetup



