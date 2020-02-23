# -*- coding: utf-8 -*-

import datetime
import logging
import os
import sys

from common import DEFAULT


def folderCreation(path, mode=0o750):
    mask = os.umask(0o000)
    os.mkdir(path, mode)
    os.umask(mask)


def getNowTime(fmt='%Y%m%d_%H%M%S'):
    return datetime.datetime.now().strftime(fmt)


class LoggerSetup:

    def __init__(self, name=None):
        logger = logging.getLogger(name=name)
        logger.setLevel(logging.DEBUG)
        self.logger = logger

    def addStreamHandler(self, level=logging.INFO, fmt=DEFAULT):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level=level)
        if fmt == DEFAULT:
            fmt = __class__.default_format()
        ch.setFormatter(fmt=fmt)
        self.logger.addHandler(ch)

    def addFileHandler(self, path, mode='a', level=logging.INFO, fmt=DEFAULT):
        fh = logging.FileHandler(filename=path, mode=mode, encoding='utf-8')
        fh.setLevel(level=level)
        if fmt == DEFAULT:
            fmt = __class__.default_format()
        fh.setFormatter(fmt=fmt)
        self.logger.addHandler(fh)

    @staticmethod
    def default_date_format():
        return '%y/%m/%d %H:%M:%S'

    @staticmethod
    def default_message_format():
        return '[%(asctime)s] [%(levelname)8s]: %(message)s'

    @staticmethod
    def default_format():
        fmt = logging.Formatter(fmt=__class__.default_message_format(),
                                datefmt=__class__.default_date_format())
        return fmt


if __name__ == '__main__':
    pass
