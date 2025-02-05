#    Copyright (c) 2019-2023 IDEMIA
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


import sys, subprocess, pathlib

HELP = '''Usage: gen_and_patch_ui.py [--force] ui_file1.ui ui_file2.ui ...

If ui file is newer than python file, perform ui to python conversion and add type annotations to generated python file.

With --force, the conversion is always performed.
'''

MARKER = '# Patched by patch_ui.py'

def patch_ui_py(ui_fname: str, py_fname: str) -> None:
    py_content = open(py_fname).read()
    if MARKER in py_content:
        print('File %s is already patched' % py_fname)
        return

    print('Patching with type annotations: %s' % py_fname)

    ui_content = open(ui_fname).read()
    ref_string = '</class>\n <widget class="'
    assert ref_string in ui_content
    class_name_start_idx = ui_content.find(ref_string) + len(ref_string)
    class_name_end_idx = ui_content.find('"', class_name_start_idx+1)
    main_widget_name = ui_content[class_name_start_idx:class_name_end_idx]

    py_new_content = []
    for py_line in py_content.split('\n'):
        if py_line.startswith('# Created by:'):
            py_new_content.append(py_line)
            py_new_content.append(MARKER)
            continue

        if ('def setupUi(self' in py_line
            or 'def retranslateUi(self' in py_line) and '->' not in py_line:
            # type annotation is not present
            py_line = py_line.replace('):', ': %s) -> None:' % main_widget_name)
            print('- adding annotation for "%s"' % py_line)

        py_new_content.append(py_line)

    with open(py_fname, 'w') as f:
        f.write('\n'.join(py_new_content))

    print('Patching done for %s.' % py_fname)

def remove_import_rc(py_fname: str) -> None:
    with open(py_fname) as f:
        lines = list(f.readlines())

    marker = 'import multigit_resources_rc'

    for i in range(len(lines)):
        if lines[i].startswith(marker):
            lines[i] = '# ' + lines[i]

    with open(py_fname, 'w') as f:
        f.writelines(lines)
    print('import resource line commented for %s.' % py_fname)


def generate_ui(ui_fname: str, py_fname: str, forceGeneration: bool = False) -> None:
    PYUIC = 'pyside6-uic'
    cmdline = [PYUIC, ui_fname, '-o', py_fname]
    print('Generating py file: ' + ' '.join(cmdline))
    subprocess.check_call(cmdline)
    print('OK')


def main() -> None:
    if '--help' in sys.argv:
        print(HELP)
        sys.exit(-1)

    forceGeneration = False
    if '--force' in sys.argv:
        print('Forcing generation')
        del sys.argv[ sys.argv.index('--force') ]
        forceGeneration = True

    ui_fnames = sys.argv[1:]
    for ui_fname in ui_fnames:
        if ui_fname.strip() == '':
            continue

        if not ui_fname.endswith('.ui'):
            print('Not a ui file: %s' % ui_fname)
            print('Ignoring file')
            continue
        py_fname = pathlib.Path(ui_fname).with_suffix('.py')
        ui_mtime = pathlib.Path(ui_fname).stat().st_mtime
        if (not py_fname.exists())  or (py_fname.stat().st_mtime <= ui_mtime) or forceGeneration:
            generate_ui(ui_fname, str(py_fname), forceGeneration)
            patch_ui_py(ui_fname, str(py_fname) )
            remove_import_rc(str(py_fname))


if __name__ == '__main__':
    main()