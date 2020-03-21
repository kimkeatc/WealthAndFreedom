# -*- coding: utf-8 -*-

from os.path import abspath, basename, dirname, join
import sys

import Utility

_ROOT = abspath(join(dirname(__file__), '..'))

# ===============================================================================
# Folders
# ===============================================================================

# Level 1: Root

ROOT_FOLDER = Utility._Folder(dirname(_ROOT), basename(_ROOT))

# Level 2: Root subfolder

BIN_FOLDER = Utility._Folder(ROOT_FOLDER.path, 'bin')

LIB_FOLDER = Utility._Folder(ROOT_FOLDER.path, 'Lib')

LIBS_FOLDER = Utility._Folder(ROOT_FOLDER.path, 'libs')

LOGS_FOLDER = Utility._Folder(ROOT_FOLDER.path, 'logs')

TEMPLATE_FOLDER = Utility._Folder(ROOT_FOLDER.path, 'template')

TEST_FOLDER = Utility._Folder(ROOT_FOLDER.path, 'test')

WEBDRIVER_FOLDER = Utility._Folder(ROOT_FOLDER.path, 'webdriver')

# Level 3:

PYTHON_SITE_PACKAGES = Utility._Folder(LIB_FOLDER.path, 'site-packages')

CHROME_WEBDRIVER_FOLDER = Utility._Folder(WEBDRIVER_FOLDER.path, 'chrome')

# ===============================================================================
# Files
# ===============================================================================

CHROME_WEBDRIVER_v79 = Utility._Folder(CHROME_WEBDRIVER_FOLDER.path, '79.0.3945.36')
CHROME_WEBDRIVER = Utility._File(CHROME_WEBDRIVER_v79.path, 'chromedriver.exe')

TRADING_PLAN_HOMEWORK = Utility._File(ROOT_FOLDER.path, 'homework.xlsx')

# ===============================================================================


class LogFolder:

    def __init__(self, foldername):
        self.dirname = LOGS_FOLDER.path
        self._foldername = foldername
        self._folderpath = join(self.dirname, foldername)

        self.bursa_screener = Utility._File(self.path, __class__.bursa_screener_filename)
        self.klse_screener = Utility._File(self.path, __class__.klse_screener_filename)

    @property
    def name(self):
        return self._foldername

    @property
    def path(self):
        return self._folderpath

    @staticmethod
    def bursa_screener_filename():
        return 'bursa_screener.xlsx'

    @staticmethod
    def klse_screener_filename():
        return 'klse_screener.xlsx'


_SYS = [ROOT_FOLDER,
        LIB_FOLDER,
        LIBS_FOLDER,
        PYTHON_SITE_PACKAGES
        ]

for _sys in _SYS:
    if _sys.path not in sys.path:
        sys.path.append(_sys.path)
