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


import pathlib, markdown2, datetime, sys

CONTENT_TXT_TEMPLATE = """
content_html = '''
%s
'''
"""


def markdown2qthtml(md_text: str) -> str:
    '''Transform a text in markdown syntax to a html subset supported by Qt

    Qt supports in the generated markdown:
    * <code> is put in fixed font
    * <pre> to show CR
    * <blockquote> to indent text

    Not supported
    * <code> does not have a grey background
    * multi-line code is not indented

    Transformations:
    * for multi-line code,
      * indent the text (blockquote),
      * make linebreaks visible in output (pre)
      * gray the code line (p style="...")
    * for words code
      * add grey background
    '''

    html_text: str
    html_text = markdown2.markdown(md_text)
    html_text = html_text.replace('<h1>', '<h1 align="center">')
    html_text = html_text.replace('<code>\n', '<p style="background-color:#f5f5f5;"><blockquote><pre><code>\n')
    html_text = html_text.replace('</code>\n', '</code></pre></blockquote></p>\n')
    html_text = html_text.replace('<code>', '<code><span style="background-color:#f5f5f5;">')
    html_text = html_text.replace('</code>', '</span></code>')
    return html_text


def markdown_to_python(source_md: pathlib.Path, dest_python: pathlib.Path) -> None:
    source_fname = source_md.name
    with open(source_md, encoding='utf8') as f:
        md_content = f.read()

    html_content = markdown2qthtml(md_content)

    with open(dest_python, 'w') as f:
        f.write(f'# Generated from {source_fname} on %s\n\n' % datetime.datetime.now().isoformat(' '))
        f.write(CONTENT_TXT_TEMPLATE % html_content)

if __name__ == '__main__':
    markdown_to_python(pathlib.Path(__file__).parent / 'CHANGELOG.md',
                       pathlib.Path(__file__).parent/'src/gui/content_whatisnew.py',
                       )

    markdown_to_python(pathlib.Path(__file__).parent / 'FULL_LICENSING_INFORMATION.md',
                       pathlib.Path(__file__).parent/'src/gui/content_full_license_info.py',
                       )

    if '--show' in sys.argv:
        from src.mg_dialog_whatisnew import showWhatIsNew
        from src.mg_dialog_about import showDialogAbout
        from PySide6.QtWidgets import QApplication
        _ = QApplication([])
        showWhatIsNew()
        showDialogAbout(None)




