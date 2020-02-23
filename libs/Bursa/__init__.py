# -*- coding: utf-8 -*-

import os
import sys

_MODULE_FOLDER_PATH = os.path.abspath(os.path.dirname(__file__))
_LIBS_FOLDER_PATH = os.path.abspath(os.path.join(_MODULE_FOLDER_PATH, '..'))

for path in [_MODULE_FOLDER_PATH, _LIBS_FOLDER_PATH]:
    if path not in sys.path:
        sys.path.append(path)
