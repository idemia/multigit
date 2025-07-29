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

    '_bz2.pyd',
    '_decimal.pyd',
    '_hashlib.pyd',
    '_lzma.pyd',
    '_wmi.pyd',

    'libcrypto-3.dll',

### Qt stuff

    'PySide6\\plugins\\imageformats\\qtiff.dll',
    'PySide6\\plugins\\imageformats\\qico.dll',
    'PySide6\\plugins\\generic\\qtuiotouchplugin.dll',
    'PySide6\\plugins\\iconengines\\qsvgicon.dll',
    'PySide6\\plugins\\imageformats\\qgif.dll',
    'PySide6\\plugins\\imageformats\\qicns.dll',
    'PySide6\\plugins\\imageformats\\qjpeg.dll',
    'PySide6\\plugins\\imageformats\\qpdf.dll',
    'PySide6\\plugins\\imageformats\\qsvg.dll',
    'PySide6\\plugins\\imageformats\\qtga.dll',
    'PySide6\\plugins\\imageformats\\qwbmp.dll',
    'PySide6\\plugins\\imageformats\\qwebp.dll',

    'PySide6\\plugins\\platforms\\qoffscreen.dll',
    'PySide6\\plugins\\platforms\\qdirect2d.dll',
    'PySide6\\plugins\\platforms\\qminimal.dll',

    'PySide6\\Qt6Network.dll',
    'PySide6\\Qt6OpenGL.dll',
    'PySide6\\Qt6Pdf.dll',
    'PySide6\\Qt6Qml.dll',
    'PySide6\\Qt6QmlMeta.dll',
    'PySide6\\Qt6QmlModels.dll',
    'PySide6\\Qt6QmlWorkerScript.dll',
    'PySide6\\Qt6Quick.dll',
    'PySide6\\Qt6Svg.dll',
    'PySide6\\QtNetwork.pyd',

    'PySide6\\translations\\qt_ar.qm',
    'PySide6\\translations\\qt_bg.qm',
    'PySide6\\translations\\qt_ca.qm',
    'PySide6\\translations\\qt_cs.qm',
    'PySide6\\translations\\qt_da.qm',
    'PySide6\\translations\\qt_de.qm',
    'PySide6\\translations\\qt_en.qm',
    'PySide6\\translations\\qt_es.qm',
    'PySide6\\translations\\qt_fa.qm',
    'PySide6\\translations\\qt_fi.qm',
    'PySide6\\translations\\qt_fr.qm',
    'PySide6\\translations\\qt_gd.qm',
    'PySide6\\translations\\qt_gl.qm',
    'PySide6\\translations\\qt_he.qm',
    'PySide6\\translations\\qt_help_ar.qm',
    'PySide6\\translations\\qt_help_bg.qm',
    'PySide6\\translations\\qt_help_ca.qm',
    'PySide6\\translations\\qt_help_cs.qm',
    'PySide6\\translations\\qt_help_da.qm',
    'PySide6\\translations\\qt_help_de.qm',
    'PySide6\\translations\\qt_help_en.qm',
    'PySide6\\translations\\qt_help_es.qm',
    'PySide6\\translations\\qt_help_fr.qm',
    'PySide6\\translations\\qt_help_gl.qm',
    'PySide6\\translations\\qt_help_hr.qm',
    'PySide6\\translations\\qt_help_hu.qm',
    'PySide6\\translations\\qt_help_it.qm',
    'PySide6\\translations\\qt_help_ja.qm',
    'PySide6\\translations\\qt_help_ka.qm',
    'PySide6\\translations\\qt_help_ko.qm',
    'PySide6\\translations\\qt_help_nl.qm',
    'PySide6\\translations\\qt_help_nn.qm',
    'PySide6\\translations\\qt_help_pl.qm',
    'PySide6\\translations\\qt_help_pt_BR.qm',
    'PySide6\\translations\\qt_help_ru.qm',
    'PySide6\\translations\\qt_help_sk.qm',
    'PySide6\\translations\\qt_help_sl.qm',
    'PySide6\\translations\\qt_help_tr.qm',
    'PySide6\\translations\\qt_help_uk.qm',
    'PySide6\\translations\\qt_help_zh_CN.qm',
    'PySide6\\translations\\qt_help_zh_TW.qm',
    'PySide6\\translations\\qt_hr.qm',
    'PySide6\\translations\\qt_hu.qm',
    'PySide6\\translations\\qt_it.qm',
    'PySide6\\translations\\qt_ja.qm',
    'PySide6\\translations\\qt_ka.qm',
    'PySide6\\translations\\qt_ko.qm',
    'PySide6\\translations\\qt_lt.qm',
    'PySide6\\translations\\qt_lv.qm',
    'PySide6\\translations\\qt_nl.qm',
    'PySide6\\translations\\qt_nn.qm',
    'PySide6\\translations\\qt_pl.qm',
    'PySide6\\translations\\qt_pt_BR.qm',
    'PySide6\\translations\\qt_pt_PT.qm',
    'PySide6\\translations\\qt_ru.qm',
    'PySide6\\translations\\qt_sk.qm',
    'PySide6\\translations\\qt_sl.qm',
    'PySide6\\translations\\qt_sv.qm',
    'PySide6\\translations\\qt_tr.qm',
    'PySide6\\translations\\qt_uk.qm',
    'PySide6\\translations\\qt_zh_CN.qm',
    'PySide6\\translations\\qt_zh_TW.qm',
    'PySide6\\translations\\qtbase_ar.qm',
    'PySide6\\translations\\qtbase_bg.qm',
    'PySide6\\translations\\qtbase_ca.qm',
    'PySide6\\translations\\qtbase_cs.qm',
    'PySide6\\translations\\qtbase_da.qm',
    'PySide6\\translations\\qtbase_de.qm',
    'PySide6\\translations\\qtbase_en.qm',
    'PySide6\\translations\\qtbase_es.qm',
    'PySide6\\translations\\qtbase_fa.qm',
    'PySide6\\translations\\qtbase_fi.qm',
    'PySide6\\translations\\qtbase_fr.qm',
    'PySide6\\translations\\qtbase_gd.qm',
    'PySide6\\translations\\qtbase_he.qm',
    'PySide6\\translations\\qtbase_hr.qm',
    'PySide6\\translations\\qtbase_hu.qm',
    'PySide6\\translations\\qtbase_it.qm',
    'PySide6\\translations\\qtbase_ja.qm',
    'PySide6\\translations\\qtbase_ka.qm',
    'PySide6\\translations\\qtbase_ko.qm',
    'PySide6\\translations\\qtbase_lv.qm',
    'PySide6\\translations\\qtbase_nl.qm',
    'PySide6\\translations\\qtbase_nn.qm',
    'PySide6\\translations\\qtbase_pl.qm',
    'PySide6\\translations\\qtbase_pt_BR.qm',
    'PySide6\\translations\\qtbase_ru.qm',
    'PySide6\\translations\\qtbase_sk.qm',
    'PySide6\\translations\\qtbase_tr.qm',
    'PySide6\\translations\\qtbase_uk.qm',
    'PySide6\\translations\\qtbase_zh_CN.qm',
    'PySide6\\translations\\qtbase_zh_TW.qm',
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
