from os.path import abspath, dirname, join
import unittest
import sys

_TESTING_FOLDER = abspath(dirname(__file__))
_MODULE_FOLDER = abspath(join(_TESTING_FOLDER, '..'))
sys.path.append(_MODULE_FOLDER)

import Record


class TestRecord(unittest.TestCase):

    def setUp(self):
        pass

    def test_Module_Init(self):
        Record.Module()

    def test_Module_FilesUpdateTrialRun(self):
        Record.Module().FilesUpdateTrialRun()

    def test_Module_FilesUpdate(self):
        # Record.Module().FilesUpdate()
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
