# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import sys

_PROJECT_FOLDER = abspath(dirname(__file__))
if _PROJECT_FOLDER not in sys.path:
    sys.path.append(_PROJECT_FOLDER)


if __name__ == '__main__':
    pass
