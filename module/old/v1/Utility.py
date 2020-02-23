# -*- coding: utf-8 -*-

from os.path import abspath, basename, dirname, join
import logging
import os
import sys

import namespace

_PROJECT_PATH = abspath(join(dirname(__file__), '..'))


def readFile(path):
    with open(path, 'r') as f:
        content = f.read()
    return content


def makeFile(path, content='', mode='a', permission=0o770):
    with open(path, mode) as f:
        f.write(content)
    os.chmod(path, permission)


def makeFolder(path, mode=0o777):
    mask = os.umask(0o000)
    os.mkdir(path, mode)
    os.umask(mask)


class Logger:

    def __init__(self, name=None):
        _logger = logging.getLogger(name=name)
        _logger.setLevel(logging.DEBUG)
        self._logger = _logger

    def addStreamHandler(self, level=logging.INFO, fmt=namespace.DEFAULT):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level=level)
        if fmt == namespace.DEFAULT:
            fmt = __class__.formatter()
        ch.setFormatter(fmt=fmt)
        self._logger.addHandler(ch)

    def addFileHandler(self, path, mode='a', level=logging.DEBUG, fmt=namespace.DEFAULT):
        fh = logging.FileHandler(filename=path, mode=mode, encoding='utf-8')
        fh.setLevel(level=level)
        if fmt == namespace.DEFAULT:
            fmt = __class__.formatter()
        fh.setFormatter(fmt=fmt)
        self._logger.addHandler(fh)

    @staticmethod
    def date_format(types=namespace.DEFAULT):
        if types == namespace.DEFAULT:
            return '%y/%m/%d %H:%M:%S'
        else:
            return ''

    @staticmethod
    def msg_format(types=namespace.DEFAULT):
        if types == namespace.DEFAULT:
            return '[%(asctime)s] [%(levelname)8s]: %(message)s'
        else:
            return ''

    @staticmethod
    def formatter(types=namespace.DEFAULT):
        if types == namespace.DEFAULT:
            fmt = logging.Formatter(fmt=__class__.msg_format(),
                                    datefmt=__class__.date_format())
        return fmt


class _File:

    def __init__(self, dirname, name):
        self.dirname = dirname
        self.name = name

    @property
    def path(self):
        return join(self.dirname, self.name)


class _Folder(_File):

    def __init__(self, dirname, name):
        _File.__init__(self, dirname, name)

    def listdir(self):
        return os.listdir(self.path)


class _ProjectSubFolder:

    def __init__(self, basepath):
        self.basepath = basepath

        # Primary sub-folders
        self.bin = _Folder(basepath, 'bin')
        self.lib = _Folder(basepath, 'Lib')
        self.logs = _Folder(basepath, 'logs')
        self.module = _Folder(basepath, 'module')
        self.resources = _Folder(basepath, 'resources')
        self.template = _Folder(basepath, 'template')
        self.test = _Folder(basepath, 'test')
        self.trading = _Folder(basepath, 'trading')
        self.webdriver = _Folder(basepath, 'webdriver')

        # Secondary sub-folders
        self.py_site_packages = _Folder(self.lib.path, 'site-packages')

        self.resource_src_folder = _Folder(self.resources.path, 'src')
        self.resource_profile_folder = _Folder(self.resources.path, 'profile')
        self.resource_summary_folder = _Folder(self.resources.path, 'summary')

        # Tertiary sub-folders
        


class RunLogFolder:

    def __init__(self, basepath, basename):
        self.basepath = basepath
        self.basename = basename

    @property
    def path(self):
        return join(self.basepath, self.basename)

    def profileFolder(self):
        return join(self.path, 'stocks_profile')

    @staticmethod
    def finishing_filename():
        return 'finished.txt'

    def finishing_filepath(self):
        return join(self.path, __class__.finishing_filename())

    @staticmethod
    def stock_json_filename(code):
        return f'{code}.json'

    def stock_json_filepath(self, code):
        return join(self.profileFolder(), __class__.stock_json_filename(code))

    @staticmethod
    def bursa_market_filename(name):
        return f'{name}.xlsx'

    def bursa_market_filepath(self, name):
        return join(self.path, __class__.bursa_market_filename(name))

    @staticmethod
    def bursa_screener_filename():
        return 'bursa_screener.xlsx'

    def bursa_screener_filepath(self):
        return join(self.path, __class__.bursa_screener_filename())

    @staticmethod
    def ace_leap_main_filename():
        return 'ace_leap_main_screener.xlsx'

    def ace_leap_main_filepath(self):
        return join(self.path, __class__.ace_leap_main_filename())

    @staticmethod
    def klse_screener_filename():
        return 'klse_screener.xlsx'

    def klse_screener_filepath(self):
        return join(self.path, __class__.klse_screener_filename())


class Project(_Folder):

    def __init__(self):
        _dirname = dirname(_PROJECT_PATH)
        _name = basename(_PROJECT_PATH)
        _Folder.__init__(self, _dirname, _name)

    def paths_to_be_initialize(self):
        _subfolder = self.subfolder()
        paths = [_subfolder.lib, _subfolder.module, _subfolder.py_site_packages]
        return paths

    def system_path_initialize(self):
        pathInstances = self.paths_to_be_initialize()
        for pathInstance in pathInstances:
            if pathInstance.path not in sys.path:
                sys.path.append(pathInstance.path)

    def subfolder(self):
        return _ProjectSubFolder(self.path)

    def config(self):
        return _File(self.subfolder().bin.path, 'config.xlsx')

    def resource_tracker(self):
        return _File(self.subfolder().resources.path, 'stocks_profile.xlsx')

    def resource_record(self):
        return _File(self.subfolder().resources.path, 'record.txt')

    def chrome_webdriver(self, version='79.0.3945.36', name='chromedriver.exe'):
        _path = join(self.subfolder().webdriver.path, 'chrome', version)
        return _File(_path, name)

    def run_log(self, foldername):
        return RunLogFolder(self.subfolder().logs.path, foldername)


if __name__ == '__main__':
    pass
