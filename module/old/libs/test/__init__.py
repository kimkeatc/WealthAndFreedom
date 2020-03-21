# -*- coding: utf-8 -*-

import os
import sys

_LIBS_TEST_FOLDER_PATH = os.path.abspath(os.path.dirname(__file__))
if _LIBS_TEST_FOLDER_PATH not in sys.path:
    sys.path.append(_LIBS_TEST_FOLDER_PATH)
