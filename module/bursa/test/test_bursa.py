# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import sys
import unittest

_TEST_FOLDER = abspath(dirname(__file__))
_MODULE_FOLDER = abspath(join(_TEST_FOLDER, '..'))
_PARENT_MODULE_FOLDER = abspath(join(_MODULE_FOLDER, '..'))

for module in [_MODULE_FOLDER, _PARENT_MODULE_FOLDER]:
    if module not in sys.path:
        sys.path.append(module)

import namespace
import bursa


class TestBursaApi(unittest.TestCase):

    def setUp(self):
        self.testimonial = bursa.BursaApi()

    def testGetMarket_AceMarket(self):
        df = self.testimonial.getMarket(namespace.ACE_MARKET)
        return df

    def testGetMarket_LeapMarket(self):
        df = self.testimonial.getMarket(namespace.LEAP_MARKET)
        return df

    def testGetMarket_MainMarket(self):
        df = self.testimonial.getMarket(namespace.MAIN_MARKET)
        return df

    def testGetMarket_StructureWarrants(self):
        df = self.testimonial.getMarket(namespace.STRUCTURED_WARRANTS)
        return df

    def testGetMarket_ETF(self):
        df = self.testimonial.getMarket(namespace.ETF)
        return df

    def testGetMarket_Bond(self):
        df = self.testimonial.getMarket(namespace.BOND)
        return df


if __name__ == '__main__':
    unittest.main(verbosity=2)
