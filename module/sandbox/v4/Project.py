from os.path import abspath, dirname, exists, join
import logging
import sys

_MODULE_FOLDER = abspath(dirname(__file__))
_PROJECT_FOLDER = abspath(join(_MODULE_FOLDER, '..'))


class Module:

    def __init__(self):
        pass

    @property
    def rootpath(self):
        path = _PROJECT_FOLDER
        return path


class ModuleFolders(Module):

    # Parent folders
    bin = 'bin'
    data = 'data'
    db = 'db'
    docs = 'docs'
    driver = 'driver'
    etc = 'etc'
    history = 'history'
    lib = 'lib'
    script = 'script'
    test = 'test'

    # Sub-folders
    python_site_package = 'site-packages'

    def __init__(self):
        super().__init__()

    @property
    def binpath(self):
        path = join(self.rootpath, self.bin)
        return path

    @property
    def datapath(self):
        path = join(self.rootpath, self.data)
        return path

    @property
    def dbpath(self):
        path = join(self.rootpath, self.db)
        return path

    @property
    def docspath(self):
        path = join(self.rootpath, self.docs)
        return path

    @property
    def driverpath(self):
        path = join(self.rootpath, self.driver)
        return path

    @property
    def etcpath(self):
        path = join(self.rootpath, self.etc)
        return path

    @property
    def libpath(self):
        path = join(self.rootpath, self.lib)
        return path

    @property
    def scriptpath(self):
        path = join(self.rootpath, self.script)
        return path

    @property
    def testpath(self):
        path = join(self.rootpath, self.test)
        return path

    @property
    def pythonSitePackagePath(self):
        path = join(self.libpath, self.python_site_package)
        return path

    def ProjectInit(self):

        paths = self.getList()
        paths.reverse()

        for path in paths:
            if not exists(path):
                logging.warning('Module folder not found %s' % path)
                continue

            if path not in sys.path:
                sys.path.insert(1, path)

    def getList(self):

        paths = [self.rootpath,
                 self.pythonSitePackagePath,
                 self.binpath,
                 self.datapath,
                 self.dbpath,
                 self.docspath,
                 self.driverpath,
                 self.etcpath,
                 self.scriptpath,
                 self.testpath]

        return paths


class ModuleFiles(ModuleFolders):

    mainModule = 'Module.py'

    def __init__(self):
        super().__init__()

    @property
    def mainModulePath(self):
        path = join(self.rootpath, self.mainModule)
        return path


if __name__ == '__main__':
    pass
