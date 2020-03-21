from os.path import abspath, split
from pathlib import Path

from utility2 import Folder

# Primary folders

ROOT_FOLDER = Folder(*split(abspath(Path(__file__).resolve().parents[1])))

BIN_FOLDER = Folder(ROOT_FOLDER.path, 'bin')

DATA_FOLDER = Folder(ROOT_FOLDER.path, 'data')

DOCS_FOLDER = Folder(ROOT_FOLDER.path, 'docs')

LIB_FOLDER = Folder(ROOT_FOLDER.path, 'Lib')

LOGS_FOLDER = Folder(ROOT_FOLDER.path, 'logs')

MODULE_FOLDER = Folder(ROOT_FOLDER.path, 'module')

TEMPLATE_FOLDER = Folder(ROOT_FOLDER.path, 'template')

TEST_FOLDER = Folder(ROOT_FOLDER.path, 'test')

WEBDRIVER_FOLDER = Folder(ROOT_FOLDER.path, 'webdriver')

# Secondary folders

PYTHON_SITE_PACKAGES_FOLDER = Folder(LIB_FOLDER.path, 'site-packages')

CHROMER_WEBDRIVER_FOLDER = Folder(WEBDRIVER_FOLDER.path, 'chrome')
