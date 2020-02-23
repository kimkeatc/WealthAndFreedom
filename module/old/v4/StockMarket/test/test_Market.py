from os.path import abspath, dirname, join
import unittest
import sys

_TESTING_FOLDER = abspath(dirname(__file__))
_MODULE_FOLDER = abspath(join(_TESTING_FOLDER, '..'))
sys.path.append(_MODULE_FOLDER)

import Market


class TestMarket(unittest.TestCase):

    def setUp(self):
        pass

    def test_MarketInit(self):
        Market.MarketOperation()


if __name__ == '__main__':
    unittest.main(verbosity=2)
