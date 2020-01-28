# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import sys

_TEST_FOLDER = abspath(dirname(__file__))
if _TEST_FOLDER not in sys.path:
    sys.path.append(_TEST_FOLDER)


if __name__ == '__main__':
    pass
