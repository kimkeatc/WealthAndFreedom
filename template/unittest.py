# -*- coding: utf-8 -*-

'''Python unittest template on Windows'''

__credits__ = []
__version__ = ''
__date__ = ''

from os.path import abspath, dirname, join
import unittest
import sys

_TEST_FOLDER = abspath(dirname(__file__))
_MODULE_FOLDER = abspath(join(_TEST_FOLDER, '..'))
sys.path.append(_MODULE_FOLDER)


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def testCase(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
