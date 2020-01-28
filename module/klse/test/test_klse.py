# -*- coding: utf-8 -*-

from os.path import abspath, dirname, join
import sys
import unittest

_TEST_FOLDER = abspath(dirname(__file__))
_MODULE_FOLDER = abspath(join(_TEST_FOLDER, '..'))
if _MODULE_FOLDER not in sys.path:
    sys.path.append(_MODULE_FOLDER)

import klse


class TestKlseApi(unittest.TestCase):

    def setUp(self):
        self.testimonial = klse.KlseApi()

    def testGetScreener(self):
        df = self.testimonial.getScreener()
        return df

    def testScreenerResultPostProcessing(self):
        df = self.testGetScreener()
        df = df.apply(self.testimonial.screenerResultPostProcessing, axis=1)
        return df


if __name__ == '__main__':
    unittest.main(verbosity=2)
