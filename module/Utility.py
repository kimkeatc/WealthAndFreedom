# -*- coding: utf-8 -*-

from os.path import abspath, dirname, exists, join, split
import logging
import os
import sys

import namespace


class Logger:

    def __init__(self, name=None):
        _logger = logging.getLogger(name)
        _logger.setLevel(logging.DEBUG)
        self._logger = _logger

    def addStreamHandler(self, level=logging.INFO, fmt=namespace.default):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        if fmt == namespace.default:
            fmt = __class__.defaultFormatter()
        ch.setFormatter(fmt)
        self._logger.addHandler(ch)

    def addFileHandler(self, path, mode='a', level=logging.DEBUG, fmt=namespace.default):
        fh = logging.FileHandler(filename=path, mode=mode, encoding='utf-8')
        fh.setLevel(level)
        if fmt == namespace.default:
            fmt = __class__.defaultFormatter()
        fh.setFormatter(fmt)
        self._logger.addFilter(fh)

    @staticmethod
    def defaultMsgFormat():
        return '[%(asctime)s] [%(levelname)8s]: %(message)s'

    @staticmethod
    def defaultDateFmt():
        return '%y/%m/%d %H:%M:%S'

    @staticmethod
    def defaultFormatter():
        fmt = logging.Formatter(fmt=__class__.defaultMsgFormat(),
                                datefmt=__class__.defaultDateFmt())
        return fmt


class _File:

    def __init__(self, dirname, name):
        self.dirname = dirname
        self.name = name

    @property
    def path(self):
        return join(self.dirname, self.name)

    def create(self, msg='', filemode='w', mode=0o770):
        with open(self.path, mode=filemode) as f:
            f.write(msg)
        os.chmod(self.path, mode)

    def read(self):
        with open(self.path, 'r') as f:
            content = f.read()
        return content

    def readlines(self):
        with open(self.path, 'r') as f:
            content = f.readlines()
        return content


class _Folder(_File):

    def __init__(self, dirname, name):
        _File.__init__(self, dirname, name)

    def listdir(self):
        try:
            return os.listdir(self.path)
        except FileNotFoundError:
            self.create()
            return self.listdir()

    def create(self, mode=0o777):
        if not exists(self.path):
            mask = os.umask(0o000)
            os.mkdir(self.path, mode)
            os.umask(mask)

    def addAttr(self, name, value):
        setattr(self, name, value)


class MyProject(_Folder):

    def __init__(self):

        _Folder.__init__(self, *split(abspath(join(dirname(__file__), '..'))))

        # Primary folders...
        self.binFolder = _Folder(self.path, 'bin')
        self.dataFolder = _Folder(self.path, 'data')
        self.libFolder = _Folder(self.path, 'Lib')
        self.logsFolder = _Folder(self.path, 'logs')
        self.moduleFolder = _Folder(self.path, 'module')
        self.sqlFolder = _Folder(self.path, 'sql')
        self.webdriverFolder = _Folder(self.path, 'webdriver')

        # Secondary folders...
        self.pySitePackageFolder = _Folder(self.libFolder.path, 'site-packages')
        self.chromeWebdriverFolder = _Folder(self.webdriverFolder.path, 'chrome')

        # Files and application...
        self.configurationFile = _File(self.binFolder.path, 'configuration.xlsx')
        self.chromeWebdriver = _File(join(self.chromeWebdriverFolder.path, '80.0.3987.106'), 'chromedriver.exe')

        self.system_path_initialize()

    def paths_to_be_initialize(self):
        return [self, self.libFolder, self.moduleFolder, self.pySitePackageFolder]

    def system_path_initialize(self):
        for pathInstance in self.paths_to_be_initialize():
            if pathInstance.path not in sys.path:
                sys.path.append(pathInstance.path)


if __name__ == '__main__':
    pass
