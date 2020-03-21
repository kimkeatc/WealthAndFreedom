# -*- coding: utf-8 -*-

from os.path import abspath, basename, dirname, join
from pathlib import Path
import os
import sys


class Folder:

    def __init__(self, dirname, name):
        self.dirname = dirname
        self.name = name

    @property
    def path(self):
        return join(self.dirname, self.name)

    def listdir(self):
        return os.listdir(self.path)


class File:

    def __init__(self, dirname, name):
        self.dirname = dirname
        self.name = name

    @property
    def path(self):
        return join(self.dirname, self.name)


class _ProjectSubFolder:

    def __init__(self, dirname):
        self.dirname = dirname

        self.setup()

    def setup(self):
        self._bin = Folder(self.dirname, 'bin')
        self._data = Folder(self.dirname, 'data')
        self._docs = Folder(self.dirname, 'docs')
        self._driver = Folder(self.dirname, 'driver')
        self._homework = Folder(self.dirname, 'homework')
        self._lib = Folder(self.dirname, 'Lib')
        self._logs = Folder(self.dirname, 'logs')
        self._module = Folder(self.dirname, 'module')
        self._py_site_packages = Folder(self.lib.path, 'site-packages')
        self._test = Folder(self.dirname, 'test')
        self._webdriver = Folder(self.driver.path, 'webdriver')
        self._chromeWebdriver = Folder(self.webdriver.path, 'chrome')

    @property
    def bin(self):
        return self._bin

    @property
    def data(self):
        return self._data

    @property
    def docs(self):
        return self._docs

    @property
    def driver(self):
        return self._driver

    @property
    def homework(self):
        return self._homework

    @property
    def lib(self):
        return self._lib

    @property
    def logs(self):
        return self._logs

    @property
    def module(self):
        return self._module

    @property
    def py_site_packages(self):
        return self._py_site_packages

    @property
    def test(self):
        return self._test

    @property
    def webdriver(self):
        return self._webdriver

    @property
    def chromeWebdriver(self):
        return self._chromeWebdriver


class Project:

    def __init__(self):
        self.dirname = dirname(self.path)
        self.name = basename(self.path)

        self.setup()

    def setup(self):
        self.subfolder = _ProjectSubFolder(self.path)

    @property
    def path(self):
        path = Path(__file__).parents[1]
        path = abspath(path)
        return path

    @property
    def SubFolder(self):
        return self.subfolder

    def PathInitialize(self):
        paths = self.PathListToBeInitialize()
        for path in paths:
            if path not in sys.path:
                sys.path.append(path)

    def PathListToBeInitialize(self):
        paths = [self.SubFolder.driver.path,
                 self.SubFolder.lib.path,
                 self.SubFolder.module.path,
                 self.SubFolder.py_site_packages.path]
        return paths

    def holidaysFilepath(self):
        return File(self.SubFolder.bin.path, 'holidays.xlsx').path

    def lastUpdateFilepath(self):
        return File(self.SubFolder.data.path, 'last_udpate.txt').path


if __name__ == '__main__':
    pass
