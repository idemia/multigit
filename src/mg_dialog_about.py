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

from typing import Optional

from PySide2.QtWidgets import QDialog, QWidget
from PySide2.QtCore import Qt

from src.gui.ui_about import Ui_dialogAbout
from src.gui.ui_about_license import Ui_FullLicenseInfoDialog
from src.gui.content_full_license_info import content_html
from src.mg_const import VERSION

VERSION_MARKER = '[version]'

class MgAboutDialog(QDialog):

    def __init__(self, parent: Optional[QWidget]) -> None:
        super().__init__(parent)
        self.setModal(False)
        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.ui = Ui_dialogAbout()
        self.ui.setupUi(self)

        self.ui.pushButtonOk.clicked.connect(self.close)
        self.ui.pushButtonFullLicense.clicked.connect(self.showFullLicenseInfo)
        htmlContent = self.ui.textBrowserContent.toHtml()
        if VERSION_MARKER in htmlContent:
            self.ui.textBrowserContent.setHtml(htmlContent.replace(VERSION_MARKER, VERSION))



    def showFullLicenseInfo(self) -> None:
        dlg = QDialog(self)
        dlg.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        ui = Ui_FullLicenseInfoDialog()
        ui.setupUi(dlg)
        ui.textBrowser.setHtml(content_html)
        dlg.show()


def showDialogAbout(parent: Optional[QWidget]) -> None:
    '''Show the about dialog'''
    dlg = MgAboutDialog(parent)
    dlg.exec()

