# -*- coding: utf-8 -*-

import logging
import os
import sys

import Namespace


class LoggerSetup:

    def __init__(self, name=None):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

    def addStreamHandler(self, fmt=Namespace.default, level=logging.INFO):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        if fmt == Namespace.default:
            fmt = __class__.defaultFormatter()
        ch.setFormatter(fmt)
        self._logger.addHandler(ch)

    @staticmethod
    def defaultFormatter():
        formatter = logging.Formatter(fmt=__class__.defaultMsgFormat(),
                                      datefmt=__class__.defaultDateFormat())
        return formatter

    @staticmethod
    def defaultMsgFormat():
        return '[%(asctime)s] [%(levelname)8s]: %(message)s'

    @staticmethod
    def defaultDateFormat():
        return '%y/%m/%d %H:%M:%S'


class _File:

    def __init__(self, dirname, filename):
        self.dirname = dirname
        self._filename = filename
        self._filepath = os.path.abspath(os.path.join(dirname, filename))

    @property
    def name(self):
        return self._filename

    @property
    def path(self):
        return self._filepath

    def create(self, msg='', mode=0o770):
        with open(self.path, 'w') as f:
            f.write(msg)
        os.chmod(self.path, mode)

    def readlines(self):
        with open(self.path, 'r') as f:
            content = f.readlines()
        return content


class _Folder:

    def __init__(self, dirname, foldername):
        self.dirname = dirname
        self._foldername = foldername
        self._folderpath = os.path.abspath(os.path.join(dirname, foldername))

    @property
    def name(self):
        return self._foldername

    @property
    def path(self):
        return self._folderpath

    def create(self, mode=0o770):
        mask = os.umask(0o000)
        try:
            os.mkdir(self.path, mode)
        except FileExistsError:
            pass
        finally:
            os.umask(mask)

    def listdir(self):
        try:
            return os.listdir(self.path)
        except FileNotFoundError:
            logging.warning(f'Folder {self.path} not exists.')
        finally:
            return None


if __name__ == '__main__':
    pass
