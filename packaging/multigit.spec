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
#

import pathlib

files_to_exclude = set([
### Pure Python dependencies
    '_bz2',
    '_hashlib',
    '_lzma',
    '_ssl',
    '_decimal',
    '_ctypes',
    '_queue',
    '_overlapped',
    '_asyncio',
     '_multiprocessing',
    'libffi-7',
    'libcrypto-1_1-x64.dll',
    'libcrypto-1_1.dll',
    'libeay32.dll',
    'libssl-1_1-x64.dll',
    'libssl-1_1.dll',
    'pyexpat',
    'libffi-7.dll',

### Windows stuff
    'api-ms-win-core-console-l1-1-0.dll',
    'api-ms-win-core-datetime-l1-1-0.dll',
    'api-ms-win-core-debug-l1-1-0.dll',
    'api-ms-win-core-errorhandling-l1-1-0.dll',
    'api-ms-win-core-file-l1-1-0.dll',
    'api-ms-win-core-file-l1-2-0.dll',
    'api-ms-win-core-file-l2-1-0.dll',
    'api-ms-win-core-handle-l1-1-0.dll',
    'api-ms-win-core-heap-l1-1-0.dll',
    'api-ms-win-core-interlocked-l1-1-0.dll',
    'api-ms-win-core-libraryloader-l1-1-0.dll',
    'api-ms-win-core-localization-l1-2-0.dll',
    'api-ms-win-core-memory-l1-1-0.dll',
    'api-ms-win-core-namedpipe-l1-1-0.dll',
    'api-ms-win-core-processenvironment-l1-1-0.dll',
    'api-ms-win-core-processthreads-l1-1-0.dll',
    'api-ms-win-core-processthreads-l1-1-1.dll',
    'api-ms-win-core-profile-l1-1-0.dll',
    'api-ms-win-core-rtlsupport-l1-1-0.dll',
    'api-ms-win-core-string-l1-1-0.dll',
    'api-ms-win-core-synch-l1-1-0.dll',
    'api-ms-win-core-synch-l1-2-0.dll',
    'api-ms-win-core-sysinfo-l1-1-0.dll',
    'api-ms-win-core-timezone-l1-1-0.dll',
    'api-ms-win-core-util-l1-1-0.dll',
    'api-ms-win-crt-conio-l1-1-0.dll',
    'api-ms-win-crt-convert-l1-1-0.dll',
    'api-ms-win-crt-environment-l1-1-0.dll',
    'api-ms-win-crt-filesystem-l1-1-0.dll',
    'api-ms-win-crt-heap-l1-1-0.dll',
    'api-ms-win-crt-locale-l1-1-0.dll',
    'api-ms-win-crt-math-l1-1-0.dll',
    'api-ms-win-crt-multibyte-l1-1-0.dll',
    'api-ms-win-crt-process-l1-1-0.dll',
    'api-ms-win-crt-runtime-l1-1-0.dll',
    'api-ms-win-crt-stdio-l1-1-0.dll',
    'api-ms-win-crt-string-l1-1-0.dll',
    'api-ms-win-crt-time-l1-1-0.dll',
    'api-ms-win-crt-utility-l1-1-0.dll',

### Qt stuff

    'PySide2\\libEGL.dll',
    'PySide2\\opengl32sw.dll',
    'PySide2\\libGLESv2.dll',
    'PySide2\\d3dcompiler_47.dll',
    'PySide2\\msvcp140.dll',
    'PySide2\\msvcp140_1.dll',

    'PySide2\\Qt5VirtualKeyboard.dll',
    'PySide2\\Qt5QmlModels.dll',
    'PySide2\\Qt5DBus.dll',
    'PySide2\\Qt5Pdf.dll',
    'PySide2\\Qt5Quick.dll',
    'PySide2\\Qt5Svg.dll',
    'PySide2\\Qt5WebSockets.dll',
    'ucrtbase.dll',
    'unicodedata',

    'PySide2\\plugins\\iconengines\\qsvgicon.dll',
    'PySide2\\plugins\\bearer\\qgenericbearer.dll',
    'PySide2\\plugins\\imageformats\\qgif.dll',
    'PySide2\\plugins\\imageformats\\qicns.dll',
    'PySide2\\plugins\\imageformats\\qjpeg.dll',
    'PySide2\\plugins\\imageformats\\qsvg.dll',
    'PySide2\\plugins\\imageformats\\qtga.dll',
    'PySide2\\plugins\\imageformats\\qtiff.dll',
    'PySide2\\plugins\\imageformats\\qwbmp.dll',
    'PySide2\\plugins\\imageformats\\qwebp.dll',
    'PySide2\\plugins\\imageformats\\qpdf.dll',
    'PySide2\\plugins\\platforms\\qminimal.dll',
    'PySide2\\plugins\\platforms\\qoffscreen.dll',
    'PySide2\\plugins\\platforms\\qwebgl.dll',
    'PySide2\\plugins\\platforms\\qdirect2d.dll',
    'PySide2\\plugins\\platforminputcontexts\\qtvirtualkeyboardplugin.dll',
    'PySide2\\plugins\\platformthemes\\qxdgdesktopportal.dll',

    'PySide2\\translations\\qtbase_uk.qm',
    'PySide2\\translations\\qtbase_it.qm',
    'PySide2\\translations\\qtbase_fi.qm',
    'PySide2\\translations\\qtbase_fr.qm',
    'PySide2\\translations\\qtbase_cs.qm',
    'PySide2\\translations\\qtbase_pl.qm',
    'PySide2\\translations\\qtbase_bg.qm',
    'PySide2\\translations\\qtbase_da.qm',
    'PySide2\\translations\\qtbase_hu.qm',
    'PySide2\\translations\\qtbase_gd.qm',
    'PySide2\\translations\\qtbase_ja.qm',
    'PySide2\\translations\\qtbase_de.qm',
    'PySide2\\translations\\qtbase_es.qm',
    'PySide2\\translations\\qtbase_en.qm',
    'PySide2\\translations\\qtbase_sk.qm',
    'PySide2\\translations\\qtbase_ko.qm',
    'PySide2\\translations\\qtbase_he.qm',
    'PySide2\\translations\\qtbase_zh_TW.qm',
    'PySide2\\translations\\qtbase_ca.qm',
    'PySide2\\translations\\qtbase_ru.qm',
    'PySide2\\translations\\qtbase_ar.qm',
    'PySide2\\translations\\qtbase_lv.qm',
    'PySide2\\translations\\qtbase_tr.qm',

## lxml stuff
    'lxml\\objectify.cp38-win32.pyd',
    'lxml\\sax.cp38-win32.pyd',
    'lxml\\builder.cp38-win32.pyd',
])

def exclude_from_toc(toc: 'TOC', exclude_list: 'List[str]') -> 'TOC':
  '''Remove from the TOC the files listed in exclude_list'''
  rm_toc = []
  for (dst, src, toc_type) in toc:
    if dst in exclude_list:
      rm_toc.append( (dst, src, toc_type) )
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
    ['..\\multigit.py'],
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
a.datas    = exclude_from_toc(a.datas, files_to_exclude)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MultiGit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # a bit heavy-weight but pyinstaller does not like relative path when running directory and spec file directory differ
    icon=str((pathlib.Path(SPECPATH).parent / 'images' / 'multigit-logo.ico').absolute())
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MultiGit',
)
