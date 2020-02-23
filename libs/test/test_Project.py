# -*- coding: utf-8 -*-

import os
import sys
import unittest

_LIBS_TEST_FOLDER_PATH = os.path.abspath(os.path.dirname(__file__))
_LIBS_FOLDER_PATH = os.path.abspath(os.path.join(_LIBS_TEST_FOLDER_PATH, '..'))

for path in [_LIBS_TEST_FOLDER_PATH, _LIBS_FOLDER_PATH]:
    if path not in sys.path:
        sys.path.append(path)

import Project


class Test(unittest.TestCase):

    def setUp(self):
        Project


if __name__ == '__main__':
    unittest.main(verbosity=2)
