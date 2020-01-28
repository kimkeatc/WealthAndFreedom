# -*- coding: utf-8 -*-

from os.path import abspath, dirname
import sys

_MODULE_FOLDER = abspath(dirname(__file__))
if _MODULE_FOLDER not in sys.path:
    sys.path.append(_MODULE_FOLDER)


if __name__ == '__main__':
    pass
