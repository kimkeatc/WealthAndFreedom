from os.path import abspath, dirname, join
import unittest
import sys

_TESTING_FOLDER = abspath(dirname(__file__))
_MODULE_FOLDER = abspath(join(_TESTING_FOLDER, '..'))
sys.path.append(_MODULE_FOLDER)

import Stock


class TestStock(unittest.TestCase):

    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
