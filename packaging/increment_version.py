#     Copyright (c) 2024 IDEMIA
#     Author: IDEMIA (Philippe Fremy, Florent Oulieres)
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

import re, pathlib
here = pathlib.Path(__file__).parent.resolve()
windows_dir = here / 'windows'
chocolatey_dir = here / 'chocolatey'

reVersion = r'([\d.][\w\-_.]+)'

files = [
    (here.parent / 'src/mg_const.py',          re.compile(f"VERSION = '{reVersion}'"), 'Free string'),
    (windows_dir / 'multigit_version_info.txt',  re.compile(fr"StringStruct\('FileVersion', '{reVersion}'\),"), 'Free string'),
    (windows_dir / 'multigit_version_info.txt',  re.compile(fr"StringStruct\('ProductVersion', '{reVersion}'\),"), 'Free string'),
    (windows_dir / 'Multigit.iss',               re.compile(r'#define VERSION "([\d\.]+)"'), 'Only digits and dots allowed'),
    (windows_dir / 'Multigit.iss',               re.compile(f'#define VERSIONSTR "{reVersion}"'), 'Free text'),
    (windows_dir / 'multigit_version_info.txt',  re.compile(r'filevers=(\([\d \,,]+\)),'),  'Tuple of 4 digits'),
    (windows_dir / 'multigit_version_info.txt',  re.compile(r'prodvers=(\([\d \,,]+\)),'), 'Tuple of 4 digits'),
    (chocolatey_dir / 'multigit.nuspec',      re.compile(r'<version>([^<]+)</version>'), 'Free string'),
]

for fpath, re_version, comment in files:
    print('- file ', fpath)
    with open(fpath) as f:
        fcontent = f.read()

    mo = re_version.search(fcontent)
    assert mo
    print(f'\tcurrent version is "{mo.group(1)}"')
    newv = ''
    while newv == '':
        newv = input(f'\tPlease enter new version ({comment}): ')

    new_version_expr = mo.group(0).replace(mo.group(1), newv)
    fcontent = fcontent.replace(mo.group(0), new_version_expr)

    with open(fpath, 'w') as f:
        f.write(fcontent)
    print('\tDone')
