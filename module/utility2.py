# -*- coding: utf-8 -*-

import logging
import sys
import os

import namespace


class File:

    def __init__(self, basepath, name):
        self._basepath = basepath
        self._name = name
        self._path = os.path.join(basepath, name)

    @property
    def basepath(self):
        return self._basepath

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path


class Folder(File):

    def __init__(self, basepath, name):
        File.__init__(self, basepath, name)

    def listdir(self):
        try:
            return os.listdir(self.path)
        except FileNotFoundError:
            logging.warning(f'Folder not exists...{self.path}...')


class SetupLogger:

    def __init__(self, name=None):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)

    @property
    def logger(self):
        return self._logger

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
