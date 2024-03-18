# -*- mode: python ; coding: utf-8 -*-

#    Copyright (c) 2022-2023 IDEMIA
#    Author: IDEMIA (Philippe Fremy, Florent Oulieres)
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

import pathlib

# we don't need to maintain an exclude list for mgitcmd because only the executable is copied over
# to the final directory of multigit
files_to_exclude = set([])


def exclude_from_toc(toc: 'TOC', exclude_list: 'List[str]') -> 'TOC':
    '''Remove from the TOC the files listed in exclude_list'''
    rm_toc = []
    for (dst, src, type) in toc:
        if dst in exclude_list:
            rm_toc.append((dst, src, type))
            print('\t\t\t\tExcluding:', dst)
        else:
            print('Keeping:', dst)

    # this is needed for some versions of pyinstaller
    if getattr(toc, '__sub__', None):
        return toc - rm_toc
    else:
        return [v for v in toc if v not in rm_toc]


block_cipher = None

a = Analysis(
    ['..\\mgitcmd.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.binaries = exclude_from_toc(a.binaries, files_to_exclude)
a.datas = exclude_from_toc(a.datas, files_to_exclude)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mgitcmd',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # a bit heavy-weight but pyinstaller does not like relative path when running directory and spec file directory differ
    icon = str((pathlib.Path(SPECPATH).parent / 'images' / 'multigit-logo.ico').absolute())
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mgitcmd',
)
